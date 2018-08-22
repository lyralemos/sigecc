var isLoggedMixin = {
  created: function () {
    this.checkIfLogged()
  },
  methods: {
    checkIfLogged () {
      if (!localStorage.getItem('user-token')) {
        this.$router.push('/login')
      }
    }
  }
}

export default isLoggedMixin
