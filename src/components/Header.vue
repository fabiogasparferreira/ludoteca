<template>
  <div class="header">
    <div class="header-body pt-5">
      <div class="row align-items-center">
        <b-col class="d-flex flex-column">
          <h6 class="header-pretitle">
            {{ pretitle }}
          </h6>

          <h1 class="header-title">
            {{ title }}
          </h1>
        </b-col>

        <div class="col-auto">
          <slot name="content-right"></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Header',
  props: ['title', 'pretitle'],
}
</script>

<style scoped></style>
