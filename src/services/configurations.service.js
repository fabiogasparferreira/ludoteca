import { authApi } from '@/services/api'

const URL = '/api/configurations/'

export default {
  /**
   * Get all configurations
   * @returns {Promise<AxiosResponse<any>>}
   */
  fetchConfigurations() {
    return authApi.get(URL, {}).then((response) => response.data)
  },
  createConfiguration(payload) {
    return authApi
      .post(URL, payload)
      .then((response) => response.data)
  },
  updateConfiguration(id, payload) {
    return authApi
      .patch(URL + `${id}/`, payload)
      .then((response) => response.data)
  },
  deleteConfiguration(id) {
    return authApi
      .delete(URL + `${id}/`)
      .then((response) => response.data)
  },

}
