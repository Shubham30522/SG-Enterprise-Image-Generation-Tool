export default function Sidebar({
  products, selectedProduct, onProductChange,
  poses, selectedPoses, onTogglePose, onToggleAll,
  resolution, onResolutionChange,
  refImagePreview, onRefUpload,
  matchPose, onMatchPoseChange,
  matchBg, onMatchBgChange,
  onAutoTune, isAutoTuning,
  onStart, isProcessing, anyPoseSelected,
  skuCount
}) {
  const allChecked = poses.length > 0 && poses.every(p => selectedPoses[p])

  return (
    <aside className="w-72 shrink-0 border-r border-white/10 bg-bg-secondary/30 backdrop-blur-sm overflow-y-auto p-5 flex flex-col gap-5">

      {/* Product Selector */}
      <div>
        <label className="text-xs font-semibold text-text-muted uppercase tracking-wider mb-2 block">
          📦 Product
        </label>
        <select
          value={selectedProduct}
          onChange={e => onProductChange(e.target.value)}
          disabled={isProcessing}
          className="w-full bg-surface border border-(--color-border) rounded-xl px-3 py-2.5 text-sm text-text-primary focus:outline-none focus:border-accent transition-colors cursor-pointer disabled:opacity-50"
        >
          {products.map(p => (
            <option key={p} value={p} className="bg-bg-secondary">{p}</option>
          ))}
        </select>
        <p className="text-xs text-text-muted mt-1.5">{skuCount} SKU folders</p>
      </div>

      <hr className="border-white/10" />

      {/* Pose Checkboxes */}
      <div>
        <label className="text-xs font-semibold text-text-muted uppercase tracking-wider mb-2 block">
          🎯 Poses
        </label>

        {/* All Toggle */}
        <label className="flex items-center gap-2.5 mb-2 cursor-pointer group">
          <input
            type="checkbox"
            checked={allChecked}
            onChange={e => onToggleAll(e.target.checked)}
            className="w-4 h-4 accent-accent rounded cursor-pointer"
          />
          <span className="text-sm font-semibold text-text-primary group-hover:text-accent transition-colors">
            All
          </span>
        </label>

        <div className="h-px bg-white/5 my-1.5" />

        {/* Individual Poses */}
        <div className="flex flex-col gap-1">
          {poses.map(pose => (
            <label key={pose} className="flex items-center gap-2.5 cursor-pointer group py-0.5">
              <input
                type="checkbox"
                checked={selectedPoses[pose] || false}
                onChange={() => onTogglePose(pose)}
                className="w-4 h-4 accent-accent rounded cursor-pointer"
              />
              <span className="text-sm text-text-secondary group-hover:text-text-primary transition-colors">
                {pose}
              </span>
            </label>
          ))}
        </div>
      </div>

      <hr className="border-white/10" />

      {/* Resolution */}
      <div>
        <label className="text-xs font-semibold text-text-muted uppercase tracking-wider mb-2 block">
          📐 Resolution
        </label>
        <select
          value={resolution}
          onChange={e => onResolutionChange(e.target.value)}
          disabled={isProcessing}
          className="w-full bg-surface border border-(--color-border) rounded-xl px-3 py-2.5 text-sm text-text-primary focus:outline-none focus:border-accent transition-colors cursor-pointer disabled:opacity-50"
        >
          <option value="1K" className="bg-bg-secondary">1K</option>
          <option value="2K" className="bg-bg-secondary">2K</option>
          <option value="4K" className="bg-bg-secondary">4K</option>
        </select>
      </div>

      <hr className="border-white/10" />

      {/* Reference Image */}
      <div>
        <label className="text-xs font-semibold text-text-muted uppercase tracking-wider mb-2 block">
          🖼️ Reference Image
        </label>

        <label className="btn-ghost text-xs text-center cursor-pointer block">
          📁 Browse...
          <input
            type="file"
            accept="image/*"
            className="hidden"
            onChange={e => e.target.files[0] && onRefUpload(e.target.files[0])}
          />
        </label>

        {refImagePreview && (
          <img src={refImagePreview} alt="Reference" className="mt-2 rounded-lg w-full h-24 object-cover border border-white/10" />
        )}

        <div className="flex flex-col gap-1.5 mt-2">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={matchPose}
              onChange={e => onMatchPoseChange(e.target.checked)}
              className="w-3.5 h-3.5 accent-accent rounded cursor-pointer"
            />
            <span className="text-xs text-text-secondary">Match Pose</span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={matchBg}
              onChange={e => onMatchBgChange(e.target.checked)}
              className="w-3.5 h-3.5 accent-accent rounded cursor-pointer"
            />
            <span className="text-xs text-text-secondary">Match Background</span>
          </label>
        </div>
      </div>

      <hr className="border-white/10" />

      {/* Actions */}
      <div className="flex flex-col gap-2.5 mt-auto">
        <button
          className="btn-amber text-sm w-full"
          onClick={onAutoTune}
          disabled={isAutoTuning || isProcessing}
        >
          {isAutoTuning ? '⏳ Tuning...' : '✨ Auto-Tune'}
        </button>

        <button
          className={`btn-primary text-sm w-full ${isProcessing ? 'animate-pulse-glow' : ''}`}
          onClick={onStart}
          disabled={isProcessing || !anyPoseSelected}
        >
          {isProcessing ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" strokeDasharray="30 70" /></svg>
              Processing...
            </span>
          ) : '▶ Start Processing'}
        </button>
      </div>
    </aside>
  )
}
