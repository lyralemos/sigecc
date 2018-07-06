<template>
  <section class="center-align">
    <div class="inicio">
      <button @click="iniciar" class="btn waves-effect waves-light pulse">Começar</button>
    </div>

  </section>
</template>

<script>
  export default {
    name: 'Home',
    methods: {
      iniciar: function () {
        if (!this.$global.liberado) {
          if (localStorage.getItem('user-token')) {
            this.$router.push('/espera')
          } else {
            this.$router.push('/perfil')
          }
        } else if (localStorage.getItem('user-token')) {
          this.$router.push('/pergunta')
        }
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
  }
</style>
