<template>
  <b-navbar toggleable="md">
    <b-container>
      <b-navbar-brand :to="{name: 'Home'}">
        <img src='@/assets/leiriacon.png'/>
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" class="w-100" is-nav>
        <b-navbar-nav>
          <b-nav-item active-class="active" :to="{ name: 'LibraryHome' }">Ludoteca</b-nav-item>
          <b-nav-item active-class="active" :to="{ name: 'StoreHome' }">Loja</b-nav-item>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-nav-item-dropdown toggle-class="pl-0" right :text="$store.getters['users/current'].name">
            <b-dropdown-item href="#">Profile</b-dropdown-item>
            <b-dropdown-item href="#">Logout</b-dropdown-item>
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
  name: "TopNav",
  components: {},
  mixins: [usersMixin],
  methods: {
    logout() {
      authorizationService.logout()
    }
  }
}
</script>

