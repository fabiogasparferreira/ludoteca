import { authApi } from '@/services/api'

const URL = '/api/library/withdraw/'

export default {
  withdrawGame(payload) {
    return authApi.post(URL, payload).then(response => response.data)
  },
  returnGame(withdrawId) {
    return authApi
      .patch(URL + `${withdrawId}/`, {
        date_returned: new Date().toISOString(),
      })
      .then(response => response.data)
  },
}
