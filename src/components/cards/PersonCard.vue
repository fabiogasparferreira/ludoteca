<template>
  <b-skeleton-wrapper :loading="loading">
    <template #loading>
      <b-card no-body>
        <b-avatar variant="light" size="8rem" />
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
          </div>
        </b-card-footer>
      </b-card>
    </template>

    <b-card no-body>
      <b-card-body>
        <span
          class="text-nowrap font-size-lg d-block overflow-hidden text-truncate"
          v-show="name"
        >
          {{ name }}
        </span>

        <div class="mt-2">
          <slot name="metadata"></slot>
        </div>
      </b-card-body>
      <b-card-footer v-if="!noFooter">
        <slot name="footer">
          <div class="d-flex flex-row align-items-center justify-content-end">
            <slot name="actions"></slot>
          </div>
        </slot>
      </b-card-footer>
    </b-card>
  </b-skeleton-wrapper>
</template>

<script>
export default {
  name: 'PersonCard',
  props: {
    loading: {
      default: false,
      type: Boolean,
    },
    name: {
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
}
</script>

<style scoped></style>
