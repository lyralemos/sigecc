<template>
  <section>
    <div class="thumbs">
      <span class="material-icons large">thumb_up</span>
    </div>
    <div class="obrigado">
      <h5>Obrigado por participar!</h5>
      <h6 v-if="$global.competicao == true">Confira abaixo a sua posição no ranking</h6>
    </div>
    <Placar v-if="$global.competicao == true"></Placar>
  </section>
</template>

<script>
  import isLoggedMixin from '../loggedin'
  import Placar from './Placar'

  export default {
    name: 'Final',
    mixins: [isLoggedMixin],
    components: { Placar },
    mounted () {
      this.updateDesafios()
    }
  }
</script>

<style>
  .thumbs{text-align: center; margin-top:15px}
  span.material-icons{
    font-size: 130px;
    background-color: #eee;
    border-radius: 90px;
    border: 1px solid #ddd;
    padding: 20px;
  }

  .obrigado{
    text-align: center;
    padding: 10px 0;
  }
</style>
