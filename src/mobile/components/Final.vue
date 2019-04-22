<template>
  <section class="centered">
    <div class="placar">
      <div class="step">
        <div class="space"></div>
        <div class="segundo" v-if="segundo">
          <img class="circle" :src="segundo.grupo.foto" alt="" v-if="segundo.grupo.foto">
          <img class="circle" src="@/assets/desconhecido.png" alt="" v-if="!segundo.grupo.foto">
          <span>{{segundo.grupo.__str__}}</span>
          <span class="posicao">2º</span>
        </div>
      </div>
      <div class="step">
        <div class="space"></div>
        <div class="primeiro" v-if="primeiro">
          <img class="circle" :src="primeiro.grupo.foto" alt="" v-if="primeiro.grupo.foto">
          <img class="circle" src="@/assets/desconhecido.png" alt="" v-if="!primeiro.grupo.foto">
          <span>{{primeiro.grupo.__str__}}</span>
          <span class="posicao">1º</span>
        </div>
      </div>
      <div class="step">
        <div class="space"></div>
        <div class="terceiro" v-if="terceiro">
          <img class="circle" :src="terceiro.grupo.foto" alt="" v-if="terceiro.grupo.foto">
          <img class="circle" src="@/assets/desconhecido.png" alt="" v-if="!terceiro.grupo.foto">
          <span>{{terceiro.grupo.__str__}}</span>
          <span class="posicao">3º</span>
        </div>
      </div>
    </div>

    <hr v-if="$global.competicao" />

    <div class="progresso">
      <h5>Confira o seu desempenho final</h5>
      <div class="nivel">
        <img class="shield" src="@/assets/shield.svg" alt="Escudo" />
        <span class="numero">{{niveis[classificacao]}}</span>
        <div class="classificacao">{{classificacao}}</div>
      </div>
      <div class="barra">
        <div class="realizado" :style="{width: porcentagem+'%'}"></div>
      </div>
      <div class="pontos">
        <span v-if="$global.competicao">{{grupo.pontos}} pts - </span>
        <span>{{Math.ceil(porcentagem)}}%</span>
      </div>
      <div class="desafios">
        <h6>Desafios realizados</h6>
        <table>
          <tr v-for="desafio in desafios" :key="desafio.id">
            <td class="strike">{{desafio.desafio.nome}}</td>
            <td v-if="$global.competicao">{{desafio.desafio.pontos}} pts</td>
          </tr>
        </table>
      </div>
    </div>
  </section>
</template>

<script>
  import isLoggedMixin from '../loggedin'
  import Placar from './Placar'

  export default {
    name: 'Final',
    mixins: [isLoggedMixin],
    components: { Placar },
    data: function () {
      return {
        grupo: {},
        desafios: {},
        porcentagem: 0,
        placar: {},
        primeiro: null,
        segundo: null,
        terceiro: null,
        niveis: {
          'Novato': 1,
          'Iniciante': 2,
          'Intermediário': 3,
          'Especialista': 4,
          'Ninja': 5
        }
      }
    },
    computed: {
      classificacao () {
        var pts = this.grupo.pontos
        switch (true) {
          case (pts <= 6):
            return 'Novato'
          case (pts > 6 && pts <= 20):
            return 'Iniciante'
          case (pts > 20 && pts <= 33):
            return 'Intermediário'
          case (pts > 33 && pts <= 54):
            return 'Especialista'
          case (pts > 88):
            return 'Ninja'
        }
      }
    },
    methods: {
      getGroupData () {
        this.$http.get('/api/v1/grupos/status')
          .then(response => {
            this.grupo = response.data.grupo
            this.desafios = this.grupo.desafios
            this.porcentagem = (this.grupo.pontos * 100) / this.grupo.total
          })
      },
      getPlacar () {
        this.$http.get('/api/v1/placar/')
          .then((response) => {
            this.placar = response.data
            this.primeiro = this.placar[0]
            this.segundo = this.placar[1]
            this.terceiro = this.placar[2]
          })
      }
    },
    mounted () {
      this.getGroupData()
      this.getPlacar()
    }
  }
</script>

<style scoped>

  .nivel{
    position: relative;
    text-align: center;
    margin: 20px 0;
  }
  .shield{
    width: 100px;
  }
  .numero {
    color:#fff;
    font-size: 60px;
    position: absolute;
    top:10px;
    left: 50%;
    transform: translateX(-50%);
  }

  .classificacao{
    font-size: 20px;
  }

  .barra{
    height: 20px;
    background-color: #cecece;
  }
  .realizado{
    background-color: #46A69A;
    height: 20px;
    transition: .2s all ease;
  }

  .desafios{
    background-color: #cecece;
    padding: 10px 15px;
    border-radius: 20px;
    margin-top:20px;
  }

  .desafios table{
    font-size: 13px;
  }

  .desafios td{
    padding-top: 10px 
  }

  .desafios h6{font-weight: bold}

  .strike{
    text-decoration: line-through;
  }

  .placar{
    margin: 0 auto;
    display: flex;
    height: 250px;
    width: 80%;
    margin-bottom: 30px;
  }

  .step{
    flex: 1;
    display: flex;
    flex-direction: column;
    position: relative;
  }

  .step .space{
    margin-top: auto;
    text-align: center;
  }

  .step .primeiro,
  .step .segundo,
  .step .terceiro{
    padding: 10px;
    text-align: center;
    color: #fff;
  }

  .primeiro{
    height: 90%;
    background-color: #46A69A;
    
  }

  .segundo{
    height: 75%;
    background-color: #0accb3;
  }

  .terceiro{
    height: 70%;
    background-color: #0accb3;
  }

  .posicao{
    position: absolute;
    bottom: 15px;
    left: 50%;
    transform: translateX(-50%);
    display: block;
    line-height: 36px;
    font-size: 50px;
  }

  .circle{
    width: 60px;
    display: block;
    margin: 0 auto 10px;
  }

</style>
