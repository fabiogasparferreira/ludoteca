<template>
  <b-dropdown toggle-class="py-1 px-2" :variant="variant" right no-caret>
    <template #button-content>
      <div class="d-flex flex-row text-gray-800 align-items-center">
        <!--                            <b-avatar size="sm"/>-->

        <span class="d-none d-sm-inline-block">{{
          $store.getters['users/current'].name
        }}</span>
        <b-avatar size="sm" class="ml-sm-2"></b-avatar>
      </div>
    </template>
    <template #default>
      <b-dropdown-item-button>
        <b-icon-person class="mr-3"></b-icon-person>
        Profile
      </b-dropdown-item-button>
      <b-dropdown-divider></b-dropdown-divider>
      <b-dropdown-item-button @click="$emit('logout')">
        <b-icon-box-arrow-right class="mr-3" />
        Logout
      </b-dropdown-item-button>
    </template>
  </b-dropdown>
</template>
<script>
export default {
  name: 'UserInfo',
  props: {
    variant: {
      type: String,
      default: 'link',
    },
    noName: {
      type: Boolean,
      default: false,
    },
    logout: {},
  },
}
</script>
