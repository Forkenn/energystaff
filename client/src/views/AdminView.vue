<script setup>
import { onMounted, ref, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';

import TheHeader from '@/components/global/TheHeader.vue'
import TheFooter from '@/components/global/TheFooter.vue'
import ThePaginator from '@/components/global/ThePaginator.vue';
import TheUserCard from '@/components/admin/TheUserCard.vue';
import TheCompanyCard from '@/components/admin/TheCompanyCard.vue';
import CatalogSearch from '@/components/global/CatalogSearch.vue';

import UserService from '@/services/user.service';
import CompaniesService from '@/services/companies.service';
import ToolsService from '@/services/tools.service';

const route = useRoute();
const router = useRouter();

const filters = ref({
  "q": "",
  "start": 0,
  "end": 50,
  "searchType": "user"
});

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
  totalItemsCount.value = 19;
}

const loadUsers = async() => {
  filters.value.start = (currentPage.value - 1) * perPage;
  filters.value.end = filters.value.start + perPage;
  try {
    const response = await UserService.getUsers(filters.value)
    users.value = response.data;
  } catch(err) {
    alert('Ошибка загрузки данных с сервера!');
  }
}

const loadCompaniesCount = async() => {
  totalItemsCount.value = 19;
}

const loadCompanies = async() => {
  filters.value.start = (currentPage.value - 1) * perPage;
  filters.value.end = filters.value.start + perPage;
  try {
    const response = await CompaniesService.getCompanies(filters.value)
    companies.value = response.data;
  } catch(err) {
    alert('Ошибка загрузки данных с сервера!');
  }
}

const beginSearch = async() => {
  if(filters.value.searchType === "user") {
    await loadUsersCount();
    await loadUsers();
    return;
  }

  await loadCompaniesCount();
  await loadCompanies();
}

watch(() => route.query.page, loadUsers)

const fetchLocations = async(params) => {
  const response = await ToolsService.getLocations(params);
  return response;
};

onMounted(async() => {
  beginSearch();
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
              <input type="text" class="form-control flex-grow-1 sys-input-1122-flex" id="InputSearch" placeholder="Фамилия, Имя, Отчество или идентификатор">
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
                      v-model="filters.searchType"
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
                      v-model="filters.searchType"
                    >
                    <label class="form-check-label" for="checkCompanySearch">
                        Компания
                    </label>
                  </div>
                  <div class="parameters mt-4 mb-2">
                    Параметры поиска
                  </div>
                  <div class="form-check">
                    <input class="form-check-input sys-check-20" type="radio" name="radioDefault" value="" id="checkFIOSearch" checked="">
                    <label class="form-check-label" for="checkFIOSearch">
                        По ФИО/наименованию
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input sys-check-20" type="radio" name="radioDefault" value="" id="checkIdSearch">
                    <label class="form-check-label" for="checkIdSearch">
                        По ID
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input sys-check-20" type="radio" name="radioDefault" value="" id="checkINNSearch">
                    <label class="form-check-label" for="checkINNSearch">
                        По ИНН
                    </label>
                  </div>
                  <div class="form-check mt-2">
                    <input class="form-check-input sys-check-20" type="checkbox" value="" id="checkVerification">
                    <label class="form-check-label" for="checkVerification">
                        Только подтверждённые
                    </label>
                  </div>
                  <div class="parameters mt-4 mb-2">
                    Сортировать
                  </div>
                  <div class="form-check">
                    <input class="form-check-input sys-check-20" type="radio" name="radioDefaultSort" value="" id="checkSort1Search" checked="">
                    <label class="form-check-label" for="checkSort1Search">
                        По убыванию ID
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input sys-check-20" type="radio" name="radioDefaultSort" value="" id="checkSort2Search">
                    <label class="form-check-label" for="checkSort2Search">
                        По возрастанию ID
                    </label>
                  </div>
                  <div class="parameters mt-4 mb-3">
                    Значения полей
                  </div>
                  <div class="custom-form-floating" style="margin-bottom: 24px;">
                    <input type="date" class="form-control sys-input-288" id="InputBirthdate" placeholder="Дата рождения/регистрации">
                    <label for="InputBirthdate">Дата рождения/регистрации</label>
                  </div>
                  <CatalogSearch :callback="fetchLocations" :isLoading="dataLoading" placeholder="Город"/>
                </div>
              </div>
            </div>
            <div class="col d-flex w-100" style="flex-direction: column;">
              <div v-if="users.count && filters.searchType === 'user'" class="vacancy-wrapper">
                <TheUserCard v-for="user in users.items" :key="user.id" :user="user" />
              </div>
              <div v-if="companies.count && filters.searchType === 'company'" class="vacancy-wrapper">
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