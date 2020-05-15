<template>
  <div class="home">
    <img alt="Hand writing" src="@/assets/hand_written.png" height="128px">
    <HomePage msg="Improve your writing with GPT2"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HomePage from '@/components/HomePage.vue'

export default {
  name: 'home',
  components: {
    HomePage
  }
}
</script>


<style>
.home {
  text-align: center;
}
</style>
