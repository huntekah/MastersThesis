import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export const store = new Vuex.Store({
  strict: true,
  state: {
    inputText: '',
    outputData: {},
    fileIsLoaded: false,
    loadingFile: false,
    waitingForCorrection: false,
    correctionModel: "left-to-right"
  },

  getters: {
    inputText: (state) => {
      return state.inputText
    },
    outputData: (state) => {
      return state.outputData
    },
    correctionModel: (state) => {
      return state.correctionModel
    },
  },

  mutations: {
    editInputText: (state, payload) => {
      state.inputText = payload
    },
    updateOutputData: (state, payload) => {
      state.outputData = payload
    },
    applyCorrection: (state, {correction, index}) => {
      state.outputData[index].name = correction
      state.outputData[index].underlined = false
      // state.inputText = state.outputData.map(e => e.name).join();
    },
    setModel: (state, payload) => {
      state.correctionModel = payload
    },
    fileIsLoaded: state => {
      state.fileIsLoaded = true
    },
    startLoading: state => {
      state.loadingFile = true
    },
    endLoading: state => {
      state.loadingFile = false
    },
    waitForCorrection: state => {
      state.waitingForCorrection = true
    },
    stopWaitingForCorrection: state => {
      state.waitingForCorrection = false
    }
  },

  actions: {
    editInputText: (context, payload) => {
      context.commit('editInputText', payload)
    },
    applyCorrection: ({state, commit}, {correction, index}) => {
      var sentence = state.outputData.map((e,i) => {
        return ((i == index) ? correction : e.name);
      }).join("");
      commit('applyCorrection',{correction, index})
      commit('editInputText', sentence)
    },
    updateOutputData: (context, payload) => {
      context.commit('updateOutputData', payload)
    },
    fileIsLoaded: context => {
      context.commit('fileIsLoaded')
    },
    sendInputTextToEngine: context => {
      // const formData = new FormData()
      console.log(context.getters.inputText)

      axios.post('http://localhost:8000/search/', {
        queryText: context.getters.inputText,
        modelType: context.getters.correctionModel
      }).then(function (response) {
        // handle success
        console.log(response)
        console.log(response.data)
        context.commit('stopWaitingForCorrection')
        context.commit('updateOutputData', response.data)
      })
        .catch(function (response) {
        // handle error
          console.log(response)
        })
    }
  }
})
