<template lang="html">
  <section>
    <h1>Questões</h1>

    <table class="table table-bordered">
      <tr>
        <th>Id</th>
        <th>Enunciado</th>
        <th>Opcões</th>
        <th>Resposta</th>
      </tr>
      <tr v-for="pergunta in questoes">
        <td>{{ pergunta.id }}</td>
        <td>{{ pergunta.enunciado }}</td>
        <td>
            <ul>
              <li>a) {{ pergunta.opcao1 }}</li>
              <li>b) {{ pergunta.opcao2 }}</li>
              <li>c) {{ pergunta.opcao3 }}</li>
              <li>d) {{ pergunta.opcao4 }}</li>
              <li>e) {{ pergunta.opcao5 }}</li>
            </ul>
        </td>
        <td>
            {{ getResposta(pergunta) }}
        </td>
      </tr>
    </table>
  </section>
</template>

<script>
export default {
  data: function () {
    return {questoes: []}
  },

  methods: {
    getQuestoes: function () {
      this.$global.loading = true
      this.$http.get('/api/v1/perguntas/')
      .then((response) => {
        this.questoes = response.data
        this.$global.loading = false
      })
      .catch((err) => {
        this.$global.loading = false
        console.log(err)
      })
    },
    getResposta: function (pergunta) {
      return pergunta[pergunta.resposta]
    }
  },
  mounted: function () {
    this.getQuestoes()
  }
}
</script>

<style lang="css">
</style>
