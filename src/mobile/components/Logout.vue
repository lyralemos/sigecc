<template>
  <section>
    saindo...
  </section>
</template>

<script>
  export default {
    name: 'Logout',
    methods: {
      logout: function () {
        console.log('asdasd')
        localStorage.removeItem('user-token')
        this.$router.push('/')
      }
    },
    mounted () {
      this.logout()
    }
  }
</script>
