<template>
  <nav class="sidebar">
    <div class="sidebar-sticky">
      <div class="logo">
        <img src="@/assets/logo.png"><br>
        Dashboard
      </div>
      <ul class="nav flex-column">
        <li class="nav-item">
          <router-link to="/" class="nav-link active"><i class="fas fa-home"></i> Home</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/alunos" class="nav-link"><i class="fas fa-graduation-cap"></i> Alunos</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/grupos" class="nav-link"><i class="fas fa-users"></i> Grupos</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/questoes" class="nav-link"><i class="fas fa-question-circle"></i> Questões</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/modulos" class="nav-link"><i class="fas fa-puzzle-piece"></i> Modulos</router-link>
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
.logo{
  font-size: 20px;
  color:#fff;
  text-align: center;
  background-color: #292929;
  padding: 20px 0;
}

.sidebar {
    width: 180px;
    background: #3a393a;
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    z-index: 100;
    box-shadow: inset -1px 0 0 rgba(0, 0, 0, .1);
}

.sidebar .nav-link{
    color: #ecf8fc;
}

.sidebar .nav-link:hover{
    background-color: #27b756;
}

.sidebar-sticky{
    position: sticky;
    top: 0;
    height: 100vh;
    overflow-x: hidden;
    overflow-y: auto;
}
</style>
