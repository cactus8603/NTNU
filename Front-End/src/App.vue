<template>
  <v-app>
    <v-app-bar app dark clipped-left
      color="indigo"
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title>{{ title }}</v-toolbar-title>
    </v-app-bar>

    <v-navigation-drawer app temporary
      v-model="drawer"
    >
      <v-list>
        <v-list-item>
          <v-list-item-avatar>
            <v-img src="https://stylizedbay.com/wp-content/uploads/2018/02/unknown-avatar.jpg"></v-img>
          </v-list-item-avatar>
        </v-list-item>

        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="title" ref="username">
              {{ username === null ? '未登入':username}}
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      
      <v-divider></v-divider>

      <v-list shaped>
        <v-list-item
          v-for="button in processedButtons"
          color="primary"
          :key="button.key"
          :to="button.link"
          >
          <v-list-item-action>
            <v-icon>{{ button.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ button.text }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-content>
      <router-view
        :isLogin="isLogin"
        :userData="userData"
        :watchingList="watchingList"
        :takingList="takingList"
        :searchAlert="searchAlert"
        :takeResult="takeResult"
        :cancelResult="cancelResult"
        @loginSuccess="isLogin = true"
        @logoutSuccess="isLogin = false"
        @searchAlertConfirm="searchAlert = false"
        @addWatch="addWatch"
        @cancelWatch="cancelWatch"
        @addTake="addTake"
        @closeTakeResult="takeResult = 0"
        @cancelTake="cancelTake"
        @closeCancelResult="cancelResult = 0"
      />
    </v-content>

    <v-footer app
      color="indigo"
    >
      <span class="white--text">&copy; 2020 冰塊製作 :)</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {

  data () {
    return {

      isLogin: false,
      username: null,
      studentId: null,
      major: null,
      watchingList: [],
      takingList: [],
      searchAlert: true,
      takeResult: 0,
      cancelResult: 0,
      
      title: '師大搶課網站',
      drawer: null,

      buttons: [
        { key: 'profile', display: 1, icon: 'mdi-account-card-details-outline', text: '個人資料', link: '/profile'},
        { key: 'search', display: 2, icon: 'mdi-magnify', text: '查詢課程', link: '/search'},
        { key: 'takings', display: 1, icon: 'mdi-account-details', text: '搶課清單', link: '/takings'},
        { key: 'watchings', display: 1, icon: 'mdi-folder-star-outline', text: '關注清單', link: '/watchings'},
        { key: 'notifications', display: 1, icon: 'mdi-bell', text: '通知', link: '/notifications'},
        { key: 'login', display: 0, icon: 'mdi-login', text: '登入', link: '/login'},
        { key: 'logout', display: 1, icon: 'mdi-logout', text: '登出', link: '/logout'}
      ]

    }
  },

  beforeMount () {
    this.loginCheck()
  },

  computed: {

    processedButtons () {
      return this.buttons.filter(button => button.display == this.isLogin || button.display === 2)
    },

    userData () {
      return [
        { key: '姓名', value: this.username },
        { key: '學號', value: this.studentId },
        { key: '系所', value: this.major }
      ]
    }

  },

  watch: {
    isLogin () {
      this.loginCheck()
    }
  },
  
  methods: {

    parseJwt (token) {
      // console.log(atob(token.split('.')[1]));
      return JSON.parse(atob(token.split('.')[1])).data;
    },

    loginCheck () {
      if ( this.$cookies.isKey('jwt') ){

        this.isLogin = true

        this.payload = this.parseJwt(this.$cookies.get('jwt'))

        this.username = this.payload.name
        this.studentId = this.payload.studentId
        this.major = this.payload.major

        this.$http.get(`/api/profile/lists`)
          .then((res) => {
            this.watchingList = res.data.data.watchingList
            this.takingList = res.data.data.takingList
          })
          .catch((err) => {
            console.log('err: ', err)
          })
      }
      else{
        this.username = null
        this.studentId = null
        this.major = null

        this.watchingList = []
        this.takingList = []
      }
    },

    addWatch (serialNo) {
      var i
      for (i = 0; i < this.watchingList.length; i++) {
        if (serialNo == this.watchingList[i]) return
      }
      
      if (this.isLogin) {
        this.$http.post(`/api/profile/addwatch`, { 'serialNo': serialNo } )
            .then(() => {
              this.watchingList.push(serialNo)
            })
            .catch((err) => {
              console.log('err: ', err)
            })
      }
    },

    cancelWatch (serialNo) {
      if (this.isLogin) {
        this.$http.post(`/api/profile/cancelwatch`, { 'serialNo': serialNo } )
            .then(() => {
              var i
              for (i = 0; i < this.watchingList.length; ) {
                if (serialNo == this.watchingList[i]) this.watchingList.splice(i, 1)
                else i++
              }
            })
            .catch((err) => {
              console.log('err: ', err)
            })
      }
    },

    addTake (course, domain) {
      this.takeResult = 1
      this.$http.post(`/api/profile/addtake`, {
        'serialNo': course.serialNo,
        'domain': domain != null ? domain : ''
      })
        .then(() => {
          this.takingList.push(course.serialNo)
          this.takeResult = 2
        })
        .catch((err) => {
          console.log('err: ', err)
          this.takeResult = 3
        })
    },

    cancelTake (course) {
      this.cancelResult = 1
      this.$http.post(`/api/profile/canceltake`, {
        'serialNo': course.serialNo
      })
        .then(() => {
          var i
          for (i = 0; i < this.takingList.length; ) {
            if (course.serialNo == this.takingList[i]) this.takingList.splice(i, 1)
            else i++
          }
          this.cancelResult = 2
        })
        .catch((err) => {
          console.log('err: ', err)
          this.cancelResult = 3
        })
    }
  }
  
}
</script>

<style></style>
