import Vue from 'vue'
import Vuex from 'vuex'
import messages from './modules/messages'
import library from './modules/library'
import users from '@/store/modules/users'
import router from '@/router'
import authorizationService from '@/services/authorization.service'
import localStorageService from '@/services/localStorage.service'
import configurations from "@/store/modules/configurations"
import store from "@/store/modules/store"

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    messages,
    library,
    users,
    configurations,
    store
  },
  actions: {
    /**
     * Do login with username and password
     * In case of success, save tokens to local storage
     * @param commit
     * @param username
     * @param password
     * @returns {Promise<AxiosResponse<any>>}
     */
    login({ commit, dispatch }, { username, password }) {
      return authorizationService.doLogin(username, password).then(response => {
        commit('AUTH_SUCCESS', response.data)
        dispatch('users/loadCurrent').then(() => router.push({ name: 'Home' }))
      })
    },
    init({dispatch}){
      dispatch('users/loadCurrent')
      dispatch('library/loadLocations')
      dispatch('library/loadPlayers')
      dispatch('store/loadSuppliers')
      dispatch('configurations/load')
    }
  },

  mutations: {
    SET_CURRENT_USER(state, user) {
      state.currentUser = user
    },
    AUTH_SUCCESS(state, tokenObj) {
      localStorageService.setRefreshToken(tokenObj.refresh)
      localStorageService.setAccessToken(tokenObj.access)
    },
    AUTH_LOGOUT() {
      localStorageService.clearTokens()
    },
  },
})
