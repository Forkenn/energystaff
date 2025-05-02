<script setup>
import { onMounted, ref, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';

import TheHeader from '@/components/global/TheHeader.vue'
import TheFooter from '@/components/global/TheFooter.vue'
import ThePaginator from '@/components/global/ThePaginator.vue';
import TheVacancyCard from '@/components/home/TheVacancyCard.vue';
import CatalogSearch from '@/components/global/CatalogSearch.vue';
import MultiSelect from '@/components/global/MultiSelect.vue';
import VacanciesService from '@/services/vacancies.service';

const route = useRoute();
const router = useRouter();

const filters = ref({ "q": "", "start": 0, "end": 50 });
const vacancies = ref({ "count": 0, "items": [] });

const serverTypes = ref([]);
const selectedTypes = ref([]);
const serverFormats = ref([]);
const selectedFormats= ref([]);
const serverSchedules = ref([]);
const selectedSchedules = ref([]);
const dataLoading = ref(true);

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

const fetchLocations = async(params) => {
  const response = await ToolsService.getLocations(params);
  return response;
};

const getVacanciesRelations = async() => {
  try {
      let response = await VacanciesService.getVacanciesSchedules();
      serverSchedules.value = response.data.items;
      response = await VacanciesService.getVacanciesFormats();
      serverFormats.value = response.data.items;
      response = await VacanciesService.getVacanciesTypes();
      serverTypes.value = response.data.items;
      dataLoading.value = false;
    } catch(err) {
    }
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
  getVacanciesRelations();
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
                <div class="filters">
                  <div class="filter-header mb-2">
                    Сортировать
                  </div>
                  <div class="form-check">
                    <input class="form-check-input sys-check-20" type="radio" name="radioDefault" value="" id="checkDateDescSort" checked="">
                    <label class="form-check-label" for="checkDateDescSort">
                      По убыванию даты
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input sys-check-20" type="radio" name="radioDefault" value="" id="checkDateAscSort">
                    <label class="form-check-label" for="checkDateAscSort">
                      По возрастанию даты
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input sys-check-20" type="radio" name="radioDefault" value="" id="checkSalaryDescSort">
                    <label class="form-check-label" for="checkSalaryDescSort">
                        По убыванию зарплат
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input sys-check-20" type="radio" name="radioDefault" value="" id="checkSalaryAscSort">
                    <label class="form-check-label" for="checkSalaryAscSort">
                        По возрастанию зарплат
                    </label>
                  </div>
                  <div class="filter-header mt-4 mb-2">
                    Регион
                  </div>
                  <CatalogSearch :callback="fetchLocations" :isLoading="dataLoading" placeholder="Город"/>
                  <div class="filter-header mt-4 mb-2">
                    Уровень дохода
                  </div>
                  <div class="form-floating sys-form-floating" style="margin-bottom: 24px;">
                    <input type="text" class="form-control sys-input-288" id="floatingSalaryFrom" placeholder="От">
                    <label for="floatingSalaryFrom">От</label>
                  </div>
                  <div class="form-floating sys-form-floating">
                    <input type="text" class="form-control sys-input-288" id="floatingSalaryFrom" placeholder="До">
                    <label for="floatingSalaryFrom">До</label>
                  </div>
                  <div class="filter-header mt-4 mb-2">
                    Занятость
                  </div>
                  <MultiSelect
                    class="sys-select-288"
                    style="margin-bottom: 24px;"
                    v-model="selectedTypes"
                    :items="serverTypes"
                    :isLoading="dataLoading"
                    placeholder="Тип занятости"
                  />
                  <MultiSelect
                    class="sys-select-288"
                    style="margin-bottom: 24px;"
                    v-model="selectedFormats"
                    :items="serverFormats"
                    :isLoading="dataLoading"
                    placeholder="Формат работы"
                  />
                  <MultiSelect
                    class="sys-select-288"
                    style="margin-bottom: 24px;"
                    v-model="selectedSchedules"
                    :items="serverSchedules"
                    :isLoading="dataLoading"
                    placeholder="График работы"
                  />
                </div>
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
  border-color: #DBE0E5;
  border-width: 1px;
  border-style: solid;
  border-radius: 10px;
  background-color: #FFFFFF;
}

.filters {
  margin: 48px;
}

.filter-header {
  font-family: "Montserrat";
  font-size: 20px;
  font-weight: 700;
  color: #343434;
}

.form-check {
  padding-left: 1.7em !important;
}

.vacancy-wrapper {
  min-width: 500px;
  max-width: 902px;
  min-height: 740px;
  width: 100%;
}

</style>