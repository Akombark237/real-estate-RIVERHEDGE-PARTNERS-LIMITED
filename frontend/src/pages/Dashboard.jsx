import { useState, useEffect, useContext } from 'react'
import axios from 'axios'
import { AuthContext } from '../context/AuthContext'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { Line, Bar, Doughnut } from 'react-chartjs-2'

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const Dashboard = () => {
  const { user } = useContext(AuthContext)
  const [stats, setStats] = useState({
    properties: 0,
    materials: 0,
    estimates: 0,
    transactions: 0
  })
  const [loading, setLoading] = useState(true)
  const [transactions, setTransactions] = useState([])
  const [properties, setProperties] = useState([])
  const [revenueData, setRevenueData] = useState([])
  const [propertyStatusData, setPropertyStatusData] = useState({
    available: 0,
    pending: 0,
    sold: 0,
    rented: 0
  })

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      // Fetch data from different endpoints
      const [propertiesRes, materialsRes, estimatesRes, transactionsRes] = await Promise.all([
        axios.get('/api/properties/'),
        axios.get('/api/materials/'),
        axios.get('/api/estimates/'),
        axios.get('/api/properties/transactions/')
      ])

      const propertiesData = propertiesRes.data.results || propertiesRes.data || []
      const transactionsData = transactionsRes.data.results || transactionsRes.data || []

      setProperties(propertiesData)
      setTransactions(transactionsData)

      // Calculate property status distribution
      const statusCounts = {
        available: 0,
        pending: 0,
        sold: 0,
        rented: 0
      }
      propertiesData.forEach(prop => {
        if (statusCounts.hasOwnProperty(prop.status)) {
          statusCounts[prop.status]++
        }
      })
      setPropertyStatusData(statusCounts)

      // Calculate revenue data (last 6 months)
      const monthlyRevenue = calculateMonthlyRevenue(transactionsData)
      setRevenueData(monthlyRevenue)

      setStats({
        properties: propertiesData.length,
        materials: materialsRes.data.results?.length || materialsRes.data.length || 0,
        estimates: estimatesRes.data.results?.length || estimatesRes.data.length || 0,
        transactions: transactionsData.length
      })
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const calculateMonthlyRevenue = (transactionsData) => {
    const months = []
    const now = new Date()

    // Get last 6 months
    for (let i = 5; i >= 0; i--) {
      const date = new Date(now.getFullYear(), now.getMonth() - i, 1)
      months.push({
        month: date.toLocaleString('default', { month: 'short' }),
        year: date.getFullYear(),
        revenue: 0,
        commission: 0,
        count: 0
      })
    }

    // Calculate revenue for each month
    transactionsData.forEach(transaction => {
      if (transaction.status === 'completed' && transaction.transaction_date) {
        const transDate = new Date(transaction.transaction_date)
        const monthIndex = months.findIndex(m =>
          m.month === transDate.toLocaleString('default', { month: 'short' }) &&
          m.year === transDate.getFullYear()
        )

        if (monthIndex !== -1) {
          months[monthIndex].revenue += parseFloat(transaction.sale_price || 0)
          months[monthIndex].commission += parseFloat(transaction.commission_amount || 0)
          months[monthIndex].count += 1
        }
      }
    })

    return months
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="flex flex-col items-center">
          <svg className="animate-spin h-12 w-12 text-blue-600 mb-4" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <div className="text-xl text-gray-600">Loading your dashboard...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      {/* Welcome Banner with Background Image */}
      <div className="rounded-2xl shadow-xl mb-8 text-white relative overflow-hidden h-64">
        {/* Background Image */}
        <div
          className="absolute inset-0 bg-cover bg-center bg-no-repeat"
          style={{
            backgroundImage: 'url(https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2073&q=80)',
          }}
        >
          {/* Gradient Overlay */}
          <div className="absolute inset-0 bg-gradient-to-r from-blue-900/85 via-blue-800/75 to-purple-900/85"></div>
        </div>

        {/* Decorative SVG */}
        <div className="absolute top-0 right-0 opacity-10">
          <svg className="h-64 w-64" fill="currentColor" viewBox="0 0 24 24">
            <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
        </div>

        {/* Content */}
        <div className="relative z-10 h-full flex flex-col justify-center p-8">
          <h1 className="text-4xl font-bold mb-2 drop-shadow-lg">
            Welcome back, {user?.first_name || user?.username}! 👋
          </h1>
          <p className="text-blue-100 text-lg drop-shadow-md">
            Here's what's happening with your real estate business today
          </p>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 overflow-hidden shadow-lg rounded-xl transform hover:scale-105 transition-transform duration-200">
          <div className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-white bg-opacity-30 rounded-lg p-3">
                <svg className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-blue-100 truncate">
                    Properties
                  </dt>
                  <dd className="text-4xl font-bold text-white">
                    {stats.properties}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-green-500 to-green-600 overflow-hidden shadow-lg rounded-xl transform hover:scale-105 transition-transform duration-200">
          <div className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-white bg-opacity-30 rounded-lg p-3">
                <svg className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-green-100 truncate">
                    Materials
                  </dt>
                  <dd className="text-4xl font-bold text-white">
                    {stats.materials}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-purple-500 to-purple-600 overflow-hidden shadow-lg rounded-xl transform hover:scale-105 transition-transform duration-200">
          <div className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-white bg-opacity-30 rounded-lg p-3">
                <svg className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-purple-100 truncate">
                    Cost Estimates
                  </dt>
                  <dd className="text-4xl font-bold text-white">
                    {stats.estimates}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-orange-500 to-orange-600 overflow-hidden shadow-lg rounded-xl transform hover:scale-105 transition-transform duration-200">
          <div className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-white bg-opacity-30 rounded-lg p-3">
                <svg className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-orange-100 truncate">
                    Transactions
                  </dt>
                  <dd className="text-4xl font-bold text-white">
                    {stats.transactions}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Analytics Charts */}
      <div className="mt-8 mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Analytics & Insights</h2>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Revenue & Commission Chart */}
          <div className="bg-white shadow-xl rounded-2xl p-6 border border-gray-100">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <svg className="h-5 w-5 text-green-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Revenue & Commission (Last 6 Months)
            </h3>
            <div style={{ height: '300px' }}>
              <Bar
                data={{
                  labels: revenueData.map(d => d.month),
                  datasets: [
                    {
                      label: 'Revenue',
                      data: revenueData.map(d => d.revenue),
                      backgroundColor: 'rgba(59, 130, 246, 0.8)',
                      borderColor: 'rgb(59, 130, 246)',
                      borderWidth: 1,
                    },
                    {
                      label: 'Commission',
                      data: revenueData.map(d => d.commission),
                      backgroundColor: 'rgba(16, 185, 129, 0.8)',
                      borderColor: 'rgb(16, 185, 129)',
                      borderWidth: 1,
                    }
                  ]
                }}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: {
                      position: 'top',
                    },
                    tooltip: {
                      callbacks: {
                        label: function(context) {
                          return context.dataset.label + ': $' + context.parsed.y.toLocaleString();
                        }
                      }
                    }
                  },
                  scales: {
                    y: {
                      beginAtZero: true,
                      ticks: {
                        callback: function(value) {
                          return '$' + value.toLocaleString();
                        }
                      }
                    }
                  }
                }}
              />
            </div>
          </div>

          {/* Property Status Distribution */}
          <div className="bg-white shadow-xl rounded-2xl p-6 border border-gray-100">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <svg className="h-5 w-5 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              Property Status Distribution
            </h3>
            <div style={{ height: '300px' }} className="flex items-center justify-center">
              <div style={{ width: '280px', height: '280px' }}>
                <Doughnut
                  data={{
                    labels: ['Available', 'Pending', 'Sold', 'Rented'],
                    datasets: [{
                      data: [
                        propertyStatusData.available,
                        propertyStatusData.pending,
                        propertyStatusData.sold,
                        propertyStatusData.rented
                      ],
                      backgroundColor: [
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(251, 191, 36, 0.8)',
                        'rgba(239, 68, 68, 0.8)',
                        'rgba(59, 130, 246, 0.8)',
                      ],
                      borderColor: [
                        'rgb(16, 185, 129)',
                        'rgb(251, 191, 36)',
                        'rgb(239, 68, 68)',
                        'rgb(59, 130, 246)',
                      ],
                      borderWidth: 2,
                    }]
                  }}
                  options={{
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                      legend: {
                        position: 'bottom',
                      },
                      tooltip: {
                        callbacks: {
                          label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = total > 0 ? ((context.parsed / total) * 100).toFixed(1) : 0;
                            return context.label + ': ' + context.parsed + ' (' + percentage + '%)';
                          }
                        }
                      }
                    }
                  }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Transaction Trends */}
        <div className="bg-white shadow-xl rounded-2xl p-6 border border-gray-100">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <svg className="h-5 w-5 text-purple-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
            Transaction Trends
          </h3>
          <div style={{ height: '300px' }}>
            <Line
              data={{
                labels: revenueData.map(d => d.month),
                datasets: [{
                  label: 'Number of Transactions',
                  data: revenueData.map(d => d.count),
                  borderColor: 'rgb(147, 51, 234)',
                  backgroundColor: 'rgba(147, 51, 234, 0.1)',
                  fill: true,
                  tension: 0.4,
                  pointRadius: 5,
                  pointHoverRadius: 7,
                  pointBackgroundColor: 'rgb(147, 51, 234)',
                  pointBorderColor: '#fff',
                  pointBorderWidth: 2,
                }]
              }}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                  legend: {
                    display: false,
                  },
                  tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                  }
                },
                scales: {
                  y: {
                    beginAtZero: true,
                    ticks: {
                      stepSize: 1,
                      callback: function(value) {
                        return Number.isInteger(value) ? value : '';
                      }
                    }
                  }
                }
              }}
            />
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mt-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <a
            href="/properties"
            className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-1 border-l-4 border-blue-500"
          >
            <div className="flex items-center mb-2">
              <svg className="h-6 w-6 text-blue-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              <h3 className="text-lg font-medium text-gray-900">Add Property</h3>
            </div>
            <p className="mt-2 text-sm text-gray-500">
              List a new property for sale or rent
            </p>
          </a>
          <a
            href="/material-prices"
            className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-1 border-l-4 border-green-500"
          >
            <div className="flex items-center mb-2">
              <svg className="h-6 w-6 text-green-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <h3 className="text-lg font-medium text-gray-900">Price Tracking</h3>
            </div>
            <p className="mt-2 text-sm text-gray-500">
              Monitor material price trends
            </p>
          </a>
          <a
            href="/transactions"
            className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-1 border-l-4 border-purple-500"
          >
            <div className="flex items-center mb-2">
              <svg className="h-6 w-6 text-purple-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h3 className="text-lg font-medium text-gray-900">Transactions</h3>
            </div>
            <p className="mt-2 text-sm text-gray-500">
              Manage property sales & commissions
            </p>
          </a>
          <a
            href="/estimates"
            className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-1 border-l-4 border-orange-500"
          >
            <div className="flex items-center mb-2">
              <svg className="h-6 w-6 text-orange-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
              <h3 className="text-lg font-medium text-gray-900">Create Estimate</h3>
            </div>
            <p className="mt-2 text-sm text-gray-500">
              Calculate construction costs
            </p>
          </a>
        </div>
      </div>
    </div>
  )
}

export default Dashboard

