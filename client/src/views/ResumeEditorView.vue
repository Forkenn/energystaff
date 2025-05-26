<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

import TheHeader from '@/components/global/TheHeader.vue'
import TheFooter from '@/components/global/TheFooter.vue'
import VacanciesService from '@/services/vacancies.service';
import ResumeService from '@/services/resume.service';
import { useUserStore } from '@/stores/user';

const router = useRouter();
let errorMsg = '';

const userStore = useUserStore();

const creatorMode = ref(true);

const serverTypes = ref([]);
const serverFormats = ref([]);
const dataLoading = ref(true);

const resumeData = ref({
  position: null,
  specialization: null,
  description: null,
  salary: null,
  resume_types: [{
      id: 0,
      name: "string"
  }],
  resume_formats: [{
      id: 0,
      name: "string"
  }],
  resume_types_ids: [],
  resume_formats_ids: []
})

const validateFields = () => {
  errorMsg = '';
  resumeData.value.salary = resumeData.value.salary === "" ? null : resumeData.value.salary;

  if(
    !resumeData.value.position ||
    resumeData.value.position?.length < 4 ||
    resumeData.value.position?.length > 120
  )
    errorMsg += '• Недопустимая позиция (допустимо от 4 до 120 символов)\n';

  if(
    !resumeData.value.specialization ||
    resumeData.value.specialization?.length < 4 ||
    resumeData.value.specialization?.length > 120
  )
    errorMsg += '• Недопустимая специализация (допустимо от 4 до 120 символов)\n';

  const salary = Number(resumeData.value.salary);

  if(salary > 5000000 || salary < 0)
    errorMsg += '• Недопустимая зарплата (допустимо до 5000000)\n';

  console.log(resumeData.value.resume_types_ids);

  if(!resumeData.value.resume_types_ids.length)
    errorMsg += '• Не указана занятость\n';

  if(!resumeData.value.resume_formats_ids.length)
    errorMsg += '• Не указан график\n';

}

const validateSalary = (event) => {
  resumeData.value.salary = event.target.value.replace(/[^\d]/g, '');
};

const convertIds = () => {
    const resumeTypesObj = resumeData.value.resume_types
    const resumeFormatsObj = resumeData.value.resume_formats
    resumeData.value.resume_types_ids = resumeTypesObj.map(
      resumeTypesObj => resumeTypesObj.id
    );
    resumeData.value.resume_formats_ids = resumeFormatsObj.map(
      resumeFormatsObj => resumeFormatsObj.id
    );
}

const editResume = async() => {
  validateFields();
  if(errorMsg != '') {
    alert(`Ошибка сохранения изменений:\n${errorMsg}`);
    return;
  }

  try {
    await ResumeService.editMyResume(resumeData.value);
    alert('Данные сохранены');
  } catch(err) {
    alert('Ошибка публикации резюме')
  }
}

const createResume = async() => {
  validateFields();
  if(errorMsg != '') {
    alert(`Ошибка сохранения изменений:\n${errorMsg}`);
    return;
  }

  try {
    await ResumeService.addResume(resumeData.value);
    alert('Данные сохранены');
  } catch(err) {
    alert('Ошибка публикации резюме')
  }
}

const deleteResume = async() => {
  try {
    await ResumeService.deleteMyResume();
    alert('Данные сохранены');
    router.go(0);
  } catch(err) {
    alert('Ошибка удаления резюме');
  }
}

const isSelectedType = (id) => {
  if (dataLoading.value) {
    return false;
  }
  for (var i = 0; i < resumeData.value.resume_types_ids.length; i++) {
    if (resumeData.value.resume_types_ids[i] === id) {
      return true;
    }
  }
  return false;
};

const toggleCheckType = (id) => {
  if (isSelectedType(id)) {
    resumeData.value.resume_types_ids = resumeData.value.resume_types_ids.filter(
      selectedId => selectedId !== id
    );
  } else {
    resumeData.value.resume_types_ids = [...resumeData.value.resume_types_ids, id];
  }
}

const isSelectedFormat = (id) => {
  if (dataLoading.value) {
    return false;
  }
  for (var i = 0; i < resumeData.value.resume_formats_ids.length; i++) {
    if (resumeData.value.resume_formats_ids[i] === id) {
      return true;
    }
  }
  return false;
};

const toggleCheckFormat = (id) => {
  if (isSelectedFormat(id)) {
    resumeData.value.resume_formats_ids = resumeData.value.resume_formats_ids.filter(
      selectedId => selectedId !== id
    );
  } else {
    resumeData.value.resume_formats_ids = [...resumeData.value.resume_formats_ids, id];
  }
}

onMounted(async () => {
  try {
    const response = await ResumeService.getMyResume();
    resumeData.value = response.data;
    creatorMode.value = false;
  } catch(err) {
    if(err.response.status != 404) {
      alert('Ошибка загрузки резюме!');
      router.push({ name: 'home' });
    }
  }

  try {
      let response = await VacanciesService.getVacanciesFormats();
      serverFormats.value = response.data.items;
      response = await VacanciesService.getVacanciesTypes();
      serverTypes.value = response.data.items;
      convertIds(true);
      dataLoading.value = false;
    } catch(err) {
      alert('Ошибка сервера!');
      router.push({ name: 'home' });
    }
})

</script>

<template>
  <TheHeader />
  <main>
    <div class="container container-pd52">
      <div class="resume-container">
        <div class="editor-wrapper">
            <h1>Данные резюме</h1>
            <div class="row">
                <div class="col d-flex">
                    <div class="custom-form-floating">
                        <input type="text" class="form-control flex-grow-1 sys-input-900-flex" id="InputPosition" placeholder="Желаемая должность" v-model="resumeData.position">
                        <label for="InputPosition">Желаемая должность <span class="required-field">*</span></label>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col d-flex">
                    <div class="custom-form-floating">
                        <input type="text" class="form-control flex-grow-1 sys-input-600-flex" id="InputSpecialization" placeholder="Специализация" v-model="resumeData.specialization">
                        <label for="InputSpecialization">Специализация <span class="required-field">*</span></label>
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
                              v-model="resumeData.salary"
                              @input="validateSalary"
                            >
                            <label for="InputSalary">Зарплата</label>
                        </div>
                        <span class="input-group-text sys-input-group-text-38">₽</span>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-auto">
                    <div style="width: 90px;">
                        Занятость <span class="required-field">*</span>
                    </div>
                </div>
                <div class="col d-flex col-checkbox" style="flex-direction: column;">
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
            </div>

            <div class="row">
                <div class="col-auto">
                    <div style="width: 90px;">
                        График <span class="required-field">*</span>
                    </div>
                </div>
                <div class="col d-flex col-checkbox" style="flex-direction: column;">
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
            </div>
            <div class="row">
                <div class="col d-flex">
                    <div class="resume-text-area">
                        <label for="formControlExtended" class="form-label">Расширенное описание</label>
                        <textarea class="form-control" id="formControlExtended" rows="15"  v-model="resumeData.description"></textarea>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col d-flex">
                    <div class="editor-buttons">
                        <button v-if="!creatorMode" type="button" class="btn btn-danger sys-btn-288" @click="deleteResume">
                            Удалить резюме
                        </button>
                        <button v-if="creatorMode" type="button" class="btn btn-primary sys-btn-288" @click="createResume">
                            Сохранить
                        </button>
                        <button v-else type="button" class="btn btn-primary sys-btn-288" @click="editResume">
                            Сохранить изменения
                        </button>
                    </div>
                </div>
            </div>
        </div>
      </div>
    </div>
  </main>
  <TheFooter />
</template>

<style scoped>

.resume-container {
  margin-top: 55px;
  margin-bottom: 55px;
  width: 100%;
  border-color: #DBE0E5;
  border-width: 1px;
  border-style: solid;
  border-radius: 10px;
  background-color: #FFFFFF;
}

.required-field {
  color: red;
  font-weight: 700;
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

.editor-wrapper .row {
    margin-bottom: 24px;
}

.col-checkbox {
    flex-direction: column;
    min-width: 288px;
    max-width: 508px;
}

.resume-text-area {
    width: 100%;
}

.resume-text-area textarea {
    max-width: 900px;
    min-width: 288px;
    max-height: 370px;
    resize: none;
}

.editor-buttons {
    display: flex;
    flex-direction: column;
    margin-left: auto;
}

</style>