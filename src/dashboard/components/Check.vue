<template lang="html">
  <span>
    <span class="badge badge-pill badge-success" v-if="bool===true">
      <i class="fas fa-check"></i>
    </span>
    <span class="badge badge-pill badge-danger" v-if="bool===false">
      <i class="fa fa-times"></i>
    </span>
  </span>
</template>

<script>
export default {
  name: 'Check',
  props: ['bool']
}
</script>
