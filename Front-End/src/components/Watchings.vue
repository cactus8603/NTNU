<template>
  <v-container fluid
    class="fill-height"
  >
    <v-row no-gutters justify="center">
      <v-col cols="12">

        <v-card outlined class="flex-grow-1">
          <v-toolbar dark flat dense color="primary">
            <v-toolbar-title>關注清單</v-toolbar-title>
          </v-toolbar>

          <v-data-table show-expand fixed-header
            :mobile-breakpoint="300"
            :headers="headers"
            :items="watchings"
            :no-data-text="noDataText"
            :items-per-page="50"
            :footer-props="{
              itemsPerPageOptions: [ 10, 50, 100, 500, -1 ],
              itemsPerPageAllText: '全部',
              itemsPerPageText: '每頁數量',
              showCurrentPage: true
            }"
            height="67vh"
            item-key="serialNo"
            class="elevation-1"
          >
            <template v-slot:item.cancel="{ item }">
              <v-btn outlined icon @click="cancelWatch(item)">
                <v-icon>mdi-star-off</v-icon></v-btn>
            </template>
            <template v-slot:expanded-item="{ headers, item }">
              <td :colspan="headers.length" class="pa-3">
                <b>時間：</b> {{ item.timeInfo }}<br>
                <b>老師：</b> {{ item.teacher }}<br>
                <b>系所：</b> {{ item.vDeptChiabbr }}<br>
                <b>學分：</b> {{ item.credit }}<br>
                <b>備註：</b> {{ item.vComment != '' ? item.vComment : '無' }}<br>
                <b>限制：</b> {{ item.vLimitCourse != '' ? item.vLimitCourse : '無' }}
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

      noDataText: '您尚未關注任何一堂課程。',

      watchings: [],
      targetCourse: null,
      cancelConfirm: false,

      headers: [
        { text: '代碼', value: 'serialNo' },
        { text: '課程名稱', value: 'name' },
        { text: '取消', align: 'center', sortable: false, value: 'cancel' },
        { text: '', value: 'data-table-expand' }
      ]
    }
  },
  
  beforeMount () {
    if (this.isLogin) {
      this.getWatchings()
    }
    else {
      this.$router.push({name: 'login'})
    }
  },

  props: ['isLogin'],

  methods: {
    
    getWatchings () {
      this.$http.get(`/api/profile/watchings`)
        .then((res) => {
          this.watchings = res.data.data
        })
        .catch((err) => {
          console.log('err: ', err)
        })
    },

    cancelWatch (course) {
      this.$emit('cancelWatch', course.serialNo)
      var i
      for (i = 0; i < this.watchings.length; ) {
        if (course.serialNo == this.watchings[i].serialNo) this.watchings.splice(i, 1)
        else i++
      }
    }

  }
  
}
</script>

<style></style>
