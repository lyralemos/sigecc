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
        Responda as perguntas abaixo de acordo com a sua experiência durante a aula.
      </h5>
      <div class="pergunta" v-for="pergunta in perguntas">
        <div class="enunciado">{{ pergunta.pergunta }}</div>

        <div class="escala">
          <span>Discordo</span>
          <span></span>
          <span style="text-align:center">Neutro</span>
          <span></span>
          <span>Concordo</span>
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
      <button type="submit" class="btn">Enviar</button>
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
      respostas: {},
      perguntas: [],
      errors: []
    }
  },
  methods: {
    getPerguntas: function () {
      this.$http.get('/api/v1/perguntas_flow/')
        .then((response) => {
          this.perguntas = response.data
        })
    },
    checkForm: function (e) {
      this.errors = []
      if (Object.keys(this.respostas).length !== 36) {
        this.errors.push('Responda todas as perguntas da avaliação')
      } else {
        this.$http.post('/api/v1/alunos/flow/', {
          'respostas': this.respostas
        }).then((response) => {
          if (response.data.result === true) {
            localStorage.setItem('flow', true)
            this.$router.push('/final')
          }
        })
      }
      window.scrollTo(0, 0)
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
    if (localStorage.getItem('flow')) {
      this.$router.push('/final')
    } else {
      this.getPerguntas()
    }
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
  }
  .respostas .resposta{
    text-align: center;
    width: 20%;
  }
  .respostas button{
    width: 90%;
    border: 3px solid #ccc;
    padding: 10px 0;
    border-radius: 38px;
    font-size: 30px;
    background-color: #fff;
  }
  .respostas button.active{
    background-color: #ccc;
  }
  .escala{display: flex;}
  .escala span{
    width: 50%;
    font-weight: 600;
  }
  .escala span+span{
    text-align: right;
  }
  .divider{
    margin-top:15px
  }

  button[type="submit"]{
    width: 100%;
    margin-bottom: 20px;
  }

</style>
