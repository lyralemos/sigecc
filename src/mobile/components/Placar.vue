<template>
  <div class="placar">
    <div class="acao">
      <i class="material-icons arrow up" @click="mostraPlacar">keyboard_arrow_up</i>
      <i class="material-icons arrow down" @click="mostraPlacar">keyboard_arrow_down</i>
    </div>
    <ul>
      <li v-for="(p, index) in placar" v-bind:class="{ selected: p.marcar }">
        <a>
          <i class="material-icons person">person_pin</i>
          <div class="info">
            <span class="posicao">{{ index+1 }}º</span>
            <div class="dados">
              <b>Colocado</b> ({{p.pontos}} pts) <br>
              <span class="nome">{{ p.grupo.__str__ }}</span>
              <i class="material-icons star" v-if="p.marcar">star</i>
            </div>
          </div>
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
  export default {
    name: 'Placar',
    data: function () {
      return {
        placar: null,
        intervalo_placar: null
      }
    },
    mounted () {
      this.startPlacar()
    },
    beforeDestroy () {
      clearInterval(this.intervalo_placar)
      var main = document.getElementsByClassName('main')
      main[0].classList.remove('competicao')
    },
    methods: {
      getPlacar: function () {
        if (this.$global.competicao) {
          this.$http.get('/api/v1/placar/', { headers: {'X-No-Loading': 'true'} })
          .then((response) => {
            this.placar = response.data
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
        var placar = document.querySelector('.placar')
        placar.classList.toggle('mostrar')
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
  padding: 0 20px;
  transition: all .2s ease;
  /* top: 82%; */
  height: 90px;
  overflow-y: auto;
}

.placar .acao{
  text-align: center;
}

.placar.mostrar{
  height: 90%;
}

.placar .down{
  display:none;
}

.placar ul{
  margin-top:0;
}

.placar.mostrar li{
  display: block !important;
}

.placar.mostrar .down{
  display: inline-block;
}

.placar.mostrar .up{
  display: none;
}

.placar li{
  display: none;
  margin-bottom: 15px;
  position: relative;
}

.placar li.selected{
  display: block;
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

.placar i.star{
  position: absolute;
  right: 10px;
  top:50%;
  transform: translateY(-50%);
}

.placar a{
  color:#333;
  display: table;
  width: 100%;
}

.placar .info{
  display: table-cell;
  vertical-align: middle;
  width: 100%;
}

.placar .posicao{
  font-size: 40px;
  margin-right: 5px;
}

.placar .dados{
  display: inline-block;
}
</style>
