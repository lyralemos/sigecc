<template>
  <section>
    <form method="post" @submit.prevent="login">
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
          <router-link to="/cadastro" v-if="$global.liberado == false">Cadastre-se</router-link>
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
        'password': null
      }
    },
    methods: {
      login: function (e) {
        this.$http.post('/api/api-token-auth/', {
          'username': this.username,
          'password': this.password
        })
          .then((response) => {
            const token = response.data.token
            localStorage.setItem('user-token', token)
            this.$router.push('/')
          })
          .catch((err) => {
            localStorage.removeItem('user-token')
            console.log(err)
          })
        e.preventDefault()
      }
    }
  }
</script>
