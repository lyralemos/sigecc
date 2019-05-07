<template>
  <div class="header">
    <div class="container">
      <div class="nivel">
        <img class="shield" src="@/assets/shield.svg" alt="Escudo" />
        <span class="numero">{{niveis[classificacao]}}</span>
      </div>
      <div class="progressao">
        <div class="classificacao">{{classificacao}}</div>
        <div class="barra">
          <div class="realizado" :style="{width: porcentagem+'%'}"></div>
        </div>
        <div class="pontos">
          <span v-if="$global.competicao">{{grupo.pontos}} pts - </span>
          <span>{{Math.ceil(porcentagem)}}%</span>
        </div>
      </div>
      <a class="rocket" @click="showDesafios">
        <img src="@/assets/rocket.svg" alt="Missões" />
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Progressao',
  data: function () {
    return {
      grupo: {},
      desafios: {},
      resolvidos: {},
      realizado: null,
      porcentagem: 0,
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
    update () {
      this.$http.get('/api/v1/grupos/status/')
        .then(response => {
          this.grupo = response.data.grupo
          this.desafios = this.grupo.desafios
          this.proximo_desafio = this.grupo.proximo_desafio
          this.porcentagem = (this.grupo.pontos * 100) / this.grupo.total

          if (this.$global.proximo_desafio !== this.proximo_desafio.id && this.grupo.questao) {
            this.$root.$emit('sigecc:popup:open', 'Novo desafio!!', this.proximo_desafio.nome, this.proximo_desafio.pontos)
            this.$global.proximo_desafio = this.proximo_desafio.id
          }
        })
    },
    appendToList (list, desafio, strike) {
      var item = document.createElement('tr')
      var nome = document.createElement('td')
      nome.appendChild(document.createTextNode(desafio.nome))
      if (strike) {
        nome.classList.add('strike')
      }
      item.appendChild(nome)
      if (this.$global.competicao) {
        var pontos = document.createElement('td')
        pontos.appendChild(document.createTextNode(desafio.pontos + ' pts'))
        item.appendChild(pontos)
      }
      list.appendChild(item)

      return list
    },
    showDesafios () {
      var list = document.createElement('table')
      for (var i = 0, len = this.desafios.length; i < len; i++) {
        var desafio = this.desafios[i]
        list = this.appendToList(list, desafio.desafio, true)
      }
      // proximo desafio
      this.appendToList(list, this.proximo_desafio, false)

      this.$root.$emit('sigecc:popup:open', 'Desafios', list.outerHTML)
    }
  },
  mounted () {
    this.$root.$on('sigecc:update', () => {
      this.update()
    })
    this.update()
  }
}
</script>
