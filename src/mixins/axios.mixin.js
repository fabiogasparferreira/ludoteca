export default {
  methods: {
    getErrorDescription(response) {
      if (!response || !response.response || response.response.status >= 500) {
        return 'Unexpected error, please contact technical support'
      } else if (response.response.status >= 400) {
        return response.response.data.detail
      }
    },
  },
}
