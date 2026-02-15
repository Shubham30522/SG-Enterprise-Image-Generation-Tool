export default function Sidebar({
  products, selectedProduct, onProductChange,
  poses, selectedPoses, onTogglePose, onToggleAll,
  resolution, onResolutionChange,
  refImagePreview, onRefUpload,
  matchPose, onMatchPoseChange,
  matchBg, onMatchBgChange,
  onAutoTune, isAutoTuning,
  onStart, isProcessing, anyPoseSelected,
  skuCount, skus, currentSkuIndex, onSkuChange,
  currentPage, onManageProduct, onShowCreateModal, onGoToGeneration
}) {
  const allChecked = poses.length > 0 && poses.every(p => selectedPoses[p])

  return (
    <aside className="w-80 shrink-0 border-r border-border bg-bg-secondary/80 backdrop-blur-md overflow-y-auto p-6 flex flex-col gap-6 relative z-20 shadow-2xl">
      
      {/* ─── Page Switcher ─── */}
      <div className="flex gap-1 bg-surface rounded-xl p-1.5 border border-border shadow-inner">
        <button
          onClick={onGoToGeneration}
          className={`flex-1 text-xs font-bold uppercase tracking-wide py-2.5 rounded-lg transition-all flex items-center justify-center gap-2 ${
            currentPage === 'generation' 
              ? 'bg-linear-to-r from-accent to-accent-hover text-white shadow-lg shadow-accent/25' 
              : 'text-text-muted hover:text-text-primary hover:bg-surface-hover'
          }`}
        >
          <span>⚡</span> Generate
        </button>
        <button
          onClick={() => onManageProduct(selectedProduct)}
          className={`flex-1 text-xs font-bold uppercase tracking-wide py-2.5 rounded-lg transition-all flex items-center justify-center gap-2 ${
            currentPage === 'product-manager' 
              ? 'bg-white text-text-primary border border-border shadow-md' 
              : 'text-text-muted hover:text-text-primary hover:bg-surface-hover'
          }`}
        >
          <span>📦</span> Manage
        </button>
      </div>

      {/* Product Selector */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <label className="text-[10px] font-bold text-text-muted uppercase tracking-widest">
            Selected Product
          </label>
          <span className="text-[10px] bg-surface px-2 py-0.5 rounded text-text-secondary border border-border">
            {products.length} Items
          </span>
        </div>
        
        <div className="relative group">
          <select
            value={selectedProduct}
            onChange={e => onProductChange(e.target.value)}
            disabled={isProcessing}
            className="w-full bg-bg-card border border-border rounded-xl px-4 py-3 text-sm text-text-primary focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/50 transition-all cursor-pointer disabled:opacity-50 appearance-none shadow-sm hover:border-accent/30"
          >
            {products.map(p => (
              <option key={p} value={p} className="bg-bg-secondary text-text-primary py-2">{p}</option>
            ))}
          </select>
          <div className="absolute right-4 top-1/2 -translate-y-1/2 text-text-muted pointer-events-none transition-transform group-hover:translate-y-0">▼</div>
        </div>

        <div className="flex items-center justify-between px-1">
          <p className="text-xs text-text-muted flex items-center gap-1.5">
            <span className={`w-2 h-2 rounded-full ${skuCount > 0 ? 'bg-emerald-500' : 'bg-red-400'}`} />
            {skuCount} Active Colors
          </p>
          <button
            onClick={() => onManageProduct(selectedProduct)}
            className="text-xs text-accent hover:text-accent-hover font-medium transition-colors flex items-center gap-1 group/edit"
          >
            Edit Product <span className="group-hover/edit:translate-x-0.5 transition-transform">→</span>
          </button>
        </div>
      </div>

      {/* ─── Add Product Button ─── */}
      <button
        onClick={onShowCreateModal}
        className="w-full py-3 text-sm font-semibold rounded-xl border border-dashed border-border bg-surface text-text-secondary hover:text-text-primary hover:border-accent/40 hover:bg-accent/5 transition-all group flex items-center justify-center gap-2"
      >
        <span className="w-5 h-5 rounded-full bg-white flex items-center justify-center text-xs group-hover:bg-accent group-hover:text-white transition-colors shadow-sm">＋</span>
        Add New Product
      </button>

      <div className="h-px bg-linear-to-r from-transparent via-border to-transparent my-1" />

      {/* ─── Generation Controls (only visible in generation mode) ─── */}
      {currentPage === 'generation' && (
        <div className="bg-surface rounded-2xl p-4 border border-border space-y-5 animate-fade-in shadow-inner">
          {/* Color / SKU Selector */}
          {skus && skus.length > 0 && (
            <div>
              <label className="text-[10px] font-bold text-text-muted uppercase tracking-widest mb-2 block">Target Color</label>
              <div className="relative group">
                <select
                  value={currentSkuIndex}
                  onChange={e => onSkuChange(Number(e.target.value))}
                  disabled={isProcessing}
                  className="w-full bg-bg-card border border-border rounded-xl px-4 py-3 text-sm text-text-primary focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/50 transition-all cursor-pointer disabled:opacity-50 appearance-none shadow-sm hover:border-accent/30"
                >
                  {skus.map((sku, idx) => (
                    <option key={sku} value={idx} className="bg-bg-secondary text-text-primary py-2">
                      {sku}
                    </option>
                  ))}
                </select>
                <div className="absolute right-4 top-1/2 -translate-y-1/2 text-text-muted pointer-events-none transition-transform group-hover:translate-y-0">▼</div>
              </div>
              <p className="text-[10px] text-text-muted mt-1.5 px-1">Color {currentSkuIndex + 1} of {skus.length}</p>
            </div>
          )}
          {/* Pose Checkboxes */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <label className="text-[10px] font-bold text-text-muted uppercase tracking-widest">
                Target Views
              </label>
              <label className="flex items-center gap-1.5 cursor-pointer group">
                <div className={`w-3 h-3 rounded border border-border flex items-center justify-center transition-colors ${allChecked ? 'bg-accent border-accent' : 'bg-white group-hover:border-accent'}`}>
                  {allChecked && <svg className="w-2 h-2 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="4"><path d="M20 6L9 17l-5-5" /></svg>}
                </div>
                <input type="checkbox" checked={allChecked} onChange={e => onToggleAll(e.target.checked)} className="hidden" />
                <span className="text-[10px] font-bold text-text-secondary group-hover:text-text-primary transition-colors">SELECT ALL</span>
              </label>
            </div>

            <div className="grid grid-cols-2 gap-2">
              {poses.map(pose => (
                <label key={pose} className={`flex items-center gap-2.5 cursor-pointer p-2 rounded-lg border transition-all ${selectedPoses[pose] ? 'bg-accent/10 border-accent/30' : 'bg-white border-transparent hover:bg-surface-hover hover:border-border shadow-sm'}`}>
                  <div className={`w-4 h-4 rounded border flex items-center justify-center transition-colors ${selectedPoses[pose] ? 'bg-accent border-accent' : 'border-border bg-slate-50'}`}>
                    {selectedPoses[pose] && <svg className="w-2.5 h-2.5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="4"><path d="M20 6L9 17l-5-5" /></svg>}
                  </div>
                  <input type="checkbox" checked={selectedPoses[pose] || false} onChange={() => onTogglePose(pose)} className="hidden" />
                  <span className={`text-xs font-medium transition-colors ${selectedPoses[pose] ? 'text-accent-hover font-bold' : 'text-text-secondary'}`}>{pose}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Resolution & Toggles */}
          <div className="space-y-4">
             {/* Resolution */}
            <div>
              <label className="text-[10px] font-bold text-text-muted uppercase tracking-widest mb-2 block">Quality</label>
              <div className="grid grid-cols-3 gap-1 bg-white p-1 rounded-lg border border-border shadow-sm">
                {['1K', '2K', '4K'].map(res => (
                  <button
                    key={res}
                    onClick={() => onResolutionChange(res)}
                    className={`text-xs font-medium py-1.5 rounded-md transition-all ${resolution === res ? 'bg-slate-100 text-text-primary shadow-inner font-bold' : 'text-text-muted hover:text-text-secondary'}`}
                  >
                    {res}
                  </button>
                ))}
              </div>
            </div>

            {/* Reference */}
             <div>
              <label className="text-[10px] font-bold text-text-muted uppercase tracking-widest mb-2 block">Reference Image</label>
              <div className="group relative">
                <label className="flex flex-col items-center justify-center w-full h-24 border-2 border-dashed border-border rounded-xl bg-white hover:bg-surface-hover hover:border-accent/30 cursor-pointer transition-all overflow-hidden shadow-sm">
                   {refImagePreview ? (
                     <img src={refImagePreview} alt="Ref" className="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity" />
                   ) : (
                     <div className="text-center">
                       <span className="block text-xl mb-1 opacity-50">📁</span>
                       <span className="text-[10px] text-text-muted uppercase font-bold">Upload Style</span>
                     </div>
                   )}
                   <input type="file" accept="image/*" className="hidden" onChange={e => e.target.files[0] && onRefUpload(e.target.files[0])} />
                </label>
                {refImagePreview && (
                  <button onClick={() => onRefUpload(null)} className="absolute top-1 right-1 bg-white p-1 rounded-md text-text-muted hover:text-red-500 shadow-md transition-all">
                    <svg className="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3"><path d="M18 6L6 18M6 6l12 12" /></svg>
                  </button>
                )}
              </div>
              
              <div className="flex gap-2 mt-2">
                 <label className={`flex-1 flex items-center justify-center gap-1.5 py-1.5 rounded-lg border text-[10px] font-bold uppercase cursor-pointer transition-all ${matchPose ? 'bg-accent/10 border-accent/30 text-accent' : 'border-border text-text-muted hover:bg-surface-hover bg-white shadow-sm'}`}>
                   <input type="checkbox" checked={matchPose} onChange={e => onMatchPoseChange(e.target.checked)} className="hidden" />
                   <span>Match Pose</span>
                 </label>
                 <label className={`flex-1 flex items-center justify-center gap-1.5 py-1.5 rounded-lg border text-[10px] font-bold uppercase cursor-pointer transition-all ${matchBg ? 'bg-accent/10 border-accent/30 text-accent' : 'border-border text-text-muted hover:bg-surface-hover bg-white shadow-sm'}`}>
                   <input type="checkbox" checked={matchBg} onChange={e => onMatchBgChange(e.target.checked)} className="hidden" />
                   <span>Match BG</span>
                 </label>
              </div>
            </div>
          </div>

          <div className="h-px bg-linear-to-r from-transparent via-border to-transparent" />

          {/* Actions */}
          <div className="space-y-3 pt-1">
            <button
              className="btn-amber text-sm w-full shadow-lg shadow-amber-500/10 hover:shadow-amber-500/20 py-3"
              onClick={onAutoTune}
              disabled={isAutoTuning || isProcessing}
            >
              {isAutoTuning ? '⏳ Optimizing...' : '✨ Auto-Tune Prompt'}
            </button>

            <button
              className={`btn-primary text-sm w-full shadow-lg shadow-accent/20 hover:shadow-accent/40 py-3 font-bold tracking-wide ${isProcessing ? 'animate-pulse-glow' : ''}`}
              onClick={onStart}
              disabled={isProcessing || !anyPoseSelected}
            >
              {isProcessing ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" strokeDasharray="30 70" /></svg>
                  Processing...
                </span>
              ) : '🚀 Start Generation'}
            </button>
          </div>
        </div>
      )}

      {/* ─── Manage Mode Hint ─── */}
      {currentPage === 'product-manager' && (
        <div className="flex-1 flex flex-col justify-center items-center text-center px-4 animate-fade-in opacity-60">
          <div className="w-20 h-20 bg-surface rounded-full flex items-center justify-center mb-4 border border-border shadow-inner">
             <span className="text-4xl filter drop-shadow-sm">📦</span>
          </div>
          <p className="text-sm font-bold text-text-secondary mb-1">Product Manager Active</p>
          <p className="text-xs text-text-muted max-w-[200px] leading-relaxed">
            Select a product above to edit its prompt, colors, and uploaded images.
          </p>
        </div>
      )}
    </aside>
  )
}
