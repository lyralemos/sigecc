<template lang="html">
  <div class="espera">
    <span class="tempo material-icons">access_time</span>
    <h5>Aguardando a liberação do próximo módulo.</h5>
  </div>
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

<style>

  .espera{
    width: 90%;
    text-align: center;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translateY(-50%) translateX(-50%);
  }

  .tempo{
    font-size: 150px;
  }
</style>
