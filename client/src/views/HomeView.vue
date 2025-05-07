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
import ToolsService from '@/services/tools.service';

const route = useRoute();
const router = useRouter();

const perPage = 6
const filters = ref({
  q: null,
  start: 0,
  end: perPage,
  desc: true,
  sortType: "dateDesc",
  location_id: null,
  salary_from: null,
  salary_to: null,
  sort_by: "date",
  employment_types_ids: null,
  employment_formats_ids: null,
  employment_schedules_ids: null
});
const vacancies = ref({ "count": 0, "items": [] });

const serverTypes = ref([]);
const selectedTypes = ref([]);

const serverFormats = ref([]);
const selectedFormats= ref([]);

const serverSchedules = ref([]);
const selectedSchedules = ref([]);

const selectedLocation = ref(null);

const dataLoading = ref(true);

const totalVacanciesCount = ref(0)

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

const convertIds = () => {
  const schedulesObj = selectedSchedules.value;
  const typesObj = selectedTypes.value;
  const formatsObj = selectedFormats.value;

  filters.value.employment_schedules_ids = schedulesObj.map(
    schedulesObj => schedulesObj.id
  );
  filters.value.employment_types_ids = typesObj.map(
    typesObj => typesObj.id
  );
  filters.value.employment_formats_ids = formatsObj.map(
    formatsObj => formatsObj.id
  );
}

const convertIdsToObjects = (ids) => {
  if(ids === null) return []

  return ids.map(id => ({
    id: parseInt(id),
    name: ""
  }));
}

const prepareFilters = async() => {
  switch(filters.value.sortType) {
    case 'dateDesc':
      filters.value.sort_by = 'date'
      filters.value.desc = true
      break;

    case 'dateAsc':
      filters.value.sort_by = 'date'
      filters.value.desc = false
      break;

    case 'salaryDesc':
      filters.value.sort_by = 'salary'
      filters.value.desc = true
      break;

    case 'salaryAsc':
      filters.value.sort_by = 'salary'
      filters.value.desc = false
      break;

    default:
      break;
  }

  filters.value.location_id = selectedLocation.value?.id || null;
  filters.value.salary_from = parseInt(filters.value.salary_from) || null
  filters.value.salary_to = parseInt(filters.value.salary_to) || null
  convertIds();
}

const getVacancies = async() => {
  filters.value.start = (currentPage.value - 1) * perPage;
  filters.value.end = filters.value.start + perPage;

  getVacanciesCount();
  const response = await VacanciesService.getVacancies(filters.value);
  vacancies.value = response.data;
}

const beginSearch = () => {
  prepareFilters();

  const query = {
    q: filters.value.q,
    sortType: filters.value.sortType,
    location_id: filters.value.location_id,
    salary_from: filters.value.salary_from,
    salary_to: filters.value.salary_to,
    page: currentPage.value,
    employment_types_ids: filters.value.employment_types_ids,
    employment_formats_ids: filters.value.employment_formats_ids,
    employment_schedules_ids: filters.value.employment_schedules_ids
  }

  const cleanedQuery = Object.fromEntries(
    Object.entries(query).filter(([_, v]) => v != null)
  );

  router.push({ name: 'home', query: cleanedQuery })
  getVacancies();
}

const parseFilters = async() => {
  filters.value.q = route.query.q || null;
  filters.value.sortType = route.query.sortType || "dateDesc";
  filters.value.salary_from = route.query.salary_from || null;
  filters.value.salary_to = route.query.salary_to || null;
  filters.value.employment_types_ids = route.query.employment_types_ids || null;
  filters.value.employment_formats_ids = route.query.employment_formats_ids || null;
  filters.value.employment_schedules_ids = route.query.employment_schedules_ids || null;

  selectedTypes.value = convertIdsToObjects(filters.value.employment_types_ids);
  selectedFormats.value = convertIdsToObjects(filters.value.employment_formats_ids);
  selectedSchedules.value = convertIdsToObjects(filters.value.employment_schedules_ids);

  const location_id = route.query.location_id || null;
  if(location_id && parseInt(location_id) != selectedLocation.value?.id) {
    try {
      const response = await ToolsService.getLocationById(location_id)
      selectedLocation.value = response.data;
      filters.value.location_id = location_id;
    } catch(err) {}
  }

  if(location_id === null) {
    selectedLocation.value = null;
    filters.value.location_id = null;
  }
  setTimeout(() => {
    dataLoading.value = false;
  }, 0);
}

watch(() => route.query, async() => {
  dataLoading.value = true;
  await parseFilters();
  //prepareFilters();
  //getVacancies();
});

//watch(() => route.query.page, getVacancies)
watch(dataLoading, (newVal) => {
  if (!newVal) {
    prepareFilters();
    getVacancies();
  }
});

onMounted(async() => {
  await getVacanciesRelations();
  await parseFilters();
  //prepareFilters();
  //getVacancies();
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
              <input type="text" class="form-control flex-grow-1 sys-input-flex" id="InputSearch" placeholder="Профессия, должность или компания" v-model="filters.q">
            </div>
            <div class="col-auto">
              <button type="button" class="btn btn-primary sys-btn-150" @click="beginSearch">Поиск</button>
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
                    <input
                      class="form-check-input sys-check-20"
                      type="radio"
                      name="radioDefault"
                      id="checkDateDescSort"
                      checked=""
                      value="dateDesc"
                      v-model="filters.sortType"
                    >
                    <label class="form-check-label" for="checkDateDescSort">
                      По убыванию даты
                    </label>
                  </div>
                  <div class="form-check">
                    <input
                      class="form-check-input sys-check-20"
                      type="radio"
                      name="radioDefault"
                      id="checkDateAscSort"
                      value="dateAsc"
                      v-model="filters.sortType"
                    >
                    <label class="form-check-label" for="checkDateAscSort">
                      По возрастанию даты
                    </label>
                  </div>
                  <div class="form-check">
                    <input
                      class="form-check-input sys-check-20"
                      type="radio"
                      name="radioDefault"
                      id="checkSalaryDescSort"
                      value="salaryDesc"
                      v-model="filters.sortType"
                    >
                    <label class="form-check-label" for="checkSalaryDescSort">
                        По убыванию зарплат
                    </label>
                  </div>
                  <div class="form-check">
                    <input
                      class="form-check-input sys-check-20"
                      type="radio"
                      name="radioDefault"
                      id="checkSalaryAscSort"
                      value="salaryAsc"
                      v-model="filters.sortType"
                    >
                    <label class="form-check-label" for="checkSalaryAscSort">
                        По возрастанию зарплат
                    </label>
                  </div>
                  <div class="filter-header mt-4 mb-2">
                    Регион
                  </div>
                  <CatalogSearch :callback="fetchLocations" :isLoading="dataLoading" placeholder="Город" v-model="selectedLocation" />
                  <div class="filter-header mt-4 mb-2">
                    Уровень дохода
                  </div>
                  <div class="form-floating sys-form-floating" style="margin-bottom: 24px;">
                    <input type="text" class="form-control sys-input-288" id="floatingSalaryFrom" placeholder="От" v-model="filters.salary_from">
                    <label for="floatingSalaryFrom">От</label>
                  </div>
                  <div class="form-floating sys-form-floating">
                    <input type="text" class="form-control sys-input-288" id="floatingSalaryFrom" placeholder="До" v-model="filters.salary_to">
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
                  <button type="button" class="btn btn-primary sys-btn-288" @click="beginSearch" style="margin-bottom: 0;">Применить</button>
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