import { useState } from 'react'
import * as api from '../api/client'

export default function CreateProductModal({ onClose, onCreated }) {
  const [name, setName] = useState('')
  const [category, setCategory] = useState('bottom')
  const [color, setColor] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!name.trim()) {
      setError('Product Name is required')
      return
    }
    if (!color.trim()) {
      setError('Initial Color SKU is required')
      return
    }

    setLoading(true)
    setError('')

    try {
      const result = await api.createProduct(name.trim(), category, color.trim())
      onCreated(result.product)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm animate-fade-in" onClick={onClose}>
      <div 
        className="glass-card p-8 w-full max-w-lg mx-4 shadow-2xl border-border transform scale-100 transition-all bg-white relative overflow-hidden" 
        onClick={e => e.stopPropagation()}
      >
        {/* Decorative Grid Background */}
        <div className="absolute inset-0 bg-[url('/grid-pattern.svg')] opacity-[0.03] pointer-events-none" />
        
        {/* Glow Effect */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-accent/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2 pointer-events-none" />

        <h2 className="text-2xl font-bold bg-linear-to-r from-text-primary to-text-secondary bg-clip-text text-transparent mb-6 flex items-center gap-3 relative z-10">
          <span className="text-3xl filter drop-shadow-sm">✨</span> Create New Product
        </h2>

        <form onSubmit={handleSubmit} className="flex flex-col gap-6 relative z-10">
          {/* Product Name */}
          <div className="group">
            <label className="text-xs font-bold text-text-secondary uppercase tracking-wider mb-2 block group-focus-within:text-accent transition-colors">
              Product Name
            </label>
            <input
              type="text"
              value={name}
              onChange={e => setName(e.target.value)}
              placeholder="e.g. Mens Linen Pant"
              autoFocus
              className="w-full bg-surface border border-border rounded-xl px-4 py-3.5 text-sm text-text-primary placeholder:text-text-muted focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/50 transition-all shadow-inner"
            />
          </div>

          <div className="grid grid-cols-2 gap-5">
            {/* Category */}
            <div className="group">
              <label className="text-xs font-bold text-text-secondary uppercase tracking-wider mb-2 block group-focus-within:text-accent transition-colors">
                Category
              </label>
              <div className="relative">
                <select
                  value={category}
                  onChange={e => setCategory(e.target.value)}
                  className="w-full bg-surface border border-border rounded-xl px-4 py-3.5 text-sm text-text-primary focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/50 transition-all appearance-none cursor-pointer hover:bg-surface-hover"
                >
                  <option value="top">Top (Shirt)</option>
                  <option value="bottom">Bottom (Pant)</option>
                  <option value="dress">Dress (Full)</option>
                </select>
                <div className="absolute right-4 top-1/2 -translate-y-1/2 text-text-muted pointer-events-none">▼</div>
              </div>
            </div>

            {/* Initial Color */}
            <div className="group">
              <label className="text-xs font-bold text-text-secondary uppercase tracking-wider mb-2 block group-focus-within:text-accent transition-colors">
                First Color SKU
              </label>
              <input
                type="text"
                value={color}
                onChange={e => setColor(e.target.value)}
                placeholder="e.g. Beige"
                className="w-full bg-surface border border-border rounded-xl px-4 py-3.5 text-sm text-text-primary placeholder:text-text-muted focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/50 transition-all shadow-inner"
              />
            </div>
          </div>

          {error && (
            <div className="text-xs font-medium text-red-600 bg-red-50 border border-red-200 rounded-xl px-4 py-3 flex items-center gap-2 animate-pulse">
              ⚠️ {error}
            </div>
          )}

          {/* Actions */}
          <div className="flex gap-4 mt-2">
            <button 
              type="button" 
              onClick={onClose} 
              className="flex-1 px-4 py-3.5 rounded-xl border border-border text-text-secondary hover:bg-surface-hover hover:text-text-primary transition-colors text-sm font-bold tracking-wide"
              disabled={loading}
            >
              Cancel
            </button>
            <button 
              type="submit" 
              className="flex-2 btn-primary text-sm shadow-lg shadow-accent/20 hover:shadow-accent/40 py-3.5 tracking-wide flex items-center justify-center gap-2" 
              disabled={loading}
            >
              {loading ? (
                <>
                  <svg className="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" strokeDasharray="30 70" /></svg>
                  Creating...
                </>
              ) : (
                '✨ Create Product'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
