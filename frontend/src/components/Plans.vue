<template>
  <section>
    <div class="container">
    <div class="columns is-mobile">
      <div class="column">
        <b-datepicker
          inline
          v-model="date"
          indicators="dots"
          v-on:input="dayTrigger">
        </b-datepicker>
      </div>
      <div class="column" v-if="selectedDate">
        <h1 class="title">{{ selectedDate.toLocaleDateString(locale, localeOptions) }}</h1>
        <div class="level">
          <div class="level-item">
            <b-field>
              <b-timepicker placeholder="Start time" v-model="newPlanStart"></b-timepicker>
            </b-field>
          </div>
          <div class="level-item">
            <b-field>
              <b-timepicker placeholder="End time" v-model="newPlanEnd"></b-timepicker>
            </b-field>
          </div>
          <div class="level-item">
            <b-field>
              <b-input placeholder="Description" v-model="newPlanDesc"></b-input>
            </b-field>
          </div>
          <div class="level-item">
            <b-field>
              <button class="button is-link is-success" v-on:click="createPlan">+ Plan</button>
            </b-field>
          </div>
        </div>
        <!-- The reason b-table is not used is because of it's limitations for row coloring !-->
        <table class="table" v-show="dayPlans.length > 0">
          <thead>
            <tr>
              <th>Start</th>
              <th>End</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-bind:key="plan.id"
              v-bind:style="{ color: '#fff', background: plan.color}"
              v-for="plan in dayPlans"
              v-on:click="planClicked(plan.id)">
              <td>{{ new Date(plan.start).getHours() }} : {{ new Date(plan.start).getMinutes() }}</td>
              <td>{{ new Date(plan.end).getHours() }} : {{ new Date(plan.end).getMinutes() }}</td>
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

let thisMonth = new Date().getMonth()
let thisYear = new Date().getFullYear()

export default {
  name: 'Plans',
  data () {
    return {
      locale: 'en-US',
      localeOptions: { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' },
      date: new Date(thisYear, thisMonth, 1),
      plans: [],
      dayPlans: [],
      selectedDate: undefined,
      newPlanStart: undefined,
      newPlanEnd: undefined,
      newPlanDesc: undefined
    }
  },
  watch: {
    selectedDate: function (val) {
      this.newPlanStart = this.newPlanEnd = val
      this.dayPlans = partitionPlans(
        this.plans.filter((plan) => {
          return val.getFullYear() === plan.start.getFullYear() &&
            val.getMonth() === plan.start.getMonth() &&
            val.getDate() === plan.start.getDate()
        }), this.getSelectDayMidday()
      ).sort((p1, p2) => p1.start > p2.start)
    }
  },
  mounted () {
    this.fetchPlans(thisYear, thisMonth + 1, undefined)
  },
  methods: {
    fetchPlans: function (year, month, presetDate) {
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

            // Due to API lack of b-datepicker explained in `dayTrigger` method.
            if (presetDate !== undefined) {
              this.selectedDate = presetDate
            }
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

            // Trigger new `dayPlan` attribute computation.
            this.selectedDate = new Date(this.newPlanStart)
          }
        })
    },
    getSelectDayMidday () {
      /**
       * This will be used for interval tree center point.
       */
      const todayDate = this.selectedDate
      const midday = (new Date(todayDate.getFullYear(), todayDate.getMonth(), todayDate.getDate(), 0, 0, 0).getTime() +
        new Date(todayDate.getFullYear(), todayDate.getMonth(), todayDate.getDate(), 23, 59, 59).getTime()) / 2
      return midday
    },
    dayTrigger: function (evt) {
      // Unfortunately b-datepicker does not inform well when current view month changes.
      //  So we have to a bit of hacking to update corresponding plans.
      if (evt.getMonth() === thisMonth && evt.getFullYear() === thisYear) {
        this.selectedDate = evt
      } else {
        thisMonth = evt.getMonth()
        thisYear = evt.getFullYear()
        this.fetchPlans(evt.getFullYear(), evt.getMonth() + 1, evt)
      }
    },
    planClicked: function (evt) {}
  }
}
</script>
