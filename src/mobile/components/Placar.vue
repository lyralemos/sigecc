<template>
  <div :class="klass" @click="mostraPlacar">
    <div class="acao">
      <i class="material-icons arrow up">keyboard_arrow_up</i>
      <i class="material-icons arrow down">keyboard_arrow_down</i>
    </div>
    <ul>
      <transition-group name="list">
      <li v-for="(p, index) in placar" v-bind:class="{ selected: p.marcar }" v-bind:key="p.id">
        <a>
          <img class="circle" :src="p.grupo.foto" alt="" v-if="p.grupo.foto">
          <img class="circle" src="@/assets/desconhecido.png" alt="" v-if="!p.grupo.foto">
          <span class="posicao">{{ index+1 }}º</span>
        </a>
        <div class="info">
          <span class="nome">{{ p.grupo.__str__ }}</span>
          <div class="barra">
            <div class="realizado" :style="{width: (p.pontos * 100) / p.grupo.total + '%'}"></div>
          </div>
          <span class="pontos">({{p.pontos}} pts) - {{Math.ceil((p.pontos * 100) / p.grupo.total)}}%</span>
        </div>
      </li>
      </transition-group>
    </ul>
  </div>
</template>

<script>
  export default {
    name: 'Placar',
    data: function () {
      return {
        placar: null,
        intervalo_placar: null,
        klass: {
          placar: true,
          full: false
        }
      }
    },
    mounted () {
      this.startPlacar()
    },
    beforeDestroy () {
      clearInterval(this.intervalo_placar)
      // var main = document.getElementsByClassName('main')
      // main[0].classList.remove('competicao')
    },
    methods: {
      getPlacar: function () {
        if (this.$global.competicao) {
          this.$http.get('/api/v1/placar/', { headers: {'X-No-Loading': 'true'} })
          .then((response) => {
            this.placar = response.data
            setTimeout(function () {
              var selected = document.querySelector('li.selected')
              if (selected) {
                var selectedPosition = selected.getBoundingClientRect()
                if (selectedPosition.x > 400 || selectedPosition.x < 0) {
                  document.querySelector('.placar ul').scroll(selectedPosition.x, 0)
                }
              }
            }, 1000)
          })
          .catch((err) => {
            console.log(err)
          })
        }
      },
      startPlacar: function () {
        // ajusta o main para o placar
        var main = document.getElementsByClassName('main')
        main[0].classList.add('competicao')

        this.intervalo_placar = setInterval(function () {
          this.getPlacar()
        }.bind(this), 10000)
        this.getPlacar()
      },
      mostraPlacar: function () {
        this.klass.full = !this.klass.full
      }
    }
  }
</script>

<style>
.placar{
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: #d8d8d8;
  /* padding: 0 20px; */
  height: 90px;
  overflow-y: auto;
  transition: .2s all ease;
}

.placar .acao{
  text-align: center;
  height: 24px;
}

.placar .info{display:none}


.placar .down{
  display:none;
}

.list-move {
  transition: .2s all ease;
}

.placar ul{
  margin-top:0;
  margin-bottom: 0;
  width:100%;
  height: 51px;
  padding-left:20px;
  overflow-x: scroll;
  overflow-y: hidden;
  white-space: nowrap;
}

.placar ul::-webkit-scrollbar {
    display: none;
  }

.placar li{
  display: inline-block;
  width: 45px;
  margin-right: 19px;
  padding: 0;
}

.placar i.arrow{
  color:#555;
  text-align: center;
  font-size: 24px;
}

.placar i.person{
  font-size: 4em;
  margin-right: 10px;
}

.placar img {
  width: 40px;
  height: 40px;
}

.placar a{
  color:#333;
  display: inline-block;
  position: relative;
}

.placar .posicao{
  position: absolute;
  right: -5px;
  bottom: 4px;
  display:inline-block;
  text-align: center;
  width: 25px;
  padding: 2px 0;
  color:#fff;
  font-size: 14px;
  background-color: #19A59A;
  border-radius: 50%;
}

.placar li.selected{
  width: 56px;
}

.placar li.selected img{
  width: 50px;
  height: 50px;
  border: 3px solid #19A59A;
}

.placar li.selected .posicao{
  font-size: 19px;
  width: 29px;
}

.placar.full{
  height: 90%;
}

.placar.full .down{
  display: inline-block;
}

.placar.full .up{
  display: none;
}

.placar.full .info{
  display:block;
  float: left;
  margin-left: 10px;
  width: calc(100% - 65px)
}

.placar.full ul{
  height: inherit;
  overflow: inherit;
  /* height: 100%; */
  padding-right: 20px;
}

.placar.full li{
  display: block;
  width: 100%;
  margin-bottom: 14px;
  overflow: auto
}

.placar.full a{
  float: left;
  width: 55px;
}

.placar.full .posicao{
  right: 0;
}

.placar.full .barra{
  background-color: #979797;
  height: 6px;
  position: relative;
  width: 100%;
}

.placar.full .realizado{
  background-color: #46A69A;
  position: absolute;
  top: 0;
  left: 0;
  height: 6px;
  transition: .2s all ease;
}

.placar.full .nome{
  font-size: 16px;
  font-weight: bold;
}

.placar.full .pontos{
  font-size:11px;
}

</style>
