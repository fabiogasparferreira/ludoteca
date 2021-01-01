<template>
  <div>
    <Header :pretitle="pretitle" :title="title">
      <template v-slot:content-right>
        <div v-if="isAuthenticated()">
          <b-dropdown class="mr-3" no-caret variant="white">
            <template #button-content>
              <b-icon-gear/>
            </template>
            <b-dropdown-item-button v-show="!bulk" @click="bulk=true">
              Enable God mode
            </b-dropdown-item-button>
            <b-dropdown-item-button v-show="bulk" @click="bulk=false">
              Disable God mode
            </b-dropdown-item-button>
          </b-dropdown>

          <b-button :to="{name: 'AddLibraryGame'}" variant="primary">
            <b-icon-plus class="mr-2"></b-icon-plus>
            Add game
          </b-button>
        </div>
      </template>
    </Header>

    <!-- Search and filters trigger -->
    <b-row class="align-items-center mb-3">

      <!-- Search -->
      <b-col>
        <form>
          <div class="input-group input-group-lg input-group-merge">
            <b-form-input v-model="search" class="form-control-prepended" debounce="300" placeholder="Search"
                          type="search"></b-form-input>
            <div class="input-group-prepend">
              <div class="input-group-text">
                <b-icon-search font-scale="0.8"></b-icon-search>
              </div>
            </div>
          </div>
        </form>
      </b-col>

      <!-- Filters trigger -->
      <b-col v-if="isAuthenticated()" cols="auto">
        <b-button v-b-toggle.filters-collapse :pressed.sync="filtersOpen" aria-expanded="false" aria-haspopup="true"
                  class="btn-white" data-toggle="dropdown"
                  size="lg">
          <b-icon-filter></b-icon-filter>
          Filters
          <b-badge v-show="Object.keys(filters).length>0" class="ml-1">{{ Object.keys(filters).length }}</b-badge>
        </b-button>
      </b-col>

    </b-row>

    <!-- Filters -->
    <b-row v-if="isAuthenticated()">
      <b-col>
        <b-collapse id="filters-collapse" class="">
          <div class="bg-light rounded p-4">
            <b-row>

              <!-- Location -->
              <b-col lg="6" sm="12">
                <b-form-group label="Location">
                  <FormSelect
                      v-model="filters['location']"
                      :options="$store.getters['library/locations']"
                      option-text="name"
                      option-value="id"
                  />
                </b-form-group>
              </b-col>

              <!-- Owner -->
              <b-col lg="6" sm="12">
                <b-form-group label="Owner">

                  <FormSelect
                      v-model="filters['player']"
                      :options="$store.getters['library/players']"
                      option-text="name"
                      option-value="id"
                      @search="searchPlayers"
                  />
                </b-form-group>
              </b-col>

              <!-- Status -->
              <!--              <b-col sm="12" lg="6">-->
              <!--                <b-form-group label="Status">-->
              <!--                  <b-form-checkbox-group-->
              <!--                      v-model="filters['status']"-->
              <!--                      :options="status_options"-->
              <!--                      size="md"-->
              <!--                      buttons-->
              <!--                      button-variant="white"-->
              <!--                  ></b-form-checkbox-group>-->
              <!--                </b-form-group>-->
              <!--                {{filters}}-->
              <!--              </b-col>-->


              <div class="d-flex w-100 flex-row justify-content-end">
                <b-link class="text-gray-800" @click="filters = initFilters()">
                  <b-icon-x></b-icon-x>
                  CLEAR FILTERS
                </b-link>
              </div>
            </b-row>
          </div>
        </b-collapse>
      </b-col>
    </b-row>

    <!-- Content -->
    <div class="mt-4">
      <b-row v-show="!loading">

        <!-- Games list -->
        <b-col v-for="(game,index) in games" :key="index" cols="12" lg="6">
          <LibraryGameCard
              v-model="selected"
              :bulk="bulk"
              :game="game"
              :value="game.id"
              v-on:checkin="openLocationModal(game)"
              v-on:change-location="openLocationModal(game)"/>
        </b-col>
      </b-row>
      <!-- Skeleton -->
      <b-row v-show="loading">
        <b-col v-for="(index) in new Array(50)" v-bind:key="index" lg="6" sm="12">
          <ItemCard>
            <template #image>
              <b-skeleton height="3.5rem" type="avatar" width="3.5rem"></b-skeleton>
            </template>
            <template #metadata>
              <b-skeleton class="text-muted" width="100px"/>
            </template>
            <template #top-right>
              <b-skeleton size="sm" type="button" width="75px"></b-skeleton>
            </template>
          </ItemCard>
        </b-col>
      </b-row>

      <CheckinModal
          id="checkin-modal"
          :game="selectedGame"
          :shelves="$store.getters['library/locations']"
          v-on:done="refreshGames"/>
    </div>

    <!-- Pagination -->
    <b-row v-show="pagination.count > pagination.count_per_page" no-gutters>

      <!-- Pagination (prev) -->
      <ul class="col list-pagination-prev pagination pagination-tabs justify-content-start">
        <li class="page-item">
          <a class="page-link" href="#">
            <i class="fe fe-arrow-left mr-1"></i> Previous
          </a>
        </li>
      </ul>

      <!-- Pagination -->
      <ul class="col list-pagination pagination pagination-tabs justify-content-center">
        <li v-for="(page, index) in pagination.pages" v-bind:key="index"
            v-bind:class="{ active: pagination.active_page === page }">
          <b-link v-if="Number.isInteger(page)" class="page" @click="setPage(page)">{{ page }}</b-link>
          <span v-else class="page">{{ page }}</span>
        </li>
      </ul>

      <!-- Pagination (next) -->
      <ul class="col list-pagination-next pagination pagination-tabs justify-content-end">
        <li class="page-item">
          <a class="page-link" href="#">
            Next <i class="fe fe-arrow-right ml-1"></i>
          </a>
        </li>
      </ul>
    </b-row>

    <div class="list-alert alert alert-dark alert-dismissible border fade" role="alert" v-bind:class="{show: bulk}">

      <!-- Content -->
      <div class="row align-items-center">
        <div class="col">

          <!-- Checkbox -->
          <div class="custom-control custom-checkbox">
            <input id="listAlertCheckbox" checked="" class="custom-control-input" disabled="" type="checkbox">
            <label class="custom-control-label text-white" for="listAlertCheckbox"><span
                class="list-alert-count">{{ selected.length }}</span> game(s)</label>
          </div>

        </div>
        <div class="col-auto mr-n3">
          <!-- Button -->
          <b-button v-if="games.length > selected.length" class="btn-white-20" size="sm" @click="selectAll">
            Select all
          </b-button>
          <b-button v-else class="btn-outline-white" size="sm" @click="unselectAll">
            Unselect all
          </b-button>
          <b-dropdown :disabled="selected.length === 0" class="ml-3" dropup no-caret size="sm" variant="white-20">
            <template #button-content>
              <div class="d-flex flex-row align-items-center">
                Actions
                <b-icon-caret-up-fill class="ml-2" font-scale="0.8"></b-icon-caret-up-fill>
              </div>
            </template>
            <b-dropdown-item-button @click="checkoutGames">Check-out</b-dropdown-item-button>
          </b-dropdown>

        </div>
      </div> <!-- / .row -->

      <!-- Close -->
      <button aria-label="Close" class="list-alert-close close" type="button" @click="bulk=false">
        <span aria-hidden="true">×</span>
      </button>

    </div>

    <ModalPlayerSelect id="filter-players-modal"></ModalPlayerSelect>
  </div>
</template>

<script>
import gamesMixin from "@/mixins/games.mixin"
import libraryService from "@/services/library.service"
import Header from "@/components/Header"
import LibraryGameCard from "@/components/LibraryGameCard"
import ModalPlayerSelect from "@/components/ModalPlayerSelect"
import playerService from "@/services/player.service"
import CheckinModal from "@/components/CheckinModal"
import ItemCard from "@/components/ItemCard"
import usersMixin from "@/mixins/users.mixin"
import FormSelect from "@/components/FormSelect";

export default {
  name: "Home",
  props: ['title', 'pretitle'],
  data() {
    return {
      search: '',
      games: [],
      loading: true,
      bulk: false,
      selected: [],
      pagination: {
        count: 0,
        count_per_page: 50,
        active_page: 1,
        pages: [],
        number_pages: 5
      },
      selectedGame: {
        game: {}
      },
      selectedGames: [],
      players: [],
      filters: this.initFilters(),
      filtersOpen: false,
      availability_options: [],
      status_options: [
        {value: 'available', text: 'Available'},
        {value: 'not-available', text: 'Withdrawn'},
        {value: 'not-checked-in', text: 'Not checked-in'},
        {value: 'checked-out', text: 'Checked-out'}
      ],
    }
  },
  components: {FormSelect, CheckinModal, ModalPlayerSelect, LibraryGameCard, Header, ItemCard},
  mixins: [gamesMixin, usersMixin],
  mounted() {
    this.pagination = this.paginationReset()
    this.refreshGames()
  },
  methods: {
    initFilters() {
      return {}
    },
    selectAll() {
      this.selected = this.games.map(game => game.id)
    },
    unselectAll() {
      this.selected = []
    },
    updatePages() {
      this.pagination.pages = []

      let current = this.pagination.active_page,
          last = Math.ceil(this.pagination.count / this.pagination.count_per_page),
          delta = 2,
          left = current - delta,
          right = current + delta + 1,
          range = [],
          l;

      for (let i = 1; i <= last; i++) {
        if (i === 1 || i === last || i >= left && i < right) {
          range.push(i);
        }
      }

      for (let i of range) {
        if (l) {
          if (i - l === 2) {
            this.pagination.pages.push(l + 1);
          } else if (i - l !== 1) {
            this.pagination.pages.push('...');
          }
        }
        this.pagination.pages.push(i);
        l = i;
      }

    },
    setPage(number) {
      this.pagination.active_page = number
      this.refreshGames()
    },
    refreshGames() {
      this.loading = true

      let params = this.getParams()

      libraryService.filterGames(params).then(response => {
        this.games = response.results
        this.pagination.count = response.count
        this.updatePages()
        this.loading = false
      })
    },
    searchPlayers(query) {
      playerService.searchPlayers(query).then(response => {
        this.players = response
      })
    },
    checkoutGames() {

      let promises = this.selected.map(id => libraryService.updateGame(id, {date_checkout: new Date(), location: ''}))

      Promise.all(promises).then(() => {
        this.$toast('Oh yeah!')
        this.bulk = false
        this.refreshGames()
      })
    },
    paginationReset() {
      return {
        count: 0,
        count_per_page: 50,
        active_page: 1,
        pages: [],
        number_pages: 5
      }
    },
    getParams() {
      let params = {}

      params['page'] = this.pagination.active_page

      if (this.search) {
        params['search'] = this.search
      }

      Object.keys(this.filters)
          .forEach(key => params[key] = this.filters[key])

      return params
    },
    openLocationModal(game) {
      this.selectedGame = game
      this.$bvModal.show('checkin-modal')
    },
  },

  watch: {
    search() {
      this.refreshGames()
    },
    filters: {
      handler: function () {
        this.refreshGames()
      },
      deep: true

    }
  },

}
</script>
<style>


.custom-control-label {
  width: 100%
}

.custom-control-input {
  display: none;
}
</style>