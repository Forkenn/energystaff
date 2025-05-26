<script setup>
import TheWarningSign from './TheWarningSign.vue'

</script>

<template>
  <div class="page-content-wrapper">
    <div class="page-overlay">
      <div class="overlay-message">
        <TheWarningSign :red="true"/>
      </div>
    </div>
  </div>
</template>

<style scoped>

.page-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(6px);
  z-index: 1055;
}

</style>