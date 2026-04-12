import { useState, useEffect, useMemo } from 'react'
import { useSearchParams } from 'react-router-dom'
import { SlidersHorizontal, X } from 'lucide-react'
import { useLangStore, useProductStore } from '../store'
import { categories } from '../data/products'
import ProductCard from '../components/product/ProductCard'

export default function ProductsPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const { lang, t } = useLangStore()
  const { products } = useProductStore()

  const initialCat = searchParams.get('cat') || 'all'
  const [activeCat, setActiveCat] = useState(initialCat)
  const [sortBy, setSortBy] = useState('newest')
  const [searchQ, setSearchQ] = useState('')
  const [showFilter, setShowFilter] = useState(false)

  useEffect(() => { window.scrollTo(0, 0) }, [])

  useEffect(() => {
    const cat = searchParams.get('cat')
    if (cat) setActiveCat(cat)
  }, [searchParams])

  const getCatLabel = (id) => {
    if (id === 'all') return lang === 'uz' ? 'Barchasi' : 'Все'
    const cat = categories.find(c => c.id === id)
    return cat ? (lang === 'uz' ? cat.label_uz : cat.label_ru) : id
  }

  const filtered = useMemo(() => {
    let list = activeCat === 'all' ? [...products] : products.filter(p => p.category === activeCat)
    if (searchQ) {
      const q = searchQ.toLowerCase()
      list = list.filter(p =>
        (lang === 'uz' ? p.name_uz : p.name_ru).toLowerCase().includes(q) ||
        p.author.toLowerCase().includes(q)
      )
    }
    switch (sortBy) {
      case 'price_asc':  return list.sort((a, b) => a.price - b.price)
      case 'price_desc': return list.sort((a, b) => b.price - a.price)
      case 'newest':     return list.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
      default:           return list
    }
  }, [products, activeCat, sortBy, searchQ, lang])

  const handleCat = (id) => {
    setActiveCat(id)
    if (id === 'all') searchParams.delete('cat')
    else setSearchParams({ cat: id })
  }

  return (
    <div className="min-h-screen bg-gray-50 pt-20">
      {/* Header */}
      <div className="bg-[#4c1d95] text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6">
          <h1 className="text-3xl font-black mb-1 font-serif">{t('nav_products')}</h1>
          <p className="text-white/60">{filtered.length} {lang === 'uz' ? 'ta mahsulot' : 'товаров'}</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
        {/* Filters Row */}
        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          {/* Search */}
          <input
            value={searchQ}
            onChange={e => setSearchQ(e.target.value)}
            placeholder={t('search_placeholder')}
            className="flex-1 px-4 py-2.5 rounded-xl border border-gray-200 bg-white outline-none focus:border-[#ffffff] text-sm"
          />

          {/* Sort */}
          <select
            value={sortBy}
            onChange={e => setSortBy(e.target.value)}
            className="px-4 py-2.5 rounded-xl border border-gray-200 bg-white outline-none text-sm font-semibold text-gray-700 focus:border-[#ffffff]"
          >
            <option value="newest">{lang === 'uz' ? 'Yangilari' : 'Новые'}</option>
            <option value="price_asc">{lang === 'uz' ? 'Arzon avval' : 'Сначала дешевле'}</option>
            <option value="price_desc">{lang === 'uz' ? 'Qimmat avval' : 'Сначала дороже'}</option>
          </select>
        </div>

        {/* Category tabs */}
        <div className="flex flex-wrap gap-2 mb-8">
          {['all', ...categories.map(c => c.id)].map(id => (
            <button
              key={id}
              onClick={() => handleCat(id)}
              className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${
                activeCat === id
                  ? 'bg-[#ffffff] text-[#4c1d95] shadow-lg shadow-yellow-200'
                  : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'
              }`}
            >
              {getCatLabel(id)}
              {id !== 'all' && (
                <span className={`ml-1.5 text-xs ${activeCat === id ? 'text-white/70' : 'text-gray-400'}`}>
                  ({products.filter(p => p.category === id).length})
                </span>
              )}
            </button>
          ))}
        </div>

        {/* Grid */}
        {filtered.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filtered.map((p, i) => (
              <div key={p.id} className="animate-fadeInUp" style={{ animationDelay: `${i * 50}ms` }}>
                <ProductCard product={p} />
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-24 text-gray-400">
            <div className="text-6xl mb-4">🔍</div>
            <p className="text-lg font-semibold">{t('no_products')}</p>
            {searchQ && (
              <button onClick={() => setSearchQ('')} className="mt-4 flex items-center gap-2 mx-auto text-[#ffffff] font-semibold">
                <X className="w-4 h-4" /> {lang === 'uz' ? "Filterni tozalash" : 'Очистить фильтр'}
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
