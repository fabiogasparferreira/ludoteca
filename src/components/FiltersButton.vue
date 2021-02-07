<template>
  <!-- Filters trigger -->
  <b-col v-if="isAuthenticated()" cols="auto">
    <b-button
      v-b-toggle:[collapseId]
      :pressed.sync="filtersOpen"
      aria-expanded="false"
      aria-haspopup="true"
      class="btn-white"
      data-toggle="dropdown"
      size="lg"
    >
      <b-icon-filter></b-icon-filter>
      Filters
      <b-badge v-show="filters.count() > 0" class="ml-1">{{
        filters.count()
      }}</b-badge>
    </b-button>
  </b-col>
</template>

<script>
import usersMixin from '@/mixins/users.mixin'

export default {
  name: 'FiltersButton',
  mixins: [usersMixin],
  props: {
    collapseId: {
      type: String,
      default: 'filters-collapse',
    },
    filters: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      filtersOpen: false,
    }
  },
}
</script>
