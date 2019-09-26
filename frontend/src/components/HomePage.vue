<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed hendrerit et tortor at congue.
       Aliquam congue <a href="/" target="_blank" rel="noopener">pharetra</a> consectetur. Sed semper.
      
    </p>
    <h3> Paper on Oddballness &#x1F5B9;</h3>
    <ul>
      <li><a href="https://zpjn.wmi.amu.edu.pl/zespol/filip-gralinski/" target="_blank" rel="noopener">oddballness.pdf</a></li>
    </ul>
    <h3> Official repo <a href="https://github.com/huntekah/MastersThesis" target="_blank" rel="noopener"><GitHubIcon/></a></h3>
    <ul>
      <li><a href="https://github.com/huntekah/MastersThesis/wiki" target="_blank" rel="noopener">Docs</a></li>
      <li><a href="https://github.com/huntekah/MastersThesis/issues" target="_blank" rel="noopener">Issues</a></li>
      <li><a href="https://github.com/huntekah/MastersThesis/blob/master/README.md" target="_blank" rel="noopener">Readme</a></li>
    </ul>
    <h3>Contribute &#128176;</h3>
    <ul>
      <li><a href="https://patronite.pl/" target="_blank" rel="noopener">Patronite</a></li>
    </ul>
  </div>
</template>

<script>
import GitHubIcon from '@/components/GitHubIcon.vue'

export default {
  name: 'HomePage',
  props: {
    msg: String
  },
  components: {
    GitHubIcon
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
