<template>
  <ItemCard :bulk="bulk" :loading="loading" :title="game.name" :variant="bgVariant">
    <template v-slot:image>
      <slot name="image">
        <b-avatar :src="game.thumbnail" rounded size="lg"></b-avatar>
      </slot>
    </template>
    <!--    <template v-slot:badges>-->
    <!--      <span v-for="(badge, index) in game.badges" v-bind:key="index" class="ml-2 badge" v-bind:class="{-->
    <!--      'badge-soft-primary': badge.label === 'Recomendado',-->
    <!--      'badge-soft-success': badge.label === 'Jogo do Ano'-->
    <!--      }"-->
    <!--      >{{ badge.label }}</span>-->
    <!--    </template>-->
    <template v-slot:metadata>
      <slot name="metadata">
        <b-icon-person-fill class="text-muted mr-2"></b-icon-person-fill>
        <span class=" text-muted">{{ num_players(game.min_players, game.max_players) }}</span>
        <b-icon-clock-fill class="ml-4 mr-2 text-muted" font-scale="0.8"></b-icon-clock-fill>
        <span class=" text-muted">{{ playtime(game.min_playtime, game.max_playtime) }} </span>
      </slot>
    </template>
    <template v-slot:top-right>
      <slot name="top-right"></slot>
    </template>
    <template v-slot:bottom-right>
      <slot name="bottom-right"></slot>
    </template>
    <template v-slot:right>
      <slot name="right"></slot>
    </template>
  </ItemCard>
</template>

<script>
import ItemCard from "@/components/ItemCard"
import gamesMixin from "@/mixins/games.mixin"

export default {
  name: "GameCard",
  props: {
    game: {
      required: true,
      type: Object,
    },
    loading: {
      default: false,
      type: Boolean
    },
    bulk: {
      default: false,
      type: Boolean
    },
    bgVariant: {
      type: String,
    }
  },

  mixins: [gamesMixin],
  components: {
    ItemCard
  },
  data() {
    return {
      selected: []
    }
  }
}
</script>

<style scoped>

</style>