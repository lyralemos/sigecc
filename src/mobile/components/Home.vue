<template>
  <section class="center-align">
    <div class="inicio">
      <router-link to="/perfil" class="btn waves-effect waves-light pulse">Começar</router-link>
    </div>

  </section>
</template>

<script>
  export default {
    name: 'Home'
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
