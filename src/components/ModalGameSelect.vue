<template>
  <!-- Modal -->
  <ModalSelect
    :id="id"
    :hide-footer="true"
    :items="games"
    :title="title"
    item-metadata="year"
    item-title="name"
    @search="search"
    @selected="$emit('game-selected', $event)"
  >
  </ModalSelect>
</template>

<script>
import bggService from '@/services/bgg.service'
import ModalSelect from '@/components/ModalSelect'

export default {
  name: 'ModalGameSelect',
  props: ['id', 'title'],
  components: {
    ModalSelect,
  },
  data: function() {
    return {
      games: [],
      loading: false,
    }
  },
  methods: {
    search(val) {
      this.loading = true
      bggService.search(val).then(response => {
        this.loading = false
        this.games = response
      })
    },
  },
}
</script>

<style scoped></style>
