<script setup>
import { onMounted, ref, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';

import TheHeader from '@/components/global/TheHeader.vue'
import TheFooter from '@/components/global/TheFooter.vue'
import ThePaginator from '@/components/global/ThePaginator.vue';
import TheUserCard from '@/components/admin/TheUserCard.vue';
import TheCompanyCard from '@/components/admin/TheCompanyCard.vue';
import TheNotFoundSign from '@/components/global/TheNotFoundSign.vue';
import CatalogSearch from '@/components/global/CatalogSearch.vue';

import UserService from '@/services/user.service';
import CompaniesService from '@/services/companies.service';
import ToolsService from '@/services/tools.service';

const route = useRoute();
const router = useRouter();

const filters = ref({
  q: "",
  start: 0,
  end: 50,
  searchBy: "name",
  searchFor: "user",
  sortOrder: "desc",
  date: null,
  birthdate: null,
  registration_date: null,
  location_id: null,
  only_verified: false,
  desc: true
});

const dataTypeLoaded = ref('users');

const users = ref({
  count: 0,
  items: []
});

const companies = ref({
  count: 0,
  items: []
});

const totalItemsCount = ref(0)
const perPage = 6

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

const loadUsersCount = async() => {
  try {
    const response = await UserService.getUsersCount(filters.value);
    totalItemsCount.value = response.data.count;
  } catch(err) {
    alert('Ошибка загрузки данных с сервера!');
  }
}

const loadUsers = async() => {
  filters.value.start = (currentPage.value - 1) * perPage;
  filters.value.end = filters.value.start + perPage;

  if(filters.value.searchBy == 'name') {
    await loadUsersCount();
    try {
      const response = await UserService.getUsers(filters.value)
      users.value = response.data;
    } catch(err) {
      alert('Ошибка загрузки данных с сервера!');
    }
    return;
  }

  try {
    users.value.items = [];
    users.value.count = 0;
    const response = await UserService.getUserById(parseInt(filters.value.q) || 0)
    users.value.items.push(response.data);
    users.value.count = 1;
    totalItemsCount.value = 1;
  } catch(err) {}
}

const loadCompaniesCount = async() => {
  try {
    const response = await CompaniesService.getCompaniesCount(filters.value);
    totalItemsCount.value = response.data.count;
  } catch(err) {
    alert('Ошибка загрузки данных с сервера!');
  }
}

const loadCompanies = async() => {
  filters.value.start = (currentPage.value - 1) * perPage;
  filters.value.end = filters.value.start + perPage;

  if(filters.value.searchBy == 'name') {
    await loadCompaniesCount();
    try {
      const response = await CompaniesService.getCompanies(filters.value)
      companies.value = response.data;
    } catch(err) {
      alert('Ошибка загрузки данных с сервера!');
    }
    return;
  }

  companies.value.items = [];
  companies.value.count = 0;
  if(filters.value.searchBy == 'inn') {
    try {
      const response = await CompaniesService.getCompanyByInn(filters.value.q)
      companies.value.items.push(response.data);
      companies.value.count = 1;
      totalItemsCount.value = 1;
    } catch(err) {}
    return;
  }

  try {
    const response = await CompaniesService.getCompany(parseInt(filters.value.q) || 0)
    companies.value.items.push(response.data);
    companies.value.count = 1;
    totalItemsCount.value = 1;
  } catch(err) {}
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
  filters.value.registration_date = filters.value.date === "" ? null : filters.value.date;
  filters.value.birthdate = filters.value.registration_date;
  filters.value.location_id = selectedLocation.value?.id || null;
}

const parseFilters = async() => {
  filters.value.q = route.query.q || null;
  filters.value.searchBy = route.query.searchBy || "name";
  filters.value.searchFor = route.query.searchFor || "user";
  filters.value.sortOrder = route.query.sortOrder || "desc";
  filters.value.only_verified = route.query.only_verified || false;

  const date = route.query.date || null;
  filters.value.date = date === "" ? null : date

  if(filters.value.searchFor == "user")
    dataTypeLoaded.value = 'users'
  else
    dataTypeLoaded.value = 'companies'

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

const selectSearch = async() => {
  if(filters.value.searchFor === "user") {
    await loadUsers();
    return;
  }

  await loadCompanies();
}

const beginSearch = async() => {
  prepareFilters();

  const query = {
    q: filters.value.q,
    searchBy: filters.value.searchBy,
    searchFor: filters.value.searchFor,
    sortOrder: filters.value.sortOrder,
    location_id: filters.value.location_id,
    date: filters.value.date === "" ? null : filters.value.date,
    only_verified: filters.value.only_verified,
    page: currentPage.value,
  }

  const cleanedQuery = Object.fromEntries(
    Object.entries(query).filter(([_, v]) => v != null)
  );

  router.push({ name: 'control_page', query: cleanedQuery });
}

watch(() => route.query, async() => {
  dataLoading.value = true;
  await parseFilters();
  //prepareFilters();
  //getVacancies();
});

watch(dataLoading, (newVal) => {
  if (!newVal) {
    prepareFilters();
    selectSearch();
  }
});

const fetchLocations = async(params) => {
  const response = await ToolsService.getLocations(params);
  return response;
};

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
                    Тип объекта
                  </div>
                  <div class="form-check">
                    <input
                      class="form-check-input sys-check-20"
                      type="radio"
                      name="radioDefaultObj"
                      value="user"
                      id="checkUsersSearch"
                      checked=""
                      v-model="filters.searchFor"
                    >
                    <label class="form-check-label" for="checkUsersSearch">
                        Пользователь
                    </label>
                  </div>
                  <div class="form-check">
                    <input
                      class="form-check-input sys-check-20"
                      type="radio"
                      name="radioDefaultObj"
                      value="company"
                      id="checkCompanySearch"
                      v-model="filters.searchFor"
                    >
                    <label class="form-check-label" for="checkCompanySearch">
                        Компания
                    </label>
                  </div>
                  <div class="parameters mt-4 mb-2">
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
                        По ФИО/наименованию
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
                  <div class="form-check">
                    <input
                      class="form-check-input sys-check-20"
                      type="radio"
                      name="radioDefault" 
                      id="checkINNSearch"
                      value="inn"
                      v-model="filters.searchBy"
                      :disabled="filters.searchFor == 'user'"
                    >
                    <label class="form-check-label" for="checkINNSearch">
                        По ИНН
                    </label>
                  </div>
                  <div class="form-check mt-2">
                    <input
                      class="form-check-input sys-check-20"
                      type="checkbox"
                      value=""
                      id="checkVerification"
                      v-model="filters.only_verified"
                      :disabled="filters.searchBy != 'name'"
                    >
                    <label class="form-check-label" for="checkVerification">
                        Только подтверждённые
                    </label>
                  </div>
                  <div class="parameters mt-4 mb-2">
                    Сортировать
                  </div>
                  <div class="form-check">
                    <input
                      class="form-check-input sys-check-20"
                      type="radio" name="radioDefaultSort"
                      id="checkSort1Search" checked=""
                      value="desc"
                      v-model="filters.sortOrder"
                      :disabled="filters.searchBy != 'name'"
                    >
                    <label class="form-check-label" for="checkSort1Search">
                        По убыванию ID
                    </label>
                  </div>
                  <div class="form-check">
                    <input
                      class="form-check-input sys-check-20"
                      type="radio"
                      name="radioDefaultSort"
                      id="checkSort2Search"
                      value="asc"
                      v-model="filters.sortOrder"
                      :disabled="filters.searchBy != 'name'"
                    >
                    <label class="form-check-label" for="checkSort2Search">
                        По возрастанию ID
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
                      placeholder="Дата рождения/регистрации"
                      v-model="filters.date"
                      :disabled="filters.searchBy != 'name'"
                    >
                    <label for="InputBirthdate">Дата рождения/регистрации</label>
                  </div>
                  <CatalogSearch
                    :callback="fetchLocations"
                    :isLoading="dataLoading"
                    placeholder="Город"
                    v-model="selectedLocation"
                    :disabled="filters.searchBy != 'name' || filters.searchFor == 'company'"
                  />
                  <button type="button" class="btn btn-primary sys-btn-288" @click="beginSearch" style="margin-bottom: 0; margin-top: 24px;">Применить</button>
                </div>
              </div>
            </div>
            <div class="col d-flex w-100" style="flex-direction: column;">
              <TheNotFoundSign v-if="!users.count && dataTypeLoaded === 'users'" />
              <div v-if="users.count && dataTypeLoaded === 'users'" class="vacancy-wrapper">
                <TheUserCard v-for="user in users.items" :key="user.id" :user="user" />
              </div>
              <TheNotFoundSign v-if="!companies.count && dataTypeLoaded === 'companies'" />
              <div v-if="companies.count && dataTypeLoaded === 'companies'" class="vacancy-wrapper">
                <TheCompanyCard v-for="company in companies.items" :key="company.id" :company="company" />
              </div>
              <ThePaginator :total="totalItemsCount" :per-page="perPage" :page="currentPage" @update:page="onPageChange" />
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