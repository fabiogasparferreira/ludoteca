<template>
  <div>
    <TopNav></TopNav>
    <b-container fluid="sm">
      <router-view />
    </b-container>
  </div>
</template>

<script>
import TopNav from '@/components/TopNav'

export default {
  name: 'HomeTemplate',
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

<style scoped></style>
