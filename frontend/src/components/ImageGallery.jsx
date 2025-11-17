import { useState } from 'react'
import axios from 'axios'
import { showToast } from '../utils/toast'

const ImageGallery = ({ images, propertyId, onUpdate, editable = false }) => {
  const [selectedImage, setSelectedImage] = useState(null)
  const [deletingId, setDeletingId] = useState(null)
  const [settingPrimary, setSettingPrimary] = useState(null)

  const handleDelete = async (imageId) => {
    if (!window.confirm('Are you sure you want to delete this image?')) {
      return
    }

    setDeletingId(imageId)
    try {
      await axios.delete(`/api/properties/images/${imageId}/`)
      showToast.success('Image deleted successfully!')
      if (onUpdate) onUpdate()
    } catch (error) {
      showToast.error('Failed to delete image')
    } finally {
      setDeletingId(null)
    }
  }

  const handleSetPrimary = async (imageId) => {
    setSettingPrimary(imageId)
    try {
      await axios.patch(`/api/properties/images/${imageId}/`, {
        is_primary: true
      })
      showToast.success('Primary image updated!')
      if (onUpdate) onUpdate()
    } catch (error) {
      showToast.error('Failed to update primary image')
    } finally {
      setSettingPrimary(null)
    }
  }

  if (!images || images.length === 0) {
    return (
      <div className="text-center py-12 bg-gray-50 rounded-xl border-2 border-dashed border-gray-300">
        <svg className="mx-auto h-16 w-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <p className="mt-4 text-gray-600 font-semibold">No images uploaded yet</p>
        <p className="text-sm text-gray-500 mt-1">Upload images to showcase this property</p>
      </div>
    )
  }

  return (
    <div>
      {/* Image Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {images.map((image) => (
          <div key={image.id} className="relative group">
            <div 
              className="aspect-square rounded-lg overflow-hidden bg-gray-100 border-2 border-gray-200 cursor-pointer hover:border-blue-500 transition-colors"
              onClick={() => setSelectedImage(image)}
            >
              <img
                src={image.image}
                alt={image.caption || 'Property image'}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              />
            </div>

            {/* Primary Badge */}
            {image.is_primary && (
              <div className="absolute top-2 left-2 bg-blue-600 text-white text-xs px-2 py-1 rounded-full font-semibold shadow-lg">
                ⭐ Primary
              </div>
            )}

            {/* Action Buttons (only if editable) */}
            {editable && (
              <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity space-y-1">
                {!image.is_primary && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      handleSetPrimary(image.id)
                    }}
                    disabled={settingPrimary === image.id}
                    className="block w-full px-2 py-1 bg-green-600 text-white text-xs rounded hover:bg-green-700 transition-colors disabled:opacity-50"
                    title="Set as primary"
                  >
                    {settingPrimary === image.id ? '...' : '⭐ Primary'}
                  </button>
                )}
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    handleDelete(image.id)
                  }}
                  disabled={deletingId === image.id}
                  className="block w-full px-2 py-1 bg-red-600 text-white text-xs rounded hover:bg-red-700 transition-colors disabled:opacity-50"
                  title="Delete image"
                >
                  {deletingId === image.id ? '...' : '🗑️ Delete'}
                </button>
              </div>
            )}

            {/* Caption */}
            {image.caption && (
              <p className="mt-1 text-xs text-gray-600 truncate" title={image.caption}>
                {image.caption}
              </p>
            )}
          </div>
        ))}
      </div>

      {/* Lightbox Modal */}
      {selectedImage && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-90 z-50 flex items-center justify-center p-4"
          onClick={() => setSelectedImage(null)}
        >
          <div className="relative max-w-6xl max-h-full">
            {/* Close Button */}
            <button
              onClick={() => setSelectedImage(null)}
              className="absolute -top-12 right-0 text-white hover:text-gray-300 transition-colors"
            >
              <svg className="h-10 w-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>

            {/* Image */}
            <img
              src={selectedImage.image}
              alt={selectedImage.caption || 'Property image'}
              className="max-w-full max-h-[90vh] object-contain rounded-lg"
              onClick={(e) => e.stopPropagation()}
            />

            {/* Caption */}
            {selectedImage.caption && (
              <div className="absolute bottom-0 left-0 right-0 bg-black bg-opacity-75 text-white p-4 rounded-b-lg">
                <p className="text-center">{selectedImage.caption}</p>
              </div>
            )}

            {/* Navigation */}
            <div className="absolute top-1/2 -translate-y-1/2 left-0 right-0 flex justify-between px-4">
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  const currentIndex = images.findIndex(img => img.id === selectedImage.id)
                  const prevIndex = currentIndex > 0 ? currentIndex - 1 : images.length - 1
                  setSelectedImage(images[prevIndex])
                }}
                className="bg-white bg-opacity-20 hover:bg-opacity-30 text-white rounded-full p-3 transition-all"
              >
                <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  const currentIndex = images.findIndex(img => img.id === selectedImage.id)
                  const nextIndex = currentIndex < images.length - 1 ? currentIndex + 1 : 0
                  setSelectedImage(images[nextIndex])
                }}
                className="bg-white bg-opacity-20 hover:bg-opacity-30 text-white rounded-full p-3 transition-all"
              >
                <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>

            {/* Image Counter */}
            <div className="absolute top-4 left-1/2 -translate-x-1/2 bg-black bg-opacity-75 text-white px-4 py-2 rounded-full text-sm">
              {images.findIndex(img => img.id === selectedImage.id) + 1} / {images.length}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ImageGallery

