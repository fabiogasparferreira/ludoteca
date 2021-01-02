<template>

  <div class="header">
    <div class="header-body">
      <div class="row align-items-center">
        <div class="col d-flex flex-row">
          <b-link :to="{name: 'LibraryHome'}">
            <b-button variant="outline-secondary">
              <b-icon-arrow-left></b-icon-arrow-left>

            </b-button>
          </b-link>
          <div class="ml-4 d-flex flex-column">
            <h6 class="header-pretitle">
              {{ pretitle }}
            </h6>

            <h1 class="header-title">
              {{ title }}
            </h1>
          </div>
        </div>
        <div class="col-auto">
          <slot name="content-right"></slot>
        </div>
      </div>

    </div>
  </div>

</template>

<script>
export default {
  name: "Header",
  props: ['title', 'pretitle']
}
</script>

<style scoped>

</style>