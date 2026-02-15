import { useState, useEffect, useCallback, useRef } from 'react'
import * as api from './api/client'
import Sidebar from './components/Sidebar'
import ImagePreview from './components/ImagePreview'
import ActionButtons from './components/ActionButtons'
import StatusBar from './components/StatusBar'
import ResultsGallery from './components/ResultsGallery'
import ProductManager from './components/ProductManager'
import CreateProductModal from './components/CreateProductModal'

export default function App() {
  // ─── Page Navigation ────────────────────────────────
  const [currentPage, setCurrentPage] = useState('generation') // 'generation' | 'product-manager'

  const [showCreateModal, setShowCreateModal] = useState(false)

  // ─── Product / SKU State ────────────────────────────
  const [products, setProducts] = useState([])
  const [selectedProduct, setSelectedProduct] = useState('')
  const [skus, setSkus] = useState([])
  const [poses, setPoses] = useState([])
  const [selectedPoses, setSelectedPoses] = useState({})
  const [resolution, setResolution] = useState('1K')

  // ─── Reference Image ───────────────────────────────
  const [refImagePath, setRefImagePath] = useState('')
  const [refImagePreview, setRefImagePreview] = useState(null)
  const [matchPose, setMatchPose] = useState(false)
  const [matchBg, setMatchBg] = useState(false)

  // ─── Generation State ──────────────────────────────
  const [isProcessing, setIsProcessing] = useState(false)
  const [currentSkuIndex, setCurrentSkuIndex] = useState(0)
  const [currentImage, setCurrentImage] = useState(null) // base64
  const [currentImageData, setCurrentImageData] = useState(null) // raw base64 for saving
  const [savedFrontPath, setSavedFrontPath] = useState(null)
  const [savedOutputFolder, setSavedOutputFolder] = useState(null)
  const [currentJobId, setCurrentJobId] = useState(null)
  const [hasSavedFront, setHasSavedFront] = useState(false)
  const [allSkuImages, setAllSkuImages] = useState([])

  // ─── Status ────────────────────────────────────────
  const [statusText, setStatusText] = useState('Select product, poses and click "Start Processing" to begin.')
  const [batchStatus, setBatchStatus] = useState('')
  const [errorMsg, setErrorMsg] = useState('')
  const [variantProgress, setVariantProgress] = useState({ current: 0, total: 0 })

  // ─── Results ───────────────────────────────────────
  const [generatedImages, setGeneratedImages] = useState([]) // {pose, image_base64, filename}
  const [batchComplete, setBatchComplete] = useState(false)
  
  // ─── Carousel State ────────────────────────────────
  const [carouselImages, setCarouselImages] = useState([]) // {pose, src}
  const [focusedIndex, setFocusedIndex] = useState(0)

  // ─── Refs ──────────────────────────────────────────
  const eventSourceRef = useRef(null)

  // ─── Load Products on Mount ────────────────────────
  const loadProducts = useCallback(() => {
    api.fetchProducts().then(prods => {
      setProducts(prods)
      if (prods.length > 0 && !selectedProduct) {
        const initial = prods.includes('shirt') ? 'shirt' : prods[0]
        setSelectedProduct(initial)
      }
    }).catch(err => setErrorMsg(err.message))
  }, [selectedProduct])

  useEffect(() => { loadProducts() }, [])

  // ─── Product Manager Navigation ────────────────────
  const handleManageProduct = useCallback((productName) => {
    // If clicking Manage from Sidebar for a different product, update selection
    if (productName && productName !== selectedProduct) {
        setSelectedProduct(productName)
    }
    setCurrentPage('product-manager')
  }, [selectedProduct])

  const handleBackToGeneration = useCallback(() => {
    setCurrentPage('generation')
    loadProducts() // refresh product list
  }, [loadProducts])

  const handleProductCreated = useCallback((productName) => {
    setShowCreateModal(false)
    loadProducts()
    setSelectedProduct(productName)
    setCurrentPage('product-manager')
  }, [loadProducts])

  // ─── Load SKUs + Poses when Product Changes ────────
  useEffect(() => {
    if (!selectedProduct) return

    Promise.all([
      api.fetchSkus(selectedProduct),
      api.fetchPoses(selectedProduct)
    ]).then(([skuData, poseData]) => {
      setSkus(skuData.skus)
      setPoses(poseData.poses)
      // Initialize all poses as unchecked
      const initial = {}
      poseData.poses.forEach(p => initial[p] = false)
      setSelectedPoses(initial)
      // Reset state
      setCurrentSkuIndex(0)
      setCurrentImage(null)
      setGeneratedImages([])
      setCarouselImages([])
      setFocusedIndex(0)
      setBatchComplete(false)
      setHasSavedFront(false)
      setSavedFrontPath(null)
      setStatusText(`Loaded ${selectedProduct}. Ready.`)
      setBatchStatus('')
      setErrorMsg('')
    }).catch(err => setErrorMsg(err.message))
  }, [selectedProduct])

  // ─── Pose Toggling ─────────────────────────────────
  const togglePose = useCallback((pose) => {
    setSelectedPoses(prev => ({ ...prev, [pose]: !prev[pose] }))
  }, [])

  const toggleAllPoses = useCallback((checked) => {
    setSelectedPoses(prev => {
      const updated = {}
      Object.keys(prev).forEach(k => updated[k] = checked)
      return updated
    })
  }, [])

  const anyPoseSelected = Object.values(selectedPoses).some(v => v)

  // ─── Reference Image Upload ────────────────────────
  const handleRefUpload = useCallback(async (file) => {
    try {
      const result = await api.uploadReferenceImage(file)
      setRefImagePath(result.path)
      // Create preview URL
      setRefImagePreview(URL.createObjectURL(file))
    } catch (err) {
      setErrorMsg(err.message)
    }
  }, [])

  // ─── SSE Event Handler ─────────────────────────────
  const handleSSEEvent = useCallback((event) => {
    switch (event.type) {
      case 'status':
        setStatusText(event.data.message)
        break
      case 'front_ready':
        setCurrentImage(`data:image/jpeg;base64,${event.data.image_base64}`)
        setCurrentImageData(event.data.image_base64)
        setAllSkuImages(event.data.all_sku_images || [])
        // Update Carousel
        setCarouselImages([{ pose: 'Front', src: `data:image/jpeg;base64,${event.data.image_base64}` }])
        setFocusedIndex(0)
        setIsProcessing(false)
        setStatusText('Front View Ready. Click Save to generate variants.')
        setErrorMsg('')
        break
      case 'variant_progress':
        setBatchStatus(event.data.message)
        setVariantProgress({ current: event.data.current, total: event.data.total })
        break
      case 'variant_ready':
        setCurrentImage(`data:image/jpeg;base64,${event.data.image_base64}`)
        setGeneratedImages(prev => [...prev, {
          pose: event.data.pose,
          image_base64: event.data.image_base64,
          filename: event.data.filename,
        }])
        // Update Carousel (Append or Update)
        setCarouselImages(prev => {
          const idx = prev.findIndex(img => img.pose === event.data.pose)
          if (idx !== -1) {
            const newArr = [...prev]
            newArr[idx] = { ...newArr[idx], src: `data:image/jpeg;base64,${event.data.image_base64}` }
            return newArr
          }
          return [...prev, { pose: event.data.pose, src: `data:image/jpeg;base64,${event.data.image_base64}` }]
        })
        // Auto-focus the new image (if it's new)
        setFocusedIndex(prev => {
            // If we are regenerating (idx found in prev), keep focus.
            // But we don't have access to prev inside this setter easily without logic duplication.
            // Simplified: If batch processing, we usually want to see the latest.
            // If regenerating, we want to stay on it.
            return carouselImages.findIndex(img => img.pose === event.data.pose) !== -1 
                ? prev // stay on it (it was already there)
                : carouselImages.length // append -> focus new (length of OLD arr is index of new)
        })
        break
      case 'done':
        setIsProcessing(false)
        setBatchStatus(event.data.message || 'Complete')
        setBatchComplete(true)
        // Update output folder from server if provided (ensures correct ZIP path)
        if (event.data.output_folder) {
          setSavedOutputFolder(event.data.output_folder)
        }
        break
      case 'error':
        setIsProcessing(false)
        setErrorMsg(event.data.message)
        setStatusText('Generation Failed.')
        break
      case 'cancelled':
        setIsProcessing(false)
        setStatusText('Cancelled.')
        break
    }
  }, [])

  // ─── Actions ───────────────────────────────────────

  const startProcessing = useCallback(async () => {
    if (!anyPoseSelected) {
      setErrorMsg('Please select at least one pose to generate.')
      return
    }

    setIsProcessing(true)
    setGeneratedImages([])
    setCarouselImages([])
    setFocusedIndex(0)
    setBatchComplete(false)
    setHasSavedFront(false)
    setSavedFrontPath(null)
    setErrorMsg('')
    setBatchStatus('')

    const sku = skus[currentSkuIndex]
    if (!sku) {
      setStatusText('No SKU folders found.')
      setIsProcessing(false)
      return
    }

    // Check if Front is selected
    if (selectedPoses['Front']) {
      try {
        const result = await api.startFrontGeneration({
          product: selectedProduct,
          sku: sku,
          resolution: resolution,
          reference_image_path: refImagePath || null,
          match_pose: matchPose,
          match_bg: matchBg,
        })
        setCurrentJobId(result.job_id)
        // Start SSE listener
        if (eventSourceRef.current) eventSourceRef.current.close()
        eventSourceRef.current = api.subscribeToJob(result.job_id, handleSSEEvent)
      } catch (err) {
        setErrorMsg(err.message)
        setIsProcessing(false)
      }
    } else {
      // Skip front, go straight to variants
      setStatusText('Front View Skipped (checkbox unchecked).')
      setIsProcessing(false)
    }
  }, [selectedProduct, skus, currentSkuIndex, selectedPoses, resolution, refImagePath, matchPose, matchBg, anyPoseSelected, handleSSEEvent])

  const saveFrontOnly = useCallback(async () => {
    if (!currentImageData) return
    try {
      const sku = skus[currentSkuIndex]
      const result = await api.saveFrontImage(selectedProduct, sku, currentImageData)
      setSavedFrontPath(result.saved_path)
      setSavedOutputFolder(result.output_folder)
      setHasSavedFront(true)
      setStatusText("Front Saved. Click 'Generate Variants' to proceed.")
    } catch (err) {
      setErrorMsg(err.message)
    }
  }, [currentImageData, selectedProduct, skus, currentSkuIndex])

  const generateVariants = useCallback(async () => {
    const selectedPoseList = Object.entries(selectedPoses)
      .filter(([k, v]) => v && k !== 'Front')
      .map(([k]) => k)

    if (selectedPoseList.length === 0) {
      setStatusText('No variant poses selected.')
      return
    }

    setIsProcessing(true)
    setBatchComplete(false)
    setGeneratedImages([])
    // Don't clear carousel images, just variants? 
    // Usually Generate Variants is clicked after Front.
    // So we keep Front (index 0) and clear others?
    // User logic: "add user review required".
    // I'll keep logic simple: If generating variants, we expect new ones.
    setCarouselImages(prev => prev.filter(img => img.pose === 'Front'))
    setFocusedIndex(0)
    setErrorMsg('')

    try {
      const result = await api.startVariantGeneration({
        product: selectedProduct,
        sku: skus[currentSkuIndex],
        resolution: resolution,
        selected_poses: selectedPoseList,
        front_image_path: savedFrontPath,
      })
      setCurrentJobId(result.job_id)
      if (eventSourceRef.current) eventSourceRef.current.close()
      eventSourceRef.current = api.subscribeToJob(result.job_id, handleSSEEvent)
    } catch (err) {
      setErrorMsg(err.message)
      setIsProcessing(false)
    }
  }, [selectedProduct, skus, currentSkuIndex, resolution, selectedPoses, savedFrontPath, handleSSEEvent])

  const saveAndAutoGen = useCallback(async () => {
    // Save front + immediately start variants
    if (!currentImageData) return
    try {
      const sku = skus[currentSkuIndex]
      const result = await api.saveFrontImage(selectedProduct, sku, currentImageData)
      setSavedFrontPath(result.saved_path)
      setSavedOutputFolder(result.output_folder)
      setHasSavedFront(true)

      // Immediately start variants
      const selectedPoseList = Object.entries(selectedPoses)
        .filter(([k, v]) => v && k !== 'Front')
        .map(([k]) => k)

      if (selectedPoseList.length === 0) {
        setStatusText('Front saved. No variant poses selected.')
        return
      }

      setIsProcessing(true)
      setBatchComplete(false)
      setGeneratedImages([])
      setCarouselImages(prev => prev.filter(img => img.pose === 'Front'))
      setFocusedIndex(0)

      const varResult = await api.startVariantGeneration({
        product: selectedProduct,
        sku: sku,
        resolution: resolution,
        selected_poses: selectedPoseList,
        front_image_path: result.saved_path,
      })
      setCurrentJobId(varResult.job_id)
      if (eventSourceRef.current) eventSourceRef.current.close()
      eventSourceRef.current = api.subscribeToJob(varResult.job_id, handleSSEEvent)
    } catch (err) {
      setErrorMsg(err.message)
      setIsProcessing(false)
    }
  }, [currentImageData, selectedProduct, skus, currentSkuIndex, resolution, selectedPoses, handleSSEEvent])

  const regenerate = useCallback(async () => {
    if (isProcessing) return
    setCurrentImage(null)
    setHasSavedFront(false)
    setSavedFrontPath(null)
    setBatchComplete(false)
    setGeneratedImages([])
    setErrorMsg('')
    setBatchStatus('')
    startProcessing()
  }, [isProcessing, startProcessing])

  // ─── Carousel Logic ────────────────────────────────
  const handleNavigate = useCallback((direction) => {
    setFocusedIndex(prev => {
        const next = prev + direction
        if (next < 0) return carouselImages.length - 1
        if (next >= carouselImages.length) return 0
        return next
    })
  }, [carouselImages])

  const handleRegenerateFocused = useCallback(async () => {
    if (isProcessing || carouselImages.length === 0) return
    const focusedImg = carouselImages[focusedIndex]
    if (!focusedImg) return

    setIsProcessing(true)
    setErrorMsg('')
    const pose = focusedImg.pose
    setBatchStatus(`Regenerating ${pose}...`)

    try {
        if (pose === 'Front') {
             // Regenerate Front
             const sku = skus[currentSkuIndex]
             const result = await api.startFrontGeneration({
               product: selectedProduct,
               sku: sku,
               resolution: resolution,
               reference_image_path: refImagePath || null,
               match_pose: matchPose,
               match_bg: matchBg,
             })
             setCurrentJobId(result.job_id)
             if (eventSourceRef.current) eventSourceRef.current.close()
             eventSourceRef.current = api.subscribeToJob(result.job_id, handleSSEEvent)
        } else {
            // Regenerate Variant
            // Must have a saved front path!
            if (!savedFrontPath) {
                setErrorMsg("Cannot regenerate variant without a saved Front image.")
                setIsProcessing(false)
                return
            }
            const result = await api.startVariantGeneration({
                product: selectedProduct,
                sku: skus[currentSkuIndex],
                resolution: resolution,
                selected_poses: [pose],
                front_image_path: savedFrontPath,
            })
            setCurrentJobId(result.job_id)
            if (eventSourceRef.current) eventSourceRef.current.close()
            eventSourceRef.current = api.subscribeToJob(result.job_id, handleSSEEvent)
        }
    } catch (err) {
        setErrorMsg(err.message)
        setIsProcessing(false)
    }
  }, [isProcessing, carouselImages, focusedIndex, currentSkuIndex, skus, selectedProduct, resolution, refImagePath, matchPose, matchBg, savedFrontPath, handleSSEEvent])

  const skip = useCallback(async () => {
    // Cancel current job, move to next SKU
    if (currentJobId) {
      try { await api.cancelGeneration(currentJobId) } catch {}
    }
    if (eventSourceRef.current) eventSourceRef.current.close()
    
    const nextIndex = currentSkuIndex + 1
    if (nextIndex >= skus.length) {
      setStatusText('All tasks completed!')
      setIsProcessing(false)
      return
    }
    setCurrentSkuIndex(nextIndex)
    setCurrentImage(null)
    setHasSavedFront(false)
    setHasSavedFront(false)
    setSavedFrontPath(null)
    setGeneratedImages([])
    setCarouselImages([])
    setFocusedIndex(0)
    setBatchComplete(false)
    setErrorMsg('')
    setBatchStatus('')
  }, [currentJobId, currentSkuIndex, skus])

  // ─── Direct Color/SKU Selection ─────────────────────
  const handleSkuChange = useCallback((index) => {
    if (index === currentSkuIndex) return
    // Cancel any running job
    if (currentJobId) {
      try { api.cancelGeneration(currentJobId) } catch {}
    }
    if (eventSourceRef.current) eventSourceRef.current.close()
    setCurrentSkuIndex(index)
    setCurrentImage(null)
    setCurrentImageData(null)
    setHasSavedFront(false)
    setSavedFrontPath(null)
    setGeneratedImages([])
    setCarouselImages([])
    setFocusedIndex(0)
    setBatchComplete(false)
    setIsProcessing(false)
    setErrorMsg('')
    setBatchStatus('')
    setVariantProgress({ current: 0, total: 0 })
    setStatusText(`Switched to color: ${skus[index]}. Ready.`)
  }, [currentJobId, currentSkuIndex, skus])

  // Auto-start processing when skuIndex changes (after skip)
  useEffect(() => {
    if (currentSkuIndex > 0 && isProcessing) {
      startProcessing()
    }
  }, [currentSkuIndex]) // intentionally not adding startProcessing to deps

  // ─── Auto-Tune ─────────────────────────────────────
  const [isAutoTuning, setIsAutoTuning] = useState(false)

  const handleAutoTune = useCallback(async () => {
    if (!selectedProduct) return
    if (!window.confirm(`This will analyze '${selectedProduct}' images and OVERWRITE existing prompt files.\n\nAre you sure?`)) return

    setIsAutoTuning(true)
    setStatusText(`Auto-Tuning '${selectedProduct}'... Please wait.`)
    try {
      await api.autoTunePrompts(selectedProduct, refImagePath)
      setStatusText('Prompts Auto-Tuned & Reloaded!')
      // Refresh poses
      const poseData = await api.fetchPoses(selectedProduct)
      setPoses(poseData.poses)
      const initial = {}
      poseData.poses.forEach(p => initial[p] = false)
      setSelectedPoses(initial)
    } catch (err) {
      setErrorMsg(`Auto-Tune Failed: ${err.message}`)
    } finally {
      setIsAutoTuning(false)
    }
  }, [selectedProduct, refImagePath])

  // ─── Cleanup ───────────────────────────────────────
  useEffect(() => {
    return () => {
      if (eventSourceRef.current) eventSourceRef.current.close()
    }
  }, [])

  // ─── Render ────────────────────────────────────────
  const currentSku = skus[currentSkuIndex]

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="px-6 py-4 border-b border-border flex items-center justify-between bg-bg-secondary/80 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <span className="text-2xl">✨</span>
          <h1 className="text-xl font-bold bg-linear-to-r from-accent to-amber bg-clip-text text-transparent">
            Gemini Auto Tool
          </h1>
        </div>
        <span className="text-sm text-text-muted">SG Enterprise</span>
      </header>

      {/* Main Layout */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <Sidebar
          products={products}
          selectedProduct={selectedProduct}
          onProductChange={setSelectedProduct}
          poses={poses}
          selectedPoses={selectedPoses}
          onTogglePose={togglePose}
          onToggleAll={toggleAllPoses}
          resolution={resolution}
          onResolutionChange={setResolution}
          refImagePreview={refImagePreview}
          onRefUpload={handleRefUpload}
          matchPose={matchPose}
          onMatchPoseChange={setMatchPose}
          matchBg={matchBg}
          onMatchBgChange={setMatchBg}
          onAutoTune={handleAutoTune}
          isAutoTuning={isAutoTuning}
          onStart={startProcessing}
          isProcessing={isProcessing}
          anyPoseSelected={anyPoseSelected}
          skuCount={skus.length}
          skus={skus}
          currentSkuIndex={currentSkuIndex}
          onSkuChange={handleSkuChange}
          currentPage={currentPage}
          onManageProduct={handleManageProduct}
          onShowCreateModal={() => setShowCreateModal(true)}
          onGoToGeneration={() => setCurrentPage('generation')}
        />

        {/* Main Content - Conditional */}
        {currentPage === 'product-manager' && selectedProduct ? (
          <ProductManager
            product={selectedProduct}
            onBack={handleBackToGeneration}
            onProductsChanged={loadProducts}
          />
        ) : (
          <main className="flex-1 flex flex-col overflow-y-auto p-6 gap-5">
            {/* Progress Tracker */}
            {currentSku && (
              <div className="glass-card px-5 py-3 flex items-center justify-between">
                <span className="text-sm text-text-secondary">
                  Processing <strong className="text-text-primary">{currentSkuIndex + 1}</strong> / {skus.length} : <strong className="text-amber">{currentSku}</strong>
                </span>
                {variantProgress.total > 0 && (
                  <div className="flex items-center gap-3">
                    <span className="text-xs text-text-muted">{batchStatus}</span>
                    <div className="progress-bar w-32">
                      <div className="progress-bar-fill" style={{ width: `${(variantProgress.current / variantProgress.total) * 100}%` }} />
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Image Preview Carousel */}
            <ImagePreview
              carouselImages={carouselImages}
              focusedIndex={focusedIndex}
              onNavigate={handleNavigate}
              onRegenerate={handleRegenerateFocused}
              isProcessing={isProcessing}
              statusText={isProcessing ? statusText : null}
            />

            {/* Action Buttons */}
            <ActionButtons
              isProcessing={isProcessing}
              hasImage={!!currentImage}
              hasSavedFront={hasSavedFront}
              onSaveAndAutoGen={saveAndAutoGen}
              onSaveFront={saveFrontOnly}
              onGenerateVariants={generateVariants}
              onRegenerate={regenerate}
              onSkip={skip}
            />

            {/* Results Gallery */}
            {generatedImages.length > 0 && (
              <ResultsGallery
                images={generatedImages}
                product={selectedProduct}
                sku={currentSku}
                outputFolder={savedOutputFolder}
                batchComplete={batchComplete}
                frontImageBase64={hasSavedFront ? currentImageData : null}
              />
            )}
          </main>
        )}
      </div>

      {/* Status Bar */}
      <StatusBar
        text={statusText}
        error={errorMsg}
        onDismissError={() => setErrorMsg('')}
      />

      {/* Create Product Modal */}
      {showCreateModal && (
        <CreateProductModal
          onClose={() => setShowCreateModal(false)}
          onCreated={handleProductCreated}
        />
      )}
    </div>
  )
}
