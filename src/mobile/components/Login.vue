<template>
  <section class="centered">
    <form method="post" @submit.prevent="login">
      <p class="errors" v-if="errors.length">
        <b>Por favor corrija os seguintes erros</b>
        <ul>
          <li v-for="error in errors">{{ error }}</li>
        </ul>
      </p>
      <div class="row">
        <div class="input-field col s12">
          <input id="id_username"
            type="text"
            v-model="username"
            required>
          <label for="id_username">Usuário</label>
        </div>

        <div class="input-field col s12">
          <input id="id_password"
            type="password"
            v-model="password"
            required>
          <label for="id_password">Senha</label>
        </div>
        <div class="center-align">
          <button type="submit" class="btn">Entrar</button> <br /><br />
          <router-link to="/cadastro" v-if="$global.liberado == false" class="waves-effect waves-teal btn-flat">Cadastre-se</router-link>
        </div>
      </div>
    </form>
  </section>
</template>

<script>
  export default {
    name: 'Login',
    data: function () {
      return {
        'username': null,
        'password': null,
        errors: []
      }
    },
    methods: {
      login: function (e) {
        this.errors = []
        this.$http.post('/api/api-token-auth/', {
          'username': this.username,
          'password': this.password
        })
          .then((response) => {
            const token = response.data.token
            localStorage.setItem('user-token', token)
            if (this.$global.liberado) {
              if (this.$global.competicao) {
                this.$router.push('/foto')
              } else {
                this.$router.push('/pergunta')
              }
            } else {
              this.$router.push('/espera')
            }
          })
          .catch((err) => {
            localStorage.removeItem('user-token')
            this.errors = err.data.non_field_errors
          })
        e.preventDefault()
      }
    }
  }
</script>
