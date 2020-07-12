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
    this.$router.push({name: 'home'})
  }
  
}
</script>

<style></style>