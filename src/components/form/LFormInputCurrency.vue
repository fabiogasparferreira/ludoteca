<template>
  <currency-input
      class="form-control form-control-lg"
      placeholder="Insert an amount"
      :value="value"
      :state="state"
      :class="{'is-invalid': state === false}"
      @input="$emit('input', $event)"/>
</template>

<script>
import { CurrencyInput } from 'vue-currency-input'
export default {
  name: "LFormCurrency",
  props: {
    value: {
      required: true
    },
    state: {
      default: true
    }
  },
  components: {
    CurrencyInput
  }
}
</script>

<style scoped>

</style>