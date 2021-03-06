<template>
  <!-- Filters -->
  <b-row v-if="isAuthenticated()">
    <b-col>
      <b-collapse :id="collapseId" class="">
        <div class="bg-light rounded p-4">
          <b-row>

            <slot></slot>

            <div class="d-flex w-100 flex-row justify-content-end">
              <b-link class="text-gray-800" @click="clearFilters">
                <b-icon-x></b-icon-x>
                CLEAR FILTERS
              </b-link>
            </div>
          </b-row>
        </div>
      </b-collapse>
    </b-col>
  </b-row>
</template>

<script>
import usersMixin from '@/mixins/users.mixin'

export default {
  name: 'Filters',
  mixins: [usersMixin],
  props: {
    value: {
      type: FiltersModel,
      required: true
    },
    collapseId: {
      type: String,
      default: 'filters-collapse',
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
  methods: {
    clearFilters() {
      this.filtersModel.filtersSelected = {}
      this.$emit('input', this.filtersModel)
    },
  },
  Model: FiltersModel
}

function FiltersModel() {
  this.filtersSelected = {}
}

FiltersModel.prototype.count = function() {
  return Object.keys(this.filtersSelected).length
}

</script>
