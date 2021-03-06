<template>
  <div>
    <b-container class="sticky sticky-top">
      <b-row class="justify-content-center">
        <b-col lg="10" md="10" sm="12" xl="8">
          <div class="header mt-3 mt-md-5 mb-0">
            <div class="header-body">
              <b-row class="align-items-center">
                <b-col cols="auto">
                  <b-button :to="backTo" class="btn-rounded-circle btn-white">
                    <span class="fe fe-arrow-left"></span></b-button
                ></b-col>
                <b-col>
                  <h6 class="header-pretitle">LIBRARY</h6>
                  <h1 class="header-title">
                    {{ title }}
                  </h1>
                </b-col>
              </b-row>
            </div>


          </div>
        </b-col>
      </b-row>
    </b-container>
    <b-container class="mt-5 mt-md-6">
      <b-row class="justify-content-center">
        <b-col lg="10" md="10" sm="12" xl="8">
          <slot name="content"></slot>
          <b-row class="mb-3 mt-5">
          <b-col>
            <hr />
          </b-col>
          <b-col cols="12" md="auto">
            <b-button
              variant="link"
              size="lg"
              block
              class="text-muted"
              :to="{ name: 'LibraryHome' }"
              >Cancel</b-button
            >
          </b-col>
          <b-col cols="12" md="auto">
            <b-button variant="primary" size="lg" block v-on:click="$emit('submit')">
              Finish
            </b-button>
          </b-col>
        </b-row>
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
