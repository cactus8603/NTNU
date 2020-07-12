<template>
  <v-img 
    class="fill-height"
    src="http://en.ntnu.edu.tw/images/index-banner04.jpg"
    aspect-ratio="10"
  >
    <v-container fluid
      class="fill-height"
    >
      <v-overlay :value="loading">
        <v-row justify="center">
          <v-col cols="auto">
            <v-progress-circular indeterminate size="64"/>
          </v-col>
        </v-row>
        <v-row justify="center">
          <v-col cols="auto" class="headline">正在登入...</v-col>
        </v-row>
      </v-overlay>

      <v-row no-gutters
        align="center"
        justify="center"
      >
        <v-col
          cols="12"
          xs="12"
          sm="8"
          md="4"
          lg="4"
          xl="4"
        >
          <v-card class="elevation-12">
            <v-toolbar dark flat
              color="primary"
            >
              <v-toolbar-title>登入</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form>
                
                <v-text-field
                  v-model="authData.studentId"
                  label="學號 (大寫)"
                  prepend-icon="mdi-account"
                  type="text"
                  :rules="studentIdRule"
                  @keyup.enter="login"
                />

                <v-text-field
                  v-model="authData.password"
                  label="密碼"
                  prepend-icon="mdi-lock"
                  :rules="passwordRule"
                  :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="showPassword ? 'text' : 'password'"
                  @click:append="showPassword = !showPassword"
                  @keyup.enter="login"
                />
              
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer />
              <v-btn color="primary" @click="login">登入</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <v-snackbar top
        class="mt-8 pt-8"
        v-model="snackbar"
        :timeout="3000"
        :color="isLogin ? 'green':'red'"
      >
        {{ isLogin ? '登入成功！':'登入失敗！' }}
        <v-btn dark text
          @click="snackbar = false"
        >
          好的
        </v-btn>
      </v-snackbar>
    </v-container>
  </v-img>
</template>

<script>  
export default {

  data () {
    return {
      loading: false,
      snackbar: false,
      authData: {
        'studentId': '',
        'password': ''
      },
      studentIdRule: [val => !!val || '請輸入學號！'],
      passwordRule: [val => !!val || '請輸入密碼！'],
      showPassword: false
    }
  },
  
  beforeMount () {
    if ( this.isLogin ) {
      this.$router.push({name: 'profile'})
    }
    this.studentId = ''
    this.password = ''
  },

  props: ['isLogin'],

  watch: {
    snackbar () {
      if ( this.isLogin && !this.snackbar )
        this.$router.push({name: 'profile'})
    }
  },
  
  methods: {

    login () {
      this.loading = true
      this.$http.post(`/api/auth/session`, this.authData)
        .then(() => {
          this.loading = false
          this.snackbar = true
          this.$emit('loginSuccess')
        })
        .catch((err) => {
          console.log('err: ', err)
          this.loading = false
          this.snackbar = true
        })
    }

  }
  
}
</script>

<style></style>