import { useState, useEffect, useCallback, useRef } from 'react'
import * as api from '../api/client'

const IMAGE_TYPES = ['Front', 'Back', 'Side', 'Detail', 'Neck']

export default function ProductManager({ product, onBack, onProductsChanged }) {
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

  const fileInputRefs = useRef({})

  // ─── Load SKUs ─────────────────────────────────────
  const loadSkus = useCallback(async () => {
    try {
      const data = await api.fetchSkus(product)
      setSkus(data.skus)
      if (data.skus.length > 0 && !selectedSku) {
        setSelectedSku(data.skus[0])
      }
    } catch (err) {
      setError(err.message)
    }
  }, [product, selectedSku])

  useEffect(() => { loadSkus() }, [product])

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
          imageMap[type] = `/api/input-image/${encodeURIComponent(product)}/${encodeURIComponent(selectedSku)}/${filename}`
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
      setSkuImages(prev => ({ ...prev, [type]: result.preview_url + '?t=' + Date.now() }))
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
      setSuccess(`Color "${newColorName.trim()}" added!`)
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError(err.message)
    } finally {
      setAddingColor(false)
    }
  }, [product, newColorName, loadSkus])

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
    } catch (err) {
      setError(err.message)
    }
  }, [product, selectedSku, skus])

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
    <div className="flex-1 flex flex-col overflow-hidden bg-bg-primary/50 relative">
      {/* Background Gradient Blob */}
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-accent/5 rounded-full blur-3xl pointer-events-none" />

      {/* ─── Header ─── */}
      <div className="px-8 py-5 border-b border-white/5 bg-bg-secondary/40 backdrop-blur-xl flex items-center justify-between shadow-lg z-10">
        <div className="flex items-center gap-4">
          <button 
            onClick={onBack} 
            className="group flex items-center gap-2 text-text-muted hover:text-text-primary transition-colors text-sm font-medium px-3 py-1.5 rounded-lg hover:bg-white/5"
          >
            <span className="group-hover:-translate-x-1 transition-transform">←</span> Back
          </button>
          <div className="w-px h-6 bg-white/10" />
          <h2 className="text-2xl font-bold bg-linear-to-r from-text-primary to-text-secondary bg-clip-text text-transparent flex items-center gap-3">
            <span className="text-2xl filter drop-shadow-md">📦</span> {product}
          </h2>
        </div>
        <div className="flex items-center gap-3">
          <button 
            onClick={handleDeleteProduct} 
            className="text-xs font-medium text-red-400/80 hover:text-red-400 transition-all px-4 py-2 rounded-xl hover:bg-red-400/10 border border-transparent hover:border-red-400/20"
          >
            🗑️ Delete Product
          </button>
        </div>
      </div>

      {/* ─── Tabs ─── */}
      <div className="px-8 pt-6 flex gap-4 border-b border-white/5 bg-linear-to-b from-bg-secondary/20 to-transparent">
        <button
          onClick={() => setActiveTab('images')}
          className={`relative px-6 py-3 text-sm font-semibold rounded-t-xl transition-all ${
            activeTab === 'images' 
              ? 'text-accent bg-white/5 border-b-2 border-accent' 
              : 'text-text-muted hover:text-text-primary hover:bg-white/5'
          }`}
        >
          🖼️ Images & Colors
          {activeTab === 'images' && (
            <div className="absolute inset-0 bg-accent/5 rounded-t-xl pointer-events-none" />
          )}
        </button>
        <button
          onClick={() => setActiveTab('prompts')}
          className={`relative px-6 py-3 text-sm font-semibold rounded-t-xl transition-all ${
            activeTab === 'prompts' 
              ? 'text-accent bg-white/5 border-b-2 border-accent' 
              : 'text-text-muted hover:text-text-primary hover:bg-white/5'
          }`}
        >
          📝 Prompt Editor
          {activeTab === 'prompts' && (
            <div className="absolute inset-0 bg-accent/5 rounded-t-xl pointer-events-none" />
          )}
        </button>
      </div>

      {/* ─── Content ─── */}
      <div className="flex-1 overflow-y-auto p-8 relative scroll-smooth">
        {/* Status Messages */}
        {error && (
          <div className="mb-6 text-sm font-medium text-red-300 bg-red-500/10 border border-red-500/20 rounded-xl px-5 py-3 flex items-center justify-between shadow-lg backdrop-blur-sm animate-fade-in">
            <span className="flex items-center gap-2">⚠️ {error}</span>
            <button onClick={() => setError('')} className="text-red-300/60 hover:text-red-300 transition-colors">✕</button>
          </div>
        )}
        {success && (
          <div className="mb-6 text-sm font-medium text-emerald-300 bg-emerald-500/10 border border-emerald-500/20 rounded-xl px-5 py-3 shadow-lg backdrop-blur-sm flex items-center gap-2 animate-fade-in">
            <span>✅ {success}</span>
          </div>
        )}

        {/* ─── Images Tab ─── */}
        {activeTab === 'images' && (
          <div className="animate-fade-in space-y-8">
            {/* Color Selector */}
            <div className="glass-card p-6 relative overflow-hidden group border-white/5 hover:border-white/10">
              <div className="absolute inset-0 bg-linear-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
              
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
                      className="px-4 py-2 text-xs font-medium text-red-400/70 hover:text-red-400 transition-colors rounded-lg hover:bg-red-400/5 hover:shadow-red-500/10 border border-transparent hover:border-red-400/10"
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
                        : 'bg-surface text-text-secondary border-white/10 hover:border-white/20 hover:bg-white/5 hover:text-white'
                    }`}
                  >
                    {sku}
                  </button>
                ))}
                {skus.length === 0 && (
                  <div className="w-full text-center py-8 border-2 border-dashed border-white/10 rounded-xl">
                    <p className="text-text-muted">No colors found. Start by adding one!</p>
                  </div>
                )}
              </div>
            </div>

            {/* Image Upload Grid */}
            {selectedSku && (
              <div className="animate-fade-in delay-100">
                <h3 className="text-lg font-bold text-text-primary mb-5 flex items-center gap-2">
                  Reference Images <span className="text-text-muted font-normal text-sm ml-2">for <span className="text-accent/80">{selectedSku}</span></span>
                </h3>
                <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
                  {IMAGE_TYPES.map((type, idx) => (
                    <div
                      key={type}
                      className="glass-card p-4 flex flex-col items-center gap-3 min-h-[240px] cursor-pointer group relative overflow-hidden   hover:border-accent/30 hover:shadow-xl hover:shadow-accent/5 transition-all duration-300 bg-bg-card/50"
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
                          <span className="text-emerald-400 text-[10px] bg-emerald-400/10 px-2 py-0.5 rounded-full border border-emerald-400/20">
                            ✓ Ready
                          </span>
                        )}
                      </div>

                      <div className="flex-1 w-full flex items-center justify-center relative rounded-xl bg-black/20 overflow-hidden border border-white/5 group-hover:border-white/10 transition-colors shadow-inner">
                        {uploading[type] ? (
                          <div className="absolute inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm z-20">
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
                            <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-all duration-300 flex flex-col items-center justify-center gap-2 backdrop-blur-[2px]">
                              <span className="text-white font-medium text-xs bg-accent px-4 py-2 rounded-lg shadow-lg transform translate-y-2 group-hover:translate-y-0 transition-transform">
                                ↻ Change Image
                              </span>
                            </div>
                          </>
                        ) : (
                          <div className="flex flex-col items-center justify-center text-text-muted group-hover:text-text-secondary transition-colors gap-3">
                             <div className="w-14 h-14 rounded-full bg-white/5 flex items-center justify-center group-hover:scale-110 transition-transform duration-300 text-2xl border border-white/5 group-hover:border-accent/30 group-hover:bg-accent/10 group-hover:text-accent shadow-sm">
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
            {showAddColor && (
              <div 
                className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-md animate-fade-in" 
                onClick={() => setShowAddColor(false)}
              >
                <div 
                  className="glass-card p-8 w-96 shadow-2xl border-white/10 transform scale-100 transition-all bg-[#0f172a]" 
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
                        className="w-full bg-bg-secondary border border-white/10 rounded-xl px-4 py-3 text-sm text-text-primary placeholder:text-text-muted focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/50 transition-all shadow-inner"
                      />
                    </div>
                    
                    <div className="flex gap-3 pt-2">
                      <button 
                        onClick={() => setShowAddColor(false)} 
                        className="flex-1 px-4 py-3 rounded-xl border border-white/10 text-text-secondary hover:bg-white/5 hover:text-white transition-colors text-sm font-medium"
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
            <div className="bg-amber-500/10 border border-amber-500/20 text-amber-200 text-sm rounded-xl px-6 py-4 flex items-start gap-4 shadow-lg backdrop-blur-sm">
              <span className="text-xl mt-0.5">💡</span>
              <div>
                <strong className="font-semibold text-amber-100 block mb-1">Important Tip</strong>
                <span className="opacity-90 leading-relaxed block">
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
                        : 'bg-surface hover:bg-white/5 text-text-secondary hover:text-white border border-white/5 hover:border-white/10'
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
              <div className="flex-1 flex flex-col gap-0 min-h-[400px] glass-card overflow-hidden border-white/10">
                {/* Editor Toolbar */}
                <div className="bg-white/5 px-5 py-3 border-b border-white/5 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-text-secondary uppercase tracking-wider">
                      Editing: <span className="text-text-primary">{activePromptTab}</span>
                    </span>
                  </div>
                  <span className={`text-xs px-3 py-1 rounded-full font-medium transition-colors ${promptDirty ? 'bg-amber-500/20 text-amber-300 border border-amber-500/20' : 'text-emerald-400 bg-emerald-400/10 border border-emerald-400/20'}`}>
                    {promptDirty ? '● Unsaved Changes' : '✓ Saved'}
                  </span>
                </div>
                
                <textarea
                  value={getPromptContent()}
                  onChange={e => setPromptContent(e.target.value)}
                  className="flex-1 w-full bg-bg-primary/30 p-6 text-sm text-text-primary font-mono leading-relaxed focus:outline-none transition-all resize-none"
                  placeholder="Enter prompt instructions here..."
                  spellCheck={false}
                />

                {/* Editor Footer */}
                <div className="bg-white/5 px-5 py-4 border-t border-white/5 flex justify-end">
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
