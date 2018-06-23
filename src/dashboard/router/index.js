import Vue from 'vue'
import Router from 'vue-router'
import Resource from 'vue-resource'
import Home from '@/dashboard/components/Home.vue'
import Alunos from '@/dashboard/components/Alunos.vue'
import Questoes from '@/dashboard/components/Questoes.vue'

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
      path: '/alunos',
      name: 'Alunos',
      component: Alunos
    },
    {
      path: '/questoes',
      name: 'Questões',
      component: Questoes
    }
  ]
})
