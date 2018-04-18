<template>
  <section>
    <div class="container">
    <div class="columns is-mobile">
      <div class="column">
        <b-datepicker
          inline
          v-model="date"
          indicators="dots"
          :events="plans"
          v-on:input="dayTrigger">
        </b-datepicker>
      </div>
      <div class="column">
        <div class="level">
          <div class="level-left">
            <h1 class="title">{{ today }}</h1>
          </div>
          <div class="level-right">
            <b-field label="Start">
              <b-timepicker size="is-small" v-model="newPlanStart"></b-timepicker>
            </b-field>
            <b-field label="End">
              <b-timepicker size="is-small" v-model="newPlanEnd"></b-timepicker>
            </b-field>
            <b-field label="Description">
              <b-input v-model="newPlanDesc"></b-input>
            </b-field>
            <button class="button is-link is-rounded is-success" v-on:click="createPlan">+ Plan</button>
          </div>
        </div>
        <table class="table">
          <thead>
            <tr>
              <th>Start</th>
              <th>End</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            <tr v-bind:key="plan.id" v-bind:style="{ color: '#fff', background: partitionedPlans[plan.id]}" v-for="plan in dayPlans" v-on:click="planClicked(plan.id)">
              <td>{{ plan.start }}</td>
              <td>{{ plan.end }}</td>
              <td>{{ plan.desc }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  </section>
</template>

<script>
import Vue from 'vue'
import partitionPlans from '../utils/plans'

const thisMonth = new Date().getMonth()
const thisYear = new Date().getFullYear()

export default {
  name: 'Plans',
  data () {
    return {
      date: new Date(thisYear, thisMonth, 1),
      today: undefined,
      plans: [],
      dayPlans: undefined,
      monthPlans: undefined,
      partitionedPlans: undefined,
      newPlanStart: undefined,
      newPlanEnd: undefined,
      newPlanDesc: undefined
    }
  },
  mounted () {
    this.fetchPlans(thisYear, thisMonth + 1)
  },
  methods: {
    fetchPlans: function (year, month) {
      Vue.axios
        .get(`/api/plans/?year=${year}&month=${month}`, {
          headers: {
            'Authorization': 'Bearer ' + Vue.localStorage.get('jwt_token', undefined, String)
          }
        })
        .then((response) => {
          if (response.status === 200) {
            this.plans = response.data.map(function (plan) {
              return {
                id: plan.id,
                date: new Date(plan.start),
                start: new Date(plan.start),
                end: new Date(plan.end),
                desc: plan.desc
              }
            })
          }
        })
    },
    createPlan: function () {
      if (this.newPlanStart >= this.newPlanEnd) {
        return
      }

      Vue.axios
        .post('/api/plans/', {
          'start': this.newPlanStart,
          'end': this.newPlanEnd,
          'desc': this.newPlanDesc
        },
        {
          headers: {
            'Authorization': 'Bearer ' + Vue.localStorage.get('jwt_token', undefined, String)
          }
        })
        .then((response) => {
          if (response.status === 201) {
            const addedPlan = response.data
            this.plans.push({
              id: addedPlan.id,
              date: new Date(addedPlan.start),
              start: new Date(addedPlan.start),
              end: new Date(addedPlan.end),
              desc: addedPlan.desc
            })
            console.log(this.plans)
          }
        })
    },
    dayTrigger: function (evt) {
      const todayDate = evt
      this.newPlanStart = this.newPlanEnd = todayDate

      this.dayPlans = this.plans.filter((plan) => {
        return todayDate.getFullYear() === plan.start.getFullYear() &&
              todayDate.getMonth() === plan.start.getMonth() &&
              todayDate.getDate() === plan.start.getDate()
      })

      const midday = (new Date(todayDate.getFullYear(), todayDate.getMonth(), todayDate.getDate(), 0, 0, 0).getTime() +
        new Date(todayDate.getFullYear(), todayDate.getMonth(), todayDate.getDate(), 23, 59, 59).getTime()) / 2
      this.partitionedPlans = partitionPlans(this.dayPlans, midday)
    },
    planClicked: function (evt) {

    }
  }
}
</script>
