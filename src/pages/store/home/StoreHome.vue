<template>
  <HomeScreenTemplate :title="title" :pre-title="pretitle">
    <GameList :loading="loading" :games="games"/>
  </HomeScreenTemplate>
</template>

<script>
import GameList from "@/pages/store/home/partials/GameList"
import HomeScreenTemplate from "@/components/templates/HomeScreenTemplate"
import storeService from "@/services/store.service"

export default {
  name: 'StoreHome',
  components: {
    HomeScreenTemplate,
    GameList,
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
