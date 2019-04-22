<template>
  <section class="centered center">
    <h5 v-if="!$global.colaboracao">Escolha uma imagem para você</h5>
    <h5 v-if="$global.colaboracao">Escolha uma imagem para o seu grupo</h5>
    <div class="capture" v-if="!picture">
      <div class="video-wrapper">
        <video ref="video" id="video" autoplay></video>
      </div>
      <div class="center">
        <button type="button" class="btn" id="snap" @click="capture()">
          <i class="material-icons">camera_alt</i>
        </button>
      </div>
    </div>
    <canvas ref="canvas" id="canvas" width="240" height="240"></canvas>
    <div v-if="picture">
      <img class="circle" ref="picture" :src="picture"  /><br /><br />
      <button type="button" class="btn" @click="save">Salvar</button> <br /><br />
      <button type="button" class="btn" @click="$router.go()">Outra foto</button>
    </div>
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
    snapshotResize: function (video, width, height) {
      var canvas = this.$refs.canvas
      var ctx = canvas.getContext('2d')
      var xStart = 0
      var yStart = 0
      var aspectRadio
      var newWidth
      var newHeight

      // video.src  = srcData;
      canvas.width = width
      canvas.height = height

      aspectRadio = video.videoHeight / video.videoWidth

      if (video.videoHeight < video.videoWidth) {
        // horizontal
        aspectRadio = video.videoWidth / video.videoHeight
        newHeight = height
        newWidth = aspectRadio * height
        xStart = -(newWidth - width) / 2
      } else {
        // vertical
        newWidth = width
        newHeight = aspectRadio * width
        yStart = -(newHeight - height) / 2
      }

      ctx.drawImage(video, xStart, yStart, newWidth, newHeight)

      return canvas.toDataURL('image/png', 0.75)
    },
    capture () {
      this.canvas = this.$refs.canvas
      this.picture = this.snapshotResize(this.video, 240, 240)
      this.stop()
    },
    start () {
      this.picture = null
      this.video = document.getElementById('video')
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
          this.video.srcObject = stream
        })
      }
    },
    stop () {
      this.video.srcObject.getTracks().forEach(track => track.stop())
      this.video.srcObject = null
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


</style>
