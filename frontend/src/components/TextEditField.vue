<template>
  <div class="container">
    <div class="row">
      <div class="col">
      <button
        type="button"
        class="btn btn-outline-success btn-lg btn-block"
        @click="sendInputTextToEngine()">
        Check the text
      </button>
      </div>
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
        <div class="col-lg-6 flex">
          <!-- {{inputText}} -->
          <v-app>
  <!-- show the corrections -->
            <v-menu v-model="correctionsListIsVisible">
              <v-list dense>
                <v-list-item
                v-for="(correction, index) in correctionsListItems"
                :key="index"
                @click="applyCorrection(correction)" >
                  <v-list-item-content>
                    <v-list-item-title>
                      {{correction}}
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-menu>
  <!-- Show list of words -->
            <div class="flex">
              <template v-for="(object, index) in outputData" class="flex">
                <div
                   @click="toggleCorrectionsList(object, index)"
                   :class="{'underlined': object.underlined}"
                   id="word"
                >
                <!-- Vue eats up spaces, so -->
                <template v-for="(letter, i) in object.name">
                    <span v-if="! /\s/.test(letter)">{{ letter }}</span>
                    <span v-else>&nbsp;</span>
                </template>

              </div>
              </template>
            </div>
          </v-app>

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
    return {
      correctionsListIsVisible: false,
      correctionsListItems: [],
      activeIndex: -1,
    }
  },
  methods: {
    updateInputText (e) {
      this.$store.commit('editInputText', e.target.value);
    },
    sendInputTextToEngine(){
      this.$store.dispatch('sendInputTextToEngine');
    },
    toggleCorrectionsList (object, index) {
      if (object.underlined) {
        this.correctionsListItems = object.corrections
        this.activeIndex = index
        this.correctionsListIsVisible = true
      }
      else {
        this.activeIndex = {}
      }
    },
    applyCorrection (correction) {
      var index = this.activeIndex
      this.$store.dispatch('applyCorrection',{correction, index})
    }
  },
  computed: {
    inputText() {
      return this.$store.getters.inputText;
    },
    outputData() {
      return this.$store.getters.outputData;
    },
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
 float: left;
}
.underlined {
  text-decoration: underline dotted red;
  background-color: rgba(255, 0, 0, 0.1);
  padding: 0px 4px;
  cursor: pointer;
  border-radius: 5% / 25%;
}
.flex {
  display: flex;
  flex: 0 0;
}
</style>
