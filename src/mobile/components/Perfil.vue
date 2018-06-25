<template lang="html">
  <section>
    <form acion="#" method="post" @submit="checkForm">

      <p class="errors" v-if="errors.length">
        <b>Por favor corrija os seguintes erros</b>
        <ul>
          <li v-for="error in errors">{{ error }}</li>
        </ul>
      </p>

      <h5>Dados pessoais</h5>
      <div class="row">
        <div class="input-field col s12">
          <input id="id_cpf"
            type="text"
            v-model="cpf"
            required>
          <label for="id_cpf">CPF</label>
          <span class="helper-text" data-error="wrong" data-success="right">Somente números</span>
        </div>

        <div class="input-field col s12">
          <input id="id_nome"
            type="text"
            v-model="nome"
            required>
          <label for="id_nome">Nome</label>
        </div>

        <div class="input-field col s12">
          <input id="id_nascimento"
            type="date"
            v-model="nascimento"
            required>
          <label for="id_nascimento">Data de Nascimento</label>
        </div>

        <div class="input-field col s12">
          <select id="id_genero" v-model="genero">
            <option value="" selected>Escolha um opção</option>
            <option value="1">Masculino</option>
            <option value="2">Feminino</option>
          </select>
          <label>Gênero</label>
        </div>
      </div>
      <h5>
        Responda as perguntas abaixo utilizando considerando se concorda
        ou não com as afirmações.
      </h5>
      <div class="pergunta" v-for="pergunta in perguntas">
        <div class="enunciado">{{ pergunta.pergunta }}</div>

        <div class="escala">
          <span>
            Discordo <br />
            plenamente
          </span>
          <span>Concordo <br>plenamente</span>
        </div>
        <div class="respostas">
          <button type="button"
            v-on:click="change(pergunta.id, 1)"
            v-bind:class="{ active: checkSelected(pergunta.id, 1) }">1</button>
          <button type="button"
            v-on:click="change(pergunta.id,2)"
            v-bind:class="{ active: checkSelected(pergunta.id, 2) }">2</button>
          <button type="button"
            v-on:click="change(pergunta.id,3)"
            v-bind:class="{ active: checkSelected(pergunta.id, 3) }">3</button>
          <button type="button"
            v-on:click="change(pergunta.id,4)"
            v-bind:class="{ active: checkSelected(pergunta.id, 4) }">4</button>
          <button type="button"
            v-on:click="change(pergunta.id,5)"
            v-bind:class="{ active: checkSelected(pergunta.id, 5) }">5</button>
          <input class="with-gap" v-bind:name="pergunta.id" type="radio" value="1" v-model="respostas[pergunta.id]" />
          <input class="with-gap" v-bind:name="pergunta.id" type="radio" value="2" v-model="respostas[pergunta.id]" />
          <input class="with-gap" v-bind:name="pergunta.id" type="radio" value="3" v-model="respostas[pergunta.id]"  />
          <input class="with-gap" v-bind:name="pergunta.id" type="radio" value="4" v-model="respostas[pergunta.id]" />
          <input class="with-gap" v-bind:name="pergunta.id" type="radio" value="5" v-model="respostas[pergunta.id]" />
        </div>

        <div class="divider"></div>
      </div>
      <button type="submit" class="btn">Enviar</button>
    </form>
  </section>
</template>

<script>
import M from 'materialize-css'

export default {
  name: 'Perfil',
  data: function () {
    return {
      cpf: null,
      nome: null,
      nascimento: null,
      genero: '',
      respostas: {},
      perguntas: [],
      errors: []
    }
  },
  methods: {
    getPerguntas: function () {
      this.$http.get('/api/v1/perguntas_perfil/')
        .then((response) => {
          this.perguntas = response.data
        })
    },
    checkForm: function (e) {
      this.errors = []
      if (Object.keys(this.respostas).length !== 18) {
        this.errors.push('Responda todas as perguntas do perfil')
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
    document.addEventListener('DOMContentLoaded', function () {
      M.FormSelect.init(document.querySelectorAll('select'))
    })
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
  }
  .respostas{
    display: flex;
  }
  .respostas button{
    width: 20%;
    border: 1px solid #ccc;
    padding: 10px 0;
  }
  .respostas button.active{
    background-color: #efefef;
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

  .errors{
    background-color: #ff7675;
    padding: 10px;
    color: #fff;
  }

  .errors ul{
    list-style-type: circle;
  }
  .errors li{
    list-style-type: circle !important;
    margin-left: 17px;
  }
</style>
