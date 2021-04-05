<template>
  <div>
    <b-row class="">
      <b-col v-for="(game, index) in games" :key="index" cols="6" md="4" xl="3">
        <Game :game="game" :loading="loading" />
      </b-col>
    </b-row>
  </div>
</template>

<script>
import Game from './Game'

export default {
  name: 'GameList',
  components: {
    Game,
  },
  props: {
    games: {
      type: Array,
      required: true,
    },
    loading: {
      type: Boolean,
      default: true,
    },
  },
}
</script>

<style scoped></style>
