<template>
  <div id="app" style="min-height: 100vh">
<!--    <TopNav></TopNav>-->
    <transition name="fade">
      <router-view />
    </transition>
  </div>
</template>

<script>
import authorizationService from '@/services/authorization.service'
// import TopNav from '@/partials/TopNav'

export default {
  name: 'App',
  components: {
    // TopNav
  },
  created() {
    if (authorizationService.isAuthenticated()) {
      this.$store.dispatch('users/loadCurrent')
      this.$store.dispatch('library/loadLocations')
      this.$store.dispatch('library/loadPlayers')
      this.$store.dispatch('configurations/load')
    }
  },
}
</script>
