<template>
  <v-container fluid
    class="fill-height"
  >
    <v-row no-gutters justify="center">
      <v-col cols="12">

        <v-card outlined class="flex-grow-1">
          <v-toolbar dark flat dense color="primary">
            <v-toolbar-title>通知</v-toolbar-title>
          </v-toolbar>

          <v-data-table fixed-header
            :mobile-breakpoint="300"
            :headers="headers"
            :items="notifications"
            :no-data-text="noDataText"
            :items-per-page="50"
            :footer-props="{
              itemsPerPageOptions: [ 10, 50, 100, 500, -1 ],
              itemsPerPageAllText: '全部',
              itemsPerPageText: '每頁數量',
              showCurrentPage: true
            }"
            height="67vh"
            item-key="time"
            class="elevation-1"
          >
            <template v-slot:item.read="{ item }">
              <v-icon>{{ item.read ? 'mdi-eye-check-outline' : 'mdi-eye' }}</v-icon>
            </template>
            <template v-slot:item.time="{ item }">
              {{ timeFormat(item.time) }}
            </template>
          </v-data-table>
        </v-card>

      </v-col>
    </v-row>
  </v-container>
</template>

<script>  
export default {

  data () {
    return {

      noDataText: '您目前沒有任何通知。',

      notifications: [],

      headers: [
        { text: '(未完成功能)', sortable: false, value: 'read' },
        { text: '時間', sortable: false, value: 'time' },
        { text: '內容', sortable: false, value: 'content' }
      ]
    }
  },
  
  beforeMount () {
    if (this.isLogin) {
      this.getNotifications()
    }
    else {
      this.$router.push({name: 'login'})
    }
  },

  props: ['isLogin'],

  methods: {

    timeFormat (time) {
      var tmp = new Date(time * 1000)
      var year = tmp.getFullYear()
      var month = '0' + ( tmp.getMonth() + 1 )
      var date = '0' + tmp.getDate()
      var hour = '0' + tmp.getHours()
      var min = '0' + tmp.getMinutes()
      var sec = '0' + tmp.getSeconds()
      time = year + '/' + month.substr(-2) + '/' + date.substr(-2) + ' - ' + hour.substr(-2) + ':' + min.substr(-2) + ':' + sec.substr(-2)
      return time
    },
    
    getNotifications () {
      this.$http.get(`/api/profile/notifications`)
        .then((res) => {
          this.notifications = res.data.data
        })
        .catch((err) => {
          console.log('err: ', err)
        })
    }

  }
  
}
</script>

<style></style>
