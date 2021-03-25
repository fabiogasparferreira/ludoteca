<template>
  <div class="mr-4 mt-2 d-block" v-b-tooltip.hover :title="tooltip">
    <b-icon font-scale="0.9" v-if="!noIcon" :icon="icon" class="text-muted mr-2"/>

    <span class="text-muted small">
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
