<template lang="html">
  <section class="centered">
    <img src="@/assets/clock-regular.svg" />
    <h5 v-if="$global.competicao">Aguardando os seus oponentes.</h5>
    <h5 v-if="!$global.competicao">Aguardando os seus colegas.</h5>
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
            clearInterval(this.interval)
            if (this.$global.competicao) {
              this.$router.push('/foto')
            } else {
              this.$router.push('/pergunta')
            }
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

<style scoped>
  h5{text-align: center}
</style>
