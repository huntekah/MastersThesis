<template>
  <div class="home">
    <img alt="Hand writing" src="@/assets/hand_written.png" width="128px">
    <HomePage msg="Welcome to the possibilities of GPT2 text writing support!"/>
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
 
