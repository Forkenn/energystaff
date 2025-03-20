<script setup>
import { onMounted } from 'vue';
import { useNegotiationsStore } from '@/stores/negotiations';

import TheHeader from '@/components/global/TheHeader.vue'
import TheFooter from '@/components/global/TheFooter.vue'
import TheVacancyCard from '@/components/home/TheVacancyCard.vue';

const negotiationsStore  = useNegotiationsStore();
onMounted(negotiationsStore.getNegotiations);

</script>

<template>
  <TheHeader />
  <main>
    <div class="container container-pd52">
      <div class="negotiations-container">
        <div class="tabs-wrapper">
          <ul class="nav nav-pills">
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="#">Все</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">В ожидании</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Приглашения</a>
            </li>
          </ul>
        </div>
        <div class="negotiations-wrapper">
          <TheVacancyCard v-for="vacancy in negotiationsStore.negotiations.items" :key="vacancy.id" :vacancy="vacancy"/>
        </div>
        <nav aria-label="Навигация" style="margin: 0 auto;">
          <ul class="pagination">
            <li class="page-item"><a class="page-link" href="#">1</a></li>
            <li class="page-item"><a class="page-link" href="#">2</a></li>
            <li class="page-item"><a class="page-link" href="#">3</a></li>
          </ul>
        </nav>
      </div>
    </div>
  </main>
  <TheFooter />
</template>

<style scoped>

.negotiations-container {
  margin-top: 55px;
  margin-bottom: 55px;
}

.tabs-wrapper {
  margin-bottom: 30px;
}

.negotiations-wrapper {
  display: flex;
  flex-direction: column;
}

</style>