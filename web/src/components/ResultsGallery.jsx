import JSZip from 'jszip'

export default function ResultsGallery({ images, product, sku, outputFolder, batchComplete, frontImageBase64 }) {
  const downloadSingle = (img) => {
    const link = document.createElement('a')
    link.href = `data:image/jpeg;base64,${img.image_base64}`
    link.download = img.filename || `${img.pose}.jpg`
    link.click()
  }

  const downloadAllAsZip = async () => {
    const zip = new JSZip()
    const folderName = `${product}_${sku || 'output'}`
    const folder = zip.folder(folderName)

    // Add front image if available
    if (frontImageBase64) {
      const frontFilename = `${sku || product}_Front.jpg`
      folder.file(frontFilename, frontImageBase64, { base64: true })
    }

    // Add all variant images
    for (const img of images) {
      const filename = img.filename || `${sku || product}_${img.pose}.jpg`
      folder.file(filename, img.image_base64, { base64: true })
    }

    // Generate and download
    const blob = await zip.generateAsync({ type: 'blob' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${folderName}.zip`
    link.click()
    URL.revokeObjectURL(url)
  }

  // Total count = front (if saved) + variants
  const totalImages = images.length + (frontImageBase64 ? 1 : 0)

  return (
    <div className="glass-card p-5 animate-fade-in bg-white border-border shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-semibold text-text-primary flex items-center gap-2">
          <span>🖼️</span> Generated Images <span className="text-text-muted font-normal">({totalImages})</span>
        </h3>
        {batchComplete && totalImages > 0 && (
          <button
            onClick={downloadAllAsZip}
            className="btn-ghost text-xs py-1.5 px-3 border-border text-text-secondary hover:bg-surface-hover transition-colors cursor-pointer"
          >
            📦 Download All as ZIP ({totalImages})
          </button>
        )}
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
        {/* Front image thumbnail */}
        {frontImageBase64 && (
          <div className="group relative rounded-xl overflow-hidden border border-accent/30 hover:border-accent/60 hover:shadow-lg transition-all animate-fade-in bg-surface">
            <img
              src={`data:image/jpeg;base64,${frontImageBase64}`}
              alt="Front"
              className="w-full aspect-square object-cover"
            />
            <div className="absolute inset-x-0 bottom-0 bg-linear-to-t from-black/80 to-transparent pt-8 pb-2 px-3 flex items-end justify-between opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <span className="text-xs font-semibold text-white">Front ⭐</span>
              <button
                onClick={() => downloadSingle({ image_base64: frontImageBase64, filename: `${sku || product}_Front.jpg`, pose: 'Front' })}
                className="text-xs text-white/80 hover:text-white transition-colors bg-white/20 p-1.5 rounded-lg backdrop-blur-sm hover:bg-white/30"
                title="Download"
              >
                📥
              </button>
            </div>
          </div>
        )}
        {/* Variant images */}
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
