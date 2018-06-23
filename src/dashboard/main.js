import Vue from 'vue'
import App from './App.vue'
import router from './router'

Vue.config.productionTip = false

const global = new Vue({data: {loading: false}})

const GlobalPlugin = {
  install (Vue) {
    Vue.prototype.$global = global
  }
}

Vue.use(GlobalPlugin)

void new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
