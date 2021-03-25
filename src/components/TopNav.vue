<template>
  <b-navbar toggleable="md">
    <b-container>
      <b-navbar-brand :to="{ name: 'LibraryHome' }">
        <img src="@/assets/leiriacon.png"/>
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" class="w-100" is-nav>
        <b-navbar-nav>
          <b-nav-item :to="{ name: 'LibraryHome' }" active-class="active">
            Ludoteca
          </b-nav-item>
          <b-nav-item :to="{ name: 'StoreHome' }" active-class="active">
            Loja
          </b-nav-item>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-button
              v-if="!isAuthenticated()"
              :to="{ name: 'Login' }"
              variant="link"
          >Sign in
          </b-button
          >
          <b-nav-item-dropdown
              v-if="isAuthenticated()"
              :text="$store.getters['users/current'].name"
              right
              toggle-class="pl-0"
          >
            <b-dropdown-item :to="{name: 'Configurations'}">Configurations</b-dropdown-item>
            <b-dropdown-divider></b-dropdown-divider>
            <b-dropdown-item-button @click="logout"
            >Logout
            </b-dropdown-item-button
            >
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-container>
  </b-navbar>
</template>
<script>
import usersMixin from '@/mixins/users.mixin'
import authorizationService from '@/services/authorization.service'
//import UserInfo from "@/components/UserInfo";

export default {
  name: 'TopNav',
  components: {},
  mixins: [usersMixin],
  methods: {
    logout() {
      authorizationService.logout()
      location.reload()
    },
    isAuthenticated() {
      return authorizationService.isAuthenticated()
    },
  },
}
</script>
