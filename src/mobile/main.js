import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Resource from 'vue-resource'
import 'materialize-css/dist/css/materialize.min.css'

Vue.config.productionTip = false

const global = new Vue({data: {loading: false}})

const GlobalPlugin = {
  install (Vue) {
    Vue.prototype.$global = global
  }
}

Vue.use(GlobalPlugin)
Vue.use(Resource)

Vue.http.interceptors.push((request, next) => {
  Vue.prototype.$global.loading = true
  next((response) => {
    Vue.prototype.$global.loading = false
  })
})

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
