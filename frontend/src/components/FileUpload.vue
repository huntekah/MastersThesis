<template>
  <div class="container">

    <form @submit.prevent="sendFile"
    enctype="multipart/form-data">
      <div class=" input-group shadow-lg p-3 mb-5 bg-white rounded">
        <!-- <div class="form-group"> -->

          <label
          for="fileUpload"
          class="">Choose an input file for correction:</label>
          <br/>
          <input
            style="display: none"
            type="file"
            ref="file"
            id="fileUpload"
            class="form-control-file .form-control-lg"
            @change="selectFile" />
          <div class='col d-flex align-items-center'>
            <button type="button" @click="$refs.file.click()" class="btn btn-outline-success">
              <img v-show="this.file==''" alt="Choose a file" src="@/assets/file_txt.png" width="32px">
              <span v-show="this.file!=''">{{this.file.name}}</span>
            </button>
          </div>
            <div class='col d-flex align-items-center'>
            <button type="submit" class="btn btn-primary">
                Edit!
            </button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import { format } from 'path';

export default {
  name: 'FileUpload',
  props: {},
  data(){
    return {
      file: "",
      fileContent: "You have not loaded a file yet!"
    }
  },
  methods: {
    selectFile() {
      this.file = this.$refs.file.files[0];
    },
    sendFile() {
      const formData = new FormData();
      const fileReader = new FileReader();
      try{
        fileReader.readAsText(this.file);
        fileReader.onloadend = (e) =>{
          var fileContent = fileReader.result;
          this.$store.dispatch('fileIsLoaded');
          this.$store.dispatch('editInputText', fileContent);
        }
      } catch (err) {
        console.log(err)
      }

      // formData.append('file',this.file);

      // try {
      //   axios.post('/TODO', formData);
      // } catch(err) {
      //   console.log(err);
      // }
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
