<template>
    <div>
      <b-row class="">
        <b-col
          v-for="(game, index) in games"
          :key="index"
          cols="6"
          md="4"
          xl="3"
        >
          <GameCard
            :game_id="game.id"
            :loading="loading"
            :image="game.game.image"
            :title="game.game.name"
            :no-footer="!$store.getters['users/current'].is_staff"
          />
        </b-col>
      </b-row>
    </div>
</template>

<script>
import GameCard from "@/components/cards/GameCard"

export default {
  name: "GameList",
    components: {
    GameCard,
  },
  props: {
    games: {
      type: Array,
      required: true
    },
    loading: {
      type: Boolean,
      default: true
    }
  }
}
</script>

<style scoped>

</style>