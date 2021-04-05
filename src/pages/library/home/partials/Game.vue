<template>
  <b-skeleton-wrapper :loading="loading">
    <template #loading>
      <b-card no-body>
        <b-card-img src="./static/blank_box.jpg" style="height: 8rem" />
        <b-card-body>
          <b-skeleton width="50%" />
          <b-skeleton class="mt-3" width="30%" />
          <b-skeleton class="mt-2" width="30%" />
        </b-card-body>
        <b-card-footer v-if="!noFooter">
          <div
            class="d-flex flex-row align-items-center justify-content-between"
          >
            <b-skeleton width="20%" />
            <b-skeleton width="20%" />
          </div>
        </b-card-footer>
      </b-card>
    </template>

    <b-card no-body>
      <div class="position-relative">
        <b-card-img-lazy
          :src="game.game.image"
          blank-src="./static/blank_box.jpg"
          blank-height="8rem"
          class="img-cover"
          style="height: 8rem; border-bottom-left-radius: 0; border-bottom-right-radius: 0"
        />
        <div
          v-if="selectable"
          class="position-absolute"
          style="
            top: 0;
            border-radius: 5px 0 5px 0;
            background-color: rgba(1, 1, 1, 0.5);
          "
        >
          <b-checkbox v-model="gameSelected" class="ml-3 mr-1 my-2" size="lg" />
        </div>
      </div>
      <b-card-body>
        <span
          class="font-size text-nowrap overflow-hidden d-block">
          {{ game.game.name }}
        </span>

        <div>
          <slot name="badges"></slot>
        </div>
        <div class="mt-3">
          <div v-if="$store.getters['users/current'].is_staff">
            <metadata-item :text="game.owner.name" icon="briefcase-fill" />
            <metadata-item
              :text="game.location ? game.location.name : 'Not available'"
              icon="geo-fill"
            />
          </div>

          <div v-else class="flex flex-column">
            <MetadataItem
              :text="num_players(game.game.min_players, game.game.max_players)"
              icon="person-fill"
            />
            <metadata-item
              :text="playtime(game.game.min_playtime, game.game.max_playtime)"
              icon="clock-fill"
            />
          </div>
        </div>
      </b-card-body>
      <b-card-footer v-show="$store.getters['users/current'].is_staff">
        <slot name="footer">
          <div
            class="d-flex flex-row align-items-center justify-content-between"
          >
            <span v-if="game.status === 'not-available'" class="text-warning"
              >{{ game.current_withdraw.requisitor.name }}
            </span>
            <span v-if="game.status === 'available'" class="text-success"
              >Available</span
            >
              <div v-if="game.status === 'available'">
                <b-link
                  class="d-inline d-md-none"
                  v-b-tooltip.hover
                  title="Withdraw"
                  :to="{ name: 'WithdrawGame', params: { id: game.id } }"
                >
                  <b-icon-arrow-up-circle
                    font-scale="1.5"
                    class="text-gray-700"
                  />
                </b-link>

                <b-button class="d-none d-md-inline" variant="light" size="sm" :to="{ name: 'WithdrawGame', params: { id: game.id } }">
                  WITHDRAW
                </b-button>
              </div>

              <div v-if="game.status === 'not-checked-in'">
                <b-link
                  class="d-inline d-md-none"
                  v-b-modal.checkin-modal
                  v-b-tooltip.hover
                  title="Check-in"
                  @click="$emit('check-in', game)"
                >
                  <b-icon-patch-plus-fill
                    font-scale="1.5"
                    class="text-gray-700"
                  />
                </b-link>
                <b-button
                  class="d-none d-md-inline"
                  variant="light"
                  size="sm"
                  @click="$emit('check-in', game)"
                >
                  CHECK-IN
                </b-button>
              </div>

              <div v-if="game.status === 'not-available'">
                <!-- Small width button -->
                <b-link
                  class="d-inline d-md-none"
                  v-b-tooltip.hover
                  title="Return"
                  @click="returnGame(game)"
                >
                  <b-icon-arrow-down-circle-fill
                    font-scale="1.5"
                    class="text-gray-700"
                  />
                </b-link>

                <!-- Medium width + button -->
                <b-button
                  class="d-none d-md-inline"
                  variant="light"
                  size="sm"
                  @click="returnGame(game)"
                >
                  RETURN
                </b-button>
              </div>
          </div>
        </slot>
      </b-card-footer>
    </b-card>
  </b-skeleton-wrapper>
</template>

<script>
import gamesMixin from '@/mixins/games.mixin'
import MetadataItem from '@/components/cards/MetadataItem'
import withdrawService from "@/services/withdraw.service"
import libraryService from "@/services/library.service"

export default {
  name: 'LibraryHomeGameCard',
  props: {
    game: {
      type: Object,
      default: () => {
        return {
          id: '',
          game: {
            min_players: 0,
            max_players: 0,
            min_playtime: 0,
            max_playtime: 0,
          },
          current_withdraw: {
            requisitor: {
              name: '',
            },
          },
        }
      },
    },
    loading: {
      default: false,
      type: Boolean,
    },
    title: {
      default: '',
      type: String,
    },
    image: {
      default: '',
      type: String,
    },
    noFooter: {
      default: false,
      type: Boolean,
    },
    noImage: {
      default: false,
      type: Boolean,
    },
    selectable: {
      default: false,
      type: Boolean,
    },
    selected: {
      default: false,
      type: Boolean,
    },
  },
    mixins: [gamesMixin],
  components: {
    MetadataItem,
  },
  computed: {
    gameSelected: {
      get() {
        return this.selected
      },
      // eslint-disable-next-line no-unused-vars
      set(val) {
        this.$emit('selected-change', this.game.id)
      },
    },
  },
  methods: {
    returnGame(game) {
      withdrawService.returnGame(game.current_withdraw.id).then(() => {
        libraryService.fetchGame(game.id).then(() => {
          this.$emit('return')
        })
      })
    },
  },

}
</script>

<style scoped></style>
