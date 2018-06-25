<template>
  <div id="app">
    <div class="content">
      <Menu></Menu>
      <main role="main">
        <nav class="navbar navbar-expand-lg navbar-dark">
          <a class="navbar-brand mx-auto" href="#">SiGECC</a>
        </nav>
        <router-view></router-view>
      </main>
    </div>
    <div class="loading mx-auto" v-if="$global.loading===true">
      <i class="fas fa-spinner fa-spin"></i> Carregando
    </div>
  </div>
</template>

<script>
import Menu from './components/Menu.vue'
export default {
  name: 'App',
  components: {
    'Menu': Menu
  }
}
</script>

<style>
html, body{height: 100%}

body{
    position: relative;
    background-color: #f7f7f7;
}

section{
  padding: 0 30px;
}

.navbar{
  background-color: #3a393a;
}

[role="main"] {
    margin-left: 180px
}

.loading{
    text-align: center;
    position: absolute;
    bottom:0;
    right:0;
    font-size: 10px;
    background-color: #ccc;
    border: 1px solid #ddd;
    padding: 2px 5px;
}
</style>
