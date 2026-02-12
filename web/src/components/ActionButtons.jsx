export default function ActionButtons({
  isProcessing, hasImage, hasSavedFront,
  onSaveAndAutoGen, onSaveFront, onGenerateVariants,
  onRegenerate, onSkip
}) {
  return (
    <div className="grid grid-cols-2 gap-3">
      {/* Row 1 */}
      <button
        className="btn-success text-sm"
        onClick={onSaveAndAutoGen}
        disabled={isProcessing || !hasImage}
        title="Save front image and automatically generate all checked variant poses"
      >
        💾 Save & Auto-Gen Variants
      </button>

      {!hasSavedFront ? (
        <button
          className="btn-ghost text-sm border-emerald-500/30 hover:border-emerald-500/50"
          onClick={onSaveFront}
          disabled={isProcessing || !hasImage}
          title="Save the front image only"
        >
          💾 Save Front
        </button>
      ) : (
        <button
          className="btn-primary text-sm"
          onClick={onGenerateVariants}
          disabled={isProcessing}
          title="Generate all checked variant poses using the saved front"
        >
          ▶ Generate Variants
        </button>
      )}

      {/* Row 2 */}
      <button
        className="btn-ghost text-sm border-red-500/20 hover:border-red-500/40 text-red-400 hover:text-red-300"
        onClick={onRegenerate}
        disabled={isProcessing || !hasImage}
        title="Regenerate the front image"
      >
        🔄 Regenerate Front
      </button>

      <button
        className="btn-ghost text-sm"
        onClick={onSkip}
        disabled={false}
        title="Skip this SKU and move to the next"
      >
        ⏭ Skip
      </button>
    </div>
  )
}
