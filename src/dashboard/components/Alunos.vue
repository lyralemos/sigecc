<template>
  <div>
    <h1>Alunos</h1>

    <table class="table table-bordered">
      <tr>
        <th>Nome</th>
        <th>Data de Nascimento</th>
        <th>Gênero</th>
      </tr>
      <tr v-for="aluno in alunos">
        <td>{{ aluno.user.first_name }}</td>
        <td>{{ aluno.nascimento }}</td>
        <td>{{ aluno.genero }}</td>
      </tr>
    </table>
  </div>
</template>

<script>

export default{
  data: function () {
    return {alunos: []}
  },

  methods: {
    getAlunos: function () {
      this.$global.loading = true
      this.$http.get('/api/v1/alunos/')
      .then((response) => {
        this.alunos = response.data
        this.$global.loading = false
      })
      .catch((err) => {
        this.$global.loading = false
        console.log(err)
      })
    }
  },
  mounted: function () {
    this.getAlunos()
  }
}
</script>
