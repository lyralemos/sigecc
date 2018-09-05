<template>
  <div id="app">
    <a class="notification" v-on:click="showPopup()">
      <span class="msg">
        <b>Desafio concluído</b>
        <span class="details">Clique para ver mais</span>
      </span>
      <img src="@/assets/rocket.svg" alt="Missões">
    </a>
    <div class="header">
      <i class="material-icons spin" v-if="$root.loading === true">autorenew</i>
      <img class="logo" src="@/assets/logo-silver.png" alt="Logo">

      <a class="rocket" v-on:click="showPopup">
        <img src="@/assets/rocket.svg" alt="Missões">
        <span class="dot">{{ $global.desafios.length - $global.resolvidos.length }}</span>
      </a>
    </div>
    <div class="container main">
      <div class="col s12">
        <router-view></router-view>
      </div>
    </div>
    <!-- <div class="loading" v-if="$root.loading === true">
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
    </div> -->
    <div class="popup-wrapper">
      <div class="missoes">
        <h5>Desafios</h5>
        <a class="close" href="#" v-on:click="closePopup"><i class="material-icons small">close</i></a>
        <ul class="missao-list">
          <li class="item" v-for="desafio in $global.desafios">
            <span v-bind:class="{ resolvido: $global.resolvidos.includes(desafio.id) }">{{ desafio.nome }}</span>
            <span class="new badge" data-badge-caption="pts" v-if="$global.competicao">{{ desafio.pontos }}</span>
          </li>
        </ul>
      </div>
      <div class="overlay" v-on:click="closePopup"></div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'App',
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
            this.$global.desafios = response.data.desafios
          })
      }
    }
  }
</script>

<style>

  @-webkit-keyframes fa-spin {
    0% {
      -webkit-transform: rotate(0deg);
      transform: rotate(0deg);
    }
    100% {
      -webkit-transform: rotate(359deg);
      transform: rotate(359deg);
    }
  }
  @keyframes fa-spin {
    0% {
      -webkit-transform: rotate(0deg);
      transform: rotate(0deg);
    }
    100% {
      -webkit-transform: rotate(359deg);
      transform: rotate(359deg);
    }
  }

  .spin {
    -webkit-animation: fa-spin 1s infinite linear;
    animation: fa-spin 1s infinite linear;
  }

  html, body, #app{height: 100%}

  body.popup{
    overflow: hidden;
  }

  #app > .container,
  #app > .container > .col{
    height: 100%;
  }

  #app{
    position: relative;
  }

  .header{
    padding: 15px 10px;
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

  .header .logo{
    vertical-align: middle;
    transform: translateX(-50%) translateY(-50%);
    position: absolute;
    left: 50%;
    top: 50%;
  }

  .header .rocket{
    width: 24px;
    height: 24px;
    display: block;
    float: right;
    position: relative;
  }

  .header .rocket img{
    position: relative;
    z-index: 2;
  }

  .header .dot{
    position: absolute;
    bottom: -10px;
    right: 0;
    font-size: 9px;
    background-color: #26a69a;
    color:#fff;
    padding: 3px 7px;
    border-radius: 10px;
    z-index: 1;
  }

  .header .trophy{
    float: left
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

  .popup-wrapper{
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    visibility: hidden;
    opacity: 0;
    transition: all .2s ease;
  }

  .popup-wrapper.show{
    visibility: visible;
    opacity: 1;
  }

  .overlay{
    position: absolute;
    top: 0;
    left: 0;
    background-color: #000;
    opacity: .4;
    width: 100%;
    height: 100%;
  }

  .missoes{
    position: absolute;
    width: 90%;
    top:50%;
    left: 50%;
    z-index: 2;
    transform: translateX(-50%) translateY(-50%);
    background-color: #fff;
    border-radius: 10px;
  }

  .missoes .close{
    float: right;
    color: #333;
    margin-top: -37px;
    margin-right: 10px;
  }

  .missoes h5{
    color:#333;
    margin: 0;
    padding: 10px 15px;
    border-bottom: 1px solid #ddd;
  }

  .missoes ul{
    margin-bottom: 7px;
  }

  .missao-list{
    margin: 0 !important;
  }

  .missao-list .item{
    padding: 10px 15px !important;
    border-bottom: 1px solid #ddd;
  }

  .missao-list .item:last-child{
    border-bottom: none
  }

  .missao-list .resolvido{
    text-decoration: line-through;
  }

  .notification{
    position: absolute;
    top: -10px;
    width: 90%;
    left:50%;
    padding: 10px;
    transform: translateX(-50%);
    background-color: #efefef;
    border: 1px solid #ddd;
    border-radius: 5px;
    transition: all .2s ease;
    color: #000;
  }

  .notification.show{
    top: 65px;
  }

  .notification .msg{
    float: left;
  }

  .notification .details{
    display: block;
    font-size: 10px;
  }

  .notification img{
    float: right;
  }


</style>
