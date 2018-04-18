import Vue from 'vue'
import Buefy from 'buefy'
import Router from 'vue-router'

import 'buefy/lib/buefy.css'

import Plans from '@/components/Plans'
import UserIn from '@/components/UserIn'
import UserRegister from '@/components/UserRegister'

Vue.use(Buefy)
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/user/in/',
      name: 'user-in',
      component: UserIn
    },
    {
      path: '/user/register/',
      name: 'user-register',
      component: UserRegister
    },
    {
      path: '/plans',
      name: 'plans',
      component: Plans
    }
  ]
})
