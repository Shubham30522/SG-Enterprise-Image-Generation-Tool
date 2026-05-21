import { useState, useEffect, useCallback, useRef } from 'react'
import * as api from '../api/client'

const IMAGE_TYPES = ['Front', 'Back', 'Side', 'Detail', 'Neck']

export default function ProductManager({ product, onBack, onProductsChanged, refImagePath }) {
  // ─── State ─────────────────────────────────────────
  const [activeTab, setActiveTab] = useState('images') // 'images' | 'prompts'
  const [skus, setSkus] = useState([])
  const [selectedSku, setSelectedSku] = useState('')
  const [skuImages, setSkuImages] = useState({}) // {Front: previewUrl, Back: previewUrl, ...}
  const [uploading, setUploading] = useState({})
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  // Prompt state
  const [masterPrompt, setMasterPrompt] = useState('')
  const [variants, setVariants] = useState({})
  const [activePromptTab, setActivePromptTab] = useState('Master')
  const [promptDirty, setPromptDirty] = useState(false)
  const [savingPrompts, setSavingPrompts] = useState(false)

  // Add color modal
  const [showAddColor, setShowAddColor] = useState(false)
  const [newColorName, setNewColorName] = useState('')
  const [addingColor, setAddingColor] = useState(false)

  // Claude prompt generation state
  const [claudeAvailable, setClaudeAvailable] = useState(false)
  const [claudeInstruction, setClaudeInstruction] = useState('')
  const [isGeneratingClaude, setIsGeneratingClaude] = useState(false)

  const fileInputRefs = useRef({})

  // ─── Load SKUs ─────────────────────────────────────
  const loadSkus = useCallback(async () => {
    try {
      const data = await api.fetchSkus(product)
      setSkus(data.skus)
      return data.skus
    } catch (err) {
      setError(err.message)
      return []
    }
  }, [product])

  useEffect(() => { 
    setSelectedSku('')
    loadSkus().then(fetchedSkus => {
        if (fetchedSkus.length > 0) {
            setSelectedSku(fetchedSkus[0])
        }
    })
  }, [product, loadSkus])

  // ─── Check Claude availability ─────────────────────
  useEffect(() => {
    api.fetchClaudeStatus().then(data => setClaudeAvailable(data.available)).catch(() => {})
  }, [])

  // ─── Load SKU Images ───────────────────────────────
  useEffect(() => {
    if (!selectedSku) return
    setSkuImages({})
    api.fetchSkuImages(product, selectedSku).then(data => {
      const imageMap = {}
      data.images.forEach(filename => {
        const baseName = filename.replace(/\.[^.]+$/, '')
        const type = IMAGE_TYPES.find(t => t.toLowerCase() === baseName.toLowerCase())
        if (type) {
          imageMap[type] = api.getInputImageUrl(product, selectedSku, filename);
        }
      })
      setSkuImages(imageMap)
    }).catch(() => {})
  }, [product, selectedSku])

  // ─── Load Prompts ──────────────────────────────────
  useEffect(() => {
    api.fetchPrompts(product)
      .then(data => {
        setMasterPrompt(data.master_prompt || '')
        setVariants(data.variants || {})
        setPromptDirty(false)
      })
      .catch(() => {})
  }, [product])

  // ─── Image Upload ──────────────────────────────────
  const handleImageUpload = useCallback(async (type, file) => {
    setUploading(prev => ({ ...prev, [type]: true }))
    setError('')
    try {
      const result = await api.uploadSkuImage(product, selectedSku, type, file)
      const absoluteUrl = api.getInputImageUrl(product, selectedSku, result.filename);
      setSkuImages(prev => ({ ...prev, [type]: absoluteUrl + '?t=' + Date.now() }))
      setSuccess(`${type} image uploaded!`)
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError(err.message)
    } finally {
      setUploading(prev => ({ ...prev, [type]: false }))
    }
  }, [product, selectedSku])

  const handleDrop = useCallback((type, e) => {
    e.preventDefault()
    e.stopPropagation()
    const file = e.dataTransfer?.files?.[0]
    if (file && file.type.startsWith('image/')) {
      handleImageUpload(type, file)
    }
  }, [handleImageUpload])

  // ─── Prompt Saving ─────────────────────────────────
  const handleSavePrompts = useCallback(async () => {
    setSavingPrompts(true)
    setError('')
    try {
      await api.savePrompts(product, masterPrompt, variants)
      setPromptDirty(false)
      setSuccess('Prompts saved successfully!')
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError(err.message)
    } finally {
      setSavingPrompts(false)
    }
  }, [product, masterPrompt, variants])

  // ─── Add Color ─────────────────────────────────────
  const handleAddColor = useCallback(async () => {
    if (!newColorName.trim()) return
    setAddingColor(true)
    setError('')
    try {
      await api.createSku(product, newColorName.trim())
      setShowAddColor(false)
      setNewColorName('')
      await loadSkus()
      setSelectedSku(newColorName.trim())
      onProductsChanged()
      setSuccess(`Color "${newColorName.trim()}" added!`)
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError(err.message)
    } finally {
      setAddingColor(false)
    }
  }, [product, newColorName, loadSkus, onProductsChanged])

  // ─── Delete Product ────────────────────────────────
  const handleDeleteProduct = useCallback(async () => {
    if (!window.confirm(`Delete "${product}" and all its data? This cannot be undone.`)) return
    try {
      await api.deleteProduct(product)
      onProductsChanged()
      onBack()
    } catch (err) {
      setError(err.message)
    }
  }, [product, onBack, onProductsChanged])

  // ─── Delete SKU ────────────────────────────────────
  const handleDeleteSku = useCallback(async () => {
    if (!selectedSku) return
    if (!window.confirm(`Delete color "${selectedSku}"? This cannot be undone.`)) return
    try {
      await api.deleteSku(product, selectedSku)
      const remaining = skus.filter(s => s !== selectedSku)
      setSkus(remaining)
      setSelectedSku(remaining[0] || '')
      onProductsChanged()
    } catch (err) {
      setError(err.message)
    }
  }, [product, selectedSku, skus, onProductsChanged])

  // ─── Claude Prompt Generation ──────────────────────
  const handleGenerateClaude = useCallback(async () => {
    if (!selectedSku) {
      setError('Please select a color/SKU first.')
      return
    }
    setIsGeneratingClaude(true)
    setError('')
    setSuccess('')
    try {
      const result = await api.generatePromptsClaude(
        product,
        selectedSku,
        claudeInstruction,
        refImagePath || null
      )
      // Reload prompts to reflect changes
      const promptData = await api.fetchPrompts(product)
      setMasterPrompt(promptData.master_prompt || '')
      setVariants(promptData.variants || {})
      setActivePromptTab('Master')
      setPromptDirty(false)
      setSuccess(`✨ Claude generated ${result.angles_generated?.length || 0} prompts: ${result.angles_generated?.join(', ')}`)
      onProductsChanged()
      setTimeout(() => setSuccess(''), 8000)
    } catch (err) {
      setError(`Claude: ${err.message}`)
    } finally {
      setIsGeneratingClaude(false)
    }
  }, [product, selectedSku, claudeInstruction, refImagePath, onProductsChanged])

  // ─── Prompt content helpers ────────────────────────
  const getPromptContent = () => {
    if (activePromptTab === 'Master') return masterPrompt
    return variants[activePromptTab] || ''
  }

  const setPromptContent = (content) => {
    setPromptDirty(true)
    if (activePromptTab === 'Master') {
      setMasterPrompt(content)
    } else {
      setVariants(prev => ({ ...prev, [activePromptTab]: content }))
    }
  }

  const promptTabs = ['Master', ...Object.keys(variants)]

  return (
    <div className="flex-1 flex flex-col overflow-hidden bg-bg-primary relative">
      {/* Background Gradient Blob */}
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-accent/5 rounded-full blur-3xl pointer-events-none" />

      {/* ─── Header ─── */}
      <div className="px-8 py-5 border-b border-border bg-bg-card/80 backdrop-blur-xl flex items-center justify-between shadow-sm z-10">
        <div className="flex items-center gap-4">
          <button 
            onClick={onBack} 
            className="group flex items-center gap-2 text-text-muted hover:text-text-primary transition-colors text-sm font-medium px-3 py-1.5 rounded-lg hover:bg-surface-hover"
          >
            <span className="group-hover:-translate-x-1 transition-transform">←</span> Back
          </button>
          <div className="w-px h-6 bg-border" />
          <h2 className="text-2xl font-bold bg-linear-to-r from-text-primary to-text-secondary bg-clip-text text-transparent flex items-center gap-3">
            <span className="text-2xl filter drop-shadow-sm">📦</span> {product}
          </h2>
        </div>
        <div className="flex items-center gap-3">
          <button 
            onClick={handleDeleteProduct} 
            className="text-xs font-medium text-red-500/80 hover:text-red-600 transition-all px-4 py-2 rounded-xl hover:bg-red-50 border border-transparent hover:border-red-200"
          >
            🗑️ Delete Product
          </button>
        </div>
      </div>

      {/* ─── Tabs ─── */}
      <div className="px-8 pt-6 flex gap-4 border-b border-border bg-linear-to-b from-surface to-transparent">
        <button
          onClick={() => setActiveTab('images')}
          className={`relative px-6 py-3 text-sm font-semibold rounded-t-xl transition-all ${
            activeTab === 'images' 
              ? 'text-accent bg-bg-card border-t border-x border-border border-b-white -mb-px shadow-sm' 
              : 'text-text-muted hover:text-text-primary hover:bg-surface-hover border border-transparent'
          }`}
        >
          🖼️ Images & Colors
          {activeTab === 'images' && (
            <div className="absolute -top-1 left-0 right-0 h-1 bg-accent rounded-t-xl" />
          )}
        </button>
        <button
          onClick={() => setActiveTab('prompts')}
          className={`relative px-6 py-3 text-sm font-semibold rounded-t-xl transition-all ${
            activeTab === 'prompts' 
              ? 'text-accent bg-bg-card border-t border-x border-border border-b-white -mb-px shadow-sm' 
              : 'text-text-muted hover:text-text-primary hover:bg-surface-hover border border-transparent'
          }`}
        >
          📝 Prompt Editor
          {activeTab === 'prompts' && (
            <div className="absolute -top-1 left-0 right-0 h-1 bg-accent rounded-t-xl" />
          )}
        </button>
      </div>

      {/* ─── Content ─── */}
      <div className="flex-1 overflow-y-auto p-8 relative scroll-smooth bg-surface/30">
        {/* Status Messages */}
        {error && (
          <div className="mb-6 text-sm font-medium text-red-600 bg-red-50 border border-red-200 rounded-xl px-5 py-3 flex items-center justify-between shadow-lg backdrop-blur-sm animate-fade-in">
            <span className="flex items-center gap-2">⚠️ {error}</span>
            <button onClick={() => setError('')} className="text-red-400 hover:text-red-600 transition-colors">✕</button>
          </div>
        )}
        {success && (
          <div className="mb-6 text-sm font-medium text-emerald-600 bg-emerald-50 border border-emerald-200 rounded-xl px-5 py-3 shadow-lg backdrop-blur-sm flex items-center gap-2 animate-fade-in">
            <span>✅ {success}</span>
          </div>
        )}

        {/* ─── Images Tab ─── */}
        {activeTab === 'images' && (
          <div className="animate-fade-in space-y-8">
            {/* Color Selector */}
            <div className="glass-card p-6 relative overflow-hidden group border-border hover:border-accent/20 bg-white shadow-sm">
              <div className="absolute inset-0 bg-linear-to-br from-accent/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
              
              <div className="flex items-center justify-between mb-5 relative z-10">
                <div className="flex items-center gap-3">
                  <span className="w-8 h-8 rounded-lg bg-accent/10 flex items-center justify-center text-accent ring-1 ring-accent/20">🎨</span>
                  <label className="text-sm font-bold text-text-secondary uppercase tracking-wider">
                    Color Variants (SKUs)
                  </label>
                </div>
                <div className="flex gap-3">
                  {selectedSku && (
                    <button 
                      onClick={handleDeleteSku} 
                      className="px-4 py-2 text-xs font-medium text-red-500/80 hover:text-red-600 transition-colors rounded-lg hover:bg-red-50 border border-transparent hover:border-red-200"
                    >
                      Delete Color
                    </button>
                  )}
                  <button 
                    onClick={() => setShowAddColor(true)} 
                    className="btn-primary text-xs py-2 px-4 shadow-lg shadow-accent/20 hover:shadow-accent/40"
                  >
                    + Add New Color
                  </button>
                </div>
              </div>

              <div className="flex flex-wrap gap-3 relative z-10">
                {skus.map(sku => (
                  <button
                    key={sku}
                    onClick={() => setSelectedSku(sku)}
                    className={`px-5 py-2.5 text-sm font-medium rounded-xl transition-all border transform hover:-translate-y-0.5 duration-200 ${
                      selectedSku === sku
                        ? 'bg-accent text-white border-accent shadow-lg shadow-accent/30'
                        : 'bg-white text-text-secondary border-border hover:border-accent/40 hover:bg-surface-hover hover:text-text-primary shadow-sm'
                    }`}
                  >
                    {sku}
                  </button>
                ))}
                {skus.length === 0 && (
                  <div className="w-full text-center py-8 border-2 border-dashed border-border rounded-xl bg-surface/50">
                    <p className="text-text-muted">No colors found. Start by adding one!</p>
                  </div>
                )}
              </div>
            </div>

            {/* Image Upload Grid */}
            {selectedSku && (
              <div className="animate-fade-in delay-100">
                <h3 className="text-lg font-bold text-text-primary mb-5 flex items-center gap-2">
                  Reference Images <span className="text-text-muted font-normal text-sm ml-2">for <span className="text-accent">{selectedSku}</span></span>
                </h3>
                <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
                  {IMAGE_TYPES.map((type, idx) => (
                    <div
                      key={type}
                      className="glass-card p-4 flex flex-col items-center gap-3 min-h-[240px] cursor-pointer group relative overflow-hidden border-border hover:border-accent/40 hover:shadow-xl hover:shadow-accent/5 transition-all duration-300 bg-white"
                      onClick={() => fileInputRefs.current[type]?.click()}
                      onDrop={(e) => handleDrop(type, e)}
                      onDragOver={(e) => { e.preventDefault(); e.stopPropagation() }}
                      style={{ animationDelay: `${idx * 50}ms` }}
                    >
                      <input
                        ref={el => fileInputRefs.current[type] = el}
                        type="file"
                        accept="image/*"
                        className="hidden"
                        onChange={e => {
                          const f = e.target.files?.[0]
                          if (f) handleImageUpload(type, f)
                          e.target.value = ''
                        }}
                      />

                      <div className="w-full flex justify-between items-center opacity-80 group-hover:opacity-100 transition-opacity">
                        <span className="text-xs font-bold text-text-secondary uppercase tracking-wider">
                          {type}
                        </span>
                        {skuImages[type] && (
                          <span className="text-emerald-500 text-[10px] bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200 font-bold">
                            ✓ Ready
                          </span>
                        )}
                      </div>

                      <div className="flex-1 w-full flex items-center justify-center relative rounded-xl bg-surface overflow-hidden border border-border group-hover:border-accent/20 transition-colors shadow-inner">
                        {uploading[type] ? (
                          <div className="absolute inset-0 flex items-center justify-center bg-white/60 backdrop-blur-sm z-20">
                            <svg className="w-8 h-8 animate-spin text-accent" viewBox="0 0 24 24" fill="none">
                              <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" strokeDasharray="30 70" />
                            </svg>
                          </div>
                        ) : skuImages[type] ? (
                          <>
                            <img
                              src={skuImages[type]}
                              alt={type}
                              className="w-full h-full object-contain p-2 transition-transform duration-500 group-hover:scale-105"
                            />
                            <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-all duration-300 flex flex-col items-center justify-center gap-2 backdrop-blur-[1px]">
                              <span className="text-white font-medium text-xs bg-accent px-4 py-2 rounded-lg shadow-lg transform translate-y-2 group-hover:translate-y-0 transition-transform">
                                ↻ Change Image
                              </span>
                            </div>
                          </>
                        ) : (
                          <div className="flex flex-col items-center justify-center text-text-muted group-hover:text-text-secondary transition-colors gap-3">
                             <div className="w-14 h-14 rounded-full bg-white flex items-center justify-center group-hover:scale-110 transition-transform duration-300 text-2xl border border-border group-hover:border-accent/30 group-hover:bg-accent/5 group-hover:text-accent shadow-sm">
                               📷
                             </div>
                             <span className="text-xs font-medium opacity-60 group-hover:opacity-100 transition-opacity transform translate-y-2 group-hover:translate-y-0">
                               Click or Drop
                             </span>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Add Color Modal */}

            {/* ─── Claude AI Prompt Generator ─── */}
            {selectedSku && (
              <div className="glass-card p-6 relative overflow-hidden group border-border hover:border-accent/20 bg-white shadow-sm animate-fade-in">
                <div className="absolute inset-0 bg-linear-to-br from-sky-500/5 via-transparent to-violet-500/5 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />

                <div className="relative z-10 space-y-4">
                  <div className="flex items-center gap-3">
                    <span className="w-8 h-8 rounded-lg bg-sky-100 flex items-center justify-center text-sky-600 ring-1 ring-sky-200">🧠</span>
                    <div>
                      <label className="text-sm font-bold text-text-secondary uppercase tracking-wider">
                        AI Prompt Generator
                      </label>
                      <p className="text-[10px] text-text-muted mt-0.5">
                        Powered by Claude Sonnet 4.6 • Generates Front + Back by default
                      </p>
                    </div>
                  </div>

                  {/* Custom Instruction Textbox */}
                  <div>
                    <label className="text-[10px] font-bold text-text-muted uppercase tracking-widest mb-1.5 block">
                      Custom Instructions <span className="text-text-muted/50">(optional)</span>
                    </label>
                    <textarea
                      value={claudeInstruction}
                      onChange={e => setClaudeInstruction(e.target.value)}
                      placeholder="e.g. Also generate Side angle • Use outdoor café background • Model should be a 25-year-old Indian woman with warm skin tone"
                      rows={3}
                      disabled={isGeneratingClaude}
                      className="w-full bg-surface border border-border rounded-xl px-4 py-3 text-sm text-text-primary placeholder:text-text-muted/60 focus:outline-none focus:border-sky-400 focus:ring-1 focus:ring-sky-400/50 transition-all shadow-inner resize-none disabled:opacity-50"
                    />
                  </div>

                  {/* Generate Button */}
                  <button
                    onClick={handleGenerateClaude}
                    disabled={isGeneratingClaude || !claudeAvailable}
                    title={!claudeAvailable ? 'GCP project not configured — add GCP_PROJECT_ID to .env' : ''}
                    className={`w-full py-3.5 text-sm font-bold rounded-xl transition-all flex items-center justify-center gap-2.5 shadow-lg ${
                      isGeneratingClaude
                        ? 'bg-sky-100 text-sky-700 border border-sky-200 cursor-wait animate-pulse'
                        : claudeAvailable
                          ? 'bg-linear-to-r from-sky-500 to-indigo-500 text-white hover:from-sky-600 hover:to-indigo-600 shadow-sky-500/25 hover:shadow-sky-500/40 hover:-translate-y-0.5 active:translate-y-0'
                          : 'bg-gray-100 text-gray-400 border border-gray-200 cursor-not-allowed'
                    }`}
                  >
                    {isGeneratingClaude ? (
                      <>
                        <svg className="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none">
                          <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" strokeDasharray="30 70" />
                        </svg>
                        Generating with Claude — this takes 15–30s...
                      </>
                    ) : claudeAvailable ? (
                      <>🧠 Generate Prompts with Claude</>
                    ) : (
                      <>🔒 Claude Not Configured</>
                    )}
                  </button>

                  {/* Info text */}
                  <p className="text-[9px] text-text-muted italic px-1 opacity-70 leading-relaxed">
                    Analyzes your garment images using the v2 photography framework. Generates prompts for Front + Back by default.
                    Request additional angles (Side, Close-up, etc.) in the custom instructions above.
                    {refImagePath ? ' ✓ Sidebar reference image will be used for background.' : ' No reference image — Claude will auto-design the background.'}
                  </p>
                </div>
              </div>
            )}
            {showAddColor && (
              <div 
                className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm animate-fade-in" 
                onClick={() => setShowAddColor(false)}
              >
                <div 
                  className="glass-card p-8 w-96 shadow-2xl transform scale-100 transition-all bg-white" 
                  onClick={e => e.stopPropagation()}
                >
                  <h3 className="text-xl font-bold text-text-primary mb-2 flex items-center gap-2">
                    <span className="text-accent">➕</span> Add New Color
                  </h3>
                  <p className="text-sm text-text-muted mb-6 leading-relaxed">
                    Create a new SKU folder for this product. You can then upload images for this color.
                  </p>
                  
                  <div className="space-y-5">
                    <div>
                      <label className="text-xs font-bold text-text-secondary uppercase tracking-wider mb-2 block">
                        Color / SKU Name
                      </label>
                      <input
                        type="text"
                        value={newColorName}
                        onChange={e => setNewColorName(e.target.value)}
                        placeholder="e.g. Navy-Blue, 02-Charcoal"
                        autoFocus
                        onKeyDown={e => e.key === 'Enter' && handleAddColor()}
                        className="w-full bg-surface border border-border rounded-xl px-4 py-3 text-sm text-text-primary placeholder:text-text-muted focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/50 transition-all shadow-inner"
                      />
                    </div>
                    
                    <div className="flex gap-3 pt-2">
                      <button 
                        onClick={() => setShowAddColor(false)} 
                        className="flex-1 px-4 py-3 rounded-xl border border-border text-text-secondary hover:bg-surface-hover hover:text-text-primary transition-colors text-sm font-medium"
                        disabled={addingColor}
                      >
                        Cancel
                      </button>
                      <button 
                        onClick={handleAddColor} 
                        className="flex-1 btn-primary text-sm shadow-lg shadow-accent/20" 
                        disabled={addingColor || !newColorName.trim()}
                      >
                        {addingColor ? '⏳ Creating...' : 'Create SKU'}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* ─── Prompts Tab ─── */}
        {activeTab === 'prompts' && (
          <div className="animate-fade-in flex flex-col h-full gap-6">
            {/* Info Banner */}
            <div className="bg-amber-50 border border-amber-200 text-amber-900 text-sm rounded-xl px-6 py-4 flex items-start gap-4 shadow-sm">
              <span className="text-xl mt-0.5">💡</span>
              <div>
                <strong className="font-semibold text-amber-800 block mb-1">Important Tip</strong>
                <span className="opacity-90 leading-relaxed block text-amber-800/80">
                  Prompts are shared across <strong>all color variants</strong>. 
                  Do NOT write specific colors like "Red Shirt" or "Blue Jeans". 
                  The AI automatically detects the color from your <strong>Front Input Image</strong>.
                </span>
              </div>
            </div>

            <div className="flex-1 flex flex-col md:flex-row gap-6 h-full overflow-hidden">
              {/* File List */}
              <div className="w-full md:w-64 flex flex-col gap-2 shrink-0">
                <label className="text-xs font-bold text-text-muted uppercase tracking-wider mb-2 px-2">Prompt Files</label>
                {promptTabs.map(tab => (
                  <button
                    key={tab}
                    onClick={() => setActivePromptTab(tab)}
                    className={`text-left px-4 py-3 rounded-xl transition-all flex items-center justify-between group ${
                      activePromptTab === tab
                        ? 'bg-accent text-white shadow-lg shadow-accent/20 font-medium scale-105 origin-left'
                        : 'bg-white hover:bg-surface-hover text-text-secondary hover:text-text-primary border border-border hover:border-accent/30 shadow-sm'
                    }`}
                  >
                    <span className="flex items-center gap-2">
                       {tab === 'Master' ? '📄' : '📝'} {tab === 'Master' ? 'Master Prompt' : tab}
                    </span>
                    {activePromptTab === tab && <div className="w-1.5 h-1.5 rounded-full bg-white shadow-sm" />}
                  </button>
                ))}
              </div>

              {/* Editor Area */}
              <div className="flex-1 flex flex-col gap-0 min-h-[400px] glass-card overflow-hidden border-border bg-white shadow-lg">
                {/* Editor Toolbar */}
                <div className="bg-surface px-5 py-3 border-b border-border flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-text-secondary uppercase tracking-wider">
                      Editing: <span className="text-text-primary">{activePromptTab}</span>
                    </span>
                  </div>
                  <span className={`text-xs px-3 py-1 rounded-full font-medium transition-colors ${promptDirty ? 'bg-amber-50 text-amber-600 border border-amber-200' : 'text-emerald-600 bg-emerald-50 border border-emerald-200'}`}>
                    {promptDirty ? '● Unsaved Changes' : '✓ Saved'}
                  </span>
                </div>
                
                <textarea
                  value={getPromptContent()}
                  onChange={e => setPromptContent(e.target.value)}
                  className="flex-1 w-full bg-white p-6 text-sm text-text-primary font-slate-900 leading-relaxed focus:outline-none transition-all resize-none shadow-inner"
                  placeholder="Enter prompt instructions here..."
                  spellCheck={false}
                />

                {/* Editor Footer */}
                <div className="bg-surface px-5 py-4 border-t border-border flex justify-end">
                   <button
                    onClick={handleSavePrompts}
                    className={`btn-success text-sm px-8 py-2.5 shadow-lg shadow-emerald-500/20 flex items-center gap-2 transform transition-all hover:-translate-y-1 ${savingPrompts ? 'opacity-70 cursor-wait' : ''}`}
                    disabled={savingPrompts || !promptDirty}
                  >
                    {savingPrompts ? '⏳ Saving...' : '💾 Save All Changes'}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
