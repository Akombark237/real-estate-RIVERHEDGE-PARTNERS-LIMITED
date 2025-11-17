import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import { AuthProvider } from './context/AuthContext'
import Layout from './components/Layout'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Materials from './pages/Materials'
import Properties from './pages/Properties'
import PropertyDetail from './pages/PropertyDetail'
import CostEstimates from './pages/CostEstimates'
import Profile from './pages/Profile'
import About from './pages/About'
import AboutEditor from './pages/AboutEditor'
import Transactions from './pages/Transactions'
import MaterialPrices from './pages/MaterialPrices'
import Reports from './pages/Reports'
import Notifications from './pages/Notifications'
import Documents from './pages/Documents'
import ActivityLogs from './pages/ActivityLogs'
import Admin from './pages/Admin'
import PrivateRoute from './components/PrivateRoute'
import RoleBasedRoute from './components/RoleBasedRoute'
import DefaultRedirect from './components/DefaultRedirect'

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          <Route path="/" element={<PrivateRoute><Layout /></PrivateRoute>}>
            {/* Default route - redirects based on role */}
            <Route index element={<DefaultRedirect />} />

            {/* Dashboard - Only for admin and agent */}
            <Route path="dashboard" element={
              <RoleBasedRoute allowedRoles={['admin', 'agent']}>
                <Dashboard />
              </RoleBasedRoute>
            } />

            {/* Materials - Only for admin and agent */}
            <Route path="materials" element={
              <RoleBasedRoute allowedRoles={['admin', 'agent']}>
                <Materials />
              </RoleBasedRoute>
            } />

            {/* Material Prices - Only for admin and agent */}
            <Route path="material-prices" element={
              <RoleBasedRoute allowedRoles={['admin', 'agent']}>
                <MaterialPrices />
              </RoleBasedRoute>
            } />

            {/* Properties - Only for admin and agent */}
            <Route path="properties" element={
              <RoleBasedRoute allowedRoles={['admin', 'agent']}>
                <Properties />
              </RoleBasedRoute>
            } />

            {/* Property Detail - Only for admin and agent */}
            <Route path="properties/:id" element={
              <RoleBasedRoute allowedRoles={['admin', 'agent']}>
                <PropertyDetail />
              </RoleBasedRoute>
            } />

            {/* Transactions - Only for admin and agent */}
            <Route path="transactions" element={
              <RoleBasedRoute allowedRoles={['admin', 'agent']}>
                <Transactions />
              </RoleBasedRoute>
            } />

            {/* Cost Estimates - Only for admin and agent */}
            <Route path="estimates" element={
              <RoleBasedRoute allowedRoles={['admin', 'agent']}>
                <CostEstimates />
              </RoleBasedRoute>
            } />

            {/* Reports - Only for admin and agent */}
            <Route path="reports" element={
              <RoleBasedRoute allowedRoles={['admin', 'agent']}>
                <Reports />
              </RoleBasedRoute>
            } />

            {/* Notifications - Only for admin and agent */}
            <Route path="notifications" element={
              <RoleBasedRoute allowedRoles={['admin', 'agent']}>
                <Notifications />
              </RoleBasedRoute>
            } />

            {/* Documents - Only for admin and agent */}
            <Route path="documents" element={
              <RoleBasedRoute allowedRoles={['admin', 'agent']}>
                <Documents />
              </RoleBasedRoute>
            } />

            {/* Activity Logs - Only for admin and agent */}
            <Route path="activity-logs" element={
              <RoleBasedRoute allowedRoles={['admin', 'agent']}>
                <ActivityLogs />
              </RoleBasedRoute>
            } />

            {/* Profile - All authenticated users */}
            <Route path="profile" element={<Profile />} />

            {/* About - All authenticated users */}
            <Route path="about" element={<About />} />

            {/* About Editor - Only for admin */}
            <Route path="about/edit" element={
              <RoleBasedRoute allowedRoles={['admin']}>
                <AboutEditor />
              </RoleBasedRoute>
            } />

            {/* Admin - Only for admin */}
            <Route path="admin" element={
              <RoleBasedRoute allowedRoles={['admin']}>
                <Admin />
              </RoleBasedRoute>
            } />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>

        {/* Toast Notification Container */}
        <ToastContainer
          position="top-right"
          autoClose={3000}
          hideProgressBar={false}
          newestOnTop
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme="light"
        />
      </Router>
    </AuthProvider>
  )
}

export default App

