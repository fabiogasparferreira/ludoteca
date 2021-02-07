<template>
  <div>
    <TopNav></TopNav>
    <div class="container">
      <router-view />
    </div>
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
