<template>
  <div id="app">
    <div class="container">
      <div class="col s12">
        <div class="header center-align">
          <img src="@/assets/logo-silver.png" alt="Logo">
          <h5 class="titulo">Sistema Experimental</h5>
        </div>
        <router-view></router-view>
      </div>
    </div>
    <div class="loading" v-if="$root.loading === true">
      <div class="preloader-wrapper big active">
        <div class="spinner-layer spinner-blue-only">
          <div class="circle-clipper left">
            <div class="circle"></div>
          </div><div class="gap-patch">
            <div class="circle"></div>
          </div><div class="circle-clipper right">
            <div class="circle"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'App',
    updated () {
      if (this.$global.liberado && !localStorage.getItem('user-token')) {
        this.$router.push('/login')
      }
    },
    mounted () {
      this.start()
    },
    methods: {
      start: function () {
        this.$http.get('/api/v1/modulos/ativo')
          .then((response) => {
            if (response.data.error) {
              this.$router.push('/fechado')
            }
            this.$global.liberado = response.data.liberado
            this.$global.competicao = response.data.competicao
            this.$global.colaboracao = response.data.colaboracao
          })
      }
    }
  }
</script>

<style>
  html, body, #app{height: 100%}

  .titulo{
    font-family: 'Dosis', sans-serif;
  }

  #app > .container,
  #app > .container > .col,
  #app > .container > .col > section{
    height: 100%;
  }

  .header{
    padding: 20px 0;
  }

  .loading{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: #fff;
    opacity: .9;
    z-index: 100;
  }

  .preloader-wrapper{
    position: absolute;
    top:50%;
    left: 50%;
    margin-left: -32px;
    margin-top: -32px;
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
