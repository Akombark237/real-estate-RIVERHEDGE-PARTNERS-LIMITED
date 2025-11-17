import { useContext } from 'react'
import { Navigate } from 'react-router-dom'
import { AuthContext } from '../context/AuthContext'

const DefaultRedirect = () => {
  const { user, loading } = useContext(AuthContext)

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  // Redirect based on user role
  if (user?.role === 'client') {
    return <Navigate to="/about" replace />
  }

  // Admin and agent go to dashboard
  return <Navigate to="/dashboard" replace />
}

export default DefaultRedirect

