<template>
  <section>
    <div class="row">
      <div class="col s12" v-if="questao && !resultado">
        <h5>Questão:</h5>
        <p class="texto">{{ questao.texto }}</p>
        <div class="divider"></div>

        <div class="perguntas" v-if="!escolhida">
          <h6>Perguntas do Grupo</h6>
          <ul>
            <li v-for="pergunta in perguntas">
              <i class="material-icons medium">person_pin</i>
              <div class="details">
                <b>{{ pergunta.pergunta.titulo }}</b><br>
                {{ pergunta.aluno.nome }}
              </div>
            </li>
          </ul>
          <div class="center">
            <button type="button" class="btn" @click="setEscolhida">Prosseguir</button>
          </div>
        </div>
        <form action="#" method="post" v-if="escolhida" @submit.prevent="responder">
          <h6>
            {{ escolhida.pergunta.titulo }}
          </h6>
          <p v-if="this.error" class="errors">
            Escolha uma resposta.
          </p>

          <label>
            <input class="with-gap" type="radio" value="opcao1" v-model="resposta" />
            <span>{{ escolhida.pergunta.opcao1 }}</span>
          </label>

          <label>
            <input class="with-gap" type="radio" value="opcao2" v-model="resposta" />
            <span>{{ escolhida.pergunta.opcao2 }}</span>
          </label>

          <label>
            <input class="with-gap" type="radio" value="opcao3" v-model="resposta" />
            <span>{{ escolhida.pergunta.opcao3 }}</span>
          </label>

          <label>
            <input class="with-gap" type="radio" value="opcao4" v-model="resposta" />
            <span>{{ escolhida.pergunta.opcao4 }}</span>
          </label>

          <label>
            <input class="with-gap" type="radio" value="opcao5" v-model="resposta" />
            <span>{{ escolhida.pergunta.opcao5 }}</span>
          </label>

          <p class="center">
            <button type="submit" class="btn">Enviar resposta</button>
          </p>
        </form>
      </div>
      <div class="resultado" v-if="resultado">
        <span class="acerto" v-if="acerto">
          <i class="material-icons large">check</i><br>
          <h5>Acertou!</h5>
        </span>
        <span class="erro" v-if="!acerto">
          <i class="material-icons large">close</i><br>
          <h5>Errou!</h5>
        </span>
        <br><br>

        <button type="button" class="btn disabled" v-if="perguntas.length > 1">Aguardando outras respostas...</button>
        <button type="button" class="btn" v-if="perguntas.length == 1" @click="getQuestao">Próxima Pergunta</button>
      </div>
    </div>
    <Placar v:if="$global.competicao == true"></Placar>
  </section>
</template>

<script>
  import isLoggedMixin from '../loggedin'
  import Placar from './Placar'

  export default {
    name: 'Pergunta',
    mixins: [isLoggedMixin],
    components: {Placar},
    data: function () {
      return {
        aluno: null,
        questao: null,
        perguntas: null,
        escolhida: null,
        resposta: null,
        error: null,
        resultado: null,
        acerto: null,
        status: null,
        intervalo: null
      }
    },
    methods: {
      resetData: function () {
        this.aluno = null
        this.questao = null
        this.perguntas = null
        this.escolhida = null
        this.resposta = null
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
            this.$global.grupo = response.data.grupo
            this.questao = response.data.questao
            this.perguntas = response.data.perguntas

            if (!this.questao.texto) {
              this.$router.push('/flow')
            }

            if (this.perguntas.length === 1) {
              this.setEscolhida()
            }
          })
          .catch((err) => {
            console.log(err)
          })
      },
      setEscolhida: function () {
        for (var index in this.perguntas) {
          var pergunta = this.perguntas[index]

          if (pergunta.aluno.id === this.aluno) {
            this.escolhida = pergunta
          }
        }
        if (this.escolhida.resposta !== '') {
          this.resultado = true
          this.acerto = this.escolhida.correto

          this.startInterval()
        }
      },
      responder: function () {
        if (!this.resposta) {
          this.error = true
        } else {
          this.error = false
          this.$http.post('/api/v1/grupos/responder/', {
            questao_aluno: this.escolhida.id,
            resposta: this.resposta
          }).then((response) => {
            this.resultado = true
            this.acerto = response.data.result

            if (this.perguntas.length > 1) {
              this.startInterval()
            }
            this.getPlacar()
          }).catch((err) => {
            console.log(err)
          })
        }
      },
      startInterval: function () {
        this.intervalo = setInterval(function () {
          this.getStatus()
        }.bind(this), 3000)
      },
      getStatus: function () {
        this.$http.get('/api/v1/grupos/status/?questao=' + this.questao.id)
          .then((response) => {
            this.status = response.data.result
            if (this.status) {
              clearInterval(this.intervalo)
              this.getQuestao()
            }
          })
          .catch((err) => {
            console.log(err)
          })
      }
    },
    mounted () {
      if (!this.$global.liberado) {
        this.$router.push('/')
      }
      this.getQuestao()
    }
  }
</script>

<style scoped>
  label{
    display: block
  }

  .texto{
    text-align: justify;
    white-space: pre-line;
  }

  .resultado{
    background: #fff;
    text-align: center;
    padding-top: 30px;
  }

  .resultado span{
    width: 200px;
    margin: auto;
    border: 1px solid #ddd;
    display: block;
    border-radius: 100px;
    padding: 28px 0;
    color: #fff;
  }

  .resultado span.erro{
    background-color: #EF4836;
  }

  .resultado span.acerto{
    background-color: #87D37C;
  }

  .resultado span i{
    color: #fff;
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

  button{
    width: 100%;
  }


</style>
