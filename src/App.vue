<template>
  <div id="app" style="min-height: 100vh">
    <router-view />
  </div>
</template>

<script>
import authorizationService from '@/services/authorization.service'
export default {
  name: 'App',
  created() {
    if (authorizationService.isAuthenticated()) {
      this.$store.dispatch('users/loadCurrent')
      this.$store.dispatch('library/loadLocations')
      this.$store.dispatch('library/loadPlayers')
    }
  },
}
</script>
