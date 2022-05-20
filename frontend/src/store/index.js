import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    auth: false
  },
  getters: {
    authenticated: state => {
      return state.auth
    }
  },
  mutations: {
    changeAuth(state, newState) {
      state.auth = newState
    }
  },
  actions: {
    changeAuthState({ commit }, newState) {
      commit('changeAuth', newState)
    }
  },
  modules: {
  }
})

export default store