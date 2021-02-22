<template>
  <b-container>
    <Filters v-model="filters" collapse-id="filters-collapse">
      <FilterSelect
        v-model="filters"
        id="location"
        label="Location"
        :options="$store.getters['library/locations']"
      />
      <FilterSelect
        v-model="filters"
        id="player"
        label="Owner"
        :options="$store.getters['library/players']"
        @search="searchPlayers"
      />
    </Filters>

    <!-- Content -->
    <div class="mt-4">
      <b-row v-show="!loading">
        <!-- Games list -->
        <b-col
          v-for="(game, index) in games"
          :key="index"
          cols="6"
          md="4"
          xl="3"
        >
          <b-skeleton-wrapper :loading="loading">
            <template #loading>
              <GameCard>
                <template #metadata>
                  <b-skeleton width="85%"></b-skeleton>
                  <b-skeleton width="55%"></b-skeleton>
                </template>
                <template #status>
                  <b-skeleton width="70%"></b-skeleton>
                </template>
              </GameCard>
            </template>

            <GameCard
              :image="game.game.image"
              :title="game.game.name"
              :no-footer="!$store.getters['users/current'].is_staff"
            >
              <template #metadata>
                <div v-if="$store.getters['users/current'].is_staff">
                  <metadata-item
                    :text="game.owner.name"
                    icon="briefcase-fill"
                  />
                  <metadata-item
                    v-if="game.location"
                    :text="game.location.name"
                    icon="geo-alt-fill"
                  />
                </div>

                <div v-else class="flex flex-column">
                  <metadata-item
                    :text="
                      num_players(game.game.min_players, game.game.max_players)
                    "
                    icon="person-fill"
                  />
                  <metadata-item
                    :text="
                      playtime(game.game.min_playtime, game.game.max_playtime)
                    "
                    icon="clock-fill"
                  />
                </div>
              </template>

              <template #footer v-if="$store.getters['users/current'].is_staff">
                <div v-if="game.status === 'not-available'">
                  <span class="text-warning"
                    >With {{ game.current_withdraw.requisitor.name }}</span
                  >
                </div>
                <div v-if="game.status === 'available'">
                  <span class="text-success">Available</span>
                </div>
                <b-button
                  v-show="game.status === 'available'"
                  :to="{ name: 'WithdrawGame', params: { id: game.id } }"
                  size="sm"
                  variant="light"
                >
                  <span class="text-muted">WITHDRAW</span>
                  <span v-if="game.location" class="text-muted">
                    ({{ game.location.name }})
                  </span>
                </b-button>

                <b-button
                  v-show="game.status === 'not-checked-in'"
                  v-b-modal.checkin-modal
                  size="sm"
                  variant="light"
                  @click="$emit('checkin', game)"
                >
                  <span class="text-muted">CHECK-IN</span>
                </b-button>

                <b-button
                  v-show="game.status === 'not-available'"
                  size="sm"
                  variant="light"
                  @click="returnGame(game)"
                >
                  <span class="text-muted">RETURN</span>
                </b-button>
              </template>
            </GameCard>
          </b-skeleton-wrapper>
        </b-col>
      </b-row>

      <!-- Skeleton -->
      <b-row v-show="loading">
        <b-col
          v-for="index in new Array(50)"
          v-bind:key="index"
          lg="4"
          md="6"
          xl="3"
          sm="12"
        >
          <ItemCard image="@/assets/blank_box.jpg">
            <template #metadata>
              <b-skeleton class="text-muted" width="100px" />
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
          <b-button
            v-if="games.length > selected.length"
            class="btn-white-20"
            size="sm"
            @click="selectAll"
          >
            Select all
          </b-button>
          <b-button
            v-else
            class="btn-outline-white"
            size="sm"
            @click="unselectAll"
          >
            Unselect all
          </b-button>
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
  </b-container>
</template>

<script>
import gamesMixin from '@/mixins/games.mixin'
import libraryService from '@/services/library.service'
import Header from '@/components/Header'
import LibraryGameCard from '@/components/cards/LibraryGameCard'
import ModalPlayerSelect from '@/components/ModalPlayerSelect'
import playerService from '@/services/player.service'
import CheckinModal from '@/components/CheckinModal'
import ItemCard from '@/components/cards/ItemCard'
import usersMixin from '@/mixins/users.mixin'
import axiosUtils from '@/mixins/axios.utils'
import Pagination from '@/components/Pagination'
import Filters from '@/components/Filters'
import FiltersButton from '@/components/FiltersButton'
import FilterSelect from '@/components/FilterSelect'
import GameCard from '@/components/cards/GameCard'

export default {
  name: 'Home',
  props: ['title', 'pretitle'],
  data() {
    return {
      search: '',
      games: new Array(50).fill({}),
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
    GameCard,
    FiltersButton,
    Pagination,
    CheckinModal,
    ModalPlayerSelect,
    LibraryGameCard,
    Header,
    ItemCard,
    Filters,
    FilterSelect,
  },
  mixins: [gamesMixin, usersMixin],
  mounted() {
    this.refreshGames()
  },
  methods: {
    selectAll() {
      this.selected = this.games.map((game) => game.id)
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

      Object.keys(this.filters).forEach(
        (key) => (params[key] = this.filters[key]),
      )

      return params
    },
    openLocationModal(game) {
      this.selectedGame = game
      this.$bvModal.show('checkin-modal')
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
