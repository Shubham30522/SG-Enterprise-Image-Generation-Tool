import { useEffect } from 'react'

export default function ImagePreview({ 
  carouselImages = [], 
  focusedIndex = 0, 
  onNavigate, 
  onRegenerate,
  isProcessing, 
  statusText 
}) {
  
  // Keyboard Navigation
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'ArrowLeft') onNavigate(-1)
      if (e.key === 'ArrowRight') onNavigate(1)
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [onNavigate])

  const currentImage = carouselImages[focusedIndex]
  const prevImage = carouselImages[focusedIndex - 1]
  const nextImage = carouselImages[focusedIndex + 1]

  return (
    <div className="glass-card h-[550px] shrink-0 flex items-center justify-center overflow-hidden relative group bg-white border-border shadow-sm">
      
      {carouselImages.length > 0 ? (
        <>
          {/* Previous Image (Left Side) */}
          {prevImage && (
            <div 
              className="absolute left-16 top-1/2 -translate-y-1/2 w-64 h-96 opacity-60 blur-[1px] scale-90 z-0 transition-all duration-300 cursor-pointer hover:opacity-80 hover:scale-95 hover:z-20 hover:blur-none"
              onClick={() => onNavigate(-1)}
            >
              <img 
                src={prevImage.src} 
                alt={prevImage.pose} 
                className="w-full h-full object-cover rounded-xl border border-border shadow-lg"
              />
            </div>
          )}

          {/* Next Image (Right Side) */}
          {nextImage && (
            <div 
              className="absolute right-16 top-1/2 -translate-y-1/2 w-64 h-96 opacity-60 blur-[1px] scale-90 z-0 transition-all duration-300 cursor-pointer hover:opacity-80 hover:scale-95 hover:z-20 hover:blur-none"
              onClick={() => onNavigate(1)}
            >
              <img 
                src={nextImage.src} 
                alt={nextImage.pose} 
                className="w-full h-full object-cover rounded-xl border border-border shadow-lg"
              />
            </div>
          )}

          {/* Main Image (Center) */}
          <div className="relative z-10 max-w-full max-h-full transition-all duration-300 transform scale-100 flex flex-col items-center px-2">
            <img
              src={currentImage.src}
              alt={currentImage.pose}
              className="max-h-[530px] w-auto object-contain rounded-xl shadow-2xl border border-border animate-fade-in bg-surface"
            />
            
            {/* Pose Label & Regenerate */}
            <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex items-center gap-3 bg-black/70 backdrop-blur-md px-4 py-2 rounded-full border border-white/10 opacity-0 group-hover:opacity-100 transition-opacity shadow-lg">
              <span className="text-sm font-semibold text-white">{currentImage.pose}</span>
              <div className="h-4 w-px bg-white/30" />
              <button 
                onClick={onRegenerate}
                className="text-xs text-amber-400 hover:text-amber-300 font-medium flex items-center gap-1.5 transition-colors disabled:opacity-50"
                disabled={isProcessing}
              >
                ↻ Regenerate
              </button>
            </div>
          </div>

          {/* Navigation Buttons */}
          <button 
            onClick={() => onNavigate(-1)}
            className="absolute left-2 top-1/2 -translate-y-1/2 z-20 p-3 rounded-full bg-white/80 hover:bg-white text-text-primary border border-border backdrop-blur transition-all opacity-0 group-hover:opacity-100 disabled:opacity-30 shadow-lg hover:scale-110"
            disabled={focusedIndex === 0}
          >
            ←
          </button>
          
          <button 
            onClick={() => onNavigate(1)}
            className="absolute right-2 top-1/2 -translate-y-1/2 z-20 p-3 rounded-full bg-white/80 hover:bg-white text-text-primary border border-border backdrop-blur transition-all opacity-0 group-hover:opacity-100 disabled:opacity-30 shadow-lg hover:scale-110"
            disabled={focusedIndex === carouselImages.length - 1}
          >
            →
          </button>

          {/* Current Index Indicator */}
          <div className="absolute bottom-4 right-4 text-xs text-text-secondary bg-surface/80 border border-border px-2 py-1 rounded backdrop-blur-sm">
            {focusedIndex + 1} / {carouselImages.length}
          </div>
        </>
      ) : (
        /* Empty State */
        <div className="flex flex-col items-center gap-3 text-center px-8 z-10 py-8">
          {isProcessing ? (
            <>
              <div className="relative">
                <div className="w-12 h-12 border-4 border-accent/20 rounded-full" />
                <div className="w-12 h-12 border-4 border-accent border-t-transparent rounded-full animate-spin absolute top-0 left-0" />
              </div>
              <p className="text-text-secondary text-sm max-w-xs font-medium">
                {statusText || 'Generating...'}
              </p>
            </>
          ) : (
            <>
              <div className="text-5xl opacity-20 filter grayscale">🖼️</div>
              <p className="text-text-muted text-sm">
                Generated images will appear here
              </p>
            </>
          )}
        </div>
      )}

      {/* Global Processing Overlay (when regenerating) */}
      {isProcessing && carouselImages.length > 0 && (
        <div className="absolute inset-0 bg-white/60 z-30 flex items-center justify-center rounded-2xl backdrop-blur-[2px]">
          <div className="flex flex-col items-center gap-3 bg-white p-6 rounded-2xl border border-border shadow-2xl">
            <div className="w-10 h-10 border-3 border-accent/30 border-t-accent rounded-full animate-spin" />
            <p className="text-text-primary text-sm font-bold">{statusText || 'Processing...'}</p>
          </div>
        </div>
      )}
    </div>
  )
}
