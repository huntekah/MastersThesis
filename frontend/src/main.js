import Vue from 'vue'
import vuetify from '@/plugins/vuetify'
import App from './App.vue'
import router from './router'
// import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import { store } from './store/store'

Vue.config.productionTip = false


new Vue({
  router,
  render: h => h(App),
  store: store,
  vuetify
}).$mount('#app')
