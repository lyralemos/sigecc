<template>
  <section class="center-align">
    <div class="inicio">
      <h5><b>Bem vindo ao Sistema Experimental!</b></h5>
      <p class="left-align">
        Hoje iremos realizar uma tarefa para testar seus conhecimentos de uma forma interativa.
        Para iniciar basta clicar no botão abaixo e seguir as instruções na tela. <br />
      </p>
      <button @click="iniciar" class="btn waves-effect waves-light pulse">Começar</button>
    </div>

  </section>
</template>

<script>
  import isLoggedMixin from '../loggedin'

  export default {
    name: 'Home',
    mixins: [isLoggedMixin],
    methods: {
      iniciar: function () {
        if (localStorage.getItem('perfil')) {
          this.$router.push('/espera')
        } else {
          this.$router.push('/perfil')
        }
        // if (!this.$global.liberado) {
        //   if (localStorage.getItem('user-token')) {
        //     this.$router.push('/espera')
        //   } else {
        //     this.$router.push('/perfil')
        //   }
        // } else if (localStorage.getItem('user-token')) {
        //   this.$router.push('/pergunta')
        // }
      }
    }
  }
</script>

<style>
  .inicio{
    width: 100%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translateX(-50%) translateY(-50%);
    padding: 15px;
  }
</style>
