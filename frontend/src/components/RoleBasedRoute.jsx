import { useContext } from 'react'
import { Navigate } from 'react-router-dom'
import { AuthContext } from '../context/AuthContext'

const RoleBasedRoute = ({ children, allowedRoles }) => {
  const { user, loading } = useContext(AuthContext)

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  // If allowedRoles is provided, check if user's role is in the list
  if (allowedRoles && !allowedRoles.includes(user.role)) {
    // Redirect to About page for unauthorized users
    return <Navigate to="/about" replace />
  }

  return children
}

export default RoleBasedRoute

