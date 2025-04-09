<script setup>
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import TheFooter from '@/components/global/TheFooter.vue';
import TheHeader from '@/components/global/TheHeader.vue';
import MultiSelect from '@/components/global/MultiSelect.vue';
import VacanciesService from '@/services/vacancies.service';
import { useUserStore } from '@/stores/user';

const route = useRoute();
const router = useRouter();

const userStore = useUserStore();

const creatorMode = ref(true);
const vacancyId = route.query.id;

const serverTypes = ref([]);
const serverFormats = ref([]);
const serverSchedules = ref([]);
const selectedSchedules = ref([]);
const schedulesLoading = ref(true);

const vacancyData = ref({
  position: "",
  specialization: "",
  description: "",
  salary: 0,
  vacancy_types: [{
      id: 0,
      name: "string"
  }],
  vacancy_formats: [{
      id: 0,
      name: "string"
  }],
  vacancy_schedules: [{
      id: 0,
      name: "string"
  }],
  vacancy_types_ids: [],
  vacancy_formats_ids: [],
  vacancy_schedules_ids: []
})

const convertIds = () => {
  const vacancySchedulesObj = vacancyData.value.vacancy_schedules
  const vacancyTypesObj = vacancyData.value.vacancy_types
  const vacancyFormatsObj = vacancyData.value.vacancy_formats
  vacancyData.value.vacancy_schedules_ids = vacancySchedulesObj.map(
    vacancySchedulesObj => vacancySchedulesObj.id
  );
  vacancyData.value.vacancy_types_ids = vacancyTypesObj.map(
    vacancyTypesObj => vacancyTypesObj.id
  );
  vacancyData.value.vacancy_formats_ids = vacancyFormatsObj.map(
    vacancyFormatsObj => vacancyFormatsObj.id
  );
}

const editVacancy = async() => {
  convertIds()
  try {
    await VacanciesService.editVacancy(vacancyId, vacancyData.value);
    router.push({ name: 'home' });
  } catch(err) {
    alert('Ошибка публикации вакансии!')
  }
}

const createVacancy = async() => {
  router.push({ name: 'home' });
}

onMounted(async () => {
  if (vacancyId) {
    try {
      const response = await VacanciesService.getVacancy(vacancyId);
      if(response.data.company_id != userStore.user.data.employer?.company_id) {
        router.push({ name: 'vacancy_editor' });
        return;
      }
      vacancyData.value = response.data;
    } catch(err) {
      alert('Вакансия не найдена!')
      router.push({ name: 'vacancy_editor' });
    } finally {
      creatorMode.value = false;
      selectedSchedules.value = vacancyData.value.vacancy_schedules;
    }
  }
  try {
      const response = await VacanciesService.getVacanciesSchedules();
      serverSchedules.value = response.data.items;
      convertIds()
      schedulesLoading.value = false;
    } catch(err) {
      alert('Ошибка сервера!')
      router.push({ name: 'home' });
    }
})

</script>

<template>
  <TheHeader />
  <main>
    <div class="container container-pd52">
      <div class="vacancy-container">
        <div class="editor-wrapper">
          <h1>
            Данные вакансии
          </h1>
          <div class="row">
            <div class="col-auto sys-col-912-flex">
              <div class="custom-form-floating">
                <input
                  type="text"
                  class="form-control flex-grow-1 sys-input-912-flex"
                  id="InputName"
                  placeholder="Должность"
                  v-model="vacancyData.position"
                >
                <label for="InputName">Должность</label>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-auto sys-col-600-flex">
              <div class="custom-form-floating">
                <input
                  type="text"
                  class="form-control flex-grow-1 sys-input-600-flex"
                  id="InputSpecialization"
                  placeholder="Специализация"
                  v-model="vacancyData.specialization"
                >
                <label for="InputSpecialization">Специализация</label>
              </div>
            </div>
            <div class="col d-flex">
              <div class="floating-input-group">
                <div class="custom-form-floating">
                  <input
                    type="text"
                    class="form-control flex-grow-1 sys-input-group-250"
                    id="InputSalary"
                    placeholder="Зарплата"
                    v-model="vacancyData.salary"
                  >
                  <label for="InputSalary">Зарплата</label>
                </div>
                <span class="input-group-text sys-input-group-text-38">₽</span>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-auto">
              <div style="width: 80px;">
                  Занятость
              </div>
            </div>
            <div class="col-auto sys-col-184">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckEmploymentFull">
                <label class="form-check-label" for="flexCheckEmploymentFull">
                    Полная занятость
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckEmploymentPartial">
                <label class="form-check-label" for="flexCheckEmploymentPartial">
                    Частичная занятость
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckEmploymentProject">
                <label class="form-check-label" for="flexCheckEmploymentProject">
                    Проектная работа
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckEmploymentIntern">
                <label class="form-check-label" for="flexCheckEmploymentIntern">
                    Стажировка
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckEmploymentPractice">
                <label class="form-check-label" for="flexCheckEmploymentPractice">
                    Практика
                </label>
              </div>
            </div>
            <div class="col-auto">
              <select id="formMultiselect" class="form-select sys-input-288" aria-label="Рабочие часы">
                <option selected>Рабочие часы</option>
                <option value="1">5/2</option>
                <option value="2">2/2</option>
                <option value="3">4/2</option>
              </select>
            </div>
            <div class="col d-flex">
              <select id="formMultiselect" class="form-select sys-input-288" aria-label="Навыки">
                <option selected>Навыки</option>
                <option value="1">SQL</option>
                <option value="2">Python</option>
                <option value="3">Git</option>
              </select>
            </div>
          </div>
          <div class="row">
            <div class="col-auto">
              <div style="width: 80px;">
                  График
              </div>
            </div>
            <div class="col-auto sys-col-184" style="flex-direction: column;">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDayFull">
                <label class="form-check-label" for="flexCheckDayFull">
                    Полный день
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDayShift">
                <label class="form-check-label" for="flexCheckDayShift">
                    Сменный день
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDayFlex">
                <label class="form-check-label" for="flexCheckDayFlex">
                    Гибкий график
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckRemote">
                <label class="form-check-label" for="flexCheckRemote">
                    Удалённая работа
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault">
                <label class="form-check-label" for="flexCheckDefault">
                    Вахтовый метод
                </label>
              </div>
            </div>
            <div class="col-auto">
              <MultiSelect class="sys-select-288"
                v-model="vacancyData.vacancy_schedules"
                :items="serverSchedules"
                :isLoading="schedulesLoading"
                placeholder="Графики работы"
              />
            </div>
          </div>
          <div class="row">
            <div class="col d-flex">
              <div class="vacancy-text-area">
                <label for="formControlExtended" class="form-label">Описание</label>
                <textarea
                  class="form-control"
                  id="formControlExtended"
                  rows="15"
                  v-model="vacancyData.description"
                ></textarea>
              </div>
            </div>
          </div>
          <div class="col d-flex">
            <div style="margin-left: auto;">
              <button v-if="creatorMode" type="button" class="btn btn-primary sys-btn-264" @click="createVacancy">
                Опубликовать
              </button>
              <button v-else type="button" class="btn btn-primary sys-btn-264" @click="editVacancy">
                Сохранить изменения
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
  <TheFooter />
</template>

<style scoped>

.vacancy-container {
  margin-top: 55px;
  margin-bottom: 55px;
  width: 100%;
  border-color: #DBE0E5;
  border-width: 1px;
  border-style: solid;
  border-radius: 10px;
  background-color: #FFFFFF;
}

.editor-wrapper {
  margin: 48px;
}

.editor-wrapper h1 {
  font-family: "Montserrat";
  font-size: 32px;
  font-weight: 700;
  color: #343434;
  margin-bottom: 24px;
}

.editor-wrapper .col {
  margin-bottom: 24px;
}

.editor-wrapper .col-auto {
  margin-bottom: 24px;
}

.col-checkbox {
  flex-direction: column;
  min-width: 288px;
  max-width: 508px;
}

.vacancy-text-area {
    width: 100%;
}

.vacancy-text-area textarea {
    max-width: 912px;
    min-width: 288px;
    max-height: 370px;
    resize: none;
}

</style>