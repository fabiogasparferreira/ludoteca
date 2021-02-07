<template>
  <ItemCard :title="person.name">
    <template v-slot:image>
      <div class="avatar">
        <span
          class="avatar-title rounded-circle"
          v-text="initials(person.name)"
        ></span>
      </div>
    </template>
    <template v-slot:metadata>
      <p class="text-muted mb-0">
        <b-icon-envelope-fill class="mr-2"></b-icon-envelope-fill>
        <span v-text="person.email"></span>
      </p>
    </template>
  </ItemCard>
</template>

<script>
import ItemCard from '@/components/ItemCard'
import personMixin from '@/mixins/person.mixin'

export default {
  name: 'PersonCard',
  components: { ItemCard },
  mixins: [personMixin],
  props: ['person'],
}
</script>

<style scoped></style>
