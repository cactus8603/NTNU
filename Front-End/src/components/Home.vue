<template>
  <v-container fluid>
    <v-row no-gutters
      align="start"
      justify="center"
    >
      <v-col
        cols="12"
      >
        <v-card outlined>
          <v-toolbar dark flat dense
            color="primary"
          >
            <v-toolbar-title>個人資料</v-toolbar-title>
          </v-toolbar>

          <!-- User's data in cookies -->
          <v-row no-gutters
            v-for="data in userData"
            :key="data.key"
          >
            <v-col
              cols="4"
              xs="4"
              sm="3"
              md="2"
              lg="2"
              xl="2"
            >
              <v-card outlined tile
                class="pa-3"
              >
                {{ data.key }}
              </v-card>
            </v-col>
            <v-card outlined tile
              class="pa-3 flex-grow-1"
            >
              {{ data.value }}
            </v-card>
          </v-row>

          <!-- User's first login time & last login time -->
          <v-row no-gutters
            v-for="time in times"
            :key="time.key"
          >
            <v-col
              cols="4"
              xs="4"
              sm="3"
              md="2"
              lg="2"
              xl="2"
            >
              <v-card outlined tile
                class="pa-3"
              >
                {{ time.key }}
              </v-card>
            </v-col>
            <v-card outlined tile
              class="pa-3 flex-grow-1"
            >
              {{ timeFormat(time.value) }}
            </v-card>
          </v-row>

        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>  
export default {

  data () {
    return {
      times: [],
      records: [],

      headers: [
        { text: '狀態', align: 'left', value: 'status' },
        { text: '代碼', value: 'serialNo' },
        { text: '課程名稱', value: 'courseName' },
        { text: '領域', value: 'domain' },
        { text: 'Cancel', value: 'cancel' }
      ]
    }
  },
  
  beforeMount () {
    if (this.isLogin) {
      this.getTimes()
      // this.getRecords()
      // console.log(this.userData)
    }
    else {
      this.$router.push({name: 'login'})
    }
  },

  props: ['isLogin', 'userData'],
  
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
    
    getTimes () {
      this.$http.get(`/api/profile/times`)
        .then((res) => {
          this.times = res.data.data
        })
        .catch((err) => {
          console.log('err: ', err)
        })
    },

    getRecords () {
      this.$http.get(`/api/profile/records`)
        .then((res) => {
          this.records = res.data.data
        })
        .catch((err) => {
          console.log('err: ', err)
        })
    },

    statusToIcon (status) {
      if (status==0) return 'mdi-help-box'
      else if (status==1) return 'mdi-checkbox-marked'
      else return 'mdi-close-box'
    },

    domainToText (domain) {
      if (domain == '') return 'None'
      else if (domain == '00UG') return '語言與文學'
      else if (domain == '01UG') return '藝術與美感'
      else if (domain == '02UG') return '哲學思維與道德推理'
      else if (domain == '03UG') return '公民素養與社會探究'
      else if (domain == '04UG') return '歷史與文化'
      else if (domain == '05UG') return '數學與邏輯思維'
      else if (domain == '06UG') return '科學與生命'
      else if (domain == '07UG') return '第二外語'
      else if (domain == '08UG') return '生活技能'
      else if (domain == '09UG') return '自主學習'
    }

  }
  
}
</script>

<style></style>