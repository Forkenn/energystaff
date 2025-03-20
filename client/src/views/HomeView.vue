<script setup>
import { onMounted } from 'vue';
import { useVacanciesStore } from '@/stores/vacancies';

import TheHeader from '@/components/global/TheHeader.vue'
import TheFooter from '@/components/global/TheFooter.vue'
import TheVacancyCard from '@/components/home/TheVacancyCard.vue';

const vacanciesStore  = useVacanciesStore();
onMounted(vacanciesStore.getVacancies);

</script>

<template>
  <TheHeader />
  <main>
    <div class="container container-pd52">
      <div class="home-wrapper">
        <div class="search-wrapper">
          <div class="row">
            <div class="col-auto">
              <button type="button" class="btn btn-primary sys-btn-288">Моё резюме</button>
            </div>
            <div class="col d-flex">
              <input type="text" class="form-control flex-grow-1 sys-input-810-flex" id="InputSearch" placeholder="Профессия, должность или компания">
            </div>
            <div class="col-auto">
              <button type="button" class="btn btn-primary sys-btn-150">Поиск</button>
            </div>
          </div>
        </div>
        <div class="main-wrapper">
          <div class="row">
            <div class="col-auto">
              <div class="filter-wrapper">

              </div>
            </div>
            <div class="col d-flex w-100" style="flex-direction: column;">
              <div v-if="vacanciesStore.vacancies.count" class="vacancy-wrapper">
                <TheVacancyCard v-for="vacancy in vacanciesStore.vacancies.items" :key="vacancy.id" :vacancy="vacancy"/>
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
        </div>
      </div>
    </div>
  </main>
  <TheFooter />
</template>

<style scoped>

.search-wrapper {
  margin-top: 55px;
}

.search-wrapper input {
  height: 48px;
}

.home-wrapper {
  margin-top: 55px;
  margin-bottom: 55px;
}

.filter-wrapper {
  width: 393px;
  height: 600px;
  border-color: #DBE0E5;
  border-width: 1px;
  border-style: solid;
  border-radius: 10px;
  background-color: #FFFFFF;
}

.vacancy-wrapper {
  min-width: 500px;
  max-width: 902px;
  min-height: 740px;
  width: 100%;
}

</style>