<template>
  <b-skeleton-wrapper :loading="loading">
    <b-card class="mb-2 mb-sm-3" :bg-variant="variant" >
      <div class="media">
        <!-- left content-->
        <div class="media-aside">
          <slot name="image"></slot>
        </div>

        <!-- body -->
        <b-media-body class="align-self-stretch d-flex flex-column">
          <div
            class="d-flex flex-row flex-grow-1 align-items-center justify-content-between"
          >
            <span v-show="title" class="mb-0">{{ title }}</span>
            <b-skeleton v-show="!title" width="50%"></b-skeleton>
            <slot name="top-right" />
          </div>
          <div
            class="d-flex flex-row flex-grow-1 align-items-center justify-content-between"
          >

              <slot name="metadata"></slot>
              <slot name="bottom-right"></slot>

          </div>
        </b-media-body>
      </div>
    </b-card>
  </b-skeleton-wrapper>
</template>

<script>
export default {
  name: 'ItemCard',
  props: {
    variant: {
      type: String,
      default: 'default',
    },
    title: {
      type: String,
    },
    loading: {
      default: false,
      type: Boolean,
    },
    bulk: {
      default: false,
      type: Boolean,
    },
  },
}
</script>
