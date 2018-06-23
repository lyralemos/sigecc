<template>
  <div>
    <h1>Ao vivo</h1>

    <div class="row">
      <div class="col-md-4">
        <h3><i class="fas fa-graduation-cap"></i> Alunos</h3>
        <span class="destaque">
          {{ modulo.alunos_count }}
        </span>
      </div>

      <div class="col-md-4">
        <h3><i class="fas fa-users"></i> Grupos</h3>
        <span class="destaque">
          {{ modulo.grupos_count }}
        </span>
      </div>

      <div class="col-md-4">
        <h3><i class="fas fa-question-circle"></i> Questões</h3>
        <span class="destaque">
          {{ modulo.questoes_count }}
        </span>
      </div>
    </div>
    <br />
    <div class="row">
      <div class="col-md-6">
        <h3><i class="fa fa-archive"></i> Modulo</h3>
        <table class="table table-bordered">
          <tr>
            <th>Opção</th>
            <th style="width:30px">Status</th>
          </tr>
          <tr>
            <td>Competição</td>
            <td style="text-align:center">
              <span class="badge badge-pill badge-success" v-if="modulo.competicao===true">
                <i class="fa fa-ckeck"></i>
              </span>
              <span class="badge badge-pill badge-danger" v-if="modulo.competicao===false">
                <i class="fa fa-times"></i>
              </span>
            </td>
          </tr>
          <tr>
            <td>Colaboração</td>
            <td style="text-align:center">
              <span class="badge badge-pill badge-success" v-if="modulo.colaboracao===true">
                <i class="fa fa-ckeck"></i>
              </span>
              <span class="badge badge-pill badge-danger" v-if="modulo.colaboracao===false">
                <i class="fa fa-times"></i>
              </span>
            </td>
          </tr>
          <tr>
            <td>Liberado</td>
            <td style="text-align:center">
              <span class="badge badge-pill badge-success" v-if="modulo.liberado===true">
                <i class="fa fa-ckeck"></i>
              </span>
              <span class="badge badge-pill badge-danger" v-if="modulo.liberado===false">
                <i class="fa fa-times"></i>
              </span>
            </td>
          </tr>
        </table>

        <div class="btn-group" role="group" aria-label="Basic example">
          <button type="button" class="btn btn-warning">Sortear grupos</button>
          <button type="button" class="btn btn-success">Liberar questões</button>
          <button type="button" class="btn btn-danger">Fechar sistema</button>
        </div>
      </div>
      <div class="col-md-6">
        <h3><i class="fa fa-trophy"></i> Placar</h3>
        <table class="table bg-light">
          <tr>
            <th>Posição</th>
            <th>Pontos</th>
            <th>Nome</th>
          </tr>
          <tr v-for="(placar, index) in modulo.placar">
            <td>{{ index+1 }}</td>
            <td>{{ placar.pontos }}</td>
            <td>{{ placar.grupo }}</td>
          </tr>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data: function () {
    return {
      modulo: [],
      interval: null
    }
  },
  methods: {
    getModulo: function () {
      this.$global.loading = true
      this.$http.get('/api/v1/modulos/ativo/')
      .then((response) => {
        this.modulo = response.data
        this.$global.loading = false
      })
      .catch((err) => {
        this.$global.loading = false
        console.log(err)
      })
    }
  },
  beforeRouteLeave (to, from, next) {
    if (this.interval) {
      clearInterval(this.interval)
    }
    next()
  },
  mounted: function () {
    this.getModulo()

    this.interval = setInterval(function () {
      this.getModulo()
    }.bind(this), 3000)
  }
}
</script>

<style></style>
