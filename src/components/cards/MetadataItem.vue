<template>
  <div class="mr-4 mt-2 d-block" v-b-tooltip.hover :title="tooltip">
    <b-icon v-if="!noIcon" :icon="icon" class="text-muted mr-2"/>

    <span class="text-muted">
      {{ text }}
    </span>
  </div>
</template>

<script>
export default {
  name: 'MetadataItem',
  props: {
    icon: {
      default: '',
      type: String,
    },
    text: {
      required: true,
      type: [String, Number]
    },
    tooltip: {
      type: String,
      default: ''
    },
    noIcon: {
      default: false,
      type: Boolean
    }
  },
}
</script>
