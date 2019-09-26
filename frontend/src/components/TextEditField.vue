<template>
  <div class="container">
    <div class="row">
      <button 
        type="button" 
        class="btn btn-outline-success btn-lg btn-block"
        @click="sendInputTextToEngine()">
        Check the text
      </button>
    </div>
    <div class="row">
      <div class="col-lg-6">
        <div class="input-group">
          <textarea 
          class="form-control" 
          :value="inputText" 
          @input="updateInputText" 
          aria-label="textarea"></textarea>
        </div>
      </div>
      <div class="col-lg-6 outputText">
        {{inputText}}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { format } from 'path';

export default {
  name: 'FileUpload',
  props: {
    msg: String
  },
  data(){
    return {}
  },
  methods: {
    updateInputText (e) {
      this.$store.commit('editInputText', e.target.value); 
    },
    sendInputTextToEngine(){
      this.$store.dispatch('sendInputTextToEngine');
    }
  }, 
  computed: {
    inputText() {
      return this.$store.getters.inputText;
    }
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.outputText {
 white-space: pre-wrap;       /* css-3 */
 white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
 white-space: -pre-wrap;      /* Opera 4-6 */
 white-space: -o-pre-wrap;    /* Opera 7 */
 overflow-wrap: anywhere;       /* Internet Explorer 5.5+ */
 word-wrap: break-word;
 word-break: break-all;
}
</style>
