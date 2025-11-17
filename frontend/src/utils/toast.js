import { toast } from 'react-toastify'

/**
 * Toast notification utility
 * Provides consistent toast notifications across the app
 */

const defaultOptions = {
  position: 'top-right',
  autoClose: 3000,
  hideProgressBar: false,
  closeOnClick: true,
  pauseOnHover: true,
  draggable: true,
}

export const showToast = {
  success: (message, options = {}) => {
    toast.success(message, { ...defaultOptions, ...options })
  },

  error: (message, options = {}) => {
    toast.error(message, { ...defaultOptions, ...options })
  },

  info: (message, options = {}) => {
    toast.info(message, { ...defaultOptions, ...options })
  },

  warning: (message, options = {}) => {
    toast.warning(message, { ...defaultOptions, ...options })
  },

  promise: (promise, messages, options = {}) => {
    return toast.promise(
      promise,
      {
        pending: messages.pending || 'Processing...',
        success: messages.success || 'Success!',
        error: messages.error || 'Something went wrong',
      },
      { ...defaultOptions, ...options }
    )
  },
}

// Helper to extract error message from API response
export const getErrorMessage = (error) => {
  if (error.response?.data?.detail) {
    return error.response.data.detail
  }
  if (error.response?.data?.message) {
    return error.response.data.message
  }
  if (error.response?.data) {
    // Handle validation errors
    const data = error.response.data
    if (typeof data === 'object') {
      const firstKey = Object.keys(data)[0]
      if (Array.isArray(data[firstKey])) {
        return `${firstKey}: ${data[firstKey][0]}`
      }
      return data[firstKey]
    }
    return data
  }
  if (error.message) {
    return error.message
  }
  return 'An unexpected error occurred'
}

export default showToast

