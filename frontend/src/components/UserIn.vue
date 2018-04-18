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
          <button class="button is-danger" v-on:click="doAuth">Login</button>
        </b-field>
      </section>
    </section>
  </section>
</template>

<script>
import Vue from 'vue'

export default {
  name: 'UserIn',
  data () {
    return {
      username: undefined,
      password: undefined
    }
  },
  methods: {
    doAuth: function () {
      Vue.axios
        .post(`/api/users/in/`, {
          username: this.username,
          password: this.password
        })
        .then((response) => {
          if (response.status === 200) {
            Vue.localStorage.set('jwt_token', response.data.token)
            this.$router.push({name: 'plans'})
          }
        })
    }
  }
}
</script>
