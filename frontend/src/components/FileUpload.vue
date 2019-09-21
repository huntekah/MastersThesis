<template>
  <div class="container">
    <form v-show="isFileFormVisible()" @submit.prevent="sendFile" enctype="multipart/form-data">
      <div class="input-group shadow-lg p-3 mb-5 bg-white rounded">
        <!-- <div class="form-group"> -->
        
          <label 
          for="fileUpload" 
          class="">{{msg}}</label>
          <input 
            type="file" 
            ref="file"
            id="fileUpload" 
            class="form-control-file .form-control-lg" 
            @change="selectFile" />
              <button type="submit" class="btn btn-primary">
                Submit
              </button>
      </div>
    </form>
    <div v-show="isFileEditorVisible()">
      TEST
      {{fileContent}}
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
      file: "",
      fileIsLoaded: false,
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
      console.log("TEST");
      console.log("1" + this.fileIsLoaded);
                      console.log("21" + this.isFileEditorVisible());
                console.log("31" + this.isFileFormVisible());
      try{
        fileReader.readAsText(this.file);
        fileReader.onloadend = (e) =>{
          this.fileContent = fileReader.result;
          this.fileIsLoaded = true;
                console.log("14" + this.isFileEditorVisible());
                console.log("51" + this.isFileFormVisible());
          // this.$router.push({ name: '/',
          //                     params: {inputText: fileReader.result
          //                   }});
        }
      } catch (err) {
        console.log(err)
      }

                console.log("61" + this.isFileEditorVisible());
                console.log("17" + this.isFileFormVisible());

      // formData.append('file',this.file);

      // try {
      //   axios.post('/TODO', formData);
      // } catch(err) {
      //   console.log(err);
      // }
    },
    isFileFormVisible(){
      return this.fileIsLoaded != true;
    },
    isFileEditorVisible(){
      return !this.isFileFormVisible();
    }
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
