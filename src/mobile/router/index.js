import Vue from 'vue'
import Router from 'vue-router'
import Resource from 'vue-resource'
import Home from '@/mobile/components/Home.vue'
import Perfil from '@/mobile/components/Perfil.vue'

Vue.use(Router)
Vue.use(Resource)

export default new Router({
  base: '/dashboard/',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/perfil',
      name: 'Perfil',
      component: Perfil
    }
  ]
})
