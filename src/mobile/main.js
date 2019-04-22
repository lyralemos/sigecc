import Vue from 'vue'
import App from './App.vue'
import router from './router'
import 'materialize-css/dist/css/materialize.min.css'
import '@/assets/mobile.css'

Vue.config.productionTip = false

const global = new Vue({
  data: {
    loading: false,
    competicao: false,
    colaboracao: false,
    liberado: false,
    grupo: null,
    desafios: [],
    resolvidos: []
  }
})

const GlobalPlugin = {
  install (Vue) {
    Vue.prototype.$global = global
  }
}

Vue.mixin({
  methods: {
    showNotification () {
      var notification = document.getElementsByClassName('notification')
      notification[0].classList.add('show')
      window.setTimeout(function () {
        this.closeNotification()
      }.bind(this), 5000)
    },
    closeNotification () {
      var notification = document.getElementsByClassName('notification')
      notification[0].classList.remove('show')
    }
  }
})

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
