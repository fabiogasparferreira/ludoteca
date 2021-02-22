<template>
  <b-skeleton-wrapper :loading="loading">
    <template #loading>
      <b-card no-body>
        <b-card-img src="./static/blank_box.jpg" style="height: 8rem"/>
        <b-card-body>
          <b-skeleton width="50%" />
          <b-skeleton class="mt-2" width="40%" />
          <b-skeleton class="mt-2" width="30%" />
          <b-skeleton class="mt-2" width="30%" />
        </b-card-body>
        <b-card-footer>
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
      <b-card-img-lazy
        :src="image"
        blank-src="./static/blank_box.jpg"
        blank-height="8rem"
        style="object-fit: cover; height: 8rem"
      />

      <b-card-body>
        <span
          class="text-nowrap font-size-lg d-block overflow-hidden text-truncate"
          v-show="title"
          >{{ title }}</span
        >

        <div class="mt-2">
          <slot name="badges"></slot>
        </div>
        <div class="mt-3">
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
  },

  mixins: [gamesMixin],
}
</script>

<style scoped></style>
