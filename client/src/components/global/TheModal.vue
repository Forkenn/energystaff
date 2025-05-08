<script setup>
import { onMounted, onBeforeUnmount } from 'vue'

const emit = defineEmits(['close'])
const close = () => emit('close')

const handleKeydown = (event) => {
  if (event.key === 'Escape') {
    close()
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <div class="modal-backdrop fade show"></div>
  <div class="modal fade show d-block" tabindex="-1" @click.self="close">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <slot name="header">
            <h5 class="modal-title">Заголовок</h5>
          </slot>
          <!--<button type="button" class="btn-close" @click="close"></button>-->
        </div>
        <div class="modal-body">
          <slot>
            Основное содержимое модального окна.
          </slot>
        </div>
        <div class="modal-footer">
          <slot name="footer">
            <button type="button" class="btn btn-secondary" @click="close">Закрыть</button>
          </slot>
        </div>
      </div>
    </div>
    <!--<div class="modal-backdrop fade show"></div>-->
  </div>
</template>

<style scoped>

.modal-content {
  font-family: "Montserrat"
}

.modal-title {
  font-weight: 700 !important;
  color: #343434 !important;
}

</style>