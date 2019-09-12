<template>
<form @submit.prevent="sendFile" enctype="multipart/form-data">
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
  <!-- </div> -->
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
      file: ""
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
      try{
      fileReader.readAsText(this.file);
        fileReader.onloadend = function(){
          console.log(fileReader.result);
          this.$router.push({ name: '/',
                              params: {inputText: fileReader.result
                            }});
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
