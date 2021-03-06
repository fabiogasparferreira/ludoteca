<template>
  <b-skeleton-wrapper :loading="loading">
    <template #loading>
      <b-card no-body>
        <b-card-img src="./static/blank_box.jpg" style="height: 8rem" />
        <b-card-body>
          <b-skeleton width="50%" />
          <b-skeleton class="mt-2" width="40%" />
          <b-skeleton class="mt-2" width="30%" />
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
          v-if="!noImage"
          :src="image"
          blank-src="./static/blank_box.jpg"
          blank-height="8rem"
          style="object-fit: cover; height: 8rem"
        />
        <div v-if="selectable"
          class="position-absolute"
          style="
            top: 0;
            border-radius: 5px 0 5px 0;
            background-color: rgba(1,1, 1, 0.5);
          "
        >
          <b-checkbox v-model="gameSelected" class="ml-3 mr-1 my-2" size="lg" />
        </div>
      </div>
      <b-card-body>
        <span
          class="text-nowrap font-size-lg d-block overflow-hidden text-truncate"
          v-show="title"
          >{{ title }}</span
        >

        <div>
          <slot name="badges"></slot>
        </div>
        <div class="mt-2">
          <slot name="metadata"></slot>
        </div>
      </b-card-body>
      <b-card-footer v-if="!noFooter">
        <slot name="footer">
          <div
            class="d-flex flex-row align-items-center justify-content-between"
          >
            <slot name="status"></slot>
            <slot name="actions"></slot>
          </div>
        </slot>
      </b-card-footer>
    </b-card>
  </b-skeleton-wrapper>
</template>

<script>
import gamesMixin from '@/mixins/games.mixin'

export default {
  name: 'GameCard',
  props: {
    loading: {
      default: false,
      type: Boolean,
    },
    game_id: {
      required: true,
      type: Number
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
      type: Boolean
    },
    selected: {
      default: false,
      type: Boolean
    }
  },
computed: {
    gameSelected:{
      get(){
        return this.selected
      },
      // eslint-disable-next-line no-unused-vars
      set(val){
        this.$emit('selected-change', this.game_id)
      }
    }
},
  mixins: [gamesMixin],
}
</script>

<style scoped></style>
