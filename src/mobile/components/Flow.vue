<template lang="html">
  <section>
    
    <form acion="#" method="post" @submit="checkForm">
      <p class="errors" v-if="errors.length">
        <b>Por favor corrija os seguintes erros</b>
        <ul>
          <li v-for="error in errors">{{ error }}</li>
        </ul>
      </p>

      <h5>
        Por favor responda o questionário abaixo.
      </h5>
      <p style="text-align:justify">
        Por favor responda as seguintes questões em relação a sua experiência na atividade que você <b>acabou de concluir</b>. 
        Estas perguntas estão relacionadas com os pensamentos e sentimentos que você pode ter experimentado ao participar. 
        Não há respostas certas ou erradas. Pense em como você se sentiu durante o evento / atividade e responda às perguntas 
        usando a escala de classificação abaixo. Para cada pergunta, escolha a resposta que melhor corresponde à sua experiência.
      </p>
      <div class="divider"></div>
      <div class="pergunta" v-for="(pergunta, index) in perguntas">
        <div class="enunciado">{{index+1}}. {{ pergunta.pergunta }}</div>

        <div class="escala">
          <span>Discordo completamente</span>
          <span>Discordo</span>
          <span style="text-align:center">Nem concordo nem discordo</span>
          <span>Concordo</span>
          <span>Concordo completamente</span>
        </div>
        <div class="respostas">
          <div class="resposta">
            <button type="button"
              v-on:click="change(pergunta.id, 1)"
              v-bind:class="{ active: checkSelected(pergunta.id, 1) }">1</button>
            <input class="with-gap" v-bind:name="pergunta.id" type="radio" value="1" v-model="respostas[pergunta.id]" />
          </div>

          <div class="resposta">
            <button type="button"
              v-on:click="change(pergunta.id,2)"
              v-bind:class="{ active: checkSelected(pergunta.id, 2) }">2</button>
              <input class="with-gap" v-bind:name="pergunta.id" type="radio" value="2" v-model="respostas[pergunta.id]" />
          </div>

          <div class="resposta">
            <button type="button"
              v-on:click="change(pergunta.id,3)"
              v-bind:class="{ active: checkSelected(pergunta.id, 3) }">3</button>
              <input class="with-gap" v-bind:name="pergunta.id" type="radio" value="3" v-model="respostas[pergunta.id]"  />
          </div>

          <div class="resposta">
            <button type="button"
              v-on:click="change(pergunta.id,4)"
              v-bind:class="{ active: checkSelected(pergunta.id, 4) }">4</button>
            <input class="with-gap" v-bind:name="pergunta.id" type="radio" value="4" v-model="respostas[pergunta.id]" />
          </div>

          <div class="resposta">
            <button type="button"
              v-on:click="change(pergunta.id,5)"
              v-bind:class="{ active: checkSelected(pergunta.id, 5) }">5</button>
            <input class="with-gap" v-bind:name="pergunta.id" type="radio" value="5" v-model="respostas[pergunta.id]" />
          </div>
        </div>

        <div class="divider"></div>
      </div>
      <button type="submit" class="btn" :disabled="btnDisabled">{{btnText}}</button>
    </form>
  </section>
</template>

<script>
import isLoggedMixin from '../loggedin'

export default {
  name: 'Flow',
  mixins: [isLoggedMixin],
  data: function () {
    return {
      aceito: false,
      respostas: {},
      perguntas: [],
      errors: [],
      parabens: false,
      btnText: 'Enviar',
      btnDisabled: false
    }
  },
  methods: {
    getPerguntas: function () {
      this.$http.get('/api/v1/perguntas_flow/')
        .then((response) => {
          this.perguntas = response.data
        })
        .catch(() => {
          this.$router.push('/final')
        })
    },
    checkForm: function (e) {
      this.errors = []
      this.btnText = 'Enviando...'
      this.btnDisabled = true
      if (Object.keys(this.respostas).length !== 36) {
        this.errors.push('Responda todas as perguntas da avaliação')
        this.btnText = 'Enviar'
        this.btnDisabled = false
        window.scrollTo(0, 0)
      } else {
        this.$http.post('/api/v1/alunos/flow/', {
          'respostas': this.respostas
        }).then((response) => {
          if (response.data.result === true) {
            this.$router.push('/final')
          }
        }).catch(() => {
          this.errors.push('Ocorreu um erro.')
          this.btnText = 'Enviar'
          this.btnDisabled = false
        })
      }
      e.preventDefault()
    },
    change: function (id, value) {
      this.$set(this.respostas, id, value)
    },
    checkSelected: function (id, value) {
      return this.respostas[id] === value
    }
  },
  mounted: function () {
    this.getPerguntas()
  }
}
</script>

<style lang="css">
  .pergunta{
    margin-bottom: 15px;
  }
  .enunciado{
    font-size: 16px;
    text-align: justify;
    margin-bottom: 10px;
  }
  .respostas{
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .respostas .resposta{
    text-align: center;
    width: 20%;
    /* height: 55px; */
  }
  .respostas button{
    width: 50px;
    height: 50px;
    border: 3px solid #ccc;
    border-radius: 50%;
    font-size: 30px;
    background-color: #fff;
    transition: .2s all ease;
  }
  .respostas button.active{
    background-color: #26a69a;
    border-color: #26a69a;
    color: #fff;
    transform: scale(1.2);
  }
  .escala{
    display: flex;
    padding: 5px 0;
  }
  .escala span{
    width: 20%;
    font-weight: 600;
    font-size: 12px;
    text-align: center;
    word-wrap: break-word;
  }
  /* .escala span+span{
    text-align: right;
  } */
  .divider{
    margin:15px 0;
  }

  button[type="submit"]{
    width: 100%;
    margin-bottom: 20px;
  }

  .align-center{
    text-align: center
  }

</style>
