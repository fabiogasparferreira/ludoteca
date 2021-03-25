<template>
  <div>
    <TopNav></TopNav>
    <b-container fluid="sm">
      <slot></slot>
    </b-container>
  </div>
</template>

<script>
import TopNav from '@/components/TopNav'

export default {
  name: 'HomeScreenTemplate',
  props: {
    title: {
      default: 'Empty title',
    },
  },
  components: {
    TopNav,
  },
}
</script>
