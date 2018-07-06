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
    <div class="placar" v-if="$global.competicao">
      <div class="acao">
        <i class="material-icons arrow up" @click="mostraPlacar">keyboard_arrow_up</i>
        <i class="material-icons arrow down" @click="mostraPlacar">keyboard_arrow_down</i>
      </div>
      <ul>
        <li v-for="(p, index) in placar" v-bind:class="{ selected: p.grupo.id == grupo }">
          <a>
            <i class="material-icons person">person_pin</i>
            <div class="info">
              <span class="posicao">{{ index+1 }}º</span>
              <div class="dados">
                <b>Colocado</b><br>
                <span class="nome">{{ p.grupo.__str__ }}</span>
                <i class="material-icons star" v-if="p.grupo.id == grupo">star</i>
              </div>
            </div>
          </a>
        </li>
      </ul>
    </div>
  </section>
</template>

<script>
  export default {
    name: 'Pergunta',
    data: function () {
      return {
        aluno: null,
        grupo: null,
        questao: null,
        perguntas: null,
        escolhida: null,
        resposta: null,
        error: null,
        resultado: null,
        acerto: null,
        status: null,
        intervalo: null,
        placar: null
      }
    },
    methods: {
      resetData: function () {
        this.aluno = null
        this.grupo = null
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
            this.grupo = response.data.grupo
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
      },
      getPlacar: function () {
        if (this.$global.competicao) {
          this.$http.get('/api/v1/placar/', { headers: {'X-No-Loading': 'true'} })
          .then((response) => {
            this.placar = response.data
            setTimeout(function () {
              this.getPlacar()
            }.bind(this), 10000)
          })
          .catch((err) => {
            console.log(err)
          })
        }
      },
      mostraPlacar: function () {
        var placar = document.querySelector('.placar')
        placar.classList.toggle('mostrar')
      }
    },
    mounted () {
      if (!this.$global.liberado) {
        this.$router.push('/')
      }
      this.getQuestao()
      this.getPlacar()
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
    transform: translateX(50%);
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

  .placar{
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #d8d8d8;
    padding: 0 20px;
    transition: all .2s ease;
    top: 82%;
  }

  .placar .acao{
    text-align: center;
  }

  .placar.mostrar{
    top:120px;
  }

  .placar .down{
    display:none;
  }

  .placar ul{
    margin-top:0;
  }

  .placar.mostrar li{
    display: block !important;
  }

  .placar.mostrar .down{
    display: inline-block;
  }

  .placar.mostrar .up{
    display: none;
  }

  .placar li{
    display: none;
    margin-bottom: 15px;
    position: relative;
  }

  .placar li.selected{
    display: block;
  }

  .placar i.arrow{
    color:#555;
    text-align: center;
    font-size: 34px;
  }

  .placar i.person{
    font-size: 4em;
    margin-right: 10px;
  }

  .placar i.star{
    position: absolute;
    right: 10px;
    top:50%;
    transform: translateY(-50%);
  }

  .placar a{
    color:#333;
    display: table;
    width: 100%;
  }

  .placar .info{
    display: table-cell;
    vertical-align: middle;
    width: 100%;
  }

  .placar .posicao{
    font-size: 40px;
    margin-right: 5px;
  }

  .placar .dados{
    display: inline-block;
  }


</style>
