<template lang="html">
  <section>
    <div class="espera">
      <span class="tempo material-icons">access_time</span>
      <h5>Aguardando a liberação do próximo módulo.</h5>
    </div>
  </section>
</template>

<script>
import isLoggedMixin from '../loggedin'

export default {
  name: 'Espera',
  mixins: [isLoggedMixin],
  data: function () {
    return {
      interval: null
    }
  },
  methods: {
    isLiberado: function () {
      this.$http.get('/api/v1/modulos/ativo/')
        .then((response) => {
          if (response.data.liberado) {
            this.$global.liberado = response.data.liberado
            localStorage.setItem('status', '/pergunta')
            this.$router.push('/pergunta')
          }
        })
    }
  },
  beforeRouteLeave (to, from, next) {
    if (this.interval) {
      clearInterval(this.interval)
    }
    next()
  },
  mounted () {
    this.isLiberado()
    this.interval = setInterval(function () {
      this.isLiberado()
    }.bind(this), 5000)
  }
}
</script>

<style lang="css">

  .espera{
    text-align: center;
    padding: 20px 0;
  }

  .tempo{
    font-size: 100px;
  }
</style>
