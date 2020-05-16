<template>
        <div class="btn-group btn-block"
        role="group"
        aria-label="Button group with nested dropdown">
          <button
            type="button"
            class="btn btn-outline-success btn-lg btn-block"
            @click="sendInputTextToEngine()">
<span v-show="isWaitingForCorrection()" class="spinner-border" style="width: 1.5rem; height: 1.5rem;" role="status" aria-hidden="true"></span>
Check the text
          </button>

          <div class="btn-group" role="group">
            <button id="btnGroupDropChooseModel"
            type="button"
            class="btn btn-outline-secondary dropdown-toggle"
            data-toggle="dropdown"
            aria-haspopup="true"
            aria-expanded="false">
              Choose Model
            </button>
            <div class="dropdown-menu dropdown-menu-right" aria-labelledby="btnGroupDropChooseModel">
              <a v-for="model in models"
              class="dropdown-item"
              v-on:click="setModel(model.name)"
              href="#">
                {{model.display_text}}
              </a>

            </div>
          </div>
        </div>
</template>

<script>
import { format } from 'path';

export default {
  name: 'CheckTextButton',
  data() {
    return {
      models: [
        {
          display_text: "Fast response",
          name: "left-to-right"
        },
        {
          display_text: "Slow, but powerful!",
          name: "bidirectional"
        },
      ]
    }
  },
  methods: {
    sendInputTextToEngine() {
      this.$store.commit('waitForCorrection')
      this.$store.dispatch('sendInputTextToEngine');
    },
    setModel(name) {
      this.$store.commit('setModel', name);
    },
    isWaitingForCorrection() {
      return this.waitingForCorrection;
    }
  },
  computed: {
    waitingForCorrection (){
      return this.$store.state.waitingForCorrection;
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
