import Vue from 'vue'
import Router from 'vue-router'

import Home from '@/dashboard/components/Home.vue'
import Alunos from '@/dashboard/components/Alunos.vue'
import Grupos from '@/dashboard/components/Grupos.vue'
import Questoes from '@/dashboard/components/Questoes.vue'
import Modulos from '@/dashboard/components/Modulos.vue'

Vue.use(Router)

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
      path: '/grupos',
      name: 'Grupos',
      component: Grupos
    },
    {
      path: '/questoes',
      name: 'Questões',
      component: Questoes
    },
    {
      path: '/modulos',
      name: 'Módulos',
      component: Modulos
    }
  ]
})
