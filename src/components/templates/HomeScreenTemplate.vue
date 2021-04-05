<template>
  <div>
    <TopNav></TopNav>
    <b-container fluid="sm">
      <Header :pretitle="preTitle" :title="title">
        <template v-slot:content-right>
          <slot name="actions"></slot>
        </template>
      </Header>

      <slot></slot>
    </b-container>
  </div>
</template>

<script>
import TopNav from '@/components/TopNav'

import Header from '@/components/Header'

export default {
  name: 'HomeScreenTemplate',
  props: {
    title: {
      default: 'Empty title',
    },
    preTitle: {
      type: String,
      required: true,
    },
  },
  components: {
    TopNav,
    Header,
  },
}
</script>
