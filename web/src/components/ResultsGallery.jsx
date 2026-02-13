import { getDownloadZipUrl } from '../api/client'

export default function ResultsGallery({ images, product, outputFolder, batchComplete }) {
  const downloadSingle = (img) => {
    const link = document.createElement('a')
    link.href = `data:image/jpeg;base64,${img.image_base64}`
    link.download = img.filename || `${img.pose}.jpg`
    link.click()
  }

  const folderName = outputFolder ? outputFolder.split(/[/\\]/).pop() : null

  return (
    <div className="glass-card p-5 animate-fade-in bg-white border-border shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-semibold text-text-primary flex items-center gap-2">
          <span>🖼️</span> Generated Images <span className="text-text-muted font-normal">({images.length})</span>
        </h3>
        {batchComplete && folderName && (
          <a
            href={getDownloadZipUrl(product, folderName)}
            className="btn-ghost text-xs py-1.5 px-3 no-underline border-border text-text-secondary hover:bg-surface-hover transition-colors"
            download
          >
            📦 Download All as ZIP
          </a>
        )}
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
        {images.map((img, idx) => (
          <div key={idx} className="group relative rounded-xl overflow-hidden border border-border hover:border-accent/40 hover:shadow-lg transition-all animate-fade-in bg-surface">
            <img
              src={`data:image/jpeg;base64,${img.image_base64}`}
              alt={img.pose}
              className="w-full aspect-square object-cover"
            />
            <div className="absolute inset-x-0 bottom-0 bg-linear-to-t from-black/80 to-transparent pt-8 pb-2 px-3 flex items-end justify-between opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <span className="text-xs font-semibold text-white">{img.pose}</span>
              <button
                onClick={() => downloadSingle(img)}
                className="text-xs text-white/80 hover:text-white transition-colors bg-white/20 p-1.5 rounded-lg backdrop-blur-sm hover:bg-white/30"
                title="Download"
              >
                📥
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
