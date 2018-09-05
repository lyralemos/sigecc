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
    updateDesafios () {
      this.$http.get('/api/v1/desafio/grupo', { headers: {'X-No-Loading': 'true'} })
        .then((response) => {
          var resolvidos = JSON.stringify(response.data.desafios)
          var resolvidosLocal = JSON.parse(localStorage.getItem('resolvidos'))

          this.$global.resolvidos = JSON.parse(resolvidos)

          if (resolvidosLocal && this.$global.resolvidos.length !== resolvidosLocal.length) {
            this.showNotification()
          }
          localStorage.setItem('resolvidos', resolvidos)
        })
    },
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
    },
    showPopup () {
      this.closeNotification()
      var popup = document.getElementsByClassName('popup-wrapper')
      popup[0].classList.add('show')
      document.body.classList.add('popup')
    },
    closePopup () {
      var popup = document.getElementsByClassName('popup-wrapper')
      popup[0].classList.remove('show')
      document.body.classList.remove('popup')
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
