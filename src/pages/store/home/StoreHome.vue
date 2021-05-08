<template>
  <HomeScreenTemplate :title="title" :pre-title="pretitle">
    <template #actions><b-button variant="primary" :to="{name: 'StoreAddGame'}">Add game</b-button></template>
    <Games :loading="loading" :games="games"/>

  </HomeScreenTemplate>
</template>

<script>
import Games from "@/pages/store/home/partials/Games"
import HomeScreenTemplate from "@/components/templates/HomeScreenTemplate"
import storeService from "@/services/store.service"

export default {
  name: 'StoreHome',
  components: {
    HomeScreenTemplate,
    Games,
  },
  props: ['title', 'pretitle'],
  data() {
    return {
      games: [],
      loading: true
    }
  },
  mounted(){
    storeService.fetchGames(1).then(response => {
      this.games = response.results
      this.loading = false
    })
  }
}
</script>

<style scoped></style>
