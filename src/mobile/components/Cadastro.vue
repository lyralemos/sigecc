<template>
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
          <label for="id_cpf">Usuário</label>
          <span class="helper-text" data-error="wrong" data-success="right">Sugestão: use sua matrícula</span>
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
            <option value="M">Masculino</option>
            <option value="F">Feminino</option>
          </select>
          <label>Sexo</label>
        </div>

        <div class="divider"></div>

        <button type="submit" class="btn">Registrar</button>
      </div>
    </form>
  </section>
</template>

<script>
  import M from 'materialize-css'

  export default {
    name: 'Cadastro',
    data: function () {
      return {
        cpf: null,
        nome: null,
        nascimento: null,
        genero: '',
        errors: []
      }
    },
    mounted: function () {
      M.FormSelect.init(document.querySelectorAll('select'))
    },
    methods: {
      checkForm: function (e) {
        this.errors = []
        this.$http.post('/api/v1/alunos/', {
          'cpf': this.cpf,
          'nome': this.nome,
          'nascimento': this.nascimento,
          'genero': this.genero
        }).then((response) => {
          var token = response.data.token
          localStorage.setItem('user-token', token)
          this.$router.push('/espera')
        }).catch((err) => {
          this.errors = err.data.errors
        })
        window.scrollTo(0, 0)
        e.preventDefault()
      }
    }
  }
</script>

<style scoped>
  button[type="submit"]{
    width: 100%;
    margin-bottom: 20px;
  }
</style>
