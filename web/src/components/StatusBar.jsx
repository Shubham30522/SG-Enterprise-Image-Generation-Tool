export default function StatusBar({ text, error, onDismissError }) {
  return (
    <div className="px-6 py-2.5 border-t border-white/10 bg-bg-secondary/50 backdrop-blur-sm flex items-center justify-between">
      <span className="text-sm text-text-secondary truncate flex-1">
        {text}
      </span>

      {error && (
        <div className="flex items-center gap-2 ml-4 animate-fade-in">
          <span className="text-sm text-red-400 font-medium truncate max-w-md" title={error}>
            ⚠️ {error}
          </span>
          <button
            onClick={onDismissError}
            className="text-red-400 hover:text-red-300 text-xs font-bold px-1.5 py-0.5 rounded hover:bg-red-500/10 transition-colors"
          >
            ✕
          </button>
        </div>
      )}
    </div>
  )
}
