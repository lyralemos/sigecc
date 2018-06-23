<template>
  <nav class="col-md-2 bg-light sidebar">
    <div class="sidebar-sticky">
      <ul class="nav flex-column">
        <li class="nav-item">
          <router-link to="/" class="nav-link active"><i class="fa fa-space-shuttle"></i> Ao vivo</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/alunos" class="nav-link"><i class="fas fa-graduation-cap"></i> Alunos</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/questoes" class="nav-link"><i class="fa fa-question-circle"></i> Questões</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/modulos" class="nav-link"><i class="fa fa-puzzle-piece"></i> Modulos</router-link>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
  export default {
    name: 'Menu'
  }
</script>

<style>
.sidebar {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    z-index: 100;
    padding: 48px 0 0;
    box-shadow: inset -1px 0 0 rgba(0, 0, 0, .1);
}

.sidebar .nav-link{
    color: #333;
}

.sidebar-sticky{
    position: sticky;
    top: 0;
    height: calc(100vh - 48px);
    padding-top: .5rem;
    overflow-x: hidden;
    overflow-y: auto;
}
</style>
