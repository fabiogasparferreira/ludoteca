<template>
  <FormSelect
      v-model="selected"
      :options="options"
      option-text="name"
      option-value="id"
  />
</template>

<script>
import FormSelect from '@/components/FormSelect'

export default {
  name: 'FilterSelect',
  components: {FormSelect},
  props: {
    value: {},
    options: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    selected: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit('input', value)
      },
    },
  },
}
</script>
