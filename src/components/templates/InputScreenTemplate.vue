<template>
  <div class="min-vh-100">
    <b-container>
      <b-row class="justify-content-center">
        <b-col lg="10" md="10" sm="12" xl="8">
          <div class="header mt-3 mt-md-5">
            <div class="header-body">
              <b-row class="align-items-center">
                <b-col cols="auto">
                  <b-button :to="backTo" class="btn-rounded-circle btn-white">
                    <span class="fe fe-arrow-left"></span></b-button
                ></b-col>
                <b-col>
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
    <b-container class="pt-5">
      <b-row class="justify-content-center">
        <b-col lg="10" md="10" sm="12" xl="8">
          <slot> </slot>
        </b-col>
      </b-row>
    </b-container>
    <b-container class="mt-5 mt-md-6">
      <b-row class="justify-content-center">
        <b-col lg="10" md="10" sm="12" xl="8">
          <form novalidate @submit.stop.prevent="onSubmit">
          <slot name="content"></slot>
                </form>
        </b-col>
      </b-row>
    </b-container>
    <b-container class="fixed-bottom position-fixed py-5">
      <b-row class="justify-content-center">
        <b-col lg="10" md="10" sm="12" xl="8">
            <div class="d-flex flex-row">
              <b-button
                variant="secondary"
                size="lg"
                :to="{ name: 'LibraryHome' }"
                >Cancel</b-button
              >
              <b-button
                variant="primary"
                size="lg"
                class="ml-5"
                block
                v-on:click="onSubmit()"
              >
                Finish
              </b-button>
              </div>
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
  methods:{
    onSubmit(){
      this.$emit('submit')
    }
  }
}
</script>

<style scoped></style>
