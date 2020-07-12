<template>
  <v-container fluid
    class="fill-height"
  >
    <!-- Cancel Take Confirm 遮罩 -->
    <v-overlay absolute v-if="cancelConfirm">
      <v-card outlined light>
        <v-toolbar dark flat dense
          color="primary"
        >
          <v-toolbar-title centered>確認</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <div class="subtitle-1 text--primary">
            請問您是否確定您要取消：<br>
            代碼：<b>{{ targetCourse.serialNo }}</b><br>
            名稱：<b>{{ targetCourse.name }}</b><br>
            時間：<b>{{ targetCourse.timeInfo }}</b>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-row justify="space-around">
            <v-col cols="auto" class="pa-0"><v-btn @click="cancelTake">是</v-btn></v-col>
            <v-col cols="auto" class="pa-0"><v-btn @click="cancelConfirm=false">否</v-btn></v-col>
          </v-row>
        </v-card-actions>
      </v-card>
    </v-overlay>

    <!-- cancel result 遮罩 -->
    <v-overlay absolute :value="cancelResult">
      <v-row v-if="cancelResult == 1" justify="center">
        <v-col cols="auto">
          <v-progress-circular indeterminate size="64"/>
        </v-col>
      </v-row>
      <v-row v-if="cancelResult == 1" justify="center">
        <v-col cols="auto" class="headline">取消中...</v-col>
      </v-row>
      <v-card outlined light
        v-if="cancelResult == 2 || cancelResult == 3"
        width="250px"
      >
        <v-toolbar dark flat dense color="primary">
          <v-toolbar-title centered>訊息</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <div v-if="cancelResult == 2" class="subtitle-1 text--primary">
            <b>成功。</b>
          </div>
          <div v-else class="subtitle-1 text--primary">
            <b>失敗。</b><br>
            這可能是 bug 導致的，<br>
            也可能是因為非法操作。<br>
            請將詳細情況告知開發者～
          </div>
        </v-card-text>
        <v-card-actions>
          <v-row justify="center"><v-col cols="auto" class="pa-0">
            <v-btn @click="$emit('closeCancelResult')">我知道了</v-btn>
          </v-col></v-row>
        </v-card-actions>
      </v-card>
    </v-overlay>

    <v-row no-gutters justify="center">
      <v-col cols="12">

        <v-card outlined class="flex-grow-1">
          <v-toolbar dark flat dense color="primary">
            <v-toolbar-title>搶課清單</v-toolbar-title>
          </v-toolbar>

          <v-data-table show-expand fixed-header
            :mobile-breakpoint="300"
            :headers="headers"
            :items="takings"
            :no-data-text="noDataText"
            :items-per-page="50"
            :footer-props="{
              itemsPerPageOptions: [ 10, 50, 100, 500, -1 ],
              itemsPerPageAllText: '全部',
              itemsPerPageText: '每頁數量',
              showCurrentPage: true
            }"
            height="67vh"
            item-key="applyTime"
            class="elevation-1"
          >
            <template v-slot:item.status="{ item }">
              <v-icon :color="statusToColor(item.status)">{{ statusToIcon(item.status) }}</v-icon>
            </template>
            <template v-slot:item.cancel="{ item }">
              <v-btn outlined icon :disabled="item.status != 0" @click="cancelTakeConfirm(item)">
                <v-icon>mdi-account-remove</v-icon></v-btn>
            </template>
            <template v-slot:expanded-item="{ headers, item }">
              <td :colspan="headers.length" class="pa-3">
                <b>課程領域：</b> {{ domainToText(item.domain) }}<br>
                <b>登記時間：</b> {{ timeFormat(item.applyTime) }}<br>
                <b>終止時間：</b> {{ item.revokeTime == null ? '尚未結束' : timeFormat(item.revokeTime) }}
              </td>
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

      noDataText: '您尚未登記過任何搶課申請。',

      takings: [],
      targetCourse: null,
      cancelConfirm: false,

      headers: [
        { text: '結果', sortable: false, value: 'status' },
        { text: '代碼', value: 'serialNo' },
        { text: '課程名稱', value: 'name' },
        { text: '取消', align: 'center', sortable: false, value: 'cancel' },
        { text: '', value: 'data-table-expand' }
      ]
    }
  },
  
  beforeMount () {
    if (this.isLogin) {
      this.getTakings()
      // console.log(this.userData)
    }
    else {
      this.$router.push({name: 'login'})
    }
  },

  props: ['isLogin', 'cancelResult'],

  watch: {
    cancelResult () {
      if (this.cancelResult == 2) {
        var i
        for (i = 0; i < this.takings.length; i++) {
          if (this.targetCourse.serialNo == this.takings[i].serialNo && this.takings[i].status == 0) {
            this.takings[i].status = 2
            this.takings[i].revokeTime = Date.now() / 1000
            break
          }
        }
        this.targetCourse = null
      }
      else if (this.cancelResult == 3) this.targetCourse = null
    }
  },

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
    
    getTakings () {
      this.$http.get(`/api/profile/takings`)
        .then((res) => {
          this.takings = res.data.data
        })
        .catch((err) => {
          console.log('err: ', err)
        })
    },

    statusToColor (status) {
      if (status==0) return 'yellow darken-2'
      else if (status==1) return 'light-green'
      else return 'red darken-1'
    },

    statusToIcon (status) {
      if (status==0) return 'mdi-help-box'
      else if (status==1) return 'mdi-checkbox-marked'
      else return 'mdi-close-box'
    },

    domainToText (domain) {
      if (domain == '') return '無'
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
    },

    cancelTakeConfirm (course) {
      this.targetCourse = course
      this.cancelConfirm = true
    },

    cancelTake () {
      this.cancelConfirm = false
      this.$emit('cancelTake', this.targetCourse)
    }

  }
  
}
</script>

<style></style>
