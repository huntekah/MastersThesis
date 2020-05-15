<template>
        <div class="btn-group btn-block"
        role="group"
        aria-label="Button group with nested dropdown">
          <button
            type="button"
            class="btn btn-outline-success btn-lg btn-block"
            @click="sendInputTextToEngine()">
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
              <a class="dropdown-item" href="#">Fast response </a>
              <a class="dropdown-item" href="#">Slow, but powerfull!
              </a>
            </div>
          </div>
        </div>
</template>

<script>
import { format } from 'path';

export default {
  name: 'CheckTextButton',
  methods: {
    sendInputTextToEngine(){
      this.$store.dispatch('sendInputTextToEngine');
    },
    // TODO - functions for clicking the right model
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
