<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/hand_written.png" width="128px">
    <HelloWorld msg="Welcome to Karol Vue.js App"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'home',
  components: {
    HelloWorld
  }
}
</script>
