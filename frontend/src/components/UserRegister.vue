<template>
  <section class="container">
    <section class="columns is-mobile">
      <section class="column">
        <b-field label="Username">
            <b-input v-model="username"></b-input>
        </b-field>
        <b-field label="Password">
            <b-input v-model="password" type="password"></b-input>
        </b-field>
        <b-field>
          <button class="button is-success" v-on:click="doRegister">Register</button>
        </b-field>
        <b-field>
          <button class="button is-warning" v-on:click="routeToLogin">Got Credentials?</button>
        </b-field>
      </section>
    </section>
  </section>
</template>

<script>
import Vue from 'vue'

export default {
  name: 'UserRegister',
  data () {
    return {
      username: undefined,
      password: undefined
    }
  },
  methods: {
    doRegister: function () {
      Vue.axios
        .post(`/api/users/register/`, {
          username: this.username,
          password: this.password
        })
        .then((response) => {
          if (response.status === 201) {
            this.$router.push({name: 'user-in'})
          }
        })
    },
    routeToLogin: function () {
      this.$router.push({name: 'user-in'})
    }
  }
}
</script>
