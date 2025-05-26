<script setup>
import { onMounted, ref, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';

import TheHeader from '@/components/global/TheHeader.vue'
import TheFooter from '@/components/global/TheFooter.vue'
import ThePaginator from '@/components/global/ThePaginator.vue';
import TheApplicantCard from '@/components/verification/TheApplicantCard.vue';
import TheWarningSign from '@/components/global/TheWarningSign.vue';
import TheNotFoundSign from '@/components/global/TheNotFoundSign.vue';
import CatalogSearch from '@/components/global/CatalogSearch.vue';

import UserService from '@/services/user.service';
import ToolsService from '@/services/tools.service';

import { useUserStore } from '@/stores/user';

const route = useRoute();
const router = useRouter();

const userStore = useUserStore();
const userData = computed(() => userStore.user.data);

const filters = ref({
  q: "",
  start: 0,
  end: 50,
  searchBy: "name",
  sortOrder: "desc",
  birthdate: null,
  location_id: null,
  only_verified: false,
  desc: true
});

const users = ref({
  count: 0,
  items: []
});

const totalUsersCount = ref(0)
const perPage = 6
const eduLevels = ref([]);

const selectedLocation = ref(null);

const dataLoading = ref(true);

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

const loadEduLevels = async() => {
  try {
    const response = await ToolsService.getEduLevels();
    eduLevels.value = response.data;
    //dataLoading.value = false;
  } catch(err) {
    alert('Ошибка загрузки данных с сервера!');
  }
}

const loadApplicantsCount = async() => {
  try {
    const response = await UserService.countApplicants(filters.value);
    totalUsersCount.value = response.data.count;
  } catch(err) {
    console.log(err)
    alert('Ошибка загрузки данных с сервера!');
  }
}

const loadApplicants = async() => {
  await loadEduLevels();

  if(!userData.value.is_verified)
    return;

  if(filters.value.searchBy == 'name') {
    await loadApplicantsCount();
    try {
      filters.value.start = (currentPage.value - 1) * perPage;
      filters.value.end = filters.value.start + perPage

      const response = await UserService.getApplicants(filters.value);
      users.value = response.data;
    } catch(err) {
      alert('Ошибка загрузки данных с сервера!');
    }
    return;
  }

  users.value.items = [];
  users.value.count = 0;
  if(filters.value.searchBy == 'id') {
    try {
      const response = await UserService.getApplicantById(parseInt(filters.value.q) || 0)
      users.value.items.push(response.data);
      users.value.count = 1;
      totalUsersCount.value = 1;
    } catch(err) {}
    return;
  }

  try {
    const response = await UserService.getApplicantByEdu(filters.value.q)
    users.value.items.push(response.data);
    users.value.count = 1;
    totalUsersCount.value = 1;
  } catch(err) {}
}

const parseFilters = async() => {
  filters.value.q = route.query.q || null;
  filters.value.searchBy = route.query.searchBy || "name";
  filters.value.sortOrder = route.query.sortOrder || "desc";
  filters.value.only_verified = route.query.only_verified || false;

  const date = route.query.birthdate || null;
  filters.value.birthdate = date === "" ? null : date

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

const prepareFilters = async() => {
  switch(filters.value.sortOrder) {
    case 'desc':
      filters.value.desc = true
      break;

    case 'asc':
      filters.value.desc = false
      break;

    default:
      break;
  }

  filters.value.birthdate = filters.value.birthdate;
  filters.value.location_id = selectedLocation.value?.id || null;
}

const beginSearch = async() => {
  prepareFilters();

  const query = {
    q: filters.value.q,
    searchBy: filters.value.searchBy,
    sortOrder: filters.value.sortOrder,
    location_id: filters.value.location_id,
    birthdate: filters.value.birthdate === "" ? null : filters.value.birthdate,
    only_verified: filters.value.only_verified,
    page: currentPage.value,
  }

  const cleanedQuery = Object.fromEntries(
    Object.entries(query).filter(([_, v]) => v != null)
  );

  router.push({ name: 'edu_verification', query: cleanedQuery });
}

watch(() => route.query, async() => {
  dataLoading.value = true;
  await parseFilters();
});

watch(dataLoading, (newVal) => {
  if (!newVal) {
    prepareFilters();
    loadApplicants();
  }
});

onMounted(async() => {
  await parseFilters();
});

</script>

<template>
  <TheHeader />
  <main>
    <div class="container container-pd52">
      <div class="verification-wrapper">
        <div class="search-wrapper">
          <div class="row">
            <div class="col d-flex">
              <input
                type="text"
                class="form-control flex-grow-1 sys-input-1122-flex"
                id="InputSearch"
                placeholder="Фамилия, Имя, Отчество или идентификатор"
                v-model="filters.q"
              >
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
                  <div class="parameters mb-2">
                    Параметры поиска
                  </div>
                  <div class="form-check">
                    <input
                      class="form-check-input sys-check-20"
                      type="radio"
                      name="radioDefault"
                      id="checkFIOSearch"
                      checked=""
                      value="name"
                      v-model="filters.searchBy"
                    >
                    <label class="form-check-label" for="checkFIOSearch">
                        По ФИО
                    </label>
                  </div>
                  <div class="form-check">
                    <input
                      class="form-check-input sys-check-20"
                      type="radio"
                      name="radioDefault"
                      id="checkEduNumSearch"
                      value="edu_num"
                      v-model="filters.searchBy"
                    >
                    <label class="form-check-label" for="checkEduNumSearch">
                        По зачётной книжке
                    </label>
                  </div>
                  <div class="form-check">
                    <input
                      class="form-check-input sys-check-20"
                      type="radio"
                      name="radioDefault"
                      id="checkIdSearch"
                      value="id"
                      v-model="filters.searchBy"
                    >
                    <label class="form-check-label" for="checkIdSearch">
                        По ID
                    </label>
                  </div>
                  <div class="form-check mt-2">
                    <input
                      class="form-check-input sys-check-20"
                      type="checkbox"
                      value=""
                      id="checkVerification"
                      :disabled="filters.searchBy != 'name'"
                      v-model="filters.only_verified"
                    >
                    <label class="form-check-label" for="checkVerification">
                        Подтверждённые
                    </label>
                  </div>
                  <div class="parameters mt-4 mb-3">
                    Значения полей
                  </div>
                  <div class="custom-form-floating" style="margin-bottom: 24px;">
                    <input
                      type="date"
                      class="form-control sys-input-288"
                      id="InputBirthdate"
                      placeholder="Дата рождения"
                      :disabled="filters.searchBy != 'name'"
                      v-model="filters.birthdate"
                    >
                    <label for="InputBirthdate">Дата рождения</label>
                  </div>
                  <CatalogSearch
                    :callback="fetchLocations"
                    :isLoading="dataLoading"
                    placeholder="Город"
                    v-model="selectedLocation"
                    :disabled="filters.searchBy != 'name'"
                  />
                  <button type="button" class="btn btn-primary sys-btn-288" @click="beginSearch" style="margin-bottom: 0; margin-top: 24px;">Применить</button>
                </div>
              </div>
            </div>
            <div class="col d-flex w-100" style="flex-direction: column;">
              <TheWarningSign v-if="!userData.is_verified" />
              <TheNotFoundSign v-else-if="!users.count" />
              <div v-if="users.count" class="vacancy-wrapper">
                <TheApplicantCard v-for="user in users.items" :key="user.id" :user="user" :edu_levels="eduLevels.items"/>
              </div>
              <ThePaginator :total="totalUsersCount" :per-page="perPage" :page="currentPage" @update:page="onPageChange" />
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

.verification-wrapper {
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

.filters .parameters {
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