import Vue from 'vue'
import Buefy from 'buefy'
import axios from 'axios'
import Router from 'vue-router'
import VueAxios from 'vue-axios'

import 'buefy/lib/buefy.css'

import Plans from '@/components/Plans'
import UserIn from '@/components/UserIn'
import VueLocalStorage from 'vue-localstorage'
import UserRegister from '@/components/UserRegister'

Vue.use(Buefy)
Vue.use(Router)
Vue.use(VueLocalStorage)
Vue.use(VueAxios, axios)

function redirectToAuth (next) {
  const jwtToken = Vue.localStorage.get('jwt_token', undefined, String)
  if (jwtToken) {
    next()
  } else {
    next({ name: 'user-in' })
  }
}

function redirectToPlans (next) {
  const jwtToken = Vue.localStorage.get('jwt_token', undefined, String)
  if (jwtToken) {
    next({ name: 'plans' })
  } else {
    next()
  }
}

export default new Router({
  routes: [
    {
      path: '/user/in/',
      name: 'user-in',
      component: UserIn,
      beforeEnter: function (to, from, next) {
        redirectToPlans(next)
      }
    },
    {
      path: '/user/register/',
      name: 'user-register',
      component: UserRegister,
      beforeEnter: function (to, from, next) {
        redirectToPlans(next)
      }
    },
    {
      path: '/plans',
      name: 'plans',
      component: Plans,
      beforeEnter: function (to, from, next) {
        redirectToAuth(next)
      }
    }
  ]
})
