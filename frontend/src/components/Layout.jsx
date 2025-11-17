import { useContext } from 'react'
import { Outlet, Link, useNavigate } from 'react-router-dom'
import { AuthContext } from '../context/AuthContext'
import NotificationBell from './NotificationBell'
import GlobalSearch from './GlobalSearch'

const Layout = () => {
  const { user, logout } = useContext(AuthContext)
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Navigation */}
      <nav className="bg-white shadow-lg border-b-4 border-blue-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-20">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <img src="/logo.svg" alt="RIVERHEDGE PARTNERS" className="h-12 w-12 mr-3" />
                <div>
                  <h1 className="text-xl font-bold text-blue-600">
                    RIVERHEDGE PARTNERS
                  </h1>
                  <p className="text-xs text-gray-500">Real Estate Platform</p>
                </div>
              </div>
              <div className="hidden sm:ml-8 sm:flex sm:space-x-4">
                {/* Show only About page for normal users (client role) */}
                {user?.role === 'client' ? (
                  <Link
                    to="/about"
                    className="bg-blue-50 border-blue-500 text-blue-700 inline-flex items-center px-4 py-2 border-b-2 text-sm font-semibold rounded-t-lg hover:bg-blue-100 transition-colors"
                  >
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    About Us
                  </Link>
                ) : (
                  <>
                    {/* Show all pages for admin and agent users */}
                    <Link
                      to="/dashboard"
                      className="bg-blue-50 border-blue-500 text-blue-700 inline-flex items-center px-4 py-2 border-b-2 text-sm font-semibold rounded-t-lg hover:bg-blue-100 transition-colors"
                    >
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                      </svg>
                      Dashboard
                    </Link>
                    <Link
                      to="/materials"
                      className="border-transparent text-gray-600 hover:bg-gray-50 hover:text-gray-900 inline-flex items-center px-4 py-2 border-b-2 text-sm font-medium rounded-t-lg transition-colors"
                    >
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                      </svg>
                      Materials
                    </Link>
                    <Link
                      to="/properties"
                      className="border-transparent text-gray-600 hover:bg-gray-50 hover:text-gray-900 inline-flex items-center px-4 py-2 border-b-2 text-sm font-medium rounded-t-lg transition-colors"
                    >
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z" />
                      </svg>
                      Properties
                    </Link>
                    <Link
                      to="/transactions"
                      className="border-transparent text-gray-600 hover:bg-gray-50 hover:text-gray-900 inline-flex items-center px-4 py-2 border-b-2 text-sm font-medium rounded-t-lg transition-colors"
                    >
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      Transactions
                    </Link>
                    <Link
                      to="/estimates"
                      className="border-transparent text-gray-600 hover:bg-gray-50 hover:text-gray-900 inline-flex items-center px-4 py-2 border-b-2 text-sm font-medium rounded-t-lg transition-colors"
                    >
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                      </svg>
                      Cost Estimates
                    </Link>
                    <Link
                      to="/reports"
                      className="border-transparent text-gray-600 hover:bg-gray-50 hover:text-gray-900 inline-flex items-center px-4 py-2 border-b-2 text-sm font-medium rounded-t-lg transition-colors"
                    >
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      Reports
                    </Link>
                    <Link
                      to="/documents"
                      className="border-transparent text-gray-600 hover:bg-gray-50 hover:text-gray-900 inline-flex items-center px-4 py-2 border-b-2 text-sm font-medium rounded-t-lg transition-colors"
                    >
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      Documents
                    </Link>
                    <Link
                      to="/activity-logs"
                      className="border-transparent text-gray-600 hover:bg-gray-50 hover:text-gray-900 inline-flex items-center px-4 py-2 border-b-2 text-sm font-medium rounded-t-lg transition-colors"
                    >
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      Activity
                    </Link>
                    <Link
                      to="/about"
                      className="border-transparent text-gray-600 hover:bg-gray-50 hover:text-gray-900 inline-flex items-center px-4 py-2 border-b-2 text-sm font-medium rounded-t-lg transition-colors"
                    >
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      About Us
                    </Link>
                    {user?.role === 'admin' && (
                      <Link
                        to="/admin"
                        className="border-transparent text-red-600 hover:bg-red-50 hover:text-red-700 inline-flex items-center px-4 py-2 border-b-2 text-sm font-medium rounded-t-lg transition-colors"
                      >
                        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
                        </svg>
                        Admin
                      </Link>
                    )}
                  </>
                )}
              </div>
            </div>
            <div className="flex items-center space-x-4">
              {/* Global Search */}
              <div className="w-96">
                <GlobalSearch />
              </div>

              {/* Notification Bell */}
              <NotificationBell />

              <Link
                to="/profile"
                className="flex items-center bg-gray-50 rounded-lg px-4 py-2 hover:bg-gray-100 transition-colors"
              >
                <div className="flex-shrink-0">
                  <div className="h-10 w-10 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center text-white font-bold text-lg">
                    {(user?.first_name?.[0] || user?.username?.[0] || user?.email?.[0] || 'U').toUpperCase()}
                  </div>
                </div>
                <div className="ml-3">
                  <p className="text-sm font-semibold text-gray-900">
                    {user?.first_name || user?.username || 'User'}
                  </p>
                  <p className="text-xs text-gray-500">
                    {user?.role || 'Member'}
                  </p>
                </div>
              </Link>
              <button
                onClick={handleLogout}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-semibold rounded-lg text-white bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 transition-all duration-200 shadow-md hover:shadow-lg"
              >
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <Outlet />
      </main>
    </div>
  )
}

export default Layout

