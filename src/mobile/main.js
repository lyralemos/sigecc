import Vue from 'vue'
import App from './App.vue'
import router from './router'
import 'materialize-css/dist/css/materialize.min.css'

Vue.config.productionTip = false

const global = new Vue({
  data: {
    loading: false,
    competicao: false,
    colaboracao: false,
    liberado: false
  }
})

const GlobalPlugin = {
  install (Vue) {
    Vue.prototype.$global = global
  }
}

Vue.use(GlobalPlugin)

void new Vue({
  el: '#app',
  computed: {
    loading () {
      return this.$global.loading
    }
  },
  router,
  components: { App },
  template: '<App/>'
})
