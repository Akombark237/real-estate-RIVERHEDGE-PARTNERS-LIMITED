import { useState, useEffect } from 'react';
import axios from 'axios';
import showToast, { getErrorMessage } from '../utils/toast';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Line } from 'react-chartjs-2';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const MaterialPrices = () => {
  const [materials, setMaterials] = useState([]);
  const [selectedMaterial, setSelectedMaterial] = useState(null);
  const [priceHistory, setPriceHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    material: '',
    price: '',
    currency: 'USD',
    region: '',
    source: 'manual',
    notes: ''
  });

  useEffect(() => {
    fetchMaterials();
  }, []);

  useEffect(() => {
    if (selectedMaterial) {
      fetchPriceHistory(selectedMaterial.id);
    }
  }, [selectedMaterial]);

  const fetchMaterials = async () => {
    try {
      const response = await axios.get('/api/materials/');
      const materialsData = response.data.results || response.data;
      setMaterials(materialsData);
      if (materialsData.length > 0 && !selectedMaterial) {
        setSelectedMaterial(materialsData[0]);
      }
    } catch (error) {
      console.error('Failed to fetch materials:', error);
      showToast.error(getErrorMessage(error));
    } finally {
      setLoading(false);
    }
  };

  const fetchPriceHistory = async (materialId) => {
    try {
      const response = await axios.get(`/api/materials/prices/?material_id=${materialId}`);
      setPriceHistory(response.data.results || response.data);
    } catch (error) {
      console.error('Failed to fetch price history:', error);
      showToast.error(getErrorMessage(error));
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      await axios.post('/api/materials/prices/', formData);
      showToast.success('Price added successfully!');
      
      // Refresh price history
      if (selectedMaterial) {
        fetchPriceHistory(selectedMaterial.id);
      }
      
      // Reset form
      setFormData({
        material: selectedMaterial?.id || '',
        price: '',
        currency: 'USD',
        region: '',
        source: 'manual',
        notes: ''
      });
      setShowForm(false);
    } catch (error) {
      console.error('Error adding price:', error);
      showToast.error(getErrorMessage(error));
    } finally {
      setSubmitting(false);
    }
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(price);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const formatDateTime = (dateString) => {
    return new Date(dateString).toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  // Calculate statistics
  const calculateStats = () => {
    if (priceHistory.length === 0) return null;

    const prices = priceHistory.map(p => parseFloat(p.price));
    const currentPrice = prices[0];
    const avgPrice = prices.reduce((a, b) => a + b, 0) / prices.length;
    const minPrice = Math.min(...prices);
    const maxPrice = Math.max(...prices);
    
    // Calculate trend (comparing current to average)
    const trend = currentPrice > avgPrice ? 'up' : currentPrice < avgPrice ? 'down' : 'stable';
    const trendPercent = avgPrice > 0 ? ((currentPrice - avgPrice) / avgPrice * 100).toFixed(2) : 0;

    return {
      current: currentPrice,
      average: avgPrice,
      min: minPrice,
      max: maxPrice,
      trend,
      trendPercent
    };
  };

  const stats = calculateStats();

  // Prepare chart data
  const chartData = {
    labels: priceHistory.slice().reverse().map(p => formatDate(p.recorded_at)),
    datasets: [
      {
        label: 'Price',
        data: priceHistory.slice().reverse().map(p => parseFloat(p.price)),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: true,
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 6,
        pointBackgroundColor: 'rgb(59, 130, 246)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      },
      title: {
        display: false
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        padding: 12,
        titleFont: {
          size: 14
        },
        bodyFont: {
          size: 13
        },
        callbacks: {
          label: function(context) {
            return 'Price: ' + formatPrice(context.parsed.y);
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: false,
        ticks: {
          callback: function(value) {
            return '$' + value.toFixed(2);
          }
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)'
        }
      },
      x: {
        grid: {
          display: false
        }
      }
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      {/* Header */}
      <div className="bg-gradient-to-r from-green-600 to-green-700 rounded-xl shadow-lg p-8 mb-6 relative overflow-hidden">
        <div className="absolute top-0 right-0 opacity-10">
          <svg className="h-48 w-48" fill="currentColor" viewBox="0 0 24 24">
            <path d="M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z"/>
          </svg>
        </div>
        <div className="relative z-10 flex justify-between items-center">
          <div>
            <h1 className="text-4xl font-bold text-white mb-2">Material Price Tracking</h1>
            <p className="text-green-100 text-lg">Monitor price trends and history</p>
          </div>
          <button
            onClick={() => {
              if (showForm) {
                setShowForm(false);
              } else {
                setFormData(prev => ({ ...prev, material: selectedMaterial?.id || '' }));
                setShowForm(true);
              }
            }}
            className="px-6 py-3 bg-white text-green-600 rounded-lg hover:bg-green-50 transition-colors font-semibold shadow-lg flex items-center"
          >
            {showForm ? (
              <>
                <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
                Cancel
              </>
            ) : (
              <>
                <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Add Price
              </>
            )}
          </button>
        </div>
      </div>

      {/* Material Selector */}
      <div className="bg-white shadow-xl rounded-2xl p-6 mb-6 border border-gray-100">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Select Material
        </label>
        <select
          value={selectedMaterial?.id || ''}
          onChange={(e) => {
            const material = materials.find(m => m.id === parseInt(e.target.value));
            setSelectedMaterial(material);
          }}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent text-lg"
        >
          {materials.map(material => (
            <option key={material.id} value={material.id}>
              {material.name} ({material.category}) - {material.unit}
            </option>
          ))}
        </select>
      </div>

      {/* Add Price Form */}
      {showForm && (
        <div className="bg-white shadow-xl rounded-2xl p-6 mb-6 border border-gray-100">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Add New Price</h2>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Price <span className="text-red-500">*</span>
                </label>
                <input
                  type="number"
                  name="price"
                  value={formData.price}
                  onChange={handleChange}
                  required
                  step="0.01"
                  min="0"
                  placeholder="0.00"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Currency
                </label>
                <select
                  name="currency"
                  value={formData.currency}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                >
                  <option value="USD">USD</option>
                  <option value="EUR">EUR</option>
                  <option value="GBP">GBP</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Region
                </label>
                <input
                  type="text"
                  name="region"
                  value={formData.region}
                  onChange={handleChange}
                  placeholder="e.g., New York, London"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Source
                </label>
                <select
                  name="source"
                  value={formData.source}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                >
                  <option value="manual">Manual Entry</option>
                  <option value="api">API Integration</option>
                  <option value="scraper">Web Scraper</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Notes
              </label>
              <textarea
                name="notes"
                value={formData.notes}
                onChange={handleChange}
                rows="2"
                placeholder="Additional notes..."
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
            </div>

            <div className="flex justify-end space-x-3">
              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-semibold"
                disabled={submitting}
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={submitting}
                className="px-6 py-2 bg-gradient-to-r from-green-600 to-green-700 text-white rounded-lg hover:from-green-700 hover:to-green-800 transition-all font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {submitting ? 'Adding...' : 'Add Price'}
              </button>
            </div>
          </form>
        </div>
      )}

      {selectedMaterial && (
        <>
          {/* Statistics Cards */}
          {stats && (
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              <div className="bg-white shadow-lg rounded-xl p-6 border-l-4 border-blue-500">
                <div className="text-sm text-gray-600 mb-1">Current Price</div>
                <div className="text-2xl font-bold text-gray-900">{formatPrice(stats.current)}</div>
              </div>
              <div className="bg-white shadow-lg rounded-xl p-6 border-l-4 border-green-500">
                <div className="text-sm text-gray-600 mb-1">Average Price</div>
                <div className="text-2xl font-bold text-gray-900">{formatPrice(stats.average)}</div>
              </div>
              <div className="bg-white shadow-lg rounded-xl p-6 border-l-4 border-yellow-500">
                <div className="text-sm text-gray-600 mb-1">Min / Max</div>
                <div className="text-lg font-bold text-gray-900">
                  {formatPrice(stats.min)} / {formatPrice(stats.max)}
                </div>
              </div>
              <div className="bg-white shadow-lg rounded-xl p-6 border-l-4 border-purple-500">
                <div className="text-sm text-gray-600 mb-1">Trend</div>
                <div className="flex items-center">
                  {stats.trend === 'up' && (
                    <svg className="h-6 w-6 text-red-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                    </svg>
                  )}
                  {stats.trend === 'down' && (
                    <svg className="h-6 w-6 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
                    </svg>
                  )}
                  <span className={`text-xl font-bold ${stats.trend === 'up' ? 'text-red-500' : stats.trend === 'down' ? 'text-green-500' : 'text-gray-500'}`}>
                    {stats.trendPercent > 0 ? '+' : ''}{stats.trendPercent}%
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Price Chart */}
          {priceHistory.length > 0 && (
            <div className="bg-white shadow-xl rounded-2xl p-6 mb-6 border border-gray-100">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Price History Chart</h3>
              <div style={{ height: '400px' }}>
                <Line data={chartData} options={chartOptions} />
              </div>
            </div>
          )}

          {/* Price History Table */}
          <div className="bg-white shadow-xl rounded-2xl overflow-hidden border border-gray-100">
            <div className="bg-gradient-to-r from-gray-50 to-white px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">
                Price History ({priceHistory.length} records)
              </h3>
            </div>

            {priceHistory.length === 0 ? (
              <div className="px-6 py-12 text-center">
                <p className="text-gray-500">No price history available for this material</p>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Region</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Source</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Notes</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {priceHistory.map((price) => (
                      <tr key={price.id} className="hover:bg-green-50 transition-colors">
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {formatDateTime(price.recorded_at)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className="text-sm font-semibold text-gray-900">{formatPrice(price.price)}</span>
                          <span className="text-xs text-gray-500 ml-1">{price.currency}</span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {price.region || 'N/A'}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {price.source}
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-500">
                          {price.notes || '-'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default MaterialPrices;

