<script setup>
import { computed, onMounted, ref } from 'vue';

import TheHeader from '../components/global/TheHeader.vue'
import TheFooter from '../components/global/TheFooter.vue'
import CatalogSearch from '@/components/global/CatalogSearch.vue';
import UserService from '@/services/user.service';
import AuthService from '@/services/auth.service';
import ToolsService from '@/services/tools.service';
import { useUserStore } from '@/stores/user';
import router from '@/router';

const userStore = useUserStore();
const userData = computed(() => userStore.user.data);
const dataLoading = ref(true);
let errorMsg = '';
const systemStatus = computed(() => {
  if(userData.value.is_superuser) {
    return "Администратор"
  }
  if(userData.value.is_edu) {
    return "Работник ОУ"
  }
  if(userData.value.is_employer) {
    return "Работодатель"
  }
  if(userData.value.is_applicant) {
    return "Соискатель"
  }
  return "Не определён"
})
const selectedInstitution = ref(null);
const selectedLocation = ref(userData.value.location);
const eduLevels = ref([]);

const oldPassword = ref(null);
const newPassword = ref(null);
const newPassword2 = ref(null);
const oldPasswordEmail = ref(null);

const validateFields = () => {
  errorMsg = '';
  if(!userData.value.surname || userData.value.surname?.length < 2)
    errorMsg += '• Недопустимая фамилия\n';

  if(!userData.value.name || userData.value.name?.length < 2)
    errorMsg += '• Недопустимое имя\n';

  if(userData.value.birthdate == '')
    errorMsg += '• Недопустимая дата рождения\n';
}

const saveChanges = async() => {
  validateFields();
  if(errorMsg != '') {
    alert(`Ошибка сохранения изменений:\n${errorMsg}`);
    return;
  }

  if (userData.value.is_applicant && !userData.value.is_superuser)
    userData.value.applicant.edu_institution_id = selectedInstitution.value?.id;

  userData.value.location_id = selectedLocation.value?.id;
  try{
    await UserService.editCurrent(userData.value);
    alert("Изменения сохранены");
  } catch(err) {
    alert("Ошибка сохранения данных");
  }
}

const changePassword = async() => {
  if(newPassword.value != newPassword2.value) {
    alert("Ошибка смены пароля\n• Новые пароли не совпадают");
    return;
  }

  if(!newPassword.value || newPassword.value.length < 8)
    errorMsg += 'Ошибка смены пароля\n• Пароль меньше 8 символов';

  try{
    await AuthService.changePassword({
      oldPassword: oldPassword.value,
      newPassword: newPassword.value
    })
    alert("Изменения сохранены");
    router.go(0);
  } catch(err) {
    alert("Ошибка смены пароля\n• Неверный пароль");
  }
}

const changeEmail = async() => {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if(userData.value.email?.length < 5 || !emailPattern.test(userData.value.email)) {
    alert("Ошибка смены почты:\n• Недопустимая электронная почта");
    return;
  }

  try{
    await AuthService.changeEmail({
      password: oldPasswordEmail.value,
      newEmail: userData.value.email
    })

    alert("Изменения сохранены");
    router.go(0);
  } catch(err) {
    if(err.response?.status == 400 && err.response?.data.detail == 'OBJECT_ALREADY_EXIST') {
      alert("Ошибка смены почты:\n• E-mail уже занят");
      return;
    }

    alert("Ошибка смены почты:\n• Неверный пароль");
  }
}

const fetchInstitutions = async(params) => {
  const response = await ToolsService.getEduInstitutions(params);
  return response;
};

const fetchLocations = async(params) => {
  const response = await ToolsService.getLocations(params);
  return response;
};

const checkLevelSelected = (id) => {
  if (userData.value.is_applicant) {
    const edu_level_id = userData.value.applicant.edu_level_id;
    if(edu_level_id == id) return true;
  }
  return false;
}

const setSex = (type) => {
  userData.value.sex = type;
}

const setStatus = (type) => {
  userData.value.applicant.edu_status = type;
}

const setLevel = (level) => {
  userData.value.applicant.edu_level_id = level;
}

onMounted(async () => {
  const edu_institution_id = userData.value.applicant?.edu_institution_id;
  if (userData.value.is_applicant) {
    if (edu_institution_id) {
      try {
        const response = await ToolsService.getEduInstitutionbyId(edu_institution_id);
        selectedInstitution.value = response.data;
      } catch(err) {
        alert('Ошибка загрузки данных с сервера');
      }
    }
  
    try {
      const response = await ToolsService.getEduLevels();
      eduLevels.value = response.data;
    } catch(err) {
      alert('Ошибка загрузки данных с сервера');
    }
  }
  dataLoading.value = false;
})

</script>

<template>
  <TheHeader />
  <main>
    <div class="container container-pd52">
      <div class="account-container account-data-container">
        <h1>Личные данные</h1>
        <div class="row form-row">
          <div class="col-auto">
            <div class="custom-form-floating">
              <input type="text" class="form-control sys-input-288" id="InputSurname" placeholder="Фамилия" v-model="userData.surname">
              <label for="InputSurname">Фамилия</label>
            </div>
          </div>
          <div class="col-auto">
            <div class="custom-form-floating">
              <input type="text" class="form-control sys-input-288" id="InputFirstname" placeholder="Имя" v-model="userData.name">
              <label for="InputFirstname">Имя</label>
            </div>
          </div>
          <div class="col-auto">
            <div class="custom-form-floating">
              <input type="text" class="form-control sys-input-288" id="InputSecondname" placeholder="Отчество" v-model="userData.last_name">
              <label for="InputSecondname">Отчество</label>
            </div>
          </div>
        </div>
        <div class="row form-row">
            <div class="col-auto">
              <div class="custom-form-floating">
                <input type="date" class="form-control sys-input-288" id="InputBirthdate" placeholder="Дата рождения" v-model="userData.birthdate">
                <label for="InputBirthdate">Дата рождения</label>
              </div>
            </div>
            <div class="col-auto">
              <CatalogSearch :callback="fetchLocations" :isLoading="dataLoading" placeholder="Город" v-model="selectedLocation"/>
            </div>
            <div class="col-auto">
              <select class="form-select sys-input-288" aria-label="Пол">
                <option v-if="userData.sex == undefined" @click="setSex(null)" selected>Пол</option>
                <option :value="false" :selected="userData.sex == false" @click="setSex(false)">Мужской</option>
                <option :value="true" :selected="userData.sex == true" @click="setSex(true)">Женский</option>
              </select>
            </div>
        </div>
        <div class="row form-row">
            <div class="col-auto">
              <div class="custom-form-floating">
                <input type="text" class="form-control sys-input-288" id="InputSystemID" placeholder="Идентификатор" v-model="userData.id" readonly>
                <label for="InputSystemID">Идентификатор</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="custom-form-floating">
                <input type="text" class="form-control sys-input-288" id="InputSystemRole" placeholder="Соискатель" v-model="systemStatus" readonly>
                <label for="InputSystemRole">Статус в системе</label>
              </div>
            </div>
            <div class="col-auto">
              <div v-if="userData.applicant && !userData.is_superuser" class="custom-form-floating">
                <input type="text" class="form-control sys-input-288" id="InputEDUid" placeholder="Номер зачётной книжки" v-model="userData.applicant.edu_number">
                <label for="InputEDUid">Номер зачётной книжки</label>
              </div>
            </div>
        </div>
        <div v-if="userData.applicant && !userData.is_superuser" class="row form-row">
            <div class="col-auto">
              <CatalogSearch :callback="fetchInstitutions" :isLoading="dataLoading" v-model="selectedInstitution"/>
            </div>
            <div class="col-auto">
              <select v-if="eduLevels.count" class="form-select sys-input-288" aria-label="Уровень образования">
                <option v-if="!userData.applicant.edu_level_id" @click="setLevel(null)" selected>Уровень образования</option>
                <option
                  v-for="level in eduLevels.items" 
                  :key="level.id"
                  :value="level.id"
                  :selected="checkLevelSelected(level.id)"
                  @click="setLevel(level.id)"
                >
                  {{ level.name }}
                </option>
              </select>
            </div>
            <div class="col-auto">
              <select class="form-select sys-input-288" aria-label="Статус обучения">
                <option v-if="!userData.applicant.edu_status" @click="setStatus(null)" selected>Статус обучения</option>
                <option
                  :value="'progress'"
                  @click="setStatus('progress')"
                  :selected="userData.applicant.edu_status && userData.applicant.edu_status == 'progress'"
                >
                  Студент
                </option>
                <option
                  :value="'completed'"
                  @click="setStatus('completed')"
                  :selected="userData.applicant.edu_status && userData.applicant.edu_status == 'completed'"
                >
                  Выпускник
                </option>
              </select>
            </div>
        </div>
        <div class="btn-account-wrapper">
          <button type="button" class="btn btn-primary sys-btn-264 btn-account" @click="saveChanges">
            Сохранить изменения
          </button>
        </div>
      </div>
      <div class="account-container account-security-container">
        <h1>Аккаунт и безопасность</h1>
        <div class="row form-row-security">
          <div class="col">
            <div class="custom-form">
              <input type="password" class="form-control" id="InputPassword" placeholder="Текущий пароль" v-model="oldPassword">
            </div>
          </div>
          <div class="col">
            <div class="custom-form">
              <input type="password" class="form-control" id="InputNewPassword" placeholder="Новый пароль" v-model="newPassword">
            </div>
          </div>
          <div class="col">
            <div class="custom-form">
              <input type="password" class="form-control" id="InputNewPassword2" placeholder="Подтверждение пароля" v-model="newPassword2">
            </div>
          </div>
          <div class="col">
            <button type="button" class="btn btn-primary sys-btn-264 btn-account" @click="changePassword">
              Сменить пароль
            </button>
          </div>
        </div>
        <div class="row form-row-security">
          <div class="col">
            <div class="custom-form">
              <input type="password" class="form-control" id="InputPasswordEmail" placeholder="Текущий пароль"v-model="oldPasswordEmail">
            </div>
          </div>
          <div class="col">
            <div class="custom-form">
              <input type="text" class="form-control" id="InputEmail" placeholder="Электронная почта" v-model="userData.email">
            </div>
          </div>
          <div class="col">
            <div class="custom-form" style="visibility: hidden;">
              <input type="text" class="form-control" id="InputEmail3" placeholder="Электронная почта">
            </div>
          </div>
          <div class="col">
            <button type="button" class="btn btn-primary sys-btn-264 btn-account" @click="changeEmail">
              Сменить почту
            </button>
          </div>
        </div>
      </div>
    </div>
  </main>
  <TheFooter />
</template>

<style scoped>

.account-container {
  width: 100%;
  margin: 0 auto;
  border-color: #DBE0E5;
  border-width: 1px;
  border-style: solid;
  border-radius: 10px;
  background-color: #FFFFFF;
}

.account-container h1 {
  font-family: "Montserrat";
  font-size: 32px;
  font-weight: 700;
  color: #343434;
  margin-top: 48px;
  margin-bottom: 24px;
  margin-left: 48px;
}

.account-data-container {
  margin-top: 55px;
  margin-bottom: 37px;
}

.account-security-container {
  min-height: 284px;
  margin-bottom: 55px;
}

.form-row {
  margin-left: 34px;
  margin-bottom: 24px;
}

.form-row select {
  height: 48px;
}

.form-row-security {
  margin-left: 34px;
}

.form-row-security input {
  height: 48px;
}

.btn-account-wrapper {
  display: flex;
  margin-bottom: 48px;
}

.btn-account {
  margin-left: auto;
  margin-right: 48px;
}

</style>