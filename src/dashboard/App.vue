<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
      <a class="navbar-brand mx-auto" href="#">Dashboard - SiGECC</a>
    </nav>
    <div class="container-fluid">
      <div class="row">
        <Menu></Menu>
        <main role="main" class="col-md-9 ml-sm-auto col-lg-10 px-4">
          <router-view></router-view>
        </main>
      </div>
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
}

[role="main"] {
    padding-top: 56px;
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

.destaque{
    font-size: 30px;
    padding-left: 35px;
}
</style>
