<template lang="html">
  <section>
    <div class="espera">
      Aguardando a liberação do sistema
    </div>
  </section>
</template>

<script>
export default {
  name: 'Espera',
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
    }.bind(this), 3000)
  }
}
</script>

<style lang="css">

  .espera{
    text-align: center;
    padding: 20px 0;
  }
</style>
