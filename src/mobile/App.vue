<template>
  <div id="app">
    <!-- <a class="notification" v-on:click="showPopup()">
      <span class="msg">
        <b>Desafio concluído</b>
        <span class="details">Clique para ver mais</span>
      </span>
      <img src="@/assets/rocket.svg" alt="Missões">
    </a> -->
    
    <!-- <div class="header"> -->
      <!-- <i class="material-icons spin" v-if="$root.loading === true">autorenew</i> -->
      <!-- <Progressao /> -->
    <!-- </div> -->
    <div class="container">
      <div class="col s12">
        <router-view></router-view>
      </div>
    </div>
    <div class="popup" v-if="popup">
      <div class="overlay"></div>
      <div class="body">
        <h3 class="title">{{popup_title}}</h3>
        <div class="message" v-html="popup_message">{{popup_message}}</div>
        <div class="points" v-if="popup_points && $global.competicao">{{popup_points}} pts</div>
        <button class="btn" @click="execPopUpAction()">Continuar</button>
      </div>
    </div>
  </div>
</template>

<script>
  import Progressao from '@/mobile/components/Progressao'
  export default {
    name: 'App',
    components: {
      Progressao
    },
    data: function () {
      return {
        popup: false,
        popup_title: null,
        popup_message: null,
        popup_points: null,
        popup_action: null
      }
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
      },
      execPopUpAction () {
        if (this.popup_action) {
          this.popup_action()
          this.popup = false
        } else {
          this.popup = false
        }
      }
    },
    mounted () {
      this.start()
      this.$root.$on('sigecc:popup:open', (title, message, points, action) => {
        this.popup = true
        this.popup_title = title
        this.popup_message = message
        this.popup_points = points
        this.popup_action = action
      })
    }
  }
</script>
