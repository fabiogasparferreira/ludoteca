import { authApi } from '@/services/api'

const URL = '/api/users/'

export default {
  fetchUsers() {
    return authApi.get(URL).then(response => response.data)
  },
  fetchUser(pk) {
    return authApi.get(URL + `${pk}/`).then(response => response.data)
  },
  postUser(payload) {
    return authApi.post(URL, payload).then(response => response.data)
  },
}
