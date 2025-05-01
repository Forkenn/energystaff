<script setup>
import { onMounted, ref, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';

import TheHeader from '@/components/global/TheHeader.vue'
import TheFooter from '@/components/global/TheFooter.vue'
import ThePaginator from '@/components/global/ThePaginator.vue';
import TheVacancyCard from '@/components/home/TheVacancyCard.vue';
import VacanciesService from '@/services/vacancies.service';

const route = useRoute();
const router = useRouter();

const filters = ref({ "q": "", "start": 0, "end": 50 });
const vacancies = ref({ "count": 0, "items": [] });

const totalVacanciesCount = ref(0)
const perPage = 6

// Pagination
const currentPage = computed(() => {
  const page = parseInt(route.query.page) || 1
  return page > 0 ? page : 1
});

const onPageChange = (newPage) => {
  router.push({ query: { ...route.query, page: newPage } })
}

const getVacanciesCount = async() => {
  try {
    const response = await VacanciesService.countVacancies(filters.value);
    totalVacanciesCount.value = response.data.count;
    //totalVacanciesCount.value = 60;
  } catch(err) {
    console.log(err)
    alert('Ошибка загрузки данных с сервера!');
  }
}

const getVacancies = async() => {
  filters.value.start = (currentPage.value - 1) * perPage;
  filters.value.end = filters.value.start + perPage

  const response = await VacanciesService.getVacancies(filters.value);
  vacancies.value = response.data;
  console.log(vacancies.value);
}

watch(() => route.query.page, getVacancies)

onMounted(async() => {
  getVacanciesCount();
  getVacancies();
});

</script>

<template>
  <TheHeader />
  <main>
    <div class="container container-pd52">
      <div class="home-wrapper">
        <div class="search-wrapper">
          <div class="row">
            <div class="col d-flex">
              <input type="text" class="form-control flex-grow-1 sys-input-flex" id="InputSearch" placeholder="Профессия, должность или компания">
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
              <div v-if="vacancies.count" class="vacancy-wrapper">
                <TheVacancyCard v-for="vacancy in vacancies.items" :key="vacancy.id" :vacancy="vacancy"/>
              </div>
              <ThePaginator :total="totalVacanciesCount" :per-page="perPage" :page="currentPage" @update:page="onPageChange" />
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