<template>
  <b-row class="mt-3">
    <b-col v-for="(column, index) in columns" v-bind:key="index">
      <div
        v-for="(row, index) in rows"
        v-bind:key="index"
        :class="{
          'bg-light': !isLocationCell(column, row),
          'bg-success': isLocationCell(column, row),
        }"
        class="my-2 shelf"
      >
        <span
          v-if="isLocationCell(column, row)"
          class="text-white font-size-lg"
          ><b-icon-geo-fill/> {{ location }}</span
        >
      </div>
    </b-col>
  </b-row>
</template>

<script>
export default {
  name: 'LocationShelves',
  props: {
    location: {
      type: String,
      default: '',
    },
  },
  computed: {
    columns() {
      const columns = []
      const shelves = this.$store.getters['library/locations'].filter(
        (item) => item.type === 'shelf',
      )
      shelves.forEach((shelf) => {
        const column = shelf.name.substring(0, 1)

        if (!columns.includes(column)) {
          columns.push(column)
        }

        columns.sort()
      })
      return columns
    },
    rows() {
      const rows = []
      const shelves = this.$store.getters['library/locations'].filter(
        (item) => item.type === 'shelf',
      )
      shelves.forEach((shelf) => {
        const row = shelf.name.substring(1, 2)

        if (!rows.includes(row)) {
          rows.push(row)
        }

        rows.sort()
      })
      return rows
    },
  },
  methods: {
    isLocationCell(column, row) {
      return column + row === this.location
    },
  },
}
</script>

<style scoped>
.shelf {
  border-radius: 5px;
  height: 4vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
