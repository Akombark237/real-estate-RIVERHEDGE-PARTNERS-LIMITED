import { useState, useEffect } from 'react'
import axios from 'axios'
import showToast, { getErrorMessage } from '../utils/toast'

const CostEstimates = () => {
  const [estimates, setEstimates] = useState([])
  const [loading, setLoading] = useState(true)
  const [showCalculator, setShowCalculator] = useState(false)
  const [calculatorData, setCalculatorData] = useState({
    project_type: 'new_construction',
    quality_level: 'standard',
    area_sqft: ''
  })
  const [calculationResult, setCalculationResult] = useState(null)

  useEffect(() => {
    fetchEstimates()
  }, [])

  const fetchEstimates = async () => {
    try {
      const response = await axios.get('/api/estimates/')
      setEstimates(response.data.results || response.data)
    } catch (error) {
      console.error('Failed to fetch estimates:', error)
      showToast.error(getErrorMessage(error))
    } finally {
      setLoading(false)
    }
  }

  const handleCalculate = async (e) => {
    e.preventDefault()

    // Client-side calculation as fallback
    const calculateClientSide = () => {
      const baseCosts = {
        'basic': 80,
        'standard': 120,
        'premium': 180,
        'luxury': 250,
      }

      const baseCostPerSqft = baseCosts[calculatorData.quality_level] || 120
      const area = parseFloat(calculatorData.area_sqft) || 0

      const materialCost = area * baseCostPerSqft * 0.60  // 60% materials
      const laborCost = area * baseCostPerSqft * 0.30     // 30% labor
      const overheadCost = area * baseCostPerSqft * 0.10  // 10% overhead
      const totalCost = materialCost + laborCost + overheadCost

      return {
        area_sqft: area,
        quality_level: calculatorData.quality_level,
        base_cost_per_sqft: baseCostPerSqft,
        material_cost: materialCost.toFixed(2),
        labor_cost: laborCost.toFixed(2),
        overhead_cost: overheadCost.toFixed(2),
        total_cost: totalCost.toFixed(2),
        currency: 'USD'
      }
    }

    try {
      const response = await axios.post('/api/estimates/calculate/', calculatorData)
      setCalculationResult(response.data)
    } catch (error) {
      console.error('Failed to calculate estimate from server, using client-side calculation:', error)
      // Use client-side calculation as fallback
      const result = calculateClientSide()
      setCalculationResult(result)
    }
  }

  const handleSaveEstimate = async () => {
    if (!calculationResult) return

    try {
      const estimateData = {
        project_name: `${calculatorData.project_type} - ${calculatorData.quality_level}`,
        project_type: calculatorData.project_type,
        quality_level: calculatorData.quality_level,
        area_sqft: calculatorData.area_sqft,
        material_cost: calculationResult.material_cost,
        labor_cost: calculationResult.labor_cost,
        equipment_cost: 0,
        overhead_cost: calculationResult.overhead_cost,
        total_cost: calculationResult.total_cost,
        status: 'draft'
      }

      await axios.post('/api/estimates/', estimateData)
      showToast.success('Estimate saved successfully!')
      setShowCalculator(false)
      setCalculationResult(null)
      setCalculatorData({ project_type: 'new_construction', quality_level: 'standard', area_sqft: '' })
      fetchEstimates()
    } catch (error) {
      console.error('Failed to save estimate:', error)
      showToast.error(getErrorMessage(error))
    }
  }

  const handleChange = (e) => {
    setCalculatorData({
      ...calculatorData,
      [e.target.name]: e.target.value
    })
    setCalculationResult(null)
  }

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-16">
        <svg className="animate-spin h-12 w-12 text-purple-600 mb-4" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p className="text-gray-600 font-medium">Loading estimates...</p>
      </div>
    )
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      {/* Header with gradient */}
      <div className="bg-gradient-to-r from-purple-600 to-purple-700 rounded-2xl shadow-xl p-8 mb-8 text-white relative overflow-hidden">
        <div className="absolute top-0 right-0 opacity-10">
          <svg className="h-64 w-64" fill="currentColor" viewBox="0 0 24 24">
            <path d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
          </svg>
        </div>
        <div className="relative z-10 flex justify-between items-center">
          <div>
            <h1 className="text-4xl font-bold mb-2">Cost Estimates 🧮</h1>
            <p className="text-purple-100">Calculate and manage project cost estimates</p>
          </div>
          <button
            onClick={() => setShowCalculator(!showCalculator)}
            className="inline-flex items-center px-6 py-3 bg-white text-purple-700 rounded-lg hover:bg-purple-50 transition-all duration-200 shadow-lg hover:shadow-xl font-semibold transform hover:-translate-y-0.5"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {showCalculator ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
              )}
            </svg>
            {showCalculator ? 'Close Calculator' : 'New Estimate'}
          </button>
        </div>
      </div>

      {showCalculator && (
        <div className="bg-white shadow-2xl rounded-2xl p-8 mb-8 border border-purple-100">
          <div className="flex items-center mb-6">
            <div className="bg-purple-100 rounded-lg p-3 mr-4">
              <svg className="h-8 w-8 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Cost Calculator</h2>
              <p className="text-sm text-gray-500">Enter project details to estimate costs</p>
            </div>
          </div>
          <form onSubmit={handleCalculate} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  <span className="flex items-center">
                    <svg className="w-4 h-4 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                    Project Type
                  </span>
                </label>
                <select
                  name="project_type"
                  value={calculatorData.project_type}
                  onChange={handleChange}
                  className="mt-1 block w-full rounded-lg border-2 border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500 px-4 py-3 text-base transition-colors"
                >
                  <option value="new_construction">🏗️ New Construction</option>
                  <option value="renovation">🔨 Renovation</option>
                  <option value="extension">📐 Extension</option>
                  <option value="remodeling">🎨 Remodeling</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  <span className="flex items-center">
                    <svg className="w-4 h-4 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                    </svg>
                    Quality Level
                  </span>
                </label>
                <select
                  name="quality_level"
                  value={calculatorData.quality_level}
                  onChange={handleChange}
                  className="mt-1 block w-full rounded-lg border-2 border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500 px-4 py-3 text-base transition-colors"
                >
                  <option value="basic">💰 Basic ($80/sqft)</option>
                  <option value="standard">⭐ Standard ($120/sqft)</option>
                  <option value="premium">💎 Premium ($180/sqft)</option>
                  <option value="luxury">👑 Luxury ($250/sqft)</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                <span className="flex items-center">
                  <svg className="w-4 h-4 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
                  </svg>
                  Area (Square Feet)
                </span>
              </label>
              <input
                type="number"
                name="area_sqft"
                required
                min="1"
                step="0.01"
                value={calculatorData.area_sqft}
                onChange={handleChange}
                className="mt-1 block w-full rounded-lg border-2 border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500 px-4 py-3 text-base transition-colors"
                placeholder="Enter area in square feet (e.g., 2000)"
              />
            </div>

            <button
              type="submit"
              className="w-full px-6 py-4 bg-gradient-to-r from-purple-600 to-purple-700 text-white rounded-lg hover:from-purple-700 hover:to-purple-800 transition-all duration-200 shadow-lg hover:shadow-xl font-semibold text-lg transform hover:-translate-y-0.5 flex items-center justify-center"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
              Calculate Cost Estimate
            </button>
          </form>

          {calculationResult && (
            <div className="mt-8 p-6 bg-gradient-to-br from-purple-50 to-blue-50 rounded-2xl border-2 border-purple-200">
              <div className="flex items-center mb-6">
                <div className="bg-purple-600 rounded-full p-2 mr-3">
                  <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold text-gray-900">Cost Breakdown</h3>
              </div>

              <div className="space-y-4">
                <div className="bg-white rounded-lg p-4 shadow-sm flex justify-between items-center">
                  <div className="flex items-center">
                    <div className="bg-blue-100 rounded-lg p-2 mr-3">
                      <svg className="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                      </svg>
                    </div>
                    <span className="text-gray-700 font-medium">Base Cost per sqft:</span>
                  </div>
                  <span className="font-bold text-lg text-gray-900">${calculationResult.base_cost_per_sqft}</span>
                </div>

                <div className="bg-white rounded-lg p-4 shadow-sm flex justify-between items-center">
                  <div className="flex items-center">
                    <div className="bg-green-100 rounded-lg p-2 mr-3">
                      <svg className="h-5 w-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                      </svg>
                    </div>
                    <span className="text-gray-700 font-medium">Material Cost (60%):</span>
                  </div>
                  <span className="font-bold text-lg text-green-600">${parseFloat(calculationResult.material_cost).toLocaleString()}</span>
                </div>

                <div className="bg-white rounded-lg p-4 shadow-sm flex justify-between items-center">
                  <div className="flex items-center">
                    <div className="bg-orange-100 rounded-lg p-2 mr-3">
                      <svg className="h-5 w-5 text-orange-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                      </svg>
                    </div>
                    <span className="text-gray-700 font-medium">Labor Cost (30%):</span>
                  </div>
                  <span className="font-bold text-lg text-orange-600">${parseFloat(calculationResult.labor_cost).toLocaleString()}</span>
                </div>

                <div className="bg-white rounded-lg p-4 shadow-sm flex justify-between items-center">
                  <div className="flex items-center">
                    <div className="bg-purple-100 rounded-lg p-2 mr-3">
                      <svg className="h-5 w-5 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                      </svg>
                    </div>
                    <span className="text-gray-700 font-medium">Overhead Cost (10%):</span>
                  </div>
                  <span className="font-bold text-lg text-purple-600">${parseFloat(calculationResult.overhead_cost).toLocaleString()}</span>
                </div>

                <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl p-5 shadow-lg mt-4">
                  <div className="flex justify-between items-center">
                    <span className="text-xl font-bold text-white">Total Project Cost:</span>
                    <span className="text-3xl font-bold text-white">
                      ${parseFloat(calculationResult.total_cost).toLocaleString()}
                    </span>
                  </div>
                  <p className="text-purple-100 text-sm mt-2">For {calculationResult.area_sqft} square feet</p>
                </div>
              </div>

              <button
                onClick={handleSaveEstimate}
                className="mt-6 w-full px-6 py-4 bg-gradient-to-r from-green-600 to-green-700 text-white rounded-lg hover:from-green-700 hover:to-green-800 transition-all duration-200 shadow-lg hover:shadow-xl font-semibold text-lg transform hover:-translate-y-0.5 flex items-center justify-center"
              >
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
                </svg>
                Save This Estimate
              </button>
            </div>
          )}
        </div>
      )}

      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul className="divide-y divide-gray-200">
          {estimates.length === 0 ? (
            <li className="px-6 py-4 text-center text-gray-500">
              No estimates found. Create your first estimate!
            </li>
          ) : (
            estimates.map((estimate) => (
              <li key={estimate.id} className="px-6 py-4 hover:bg-gray-50">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h3 className="text-lg font-medium text-gray-900">{estimate.project_name}</h3>
                    <p className="text-sm text-gray-500">
                      {estimate.project_type} | {estimate.quality_level} | {estimate.area_sqft} sqft
                    </p>
                    <div className="mt-2 grid grid-cols-4 gap-4 text-sm">
                      <div>
                        <span className="text-gray-500">Materials:</span>
                        <span className="ml-1 font-medium">${parseFloat(estimate.material_cost).toLocaleString()}</span>
                      </div>
                      <div>
                        <span className="text-gray-500">Labor:</span>
                        <span className="ml-1 font-medium">${parseFloat(estimate.labor_cost).toLocaleString()}</span>
                      </div>
                      <div>
                        <span className="text-gray-500">Overhead:</span>
                        <span className="ml-1 font-medium">${parseFloat(estimate.overhead_cost).toLocaleString()}</span>
                      </div>
                      <div>
                        <span className="text-gray-500">Total:</span>
                        <span className="ml-1 font-bold text-primary-600">
                          ${parseFloat(estimate.total_cost).toLocaleString()}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="ml-4">
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      estimate.status === 'approved' ? 'bg-green-100 text-green-800' :
                      estimate.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {estimate.status}
                    </span>
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

export default CostEstimates

