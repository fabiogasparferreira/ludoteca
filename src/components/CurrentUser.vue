<template>
  <b-link>
    <div class="d-flex flex-row">
      <b-avatar
        :src="
          'https://randomuser.me/api/portraits/lego/' +
            Math.floor(Math.random() * 9) +
            '.jpg'
        "
      ></b-avatar>
      <div class="d-flex flex-column">
        <span>{{ this.$store.getters['users/current'].name }}</span>
        <span class="text-muted d-block mt-1">{{
          this.$store.getters['users/current'].email
        }}</span>
      </div>
    </div>
  </b-link>
</template>

<script>
export default {
  name: 'CurrentUser',
}
</script>

<style scoped></style>
