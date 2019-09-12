<template>

  <div class="fileCorrectionView">
    <img alt="File txt logo" src="../assets/file_txt.png" width="128px">
    <FileUpload msg="Here you can input a file for correction"/>
  </div>
</template>

<script>
import FileUpload from '@/components/FileUpload.vue'

export default {
  name: 'fileCorrectionView',
  components: {
    FileUpload
  }
}
</script>
