import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    auth: false,
    vk_auth: false
  },
  getters: {
    authenticated: state => {
      return state.auth
    },

    vkAuthenticated: state => {
      return state.vk_auth
    }
  },
  mutations: {
    changeAuth(state, newState) {
      state.auth = newState
    },

    changeVKAuth(state, newState) {
      state.vk_auth = newState
    }
  },
  actions: {
    changeAuthState({ commit }, newState) {
      commit('changeAuth', newState)
    },

    changeVKAuthState({ commit }, newState) {
      commit('changeVKAuth', newState)
    }
  },
  modules: {
  }
})

export default store