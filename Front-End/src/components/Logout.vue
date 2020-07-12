<template>
  <v-container fluid/>
</template>

<script>  
export default {

  data () {
    return {
      
    }
  },
  
  beforeMount () {
    this.logout()
  },

  props: ['isLogin'],
  
  methods: {

    logout () {
      this.$http.get(`/api/auth/session`)
        .then(() => {
          this.$emit('logoutSuccess')
          this.$router.push({name: 'login'})
        })
        .catch((err) => {
          console.log('err: ', err)
        })
    }

  }
  
}
</script>

<style></style>