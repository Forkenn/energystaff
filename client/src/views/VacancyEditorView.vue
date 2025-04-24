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
const dataLoading = ref(true);

const vacancyData = ref({
  position: "",
  specialization: "",
  description: "",
  salary: 0,
  salaryFrom: true,
  hours: "",
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

const convertIds = (full=false) => {
  const vacancySchedulesObj = vacancyData.value.vacancy_schedules
  vacancyData.value.vacancy_schedules_ids = vacancySchedulesObj.map(
    vacancySchedulesObj => vacancySchedulesObj.id
  );

  if(full) {
    const vacancyTypesObj = vacancyData.value.vacancy_types
    const vacancyFormatsObj = vacancyData.value.vacancy_formats
    vacancyData.value.vacancy_types_ids = vacancyTypesObj.map(
      vacancyTypesObj => vacancyTypesObj.id
    );
    vacancyData.value.vacancy_formats_ids = vacancyFormatsObj.map(
      vacancyFormatsObj => vacancyFormatsObj.id
    );
  }
}

const editVacancy = async() => {
  convertIds();
  try {
    await VacanciesService.editVacancy(vacancyId, vacancyData.value);
    router.push({ name: 'home' });
  } catch(err) {
    alert('Ошибка публикации вакансии!')
  }
}

const createVacancy = async() => {
  convertIds();
  try {
    await VacanciesService.addVacancy(vacancyData.value);
    router.push({ name: 'home' });
  } catch(err) {
    alert('Ошибка публикации вакансии!')
  }
}

const isSelectedType = (id) => {
  if (dataLoading.value) {
    return false;
  }
  for (var i = 0; i < vacancyData.value.vacancy_types_ids.length; i++) {
    if (vacancyData.value.vacancy_types_ids[i] === id) {
      return true;
    }
  }
  return false;
};

const toggleCheckType = (id) => {
  if (isSelectedType(id)) {
    vacancyData.value.vacancy_types_ids = vacancyData.value.vacancy_types_ids.filter(
      selectedId => selectedId !== id
    );
  } else {
    vacancyData.value.vacancy_types_ids = [...vacancyData.value.vacancy_types_ids, id];
  }
}

const isSelectedFormat = (id) => {
  if (dataLoading.value) {
    return false;
  }
  for (var i = 0; i < vacancyData.value.vacancy_formats_ids.length; i++) {
    if (vacancyData.value.vacancy_formats_ids[i] === id) {
      return true;
    }
  }
  return false;
};

const toggleCheckFormat = (id) => {
  if (isSelectedFormat(id)) {
    vacancyData.value.vacancy_formats_ids = vacancyData.value.vacancy_formats_ids.filter(
      selectedId => selectedId !== id
    );
  } else {
    vacancyData.value.vacancy_formats_ids = [...vacancyData.value.vacancy_formats_ids, id];
  }
}

onMounted(async () => {
  if (vacancyId) {
    try {
      const response = await VacanciesService.getVacancy(vacancyId);
      if(response.data.company.id != userStore.user.data.employer?.company_id) {
        router.push({ name: 'vacancy_editor' });
        return;
      }
      vacancyData.value = response.data;
    } catch(err) {
      alert('Вакансия не найдена!')
      router.push({ name: 'vacancy_editor' });
    } finally {
      creatorMode.value = false;
    }
  }

  try {
      let response = await VacanciesService.getVacanciesSchedules();
      serverSchedules.value = response.data.items;
      response = await VacanciesService.getVacanciesFormats();
      serverFormats.value = response.data.items;
      response = await VacanciesService.getVacanciesTypes();
      serverTypes.value = response.data.items;
      convertIds(true);
      dataLoading.value = false;
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
            <div class="col-auto sys-col-600-flex">
              <div class="custom-form-floating">
                <input
                  type="text"
                  class="form-control flex-grow-1 sys-input-600-flex"
                  id="InputName"
                  placeholder="Должность"
                  v-model="vacancyData.position"
                >
                <label for="InputName">Должность</label>
              </div>
            </div>
            <div class="col d-flex">
              <div class="custom-form-floating">
                <input
                  type="text"
                  class="form-control flex-grow-1 sys-input-288"
                  id="InputCity"
                  placeholder="Город"
                >
                <label for="InputCity">Город</label>
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
                <input class="form-check-input sys-check-20" type="checkbox" value="" id="checkTypeFull" :id="1" @click="toggleCheckType(1)" :checked="isSelectedType(1)">
                <label class="form-check-label sys-check-label" for="checkTypeFull">
                    Полная занятость
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input sys-check-20" type="checkbox" value="" id="checkTypePartial" :id="2" @click="toggleCheckType(2)" :checked="isSelectedType(2)">
                <label class="form-check-label sys-check-label" for="checkTypePartial">
                    Частичная занятость
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input sys-check-20" type="checkbox" value="" id="checkTypeProject" :id="3" @click="toggleCheckType(3)" :checked="isSelectedType(3)">
                <label class="form-check-label sys-check-label" for="checkTypeProject">
                    Проектная работа
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input sys-check-20" type="checkbox" value="" id="checkTypeIntern" :id="4" @click="toggleCheckType(4)" :checked="isSelectedType(4)">
                <label class="form-check-label sys-check-label" for="checkTypeIntern">
                    Стажировка
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input sys-check-20" type="checkbox" value="" id="checkTypePractice" :id="5" @click="toggleCheckType(5)" :checked="isSelectedType(5)">
                <label class="form-check-label sys-check-label" for="checkTypePractice">
                    Практика
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input sys-check-20" type="checkbox" value="" id="checkTypeVacht" :id="6" @click="toggleCheckType(6)" :checked="isSelectedType(6)">
                <label class="form-check-label sys-check-label" for="checkTypeVacht">
                    Вахта
                </label>
              </div>
            </div>
            <div class="col-auto">
              <div class="custom-form-floating">
                <input
                  type="text"
                  class="form-control flex-grow-1 sys-input-600-flex"
                  id="InputSpecialization"
                  placeholder="Рабочие часы"
                  v-model="vacancyData.hours"
                >
                <label for="InputSpecialization">Рабочие часы</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-check" style="padding-top: 10px;">
                <input class="form-check-input sys-check-20" type="checkbox" value="" id="checkSalaryFrom" v-model="vacancyData.salaryFrom">
                <label class="form-check-label sys-check-label" for="checkSalaryFrom">
                    {{ vacancyData.salaryFrom ? "Нижняя граница" : "Верхняя граница" }} {{ "з/п" }}
                </label>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-auto">
              <div style="width: 80px;">
                  Формат
              </div>
            </div>
            <div class="col-auto sys-col-184" style="flex-direction: column;">
              <div class="form-check">
                <input class="form-check-input sys-check-20" type="checkbox" value="" id="checkFormatPlace" :id="1" @click="toggleCheckFormat(1)" :checked="isSelectedFormat(1)">
                <label class="form-check-label" for="checkFormatPlace">
                    На месте
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input sys-check-20" type="checkbox" value="" id="checkFormatRemote" :id="2" @click="toggleCheckFormat(2)" :checked="isSelectedFormat(2)">
                <label class="form-check-label" for="checkFormatRemote">
                    Удалённый
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input sys-check-20" type="checkbox" value="" id="checkFormatGybrid" :id="3" @click="toggleCheckFormat(3)" :checked="isSelectedFormat(3)">
                <label class="form-check-label" for="checkFormatGybrid">
                    Гибрид
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input sys-check-20" type="checkbox" value="" id="checkFormatTravel" :id="4" @click="toggleCheckFormat(4)" :checked="isSelectedFormat(4)">
                <label class="form-check-label" for="checkFormatTravel">
                    Разъездной
                </label>
              </div>
            </div>
            <div class="col-auto">
              <MultiSelect class="sys-select-288"
                v-model="vacancyData.vacancy_schedules"
                :items="serverSchedules"
                :isLoading="dataLoading"
                placeholder="График работы"
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