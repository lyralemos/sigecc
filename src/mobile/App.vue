<template>
  <div id="app">
    <div class="header">
      <img src="@/assets/logo-silver.png" alt="Logo">
      <h5 class="titulo">Sistema Experimental</h5>
    </div>
    <div class="container main">
      <div class="col s12">
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
      // if (!localStorage.getItem('user-token')) {
      //   this.$router.push('/login')
      // }
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

  #app > .container,
  #app > .container > .col{
    height: 100%;
  }

  #app{
    position: relative;
  }

  .header{
    padding: 10px 0;
    background-color: #f1f1f1;
    border-bottom: 1px solid #ddd;
    position: fixed;
    top:0;
    left: 0;
    width: 100%;
  }

  .titulo{
    font-family: 'Dosis', sans-serif;
    margin: 0;
    display: inline-block;
    vertical-align: middle;
    margin-left: 10px;
  }

  .header img{
    vertical-align: middle;
    margin-left: 10px;
  }

  .main{
    padding-top: 80px;
  }

  .competicao{
    height: calc(100%  - 90px) !important;
    overflow-y: auto;
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
