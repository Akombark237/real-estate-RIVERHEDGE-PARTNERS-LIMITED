import { useState, useEffect, useContext } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import axios from 'axios'
import showToast, { getErrorMessage } from '../utils/toast'
import { AuthContext } from '../context/AuthContext'
import ImageUpload from '../components/ImageUpload'
import ImageGallery from '../components/ImageGallery'
import PropertyMap from '../components/PropertyMap'

const PropertyDetail = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { user } = useContext(AuthContext)
  const [property, setProperty] = useState(null)
  const [loading, setLoading] = useState(true)
  const [currentImageIndex, setCurrentImageIndex] = useState(0)
  const [showImageUpload, setShowImageUpload] = useState(false)

  useEffect(() => {
    fetchPropertyDetail()
  }, [id])

  const fetchPropertyDetail = async () => {
    try {
      const response = await axios.get(`/api/properties/${id}/`)
      console.log('Property detail:', response.data)
      setProperty(response.data)
    } catch (error) {
      console.error('Failed to fetch property:', error)
      showToast.error(getErrorMessage(error))
      navigate('/properties')
    } finally {
      setLoading(false)
    }
  }

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(price)
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  const getStatusColor = (status) => {
    const colors = {
      available: 'bg-green-100 text-green-800',
      pending: 'bg-yellow-100 text-yellow-800',
      sold: 'bg-red-100 text-red-800',
      rented: 'bg-blue-100 text-blue-800',
      off_market: 'bg-gray-100 text-gray-800'
    }
    return colors[status] || 'bg-gray-100 text-gray-800'
  }

  const getPropertyTypeIcon = (type) => {
    const icons = {
      residential: '🏠',
      commercial: '🏢',
      land: '🌳',
      industrial: '🏭',
      mixed: '🏘️'
    }
    return icons[type] || '🏠'
  }

  const nextImage = () => {
    if (property?.images?.length > 0) {
      setCurrentImageIndex((prev) => (prev + 1) % property.images.length)
    }
  }

  const prevImage = () => {
    if (property?.images?.length > 0) {
      setCurrentImageIndex((prev) => (prev - 1 + property.images.length) % property.images.length)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="flex flex-col items-center">
          <svg className="animate-spin h-12 w-12 text-blue-600 mb-4" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <div className="text-xl text-gray-600">Loading property details...</div>
        </div>
      </div>
    )
  }

  if (!property) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">Property not found</p>
        <button
          onClick={() => navigate('/properties')}
          className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Back to Properties
        </button>
      </div>
    )
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      {/* Back Button */}
      <button
        onClick={() => navigate('/properties')}
        className="mb-4 flex items-center text-blue-600 hover:text-blue-700 font-medium"
      >
        <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7"/>
        </svg>
        Back to Properties
      </button>

      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-xl shadow-lg p-8 mb-6 relative overflow-hidden">
        <div className="absolute top-0 right-0 opacity-10">
          <svg className="h-48 w-48" fill="currentColor" viewBox="0 0 24 24">
            <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
          </svg>
        </div>
        <div className="relative z-10">
          <div className="flex justify-between items-start">
            <div className="flex-1">
              <div className="flex items-center mb-2">
                <span className="text-4xl mr-3">{getPropertyTypeIcon(property.property_type)}</span>
                <h1 className="text-4xl font-bold text-white">{property.title}</h1>
              </div>
              <p className="text-blue-100 text-lg mb-4">
                📍 {property.address}, {property.city}, {property.state}
              </p>
              <div className="flex items-center space-x-4">
                <span className={`px-4 py-2 rounded-full text-sm font-semibold ${getStatusColor(property.status)}`}>
                  {property.status.replace('_', ' ').toUpperCase()}
                </span>
                <span className="text-blue-100 text-sm">
                  Listed on {formatDate(property.listing_date)}
                </span>
              </div>
            </div>
            <div className="text-right">
              <div className="text-5xl font-bold text-white mb-2">
                {formatPrice(property.price)}
              </div>
              <div className="text-blue-100 text-sm">
                {property.property_type.replace('_', ' ').toUpperCase()}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Images and Description */}
        <div className="lg:col-span-2 space-y-6">
          {/* Image Gallery */}
          <div className="bg-white shadow-xl rounded-2xl overflow-hidden">
            <div className="relative">
              {property.images && property.images.length > 0 ? (
                <>
                  <img
                    src={property.images[currentImageIndex].image}
                    alt={property.images[currentImageIndex].caption || property.title}
                    className="w-full h-96 object-cover"
                  />
                  {property.images.length > 1 && (
                    <>
                      <button
                        onClick={prevImage}
                        className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-white/80 hover:bg-white p-2 rounded-full shadow-lg"
                      >
                        <svg className="h-6 w-6 text-gray-800" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7"/>
                        </svg>
                      </button>
                      <button
                        onClick={nextImage}
                        className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-white/80 hover:bg-white p-2 rounded-full shadow-lg"
                      >
                        <svg className="h-6 w-6 text-gray-800" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"/>
                        </svg>
                      </button>
                      <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-black/50 text-white px-3 py-1 rounded-full text-sm">
                        {currentImageIndex + 1} / {property.images.length}
                      </div>
                    </>
                  )}
                </>
              ) : (
                <div className="w-full h-96 bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center">
                  <div className="text-center">
                    <svg className="h-24 w-24 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                    </svg>
                    <p className="text-gray-500 text-lg">No images available</p>
                  </div>
                </div>
              )}
            </div>

            {/* Thumbnail Gallery */}
            {property.images && property.images.length > 1 && (
              <div className="p-4 bg-gray-50 flex space-x-2 overflow-x-auto">
                {property.images.map((image, index) => (
                  <button
                    key={image.id}
                    onClick={() => setCurrentImageIndex(index)}
                    className={`flex-shrink-0 w-20 h-20 rounded-lg overflow-hidden border-2 ${
                      index === currentImageIndex ? 'border-blue-600' : 'border-transparent'
                    }`}
                  >
                    <img
                      src={image.image}
                      alt={image.caption || `Image ${index + 1}`}
                      className="w-full h-full object-cover"
                    />
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Description */}
          <div className="bg-white shadow-xl rounded-2xl p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Description</h2>
            <p className="text-gray-700 leading-relaxed whitespace-pre-line">
              {property.description}
            </p>
          </div>

          {/* Image Management (only for property owner/agent) */}
          {user && (user.id === property.agent || user.role === 'admin') && (
            <div className="bg-white shadow-xl rounded-2xl p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold text-gray-900">Manage Images</h2>
                <button
                  onClick={() => setShowImageUpload(!showImageUpload)}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold flex items-center"
                >
                  {showImageUpload ? (
                    <>
                      <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                      Cancel Upload
                    </>
                  ) : (
                    <>
                      <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
                      </svg>
                      Upload Images
                    </>
                  )}
                </button>
              </div>

              {showImageUpload ? (
                <ImageUpload
                  propertyId={property.id}
                  onUploadComplete={() => {
                    setShowImageUpload(false)
                    fetchPropertyDetail()
                  }}
                />
              ) : (
                <ImageGallery
                  images={property.images}
                  propertyId={property.id}
                  onUpdate={fetchPropertyDetail}
                  editable={true}
                />
              )}
            </div>
          )}

          {/* Features */}
          {property.features && Object.keys(property.features).length > 0 && (
            <div className="bg-white shadow-xl rounded-2xl p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Features & Amenities</h2>
              <div className="grid grid-cols-2 gap-3">
                {Object.entries(property.features).map(([key, value]) => (
                  <div key={key} className="flex items-center">
                    <svg className="h-5 w-5 text-green-600 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                    </svg>
                    <span className="text-gray-700">{key}: {value}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Right Column - Details and Actions */}
        <div className="space-y-6">
          {/* Property Specifications */}
          <div className="bg-white shadow-xl rounded-2xl p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Property Details</h2>
            <div className="space-y-3">
              {property.bedrooms && (
                <div className="flex justify-between items-center py-2 border-b border-gray-100">
                  <span className="text-gray-600">🛏️ Bedrooms</span>
                  <span className="font-semibold text-gray-900">{property.bedrooms}</span>
                </div>
              )}
              {property.bathrooms && (
                <div className="flex justify-between items-center py-2 border-b border-gray-100">
                  <span className="text-gray-600">🚿 Bathrooms</span>
                  <span className="font-semibold text-gray-900">{property.bathrooms}</span>
                </div>
              )}
              {property.size_sqft && (
                <div className="flex justify-between items-center py-2 border-b border-gray-100">
                  <span className="text-gray-600">📐 Size</span>
                  <span className="font-semibold text-gray-900">{property.size_sqft.toLocaleString()} sqft</span>
                </div>
              )}
              {property.year_built && (
                <div className="flex justify-between items-center py-2 border-b border-gray-100">
                  <span className="text-gray-600">📅 Year Built</span>
                  <span className="font-semibold text-gray-900">{property.year_built}</span>
                </div>
              )}
              {property.parking_spaces > 0 && (
                <div className="flex justify-between items-center py-2 border-b border-gray-100">
                  <span className="text-gray-600">🚗 Parking</span>
                  <span className="font-semibold text-gray-900">{property.parking_spaces} spaces</span>
                </div>
              )}
            </div>
          </div>

          {/* Location Map */}
          <div className="bg-white shadow-xl rounded-2xl p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">📍 Location</h2>
            <PropertyMap
              latitude={property.latitude}
              longitude={property.longitude}
              title={property.title}
              address={`${property.address}, ${property.city}, ${property.state}`}
              height="300px"
            />
            <div className="mt-4 p-3 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-700">
                <span className="font-semibold">Address:</span> {property.address}
              </p>
              <p className="text-sm text-gray-700 mt-1">
                <span className="font-semibold">City:</span> {property.city}, {property.state}
              </p>
            </div>
          </div>

          {/* Agent Information */}
          {property.agent_name && (
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 shadow-xl rounded-2xl p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Contact Agent</h2>
              <div className="flex items-center mb-4">
                <div className="bg-blue-600 text-white rounded-full h-12 w-12 flex items-center justify-center text-xl font-bold mr-3">
                  {property.agent_name.charAt(0)}
                </div>
                <div>
                  <p className="font-semibold text-gray-900">{property.agent_name}</p>
                  <p className="text-sm text-gray-600">Real Estate Agent</p>
                </div>
              </div>
              <button className="w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold transition-colors duration-200">
                📞 Contact Agent
              </button>
            </div>
          )}

          {/* Action Buttons */}
          <div className="bg-white shadow-xl rounded-2xl p-6 space-y-3">
            <button className="w-full px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 font-semibold transition-colors duration-200 flex items-center justify-center">
              <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
              </svg>
              Schedule Viewing
            </button>
            <button className="w-full px-4 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 font-semibold transition-colors duration-200 flex items-center justify-center">
              <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"/>
              </svg>
              Share Property
            </button>
            <button className="w-full px-4 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 font-semibold transition-colors duration-200 flex items-center justify-center">
              <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/>
              </svg>
              Print Details
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PropertyDetail

