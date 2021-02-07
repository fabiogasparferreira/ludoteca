<template>
  <!-- Filters -->
  <b-row v-if="isAuthenticated()">
    <b-col>
      <b-collapse :id="collapseId" class="">
        <div class="bg-light rounded p-4">
          <b-row>
            <!-- Location -->
            <b-col lg="6" sm="12" v-if="showFilterType('location')">
              <b-form-group label="Location">
                <FormSelect
                  v-model="filtersModel.filtersSelected['location']"
                  :options="$store.getters['library/locations']"
                  option-text="name"
                  option-value="id"
                />
              </b-form-group>
            </b-col>

            <!-- Owner -->
            <b-col lg="6" sm="12" v-if="showFilterType('player')">
              <b-form-group label="Owner">
                <FormSelect
                  v-model="filtersModel.filtersSelected['player']"
                  :options="$store.getters['library/players']"
                  option-text="name"
                  option-value="id"
                  @search="searchPlayers"
                />
              </b-form-group>
            </b-col>

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
import playerService from '@/services/player.service'
import FormSelect from '@/components/FormSelect'

export default {
  name: 'Filters',
  components: { FormSelect },
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
  data() {
    return {
      players: [],
    }
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
    showFilterType(type) {
      return this.filtersModel.filterTypes.has(type)
    },
    clearFilters() {
      this.filtersModel.filtersSelected = {}
    },
    searchPlayers(query) {
      playerService.searchPlayers(query).then(response => {
        this.players = response
      })
    },
  },
  Model: FiltersModel
}

function FiltersModel(filterTypes = []) {
  this.filtersSelected = {}
  this.filterTypes = new Set(filterTypes)
}

FiltersModel.prototype.count = function() {
  return Object.keys(this.filtersSelected).length
}

FiltersModel.Type = {
  LOCATION: "location",
  PLAYER: "player"
}

</script>
