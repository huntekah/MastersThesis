<template>

  <div class="fileCorrectionView">
    <div class="d-flex justify-content-center">
      <img alt="File txt logo" src="../assets/file_txt.png" width="128px">
      </div>
    <FileUpload v-show="isFileFormVisible()"/>
    <TextEditField v-show="isFileEditorVisible()"/>
    <div v-show="isFileLoading()">
      <div class="d-flex justify-content-center">
        <div class="spinner-border" role="status">
          <span class="sr-only">Loading...</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FileUpload from '@/components/FileUpload.vue';
import TextEditField from '@/components/TextEditField.vue';

export default {
  name: 'fileCorrectionView',
  components: {
    FileUpload,
    TextEditField
  },
  data(){
    return {
    }
  },
  methods: {
    isFileFormVisible(){
      return this.fileIsLoaded != true;
    },
    isFileEditorVisible(){
      return !this.isFileFormVisible();
    },
    isFileLoading(){
      return this.loadingFile;
    }
  },
  computed: {
    loadingFile(){
      return this.$store.state.loadingFile;
    },
    fileIsLoaded(){
      return this.$store.state.fileIsLoaded;
    }
  }
}
</script>
