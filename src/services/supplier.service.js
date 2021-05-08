import { authApi } from '@/services/api'

const URL = '/api/store/suppliers/'

export default {
  /**
   * Get all suppliers
   * @returns {Promise<*>}
   */
  fetchAll() {
    return authApi
      .get(URL)
      .then(response => response.data)
  },
  /**
   * Get game by game id
   * @param id
   * @returns {Promise<*>}
   */
  get(id) {
    return authApi
      .get(URL + `${id}/`)
      .then(response => response.data)
  },

  /**
   * Filter and search suppliers
   * @param params
   * @returns {Promise<AxiosResponse<any>>}
   */
  filter(params) {
    return authApi
      .get(URL, {
        params: params,
      })
      .then(response => response.data)
  },

  /**
   * Create a new supplier
   * @param payload
   * @returns {Promise<AxiosResponse<any>>}
   */
  create(payload) {
    return authApi.post(URL, payload).then(response => response.data)
  },

  /**
   * Update supplier information with the given id
   * @param id
   * @param payload - content to update
   * @returns {Promise<AxiosResponse<any>>}
   */
  update(id, payload) {
    return authApi
      .patch(URL + `${id}/`, payload)
      .then(response => response.data)
  },

  /**
   * Delete supplier with the given id
   * @param id
   * @returns {Promise<AxiosResponse<any>>}
   */
  deleteGame(id) {
    return authApi
      .delete(URL + `${id}/`)
      .then(response => response.data)
  },
}
