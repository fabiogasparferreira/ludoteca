<template>
  <div>
    <!--    <b-navbar class="py-5">-->
    <b-container>
      <div
        class="d-flex row align-content-between justify-content-between w-100 pt-6 pb-4"
      >
        <!--        <b-col>-->

        <!--                <b-button :to="backTo" variant="white" class="btn btn-lg btn-rounded-circle "><b-icon-arrow-left /></b-button>-->
        <!--            </b-col>-->




        <!-- Title -->
        <div>
                       <h6 class=" text-uppercase text-muted">
                  {{ preTitle }}
                </h6>
          <h1 class="mb-0">
            {{ title }}
          </h1>
        </div>
        <div>
          <b-button variant="primary">Save</b-button>
        </div>
      </div>
    </b-container>
    <!--    </b-navbar>-->
    <hr  class="mt-0"/>
    <b-container class="mt-6">
      <b-row class="justify-content-center">
        <b-col lg="10" md="12" sm="12" xl="8">
          <slot name="content"></slot>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
  name: 'InputScreen',
  components: {},
  props: {
    preTitle: {},
    title: {},
    subTitle: {},
    backTo: {
      type: Object,
    },
  },
  data() {
    return {
      items: ['Item 1', 'Item 2', 'Item 3'],
      // there will be a selected item
      selected: null,
    }
  },
}
</script>

<style scoped></style>
