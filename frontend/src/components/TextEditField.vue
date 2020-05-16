<template>
<v-app height="100%">
  <div class="container">
    <div class="row">
      <div class="col">
        <CheckTextButton />
      </div>
    </div>
    <div class="row">
      <div class="col-lg-6">
        <div class="input-group shadow">
          <textarea class="form-control" :value="inputText" @input="updateInputText" aria-label="textarea" rows="10" style="height:100%;"></textarea>
        </div>
      </div>
      <div class="col-lg-6">
        <!-- {{inputText}} -->

        <!-- show the corrections -->
        <v-menu v-model="correctionsListIsVisible" :absolute="true" :position-x="menu_x" :position-y="menu_y" transition="slide-y-transition">
          <v-list dense>
            <v-list-item v-for="(correction, index) in correctionsListItems" :key="index" @click="applyCorrection(correction)">
              <v-list-item-content>
                <v-list-item-title>
                  {{correction}}
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-menu>
        <!-- Show list of words -->
        <div class="shadow outputField">
          <template v-for="(object, index) in outputData">
            <div @click="toggleCorrectionsList(object, index, $event)" :class="{'underlined': object.underlined}" style="display: inline-block;">
              <!-- Vue eats up spaces, so -->
              <template v-for="(letter, i) in object.name">
                <span v-if="! /\s/.test(letter)">{{ letter }}</span>
                <span v-else>&nbsp;</span>
              </template>

            </div>
          </template>
        </div>


      </div>
    </div>
  </div>
</v-app>
</template>

<script>
import axios from 'axios';
import {
  format
} from 'path';
import CheckTextButton from '@/components/CheckTextButton.vue'


export default {
  name: 'FileUpload',
  props: {
    msg: String
  },
  components: {
    CheckTextButton
  },
  data() {
    return {
      correctionsListIsVisible: false,
      correctionsListItems: [],
      activeIndex: -1,
      menu_x: 0,
      menu_y: 0,
    }
  },
  methods: {
    updateInputText(e) {
      this.$store.commit('editInputText', e.target.value);
    },
    sendInputTextToEngine() {
      this.$store.dispatch('sendInputTextToEngine');
    },
    toggleCorrectionsList(object, index, e) {
      e.preventDefault()
      if (object.underlined) {
        this.correctionsListItems = object.corrections
        this.activeIndex = index
        this.correctionsListIsVisible = false

        this.menu_x = e.clientX
        this.menu_y = e.clientY
        //nice animation of closing window.
        this.$nextTick(() => {
          this.correctionsListIsVisible = true
        })
      } else {
        this.activeIndex = {}
      }
    },
    applyCorrection(correction) {
      var index = this.activeIndex
      this.$store.dispatch('applyCorrection', {
        correction,
        index
      })
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

.outputField {
  padding: .375rem .75rem;
  height: 100%;
  text-align: left;
}

.underlined {
  text-decoration: underline dotted red;
  background-color: rgba(255, 0, 0, 0.1);
  padding: 0px 0px;
  cursor: pointer;
  border-radius: 5% / 25%;
}

.flex {
  display: flex;
  flex: 0 0;
}
</style>
