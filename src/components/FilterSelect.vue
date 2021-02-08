<template>
  <b-col lg="6" sm="12">
    <b-form-group :label="label">
      <FormSelect
          v-model="filtersModel.filtersSelected[id]"
          :options="options"
          option-text="name"
          option-value="id"
      />
    </b-form-group>
  </b-col>
</template>

<script>
import FormSelect from '@/components/FormSelect'
import Filters from '@/components/Filters'

export default {
  name: 'FilterSelect',
  components: {FormSelect},
  props: {
    value: {
      type: Filters.Model,
      required: true,
    },
    id: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      default: '',
    },
    options: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    filtersModel: {
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
