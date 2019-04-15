<template>
  <section>
    <h1>Grupos</h1>

    <table class="table table-bordered">
      <tr>
        <th>Nome</th>
        <th>Alunos</th>
      </tr>
      <tr v-for="grupo in grupos" v-bind:key="grupo.id">
        <td>{{ grupo.__str__ }}</td>
        <td>
          <ul>
            <li v-for="aluno in grupo.aluno_set">
              {{ aluno }}
            </li>
          </ul>
        </td>
      </tr>
    </table>
  </section>
</template>

<script>

export default{
  data: function () {
    return {grupos: []}
  },

  methods: {
    getGrupos: function () {
      this.$global.loading = true
      this.$http.get('/api/v1/grupos/')
      .then((response) => {
        this.grupos = response.data
        this.$global.loading = false
      })
      .catch((err) => {
        this.$global.loading = false
        console.log(err)
      })
    }
  },
  mounted: function () {
    this.getGrupos()
  }
}
</script>
