import Vue from 'vue'
import Router from 'vue-router'
import Resource from 'vue-resource'
import Home from '@/mobile/components/Home.vue'
import Espera from '@/mobile/components/Espera.vue'
import Perfil from '@/mobile/components/Perfil.vue'
import Pergunta from '@/mobile/components/Pergunta.vue'
import Login from '@/mobile/components/Login.vue'
import Logout from '@/mobile/components/Logout.vue'

Vue.use(Router)
Vue.use(Resource)

Vue.http.interceptors.push((request, next) => {
  var token = localStorage.getItem('user-token')
  if (token) {
    request.headers.set('Authorization', 'Token ' + token)
  }

  var loading = request.headers.get('X-No-Loading')
  if (loading !== 'true') {
    Vue.prototype.$global.loading = true
  }

  next((response) => {
    Vue.prototype.$global.loading = false
  })
})

export default new Router({
  base: '/dashboard/',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/espera',
      name: 'Espera',
      component: Espera
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/logout',
      name: 'Logout',
      component: Logout
    },
    {
      path: '/perfil',
      name: 'Perfil',
      component: Perfil
    },
    {
      path: '/pergunta',
      name: 'Pergunta',
      component: Pergunta
    }
  ]
})
