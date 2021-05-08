<template>
  <HomeScreenTemplate :title="title" :pre-title="pretitle">
    <template #actions>
      <div v-if="isAuthenticated()">
          <b-dropdown class="mr-3" no-caret variant="white">
            <template #button-content>
              <b-icon-gear />
            </template>
            <b-dropdown-item-button v-show="!bulk" @click="bulk = true">
              Enable God mode
            </b-dropdown-item-button>
            <b-dropdown-item-button v-show="bulk" @click="bulk = false">
              Disable God mode
            </b-dropdown-item-button>
          </b-dropdown>

          <b-button :to="{ name: 'AddLibraryGame' }" variant="primary">
            <b-icon-plus class="mr-2"></b-icon-plus>
            Add game
          </b-button>
        </div>
    </template>

    <!-- Search and filters trigger -->
    <b-row class="align-items-center mb-3">
      <!-- Search -->
      <b-col>
        <form>
          <div class="input-group input-group-lg input-group-merge">
            <b-form-input
              v-model="search"
              class="form-control-prepended"
              debounce="300"
              placeholder="Search"
              type="search"
            ></b-form-input>
            <div class="input-group-prepend">
              <div class="input-group-text">
                <b-icon-search font-scale="0.8"></b-icon-search>
              </div>
            </div>
          </div>
        </form>
      </b-col>

      <FiltersButton :filters="filters" collapse-id="filters-collapse" />
    </b-row>

    <Filters v-model="filters" collapse-id="filters-collapse">
      <FilterSelect
        v-model="filters"
        id="location"
        label="Location"
        :options="$store.getters['library/locations']"
      />
      <FilterSelect
        v-model="filters"
        id="owner"
        label="Owner"
        :options="$store.getters['library/players']"
        @search="searchPlayers"
      />
    </Filters>

    <!-- Content -->
    <div class="mt-5">
      <b-row>
        <!-- Games list -->
        <b-col
          v-for="(game, index) in games"
          :key="index"
          cols="12"
          sm="6"
          md="4"
          xl="3"
        >
          <Game
              :game="game"
            :loading="loading"
            :selectable="isGameSelectable(game)"
            :selected="selected.includes(game.id)"
            @selected-change="updateSelected"
              @check-in="openLocationModal"
              @return="refreshGames"
          >
          </Game>
        </b-col>
      </b-row>

      <CheckinModal
        id="checkin-modal"
        :game="selectedGame"
        :shelves="$store.getters['library/locations']"
        @done="refreshGames"
      />
    </div>

    <Pagination v-model="currentPage" :total-count="totalGamesCount" />

    <div
      class="list-alert alert alert-dark alert-dismissible border fade"
      role="alert"
      v-bind:class="{ show: bulk }"
    >
      <!-- Content -->
      <div class="row align-items-center">
        <div class="col">
          <!-- Checkbox -->
          <div class="custom-control custom-checkbox">
            <input
              id="listAlertCheckbox"
              checked=""
              class="custom-control-input"
              disabled=""
              type="checkbox"
            />
            <label
              class="custom-control-label text-white"
              for="listAlertCheckbox"
              ><span class="list-alert-count">{{ selected.length }}</span>
              game(s)</label
            >
          </div>
        </div>
        <div class="col-auto mr-n3">
          <!-- Button -->
<!--          <b-button-->
<!--            v-if="games.length > selected.length"-->
<!--            class="btn-white-20"-->
<!--            size="sm"-->
<!--            @click="selectAll"-->
<!--          >-->
<!--            Select all-->
<!--          </b-button>-->
<!--          <b-button-->
<!--            v-else-->
<!--            class="btn-outline-white"-->
<!--            size="sm"-->
<!--            @click="unselectAll"-->
<!--          >-->
<!--            Unselect all-->
<!--          </b-button>-->
          <b-dropdown
            :disabled="selected.length === 0"
            class="ml-3"
            dropup
            no-caret
            size="sm"
            variant="white-20"
          >
            <template #button-content>
              <div class="d-flex flex-row align-items-center">
                Actions
                <b-icon-caret-up-fill
                  class="ml-2"
                  font-scale="0.8"
                ></b-icon-caret-up-fill>
              </div>
            </template>
            <b-dropdown-item-button @click="checkoutGames"
              >Check-out
            </b-dropdown-item-button>
          </b-dropdown>
        </div>
      </div>
      <!-- / .row -->

      <!-- Close -->
      <button
        aria-label="Close"
        class="list-alert-close close"
        type="button"
        @click="bulk = false"
      >
        <span aria-hidden="true">×</span>
      </button>
    </div>

    <ModalPlayerSelect id="filter-players-modal"></ModalPlayerSelect>
  </HomeScreenTemplate>
</template>

<script>
import gamesMixin from '@/mixins/games.mixin'
import libraryService from '@/services/library.service'
import ModalPlayerSelect from '@/components/ModalPlayerSelect'
import playerService from '@/services/player.service'
import CheckinModal from '@/components/CheckinModal'
import usersMixin from '@/mixins/users.mixin'
import axiosUtils from '@/mixins/axios.utils'
import Pagination from '@/components/Pagination'
import Filters from '@/components/Filters'
import FiltersButton from '@/components/FiltersButton'
import FilterSelect from '@/components/FilterSelect'
import HomeScreenTemplate from "@/components/templates/HomeScreenTemplate"
import Game from "./partials/Game"

export default {
  name: 'Home',
  props: ['title', 'pretitle'],
  data() {
    return {
      search: '',
      games: new Array(60).fill({
        game: { name: '', image: '' },
        owner: { name: '' },
        id: 0
      }),
      loading: true,
      bulk: false,
      selected: [],
      selectedGame: {
        game: {},
      },
      selectedGames: [],
      players: [],
      filters: new Filters.Model(),
      availability_options: [],
      status_options: [
        { value: 'available', text: 'Available' },
        { value: 'not-available', text: 'Withdrawn' },
        { value: 'not-checked-in', text: 'Not checked-in' },
        { value: 'checked-out', text: 'Checked-out' },
      ],
      currentPage: 1,
      totalGamesCount: 0,
    }
  },
  components: {
    HomeScreenTemplate,
    FiltersButton,
    Pagination,
    CheckinModal,
    ModalPlayerSelect,
    Game,
    Filters,
    FilterSelect,
  },
  mixins: [gamesMixin, usersMixin],
  created() {
    this.refreshGames()
  },
  methods: {
    selectAll() {
      const availableGames = this.games.filter((game) =>
        this.isGameSelectable(game),
      )

      availableGames.forEach((game) => this.updateSelected(game.id))
    },
    unselectAll() {
      this.selected = []
    },
    refreshGames() {
      this.loading = true

      let params = this.getParams()

      libraryService.filterGames(params).then((response) => {
        this.games = response.results
        this.totalGamesCount = response.count
        this.loading = false
      })
    },
    searchPlayers(query) {
      playerService.searchPlayers(query).then((response) => {
        this.players = response
      })
    },
    checkoutGames() {
      const isOwnerLeiriaCon = this.games.filter(
        (game) =>
          game.owner.name == 'leiriacon' && this.selected.includes(game.id),
      ).length

      if (isOwnerLeiriaCon) {
        this.$bvModal
          .msgBoxConfirm(
            "You selected games from leiriacon's library. Do you want to check-out?",
            {
              title: 'Check-out',
              okVariant: 'danger',
              okTitle: 'Yes',
              cancelTitle: 'No',
            },
          )
          .then((confirmed) => {
            if (confirmed) {
              this.deleteCheckedOutGames()
            }
          })
          .catch((error) =>
            this.$toast.error('Error checking-out game(s): ' + error),
          )
      } else {
        this.deleteCheckedOutGames()
      }
    },
    deleteCheckedOutGames() {
      let promises = this.selected.map((id) => libraryService.deleteGame(id))

      Promise.all(promises)
        .then(() => {
          this.$toast.success(`Checked-out ${promises.length} game(s)!`)
        })
        .catch((response) => {
          this.$toast.error(
            'Error checking-out game(s): ' +
              axiosUtils.getErrorDescription(response),
          )
        })
        .finally(() => {
          this.bulk = false
          this.unselectAll()
          this.refreshGames()
        })
    },
    getParams() {
      let params = {}

      params['page'] = this.currentPage

      if (this.search) {
        params['search'] = this.search
      }

      Object.keys(this.filters.filtersSelected).forEach(
        (key) => (params[key] = this.filters.filtersSelected[key]),
      )

      return params
    },
    openLocationModal(game) {
      this.selectedGame = game
      this.$bvModal.show('checkin-modal')
    },
    updateSelected(game_id) {
      if (this.selected.includes(game_id)) {
        this.selected.splice(this.selected.indexOf(game_id))
      } else {
        this.selected.push(game_id)
      }
    },
    isGameSelectable(game) {
      return this.bulk && game.status === 'available'
    },
  },

  watch: {
    search() {
      // anytime the search string is change we should reset page number
      // otherwise the user could face a 404 because the page is not available for the search results
      this.currentPage = 1

      this.refreshGames()
    },
    filters: {
      handler: function () {
        this.refreshGames()
      },
      deep: true,
    },
    currentPage() {
      this.refreshGames()
    },
  },
}
</script>
<style lang="scss"></style>
