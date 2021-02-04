<template>
  <div>
    <b-form-select
      :options="options"
      v-model="selected"
      :value-field="optionValue"
      :text-field="optionText"
      :state="state"
    >
      <template #first>
        <b-form-select-option :value="null" disabled
          >-- Select an option --</b-form-select-option
        >
      </template>
    </b-form-select>
  </div>
</template>

<script>
export default {
  name: 'FormSelect',
  components: {},
  props: {
    reduce: {
      type: Function,
    },
    value: {},
    state: {
      type: Boolean,
      default: null,
    },
    options: {
      type: Array,
      default: () => [],
    },
    optionText: {
      type: String,
      default: 'name',
    },
    optionValue: {
      type: String,
      default: 'id',
    },
    placeholder: {
      type: String,
      default: 'Select an option',
    },
  },
  data: () => {
    return {
      selected: null,
    }
  },
  watch: {
    selected: function(val) {
      this.$emit('input', val)
    },
  },
}
</script>
