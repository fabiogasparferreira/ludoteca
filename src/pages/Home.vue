<template>
  <div>
    <b-row class="mt-5">
      <b-col>
        <b-button size="lg" class="py-4" variant="dark" :to="{name: 'LibraryHome'}" block>Go to Library</b-button>
      </b-col>
      <b-col>
        <b-button size="lg" class="py-4" variant="info" :to="{name: 'StoreHome'}" block>Go to Store</b-button>
      </b-col>
    </b-row>

  </div>
</template>

<script>


export default {
  name: "Home",
  data() {
    return {}
  },

}
</script>
