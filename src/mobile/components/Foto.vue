<template>
  <section class="centered center">
    <h5 v-if="!$global.colaboracao">Escolha uma foto para você</h5>
    <h5 v-if="$global.colaboracao">Escolha uma foto para o seu grupo</h5>

    <canvas ref="canvas" id="canvas" width="240" height="240"></canvas>
    <input class="image-input" ref="capture" @change="loadPicture" type="file" accept="image/*" capture>
    
    <div v-if="picture">
      <img class="circle" ref="picture" :src="picture"  /><br /><br />
      <button type="button" class="btn" @click="save">Salvar</button> <br /><br />
    </div>
    <button class="btn" @click="abrirCamera">
      <i class="material-icons">camera_alt</i>
    </button>
  </section>
</template>

<script>
export default {
  name: 'Foto',
  data: function () {
    return {
      video: null,
      canvas: {},
      captures: [],
      picture: null
    }
  },
  methods: {
    loadPicture (evt) {
      var self = this
      var file = evt.target.files[0]
      var img = document.createElement('img')
      var reader = new FileReader()

      reader.onload = function (e) {
        img.onload = function (e) {
          var xStart = 0
          var yStart = 0
          var aspectRadio
          var newWidth
          var newHeight
          var canvas = self.$refs.canvas
          var ctx = canvas.getContext('2d')
          // ctx.drawImage(img, 0, 0)

          var width = 240
          var height = 240

          canvas.width = width
          canvas.height = height

          aspectRadio = img.height / img.width

          if (img.height < img.width) {
            // horizontal
            aspectRadio = img.width / img.height
            newHeight = height
            newWidth = aspectRadio * height
            xStart = -(newWidth - width) / 2
          } else {
            // vertical
            newWidth = width
            newHeight = aspectRadio * width
            yStart = -(newHeight - height) / 2
          }

          ctx.drawImage(img, xStart, yStart, newWidth, newHeight)

          self.picture = canvas.toDataURL('image/png', 0.75)
        }
        img.src = e.target.result
      }
      reader.readAsDataURL(file)
    },
    start () {
      this.picture = null
      // this.video = document.getElementById('video')
      // if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      //   navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
      //     this.video.srcObject = stream
      //   })
      // }
    },
    stop () {
      this.video.srcObject.getTracks().forEach(track => track.stop())
      this.video.srcObject = null
    },
    abrirCamera () {
      this.$refs.capture.click()
    },
    save () {
      this.$http.patch('/api/v1/grupos/foto/', {foto: this.picture})
        .then(response => {
          if (response.data.result) {
            this.$router.push('/espera')
          }
        })
    }
  },
  mounted () {
    this.start()
  }
}
</script>

<style>

#video {
  background-color: #000000;
  width: 100%;
  }

#canvas {
    display: none;
}
li {
    display: inline;
    padding: 5px;
}

.circle {
  border-radius: 50%;
}

.image-input {
  display:none;
}


</style>
