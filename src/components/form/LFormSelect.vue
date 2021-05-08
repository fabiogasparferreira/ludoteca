<template>
  <b-input-group>
    <b-form-input
        :state="state"
        placeholder="Select an option"
        size="lg"
        readonly
        :value="value"
        @input="$emit('input')"/>
        <b-form-input
      :value="value"
      :state="state"
      hidden
  />
    <b-input-group-append>
      <b-button @click="$emit('select')" variant="outline-secondary">
        <i class="fe fe-search mr-2"/>Search
      </b-button>
    </b-input-group-append>

  </b-input-group>
</template>

<script>

export default {
  name: 'LFormSelect',
  components: {

  },
  props: {
    value: {
      required: true
    },
    placeholder: {
      type: String,
      default: '',
    },
    state: {
      default: null
    }
  }
}
</script>

<style scoped></style>
