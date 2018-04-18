<template>
  <div id="app" class="container">
    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <h1><strong>Plannr</strong></h1>
      </div>
      <div class="navbar-end" v-show="isLoggedIn()">
        <button class="button is-danger" v-on:click="logout">Logout</button>
      </div>
    </nav>
    <router-view/>
  </div>
</template>

<script>
import Vue from 'vue'

export default {
  name: 'App',
  methods: {
    logout: function () {
      Vue.localStorage.remove('jwt_token')
      this.$router.push({name: 'user-in'})
    },
    isLoggedIn: function () {
      const jwtToken = Vue.localStorage.get('jwt_token')
      return jwtToken !== undefined && jwtToken !== null
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
