<template>
  <b-container>
    <Header
      :pretitle="pretitle"
      :title="title"
      :bulk="bulk"
      @bulk-change="bulk = $event"
    />

    <GameList />
  </b-container>
</template>

<script>
import Header from './partials/Header'
import GameList from "@/pages/store/home/partials/GameList"

export default {
  name: 'StoreHome',
  components: {
    GameList,
    Header,
  },
  props: ['title', 'pretitle'],
  data() {
    return {
      bulk: false,
    }
  },
}
</script>

<style scoped></style>
