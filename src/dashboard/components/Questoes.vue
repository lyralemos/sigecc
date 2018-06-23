<template lang="html">
  <div>
    <h1>Questões</h1>

    <table class="table table-bordered">
      <tr>
        <th>Id</th>
        <th>Texto</th>
        <th>Perguntas</th>
      </tr>
      <tr v-for="questao in questoes">
        <td>{{ questao.id }}</td>
        <td>{{ questao.texto }}</td>
        <td>
          <span v-for="pergunta in questao.pergunta_set">
            Respostas:
            <ul>
              <li>a) {{ pergunta.opcao1 }}</li>
              <li>b) {{ pergunta.opcao2 }}</li>
              <li>c) {{ pergunta.opcao3 }}</li>
              <li>d) {{ pergunta.opcao4 }}</li>
              <li>e) {{ pergunta.opcao5 }}</li>
            </ul>
            <b>Resposta: {{ getResposta(pergunta) }}</b>
          </span>
        </td>
      </tr>
    </table>
  </div>
</template>

<script>
export default {
  data: function () {
    return {questoes: []}
  },

  methods: {
    getQuestoes: function () {
      this.$global.loading = true
      this.$http.get('/api/v1/questoes/')
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
