<script setup>
import { onMounted, ref } from 'vue';

import TheHeader from '@/components/global/TheHeader.vue'
import TheFooter from '@/components/global/TheFooter.vue'
import TheUserCard from '@/components/verification/TheUserCard.vue';
import CatalogSearch from '@/components/global/CatalogSearch.vue';

import UserService from '@/services/user.service';
import ToolsService from '@/services/tools.service';

const filters = ref({ "q": "", "start": 0, "end": 50 });
const users = ref({
  count: 0,
  items: []
});

const eduLevels = ref([]);
const dataLoading = ref(true);

const loadApplicants = async() => {
  try {
    const response = await ToolsService.getEduLevels();
    eduLevels.value = response.data;
    dataLoading.value = false;
  } catch(err) {
    alert('Ошибка загрузки данных с сервера!');
  }

  try {
    const response = await UserService.getApplicants(filters.value);
    users.value = response.data;
  } catch(err) {
    alert('Ошибка загрузки данных с сервера!');
  }
}

const fetchLocations = async(params) => {
  const response = await ToolsService.getLocations(params);
  return response;
};

onMounted(loadApplicants);

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
              <button type="button" class="btn btn-primary sys-btn-150">Поиск</button>
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
                    <input class="form-check-input sys-check-20" type="radio" name="radioDefault" value="" id="checkFIOSearch" checked="">
                    <label class="form-check-label" for="checkFIOSearch">
                        По ФИО
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input sys-check-20" type="radio" name="radioDefault" value="" id="checkEduNumSearch">
                    <label class="form-check-label" for="checkEduNumSearch">
                        По зачётной книжке
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input sys-check-20" type="radio" name="radioDefault" value="" id="checkIdSearch">
                    <label class="form-check-label" for="checkIdSearch">
                        По ID
                    </label>
                  </div>
                  <div class="form-check mt-2">
                    <input class="form-check-input sys-check-20" type="checkbox" value="" id="checkVerification">
                    <label class="form-check-label" for="checkVerification">
                        Подтверждённые
                    </label>
                  </div>
                  <div class="parameters mt-4 mb-3">
                    Значения полей
                  </div>
                  <div class="custom-form-floating" style="margin-bottom: 24px;">
                    <input type="date" class="form-control sys-input-288" id="InputBirthdate" placeholder="Дата рождения">
                    <label for="InputBirthdate">Дата рождения</label>
                  </div>
                  <CatalogSearch :callback="fetchLocations" :isLoading="dataLoading" placeholder="Город"/>
                </div>
              </div>
            </div>
            <div class="col d-flex w-100" style="flex-direction: column;">
              <div v-if="users.count" class="vacancy-wrapper">
                <TheUserCard v-for="user in users.items" :key="user.id" :user="user" :edu_levels="eduLevels.items"/>
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