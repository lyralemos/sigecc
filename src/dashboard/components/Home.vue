<template>
  <div class="home">
    <section class="inferior">
      <div class="item">
        <i class="fas fa-graduation-cap"></i><br />
        <span class="numero">{{ modulo.alunos_count }}</span><br />
        <span class="detalhe">Alunos</span><br />
        <span class="discreto">Cadastrados no módulo</span>
      </div>
      <div class="item">
        <i class="fas fa-users"></i><br />
        <span class="numero">{{ modulo.grupos_count }}</span><br />
        <span class="detalhe">Grupos</span><br />
        <span class="discreto">Cadastrados no módulo</span>
      </div>
      <div class="item">
        <i class="fas fa-question-circle"></i><br />
        <span class="numero">{{ modulo.questoes_count }}</span><br />
        <span class="detalhe">Questões</span><br />
        <span class="discreto">Disponíveis para os alunos</span>
      </div>
      <div class="item">
        <i class="fas fa-chart-line"></i><br />
        <span class="numero">{{ modulo.respostas_count }}</span><br />
        <span class="detalhe">Respostas</span><br />
        <span class="discreto">Total de respostas até agora.</span>
      </div>
    </section>
    <section class="tabelas">
      <div class="item">
        <div class="titulo">
          <span>Módulo ativado</span>
        </div>
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Opção</th>
              <th style="width:30px">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Competição</td>
              <td style="text-align:center">
                <Check :bool="modulo.competicao"></Check>
              </td>
            </tr>
            <tr>
              <td>Colaboração</td>
              <td style="text-align:center">
                <Check :bool="modulo.colaboracao"></Check>
              </td>
            </tr>
            <tr>
              <td>Liberado</td>
              <td style="text-align:center">
                <Check :bool="modulo.liberado"></Check>
              </td>
            </tr>
            <tr>
              <td>Finalizado</td>
              <td style="text-align:center">
                <Check :bool="modulo.finalizado"></Check>
              </td>
            </tr>
          </tbody>
        </table>
        <a href="#"
          class="btn btn-primary"
          v-bind:class="{'disabled':modulo.liberado}"
          v-on:click="liberar">Liberar</a>
        <a class="btn btn-secondary"
          v-bind:class="{'disabled':!modulo.liberado}"
          v-on:click="finalizar">Finalizar</a>
      </div>
      <div class="item">
        <div class="titulo">
          <span>Placar</span>
        </div>
        <table class="table">
          <tr>
            <th>Posição</th>
            <th>Nome</th>
            <th v-if="modulo.competicao">Pontos</th>
            <th>Acertos</th>
          </tr>
          <tr v-for="(placar, index) in modulo.placar" :key="placar.id">
            <td>{{ index+1 }}</td>
            <td>{{ placar.grupo.__str__ }}</td>
            <td v-if="modulo.competicao">{{ placar.pontos }}</td>
            <td>{{placar.grupo.acertos}}</td>
          </tr>
        </table>
      </div>
    </section>
  </div>
</template>

<script>
import Check from './Check.vue'
export default {
  name: 'Home',
  components: {
    'Check': Check
  },
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
    },
    liberar: function () {
      if (!this.modulo.liberado) {
        var c = confirm('Deseja liberar o sistema para os alunos?')
        if (c) {
          this.$global.loading = true
          this.$http.get('/api/v1/modulos/liberar/')
            .then((response) => {
              this.$global.loading = false
            })
            .catch((err) => {
              this.$global.loading = false
              console.log(err)
            })
        }
      }
    },
    finalizar: function () {
      if (this.modulo.liberado) {
        var c = confirm('Deseja finalizar o módulo?')
        if (c) {
          this.$global.loading = true
          this.$http.get('/api/v1/modulos/finalizar/')
            .then((response) => {
              this.$global.loading = false
            })
            .catch((err) => {
              this.$global.loading = false
              console.log(err)
            })
        }
      }
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

<style>
  .tabelas{
    padding-top: 20px;
    display: flex;
  }

  .tabelas .item{
    width: 47%;
    text-align: left;
  }

  .tabelas .item i{font-size:14px }

  .titulo span{
    text-transform: uppercase;
    font-weight: bold;
    font-size: 15px;
    color: #67472b;
    display: inline-block;
  }

  .inferior{
    padding-top: 30px;
    padding-bottom: 30px;
    display: flex;
  }

  .item{
    background-color: #fff;
    padding: 20px;
    width: 22%;
    text-align: center;
    margin-right: 3%;
  }
  .item i{font-size: 30px;}
  .item .numero{font-size: 40px}
  .item .detalhe{color:#27b756}
  .item .discreto{font-size: 11px; color: #aaa}
</style>
