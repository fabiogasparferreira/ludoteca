<template>
  <div id="app" style="min-height: 100vh">
    <transition name="fade">
      <router-view />
    </transition>
  </div>
</template>

<script>
import authorizationService from '@/services/authorization.service'

export default {
  name: 'App',
  components: {
  },
  created() {
    if (authorizationService.isAuthenticated()) {
      this.$store.dispatch("init")
    }
  },
}
</script>
