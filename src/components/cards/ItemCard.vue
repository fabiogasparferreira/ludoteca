<template>
  <b-card no-body :bg-variant="variant" :title="title" class="">
    <b-card-img-lazy
      :src="image"
      blank-src="@/assets/blank_box.jpg"
      blank-height="8rem"
      style="object-fit: cover; height: 8rem;"
    />

    <b-card-body>
      <span
        class="text-nowrap font-size-lg d-block overflow-hidden text-truncate"
        v-show="title"
        >{{ title }}</span
      >
      <b-skeleton v-show="!title" width="50%"></b-skeleton>

      <div class="mt-2">
        <slot name="badges"><b-badge variant="soft-primary">2021's picks</b-badge></slot>

      </div>
      <div class="mt-3">
        <slot name="metadata"></slot>
      </div>
    </b-card-body>
    <b-card-footer>
      <slot name="status">
        <span class="d-inline text-warning">With Jamie</span>
      </slot>

      <slot name="actions">
        <b-button class="float-right" size="sm" variant="light"
          >RETURN</b-button
        >
      </slot>
    </b-card-footer>
  </b-card>
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
    image: {
      default: '',
      type: String,
    },
  },
}
</script>

<style lang="scss">
.card-image {
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  border-radius: 5px 5px;
  //background: linear-gradient(180deg, rgba(0, 0, 0, 0.6), transparent);
  //background: rgba(0, 0, 0, 0.6);
  //background: rgba(255, 255, 255, 0.7);
}

//.card-hover:hover {
//  .card-image{visibility: visible; }
//}
</style>
