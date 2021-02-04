<template>
  <!-- Modal -->
  <b-modal :id="id" :title="title">
    <template>
      <!--            <div class="d-flex flex-row align-items-center justify-content-between">-->
      <!-- Back -->
      <!--                <slot name="back"></slot>-->
      <!-- Title -->
      <h3 class="mb-0">
        <slot name="title">{{ title }}</slot>
      </h3>

      <!-- Close -->
      <!--                <button type="button" class="close" data-dismiss="modal" aria-label="Close">-->
      <!--                    <span aria-hidden="true">&times;</span>-->
      <!--                </button>-->
      <!--            </div>-->
    </template>
    <template v-slot:default>
      <slot name="content"></slot>
    </template>
    <template v-slot:modal-footer>
      <slot name="footer"></slot>
    </template>
  </b-modal>
</template>

<script>
export default {
  name: 'Modal',
  props: ['id', 'title'],
}
</script>

<style scoped></style>
