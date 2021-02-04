import userService from '@/services/user.service'

const state = {
  current: {
    email: '',
    username: '',
    is_staff: false,
    is_superuser: false,
  },
}

const getters = {
  current: state => {
    return state.current
  },
}

const actions = {
  loadCurrent({ commit }) {
    userService.fetchUser('current').then(response => {
      commit('setCurrent', response)
    })
  },
}

const mutations = {
  setCurrent(state, user) {
    state.current = user
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
