<template>
  <div class="mr-4 d-inline-block">
    <b-icon :icon="icon" class="text-muted mr-2"/>

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
      required: true,
      type: String,
    },
    text: {
      required: true,
      type: [String, Number]
    },
  },
}
</script>
