<template>

  <div class="textCorrectionView">
    <img alt="Hand writing" src="../assets/hand_written.png" width="128px">
    <TextEditField msg="This is a loevly day!"/>
  </div>
</template>

<script>
import TextEditField from '@/components/TextEditField.vue'

export default {
  name: 'textCorrectionView',
  components: {
    TextEditField
  }
}
</script>
<style>
.textCorrectionView{
  text-align: center;
}
</style>
