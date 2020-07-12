import Vue from 'vue'
import App from './App.vue'

import VueResource from 'vue-resource'
import VueCookies from 'vue-cookies'

import router from './router'
import vuetify from './plugins/vuetify';

Vue.use(VueResource)
Vue.use(VueCookies)
Vue.config.productionTip = false

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')