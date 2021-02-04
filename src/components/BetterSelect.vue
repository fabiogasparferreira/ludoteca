<template>
  <div>
    <b-dropdown
      block
      class="d-block"
      menu-class="mh-300-px overflow-auto w-100"
      no-caret
      no-flip
      toggle-class="p-0"
      variant="link"
    >
      <template #button-content>
        <b-form-select
          v-model="selected"
          :options="options"
          :state="state"
          :text-field="textField"
          :value-field="valueField"
          required
        >
          <template #first>
            <b-form-select-option disabled hidden selected value=""
              >Select an option</b-form-select-option
            >
          </template>
        </b-form-select>
      </template>
      <template #default>
        <b-dropdown-form>
          <b-form-group class="mb-0 mt-2">
            <b-form-input
              v-model="search"
              autofocus
              debounce="300"
              placeholder="Type here to start search"
              size="sm"
            ></b-form-input>
          </b-form-group>
        </b-dropdown-form>
        <b-dropdown-item-button
          v-for="(option, index) in options"
          v-bind:key="index"
          :active="option[valueField] === selected"
          @click="select(option)"
        >
          {{ option[textField] }}
        </b-dropdown-item-button>
      </template>
    </b-dropdown>
  </div>
</template>

<script>
export default {
  data() {
    return {
      search: '',
      selected: '',
    }
  },
  methods: {
    select(val) {
      this.selected = val[this.valueField]
      this.$emit('input', val[this.valueField])
    },
  },
  props: {
    value: {
      required: true,
      default: '',
      type: String,
    },
    options: {
      type: Array,
      default: function() {
        return []
      },
    },
    valueField: {
      default: 'value',
      type: String,
    },
    textField: {
      default: 'text',
      type: String,
    },
    state: {},
  },
  watch: {
    search: function(val) {
      this.$emit('search', val)
    },
  },
}
</script>
