import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export const store = new Vuex.Store({
  strict: true,
  state: {
    inputText: '',
    fileIsLoaded: false,
    loadingFile: false
  },
  getters: {
    inputText: (state) => {
      return state.inputText
    }
  },
  mutations: {
    editInputText: (state, payload) => {
      state.inputText = payload
    },
    fileIsLoaded: state => {
      state.fileIsLoaded = true
    },
    startLoading: state => {
      state.loadingFile = true
    },
    endLoading: state => {
      state.loadingFile = false
    }
  },
  actions: {
    editInputText: (context, payload) => {
      context.commit('editInputText', payload)
    },
    fileIsLoaded: context => {
      context.commit('fileIsLoaded')
    },
    sendInputTextToEngine: context => {
      // const formData = new FormData()
      console.log(context.getters.inputText)
      // axios.get('http://localhost:8000/search/', {
      //   'q': 'Ala ma kota',
      //   'crossdomain': true
      // }).catch(function (response) {
      //       // handle error
      //         console.log(response)
      //       })
      axios.post('http://localhost:8000/search/', {
        queryText: context.getters.inputText
      }).then(function (response) {
        // handle success
        console.log(response)
      })
        .catch(function (response) {
        // handle error
          console.log(response)
        })
    }
  }
})
