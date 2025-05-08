<script setup>
import { ref } from 'vue'
import TheModal from './TheModal.vue';

const showModalContacts = ref(false)
</script>

<template>
  <footer class="wrapper-footer">
    <div class="container container-pd52">
      <span class="footer-text">© 2024-2025 Все права защищены</span>
      <span class="footer-text left-group">
        <a href="#" style="margin-right: 8px;" @click.prevent="showModalContacts = true">Контакты</a>
        <span style="margin-right: 8px;">&bull;</span>
        <a target="_blank" href="/api/docs">API</a>
      </span>
    </div>
  </footer>

  <TheModal v-if="showModalContacts" @close="showModalContacts = false">
    <template #header>
      <h5 class="modal-title">Контактная информация</h5>
    </template>

    <p>По вопросам верификации: <a href="mailto:admin@example.com">admin@example.com</a></p>
    <p>По вопросам работы сервиса: <a href="mailto:support@example.com">support@example.com</a></p>
    <p>Телефон: +7 (800) 555-35-35</p>

    <template #footer>
      <button class="btn btn-secondary" @click="showModalContacts = false">Закрыть</button>
    </template>
  </TheModal>

</template>

<style scoped>

.wrapper-footer {
  background: #27282A;
  height: 90px;
  font-size: 16px;
  font-family: 'Montserrat';
}

.container {
  display: flex;
  align-items: center;
  height: 100%;
}

.modal-title {
  font-weight: 700 !important;
  color: #343434 !important;
}

.footer-text {
  color: #FFFFFF;
  font-weight: 400;
}

.left-group {
  margin-left: auto;
}

.left-group a {
  text-decoration: none;
  color: #FFFFFF;
}

.left-group a:hover {
  color: #B0B3B8;
}

</style>
