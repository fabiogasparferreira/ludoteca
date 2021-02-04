import { unauthApi } from '@/services/api'

export default {
  fetchMessages() {
    return unauthApi.get(`messages/`).then(response => response.data)
  },
  postMessage(payload) {
    return unauthApi.post(`messages/`, payload).then(response => response.data)
  },
  deleteMessage(msgId) {
    return unauthApi.delete(`messages/${msgId}`).then(response => response.data)
  },
}
