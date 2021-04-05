<template>
  <b-skeleton-wrapper :loading="loading">
    <template #loading>
      <b-card no-body>
        <b-card-img src="/static/blank_box.jpg" style="height: 12rem" />
        <b-card-body>
          <b-skeleton width="50%" />
          <b-skeleton class="mt-3" width="30%" />
          <b-skeleton class="mt-2" width="30%" />
        </b-card-body>
      </b-card>
    </template>

    <b-card no-body>
      <div class="position-relative">
        <b-card-img-lazy
          :src="game.game.image"
          class="img-cover"
          blank-src="/static/blank_box.jpg"
          blank-height="10rem"
          style="height: 10rem; border-bottom-left-radius: 0; border-bottom-right-radius: 0"
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
        <span class="text-nowrap overflow-hidden d-block">
          {{ game.game.name }}</span
        >
        <div class="mt-1">
                <span v-if="game.stock > 0 && game.stock <= 5" class="small text-warning d-block"
          >Only {{ game.stock }} available</span
        >
        <span v-if="game.stock > 5" class="small text-success d-block"
          >Available</span
        >
        <span v-if="game.stock === 0" class="small d-block text-danger"
          >Sold out</span
        ></div>
        <b-row class="mt-4 no-gutters">
          <b-col>
            <div class="">
              <h3 class="font-weight-lighter text-gray-900 mb-0">
                {{ game.selling_price }}€
              </h3>
            </div>
          </b-col>
          <b-col>
            <div class="d-flex flex-row align-content-center align-items-center">
              <b-icon-award-fill class="text-muted"/>
              <h3 class="ml-2 font-weight-lighter mb-0"
                >{{ (game.selling_price * 0.9).toFixed(2) }}€</h3>
            </div>
          </b-col>
        </b-row>


      </b-card-body>
    </b-card>
  </b-skeleton-wrapper>
</template>

<script>
import gamesMixin from '@/mixins/games.mixin'

export default {
  name: 'StoreHomePartialGameCard',
  props: {
    loading: {
      default: false,
      type: Boolean,
    },
    game: {
      default: () => {
        return {
          id: '',
          stock: 0,
          selling_price: 0,
          game: {
            image: '',
            name: '',
          },
        }
      },
      type: Object,
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
  mixins: [gamesMixin],
}
</script>

<style scoped></style>
