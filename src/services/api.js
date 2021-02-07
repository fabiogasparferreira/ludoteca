import axios from 'axios'
import Cookies from 'js-cookie'
import router from 'vue-router'
import localStorageService from '@/services/localStorage.service'
import authorizationService from '@/services/authorization.service'

export { unauthApi, authApi }

const HEADERS = {
  'Content-Type': 'application/json',
  'X-CSRFToken': Cookies.get('csrftoken'),
}

const API_URL = ''

const TIMEOUT = 7000

/**
 * Object for requests that doesn't require authentication
 * @type {AxiosInstance}
 */
const unauthApi = axios.create({
  baseURL: API_URL,
  headers: HEADERS,
  timeout: TIMEOUT,
})

/**
 * Object for request that require authentication
 * @type {AxiosInstance}
 */
const authApi = axios.create({
  baseURL: API_URL,
  headers: HEADERS,
  timeout: TIMEOUT,
})

/**
 * Add access token to request
 */
authApi.interceptors.request.use(config => {
  const token = localStorageService.getAccessToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

/**
 * Interceptor for requests with access token
 * If any request returns 401 due to token expiration, call refresh, save new token and call original request again
 * If any other error or if refresh request returns error, redirect to login
 */
authApi.interceptors.response.use(
  response => {
    return response
  },
  function(error) {
    const originalRequest = error.config

    // catch 401 response when the token expired
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      if (!localStorageService.getRefreshToken()) {
        //toast.e('Oups! Missing credentials')
        router.push({ name: 'Login' })
      }

      // call API to get a new token
      return authorizationService.refreshToken().then(token => {
        // update original request authorization header
        authApi.defaults.headers.common['Authorization'] = 'Bearer ' + token

        // return originalRequest
        return authApi(originalRequest)
      })
    } else {
      // return any other error
      return Promise.reject(error)
    }
  },
)
