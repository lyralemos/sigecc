<template>
  <section>
    <h1>Módulos</h1>

    <table class="table table-bordered">
      <tr>
        <th>Nome</th>
        <th>Colaboração</th>
        <th>Competição</th>
        <th>Ativo</th>
        <th>Liberado</th>
      </tr>
      <tr v-for="modulo in modulos" v-bind:key="modulo.id">
        <td>{{ modulo.nome }}</td>
        <td><Check :bool="modulo.colaboracao"></Check></td>
        <td><Check :bool="modulo.competicao"></Check></td>
        <td><Check :bool="modulo.ativo"></Check></td>
        <td><Check :bool="modulo.liberado"></Check></td>
      </tr>
    </table>
  </section>
</template>

<script>
import Check from './Check.vue'

export default{
  name: 'Modulos',
  components: {
    'Check': Check
  },
  data: function () {
    return {modulos: []}
  },

  methods: {
    getModulos: function () {
      this.$global.loading = true
      this.$http.get('/api/v1/modulos/')
      .then((response) => {
        this.modulos = response.data
        this.$global.loading = false
      })
      .catch((err) => {
        this.$global.loading = false
        console.log(err)
      })
    }
  },
  mounted: function () {
    this.getModulos()
  }
}
</script>
