<template>
  <section class="center-align">
    <div class="centered">
      <h5><b>Bem vindo ao Sistema Experimental!</b></h5>
      <p style="text-align:justify">
        Hoje iremos realizar uma tarefa diferente! Para testar seus conhecimentos
        de uma forma interativa vamos participar de um jogo.<br /><br />

        Você será desafiado com questões objetivas e terá que respondê-las
        para conseguir avançar.
        <span v-if="$global.competicao">
          Acerte as questões em troca de pontos e ganhar dos seus colegas!!
        </span>
        <br /><br />

        Avance no jogo com atenção aos <a href="#" v-on:click="showPopup">desafios</a> e divirta-se.

      </p>
      <button @click="iniciar" class="btn waves-effect waves-light pulse">Começar</button>
    </div>

  </section>
</template>

<script>
  export default {
    name: 'Home',
    methods: {
      iniciar: function () {
        var status = localStorage.getItem('status') || '/perfil'
        this.$router.push(status)
        // if (localStorage.getItem('perfil')) {
        //   this.$router.push('/espera')
        // } else {
        //   this.$router.push('/perfil')
        // }
      }
    }
  }
</script>

<style>
</style>
