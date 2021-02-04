<template>
  <b-container>
    <b-row class="justify-content-center mb-7 mt-5">
      <b-col cols="12" xl="10">
        <b-row class="justify-content-center">
          <b-col>
            <b-button :to="backTo">
              <b-icon-arrow-left />
              <span class="d-none d-sm-inline-block">back</span>
            </b-button>
          </b-col>
          <b-col class="text-center d-flex align-items-center" cols="auto">
            <!-- Pretitle -->
            <!--        <h6 class=" text-uppercase text-muted">-->
            <!--          {{ preTitle }}-->
            <!--        </h6>-->

            <!-- Title -->
            <h1 class="mb-0">
              {{ title }}
            </h1>
          </b-col>
          <b-col class="d-flex justify-content-end align-items-center">
            <UserInfo />
          </b-col>
        </b-row>
      </b-col>
    </b-row>

    <b-row class="justify-content-center">
      <b-col lg="10" md="12" sm="12" xl="8">
        <slot name="content"></slot>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import UserInfo from '@/components/UserInfo'

export default {
  name: 'InputScreen',
  components: { UserInfo },
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
