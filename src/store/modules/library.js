import playersService from '@/services/player.service'
import libraryService from '@/services/library.service'

const state = {
  games: [],
  locations: [],
  players: [],
}

const getters = {
  games: state => {
    return state.games
  },
  locations: state => {
    return state.locations
  },
  players: state => {
    return state.players
  },
}

const actions = {
  loadLocations({ commit }) {
    libraryService.getLocations().then(data => {
      commit('setLocations', data)
    })
  },
  loadPlayers({ commit }) {
    playersService.fetchPlayers().then(data => {
      commit('setPlayers', data)
    })
  },
}

const mutations = {
  setGames(state, games) {
    state.games = games
  },
  addGame(state, game) {
    state.games.push(game)
  },
  deleteGame(state, gameId) {
    state.games = state.games.filter(obj => obj.pk !== gameId)
  },
  setLocations(state, payload) {
    state.locations = payload
  },
  setPlayers(state, payload) {
    state.players = payload
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
