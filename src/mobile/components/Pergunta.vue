<template>
  <section class="main">
    <Progressao />
    <div class="row" v-if="!mostra_grupo">
      <div class="col s12" v-if="questao && !resultado">
        <template v-if="aluno === respondedor.id">
          <h5>Questão:</h5>
          <div class="divider"></div>
          <form action="#" method="post" @submit.prevent="responder">
            <h6>
              {{ pergunta.enunciado }}
            </h6>
            <p v-if="this.error" class="errors">
              Escolha uma resposta.
            </p>

            <label class="resposta">
              <input class="with-gap" type="radio" value="opcao1" v-model="resposta" />
              <span>{{ questao.pergunta.opcao1 }}</span>
            </label>

            <label class="resposta">
              <input class="with-gap" type="radio" value="opcao2" v-model="resposta" />
              <span>{{ questao.pergunta.opcao2 }}</span>
            </label>

            <label class="resposta">
              <input class="with-gap" type="radio" value="opcao3" v-model="resposta" />
              <span>{{ questao.pergunta.opcao3 }}</span>
            </label>

            <label class="resposta">
              <input class="with-gap" type="radio" value="opcao4" v-model="resposta" />
              <span>{{ questao.pergunta.opcao4 }}</span>
            </label>

            <label class="resposta">
              <input class="with-gap" type="radio" value="opcao5" v-model="resposta" />
              <span>{{ questao.pergunta.opcao5 }}</span>
            </label>

            <p class="center" v-if="aluno === respondedor.id">
              <button type="submit" class="btn">Responder</button>
            </p>
          </form>
        </template>
        <template v-if="aluno !== respondedor.id">
          <div style="text-align: center">
            <img style="max-width:250px" src="@/assets/hands-helping-solid.svg" alt="">
            <h5>Ajude a {{respondedor.nome}} responder a próxima questão.</h5>
          </div>
        </template>
      </div>
      <div class="popup" v-if="resultado">
        <div class="overlay"></div>
        <div class="body">
          <template v-if="acerto">
            <img class="thumbs sucesso" src="@/assets/thumbs-up-regular.svg" alt="Parabéns" />
            <div class="mensagem">Parabéns! <br />Você acertou</div>
          </template>
          <template v-if="!acerto">
            <img class="thumbs erro" src="@/assets/thumbs-down-regular.svg" alt="Que pena" />
            <div class="mensagem">
              Que pena! <br /> 
              Não foi dessa vez.
              </div>
          </template>
          <br>
          <button type="button" class="btn" @click="getQuestao">Continuar</button>
        </div>
      </div>
    </div>
    <div v-if="mostra_grupo">
      <h5>Conheça o seu grupo:</h5>
      <ul class="grupo" v-if="grupo_questao">
        <li v-for="aluno in grupo_questao.grupo.aluno_set" :key="aluno">{{aluno}}</li>
      </ul>

      <h6>Vocês deverão colaborar para realizar as atividades, portanto se aproximem.</h6>

      <button class="btn" @click="mostra_grupo = false">Continuar</button>
    </div>
    <Placar v-if="$global.competicao == true" ref="placar"></Placar>
  </section>
  
</template>

<script>
  import isLoggedMixin from '../loggedin'
  import Placar from './Placar'
  import Progressao from './Progressao'

  export default {
    name: 'Pergunta',
    mixins: [isLoggedMixin],
    components: {Placar, Progressao},
    data: function () {
      return {
        aluno: null,
        grupo_questao: null,
        questao: null,
        pergunta: null,
        resposta: null,
        respondedor: null,
        error: null,
        resultado: null,
        acerto: null,
        status: null,
        intervalo: null,
        mostra_grupo: this.$global.colaboracao
      }
    },
    methods: {
      resetData: function () {
        this.aluno = null
        this.grupo_questao = null
        this.questao = null
        this.pergunta = null
        this.resposta = null
        this.respondedor = null
        this.error = null
        this.resultado = null
        this.acerto = null
        this.status = null
      },
      getQuestao: function () {
        this.resetData()
        this.$http.get('/api/v1/grupos/perguntas/')
          .then((response) => {
            this.aluno = response.data.aluno
            this.$global.grupo = response.data.grupo_questao.grupo
            this.grupo_questao = response.data.grupo_questao
            this.questao = this.grupo_questao.questao
            this.pergunta = this.questao.pergunta
            this.respondedor = response.data.grupo_questao.respondedor

            // if (this.grupo_questao.grupo.aluno_set.length !== 1) {
            //   this.mostra_grupo = false
            // }

            if (this.aluno !== this.respondedor.id) {
              // loop que verifica se questao foi respondida
              this.getStatus()
            }
            this.$root.$emit('sigecc:update')
          })
          .catch(() => {
            // console.log(err)
            this.$router.push('/flow')
          })
      },
      responder: function () {
        if (!this.resposta) {
          this.error = true
        } else {
          this.error = false
          this.$http.post('/api/v1/grupos/responder/', {
            grupo_questao: this.grupo_questao.id,
            resposta: this.resposta
          }).then((response) => {
            this.resultado = true
            this.acerto = response.data.result

            if (this.$global.competicao) {
              this.$refs.placar.getPlacar()
            }
          }).catch((err) => {
            console.log(err)
          })
        }
      },
      getStatus: function () {
        this.$http.get('/api/v1/grupos/respondido/?id=' + this.grupo_questao.id)
          .then((response) => {
            this.status = response.data.result
            if (this.status) {
              this.getQuestao()
            } else {
              setTimeout(function () {
                this.getStatus()
              }.bind(this), 2000)
            }
          })
          .catch(() => {
            // console.log(err)
            // se der erro aqui é porque não tem mais perguntas
            // redirecionando para flow
            this.$router.push('/flow')
          })
      }
    },
    mounted () {
      if (!this.$global.liberado) {
        this.$router.push('/')
      } else {
        this.getQuestao()
      }
    }
  }
</script>

<style scoped>

  .competicao form{
    padding-bottom:90px; 
  }

  h6{
    line-height: 22px;
    margin: 15px 0;
  }

  label{
    display: block
  }

  .texto{
    text-align: justify;
    white-space: pre-line;
  }

  .thumbs {
    width: 138px;
  }

  .popup .mensagem{
    font-size: 25px;
  }

  .perguntas li{
    background-color: #ddd;
    padding: 10px 20px;
    display: table;
    width: 100%;
  }

  .perguntas .details{
    display: table-cell;
    vertical-align: middle;
    width: 80%;
  }

  label.resposta{
    margin-bottom: 10px;
  }

  label.resposta span{
    line-height: 19px;
  }

  button{
    width: 100%;
  }
  .acerto i{
    font-size: 9rem;
  }

  .popup .body{
    padding: 15px;
  }

  .grupo{
    border: 1px solid #cecece;
    border-radius: 20px;
    background-color: #f1f1f1;
  }
  .grupo li{
    display: block;
    padding: 5px 15px;
    text-align: center;
    font-size: 20px;
  }

</style>
