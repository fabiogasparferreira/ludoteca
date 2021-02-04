export default {
  methods: {
    validateState(name) {
      const { $dirty, $error } = this.$v.form[name]
      return $dirty ? ($error ? false : null) : null
    },
  },
}
