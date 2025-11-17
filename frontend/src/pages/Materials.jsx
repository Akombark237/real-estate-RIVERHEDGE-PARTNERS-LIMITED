import { useState, useEffect } from 'react'
import axios from 'axios'
import showToast, { getErrorMessage } from '../utils/toast'

const Materials = () => {
  const [materials, setMaterials] = useState([])
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [showForm, setShowForm] = useState(false)
  const [editingMaterial, setEditingMaterial] = useState(null)
  const [deletingId, setDeletingId] = useState(null)
  const [formData, setFormData] = useState({
    name: '',
    category: 'structural',
    unit: 'piece',
    description: ''
  })

  useEffect(() => {
    fetchMaterials()
  }, [])

  const fetchMaterials = async () => {
    try {
      const response = await axios.get('/api/materials/')
      console.log('Materials response:', response.data)
      setMaterials(response.data.results || response.data)
    } catch (error) {
      console.error('Failed to fetch materials:', error)
      showToast.error(getErrorMessage(error))
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    // Validation
    if (!formData.name.trim()) {
      showToast.error('Material name is required')
      return
    }

    setSubmitting(true)
    try {
      if (editingMaterial) {
        // Update existing material
        console.log('Updating material:', formData)
        const response = await axios.put(`/api/materials/${editingMaterial.id}/`, formData)
        console.log('Material updated:', response.data)
        showToast.success('Material updated successfully!')
      } else {
        // Create new material
        console.log('Submitting material:', formData)
        const response = await axios.post('/api/materials/', formData)
        console.log('Material created:', response.data)
        showToast.success('Material added successfully!')
      }
      setShowForm(false)
      setEditingMaterial(null)
      setFormData({ name: '', category: 'structural', unit: 'piece', description: '' })
      fetchMaterials()
    } catch (error) {
      console.error('Failed to save material:', error)
      console.error('Error response:', error.response?.data)
      showToast.error(getErrorMessage(error))
    } finally {
      setSubmitting(false)
    }
  }

  const handleEdit = (material) => {
    setEditingMaterial(material)
    setFormData({
      name: material.name,
      category: material.category,
      unit: material.unit,
      description: material.description || ''
    })
    setShowForm(true)
  }

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this material? This action cannot be undone.')) {
      return
    }

    setDeletingId(id)
    try {
      await axios.delete(`/api/materials/${id}/`)
      showToast.success('Material deleted successfully!')
      fetchMaterials()
    } catch (error) {
      console.error('Failed to delete material:', error)
      showToast.error(getErrorMessage(error))
    } finally {
      setDeletingId(null)
    }
  }

  const handleCancelEdit = () => {
    setShowForm(false)
    setEditingMaterial(null)
    setFormData({ name: '', category: 'structural', unit: 'piece', description: '' })
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  if (loading) {
    return <div className="text-center py-8">Loading...</div>
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      {/* Header with gradient */}
      <div className="bg-gradient-to-r from-green-600 to-green-700 rounded-xl shadow-lg p-8 mb-6 relative overflow-hidden">
        <div className="absolute top-0 right-0 opacity-10">
          <svg className="h-48 w-48" fill="currentColor" viewBox="0 0 24 24">
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
          </svg>
        </div>
        <div className="relative z-10 flex justify-between items-center">
          <div>
            <h1 className="text-4xl font-bold text-white mb-2">Building Materials</h1>
            <p className="text-green-100 text-lg">Manage your construction materials inventory</p>
          </div>
          <button
            onClick={() => {
              if (showForm) {
                handleCancelEdit()
              } else {
                setShowForm(true)
              }
            }}
            className="px-6 py-3 bg-white text-green-700 rounded-lg hover:bg-green-50 font-semibold shadow-md transition-all duration-200 transform hover:scale-105"
          >
            {showForm ? '✕ Cancel' : '+ Add Material'}
          </button>
        </div>
      </div>

      {showForm && (
        <div className="bg-white shadow-xl rounded-2xl p-8 mb-6 border border-green-100">
          <div className="flex items-center mb-6">
            <div className="bg-green-100 p-3 rounded-lg mr-4">
              <svg className="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                {editingMaterial ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
                )}
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-900">
              {editingMaterial ? 'Edit Material' : 'Add New Material'}
            </h2>
          </div>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700">Name</label>
              <input
                type="text"
                name="name"
                required
                value={formData.name}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border"
              />
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Category</label>
                <select
                  name="category"
                  value={formData.category}
                  onChange={handleChange}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border"
                >
                  <option value="structural">Structural Materials</option>
                  <option value="finishing">Finishing Materials</option>
                  <option value="electrical">Electrical Supplies</option>
                  <option value="plumbing">Plumbing Supplies</option>
                  <option value="roofing">Roofing Materials</option>
                  <option value="flooring">Flooring Materials</option>
                  <option value="paint">Paint & Coatings</option>
                  <option value="hardware">Hardware</option>
                  <option value="other">Other</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Unit</label>
                <select
                  name="unit"
                  value={formData.unit}
                  onChange={handleChange}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border"
                >
                  <option value="piece">Piece</option>
                  <option value="kg">Kilogram</option>
                  <option value="bag">Bag</option>
                  <option value="ton">Ton</option>
                  <option value="sqm">Square Meter</option>
                  <option value="sqft">Square Foot</option>
                  <option value="liter">Liter</option>
                  <option value="gallon">Gallon</option>
                  <option value="meter">Meter</option>
                  <option value="foot">Foot</option>
                  <option value="bundle">Bundle</option>
                  <option value="box">Box</option>
                </select>
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700">Description</label>
              <textarea
                name="description"
                rows="3"
                value={formData.description}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm px-3 py-2 border"
              />
            </div>
            
            <button
              type="submit"
              disabled={submitting}
              className="w-full px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {submitting ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {editingMaterial ? 'Updating...' : 'Creating...'}
                </>
              ) : (
                editingMaterial ? 'Update Material' : 'Create Material'
              )}
            </button>
          </form>
        </div>
      )}

      {/* Materials List */}
      <div className="bg-white shadow-xl rounded-2xl overflow-hidden border border-gray-100">
        <div className="bg-gradient-to-r from-gray-50 to-white px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">
            Materials Inventory ({materials.length})
          </h3>
        </div>
        <ul className="divide-y divide-gray-200">
          {materials.length === 0 ? (
            <li className="px-6 py-12 text-center">
              <div className="flex flex-col items-center">
                <div className="bg-gray-100 p-4 rounded-full mb-4">
                  <svg className="h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
                  </svg>
                </div>
                <p className="text-gray-500 text-lg font-medium">No materials found</p>
                <p className="text-gray-400 text-sm mt-1">Add your first material to get started!</p>
              </div>
            </li>
          ) : (
            materials.map((material) => (
              <li key={material.id} className="px-6 py-5 hover:bg-green-50 transition-colors duration-150">
                <div className="flex items-center justify-between">
                  <div className="flex items-start flex-1">
                    <div className="bg-green-100 p-3 rounded-lg mr-4">
                      <svg className="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
                      </svg>
                    </div>
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-gray-900">{material.name}</h3>
                      <div className="flex items-center mt-1 space-x-4">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                          {material.category}
                        </span>
                        <span className="text-sm text-gray-500">
                          Unit: <span className="font-medium text-gray-700">{material.unit}</span>
                        </span>
                      </div>
                      {material.description && (
                        <p className="mt-2 text-sm text-gray-600">{material.description}</p>
                      )}
                      {material.current_price && (
                        <p className="mt-2 text-sm font-semibold text-green-600">
                          💰 Current Price: ${material.current_price}
                        </p>
                      )}
                    </div>
                  </div>
                  <div className="ml-4 flex flex-col items-end space-y-2">
                    <span className={`px-3 py-1 text-xs font-semibold rounded-full ${
                      material.is_active
                        ? 'bg-green-100 text-green-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      {material.is_active ? '✓ Active' : 'Inactive'}
                    </span>
                    <div className="flex space-x-2 mt-2">
                      <button
                        onClick={() => handleEdit(material)}
                        className="px-3 py-1.5 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors duration-200 flex items-center"
                      >
                        <svg className="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                        </svg>
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(material.id)}
                        disabled={deletingId === material.id}
                        className="px-3 py-1.5 bg-red-600 text-white text-sm rounded-lg hover:bg-red-700 transition-colors duration-200 flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {deletingId === material.id ? (
                          <>
                            <svg className="animate-spin h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24">
                              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Deleting...
                          </>
                        ) : (
                          <>
                            <svg className="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                            </svg>
                            Delete
                          </>
                        )}
                      </button>
                    </div>
                  </div>
                </div>
              </li>
            ))
          )}
        </ul>
      </div>
    </div>
  )
}

export default Materials

