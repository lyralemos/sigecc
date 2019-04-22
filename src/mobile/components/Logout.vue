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
        localStorage.removeItem('user-token')
        localStorage.removeItem('status')
        localStorage.removeItem('resolvidos')
        this.$global = {}
        this.$router.push('/')
      }
    },
    mounted () {
      this.logout()
    }
  }
</script>
