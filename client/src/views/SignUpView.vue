<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router';

import TheHeader from '../components/global/TheHeader.vue'
import TheFooter from '../components/global/TheFooter.vue'
import CatalogSearch from '@/components/global/CatalogSearch.vue';
import AuthService from '@/services/auth.service'
import ToolsService from '@/services/tools.service';
import { useAuthRedirect } from '@/composables/useAuthRedirect';

useAuthRedirect();
const router = useRouter();
let errorMsg = '';

const userData= ref({
  surname: null,
  name: null,
  email: null,
  password: null,
})

const confirmPassword = ref(null);

const employerData = ref({
  company_id: null,
  company_name: null,
})

const selectedInstitution = ref(null);
const eduData = ref({
  edu_institution_id: null
})

const validateFields = () => {
  errorMsg = '';
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if(userData.value.password != confirmPassword.value)
    errorMsg += '• Несовпадение паролей\n';

  if(!userData.value.password || userData.value.password?.length < 8)
    errorMsg += '• Пароль меньше 8 символов\n';

  if(!userData.value.surname || userData.value.surname?.length < 2)
    errorMsg += '• Недопустимая фамилия\n';

  if(!userData.value.name || userData.value.name?.length < 2)
    errorMsg += '• Недопустимое имя\n';

  if(userData.value.email?.length < 5 || !emailPattern.test(userData.value.email))
    errorMsg += '• Недопустимая электронная почта\n';
}

const validateFieldsEDU = () => {
  if(!selectedInstitution.value) {
    errorMsg += '• Не выбрано ОУ или выбрано несуществующее\n';
  }
}

const validateFieldsEmployer = () => {
  if(employerData.value.company_name && flexSwitchCompany.value) {
    employerData.value.company_name = null
  }

  if(employerData.value.company_id && !flexSwitchCompany.value) {
    employerData.value.company_id = null
  }

  if(!employerData.value.company_id && flexSwitchCompany.value) {
    errorMsg += '• Не указан идентификатор компании\n';
  }

  if(!employerData.value.company_name && !flexSwitchCompany.value) {
    errorMsg += '• Не указано наименование компании\n';
  }
}

const showErr = (err) => {
  if (
    err.response?.status == 400 &&
    err.response?.data.detail == 'REGISTER_USER_ALREADY_EXISTS'
  ) {
    alert("Данный E-mail уже занят");
    return;
  }
  
  if (
    err.response?.status == 404 
  ) {
    alert("Компании или образовательного учреждения не существует");
    return;
  }

  if (err.response?.status == 422) {
    alert("Недопустмые данные регистрации");
    return;
  }
  alert(`Ошибка сервера (${err.response?.status || '500'})`);
}

const registerApplicant = async() => {
  validateFields();
  if(errorMsg != '') {
    alert(`Ошибка регистрации:\n${errorMsg}`);
    return;
  }

  try {
    await AuthService.registerApplicant(userData.value)
    router.push({ name: 'login_page' });
  } catch(err) {
    showErr(err);
  }
}

const registerEmployer = async() => {
  validateFields();
  validateFieldsEmployer();
  if(errorMsg != '') {
    alert(`Ошибка регистрации:\n${errorMsg}`);
    return;
  }

  if (employerData.value.company_id) {
    employerData.value.company_id = Number(employerData.value.company_id)
  }

  const userEmployerData = reactive({
    ...userData.value,
    ...employerData.value
  });

  try {
    await AuthService.registerEmployer(userEmployerData)
    router.push({ name: 'login_page' });
  } catch(err) {
    showErr(err);
  }
}

const registerEdu = async() => {
  validateFields();
  validateFieldsEDU();
  if(errorMsg != '') {
    alert(`Ошибка регистрации:\n${errorMsg}`);
    return;
  }

  eduData.value.edu_institution_id = selectedInstitution.value.id
  const userEduData = reactive({
    ...userData.value,
    ...eduData.value
  });

  try {
    await AuthService.registerEDU(userEduData)
    router.push({ name: 'login_page' });
  } catch(err) {
    showErr(err);
  }
}

//==============Containers state control=========================
const flexSwitchEmployer = ref(false)
const flexSwitchEDU = ref(false)
const flexSwitchCompany = ref(false)
const containerFlag = ref(true)
const employerContainerFlag = ref(false)
const eduContainerFlag = ref(false)

const toggleSwitch = (num) => {
    if (num == 1)
        flexSwitchEDU.value = false;
    else
        flexSwitchEmployer.value = false;
}

const toggleContainer = () => {
  if (flexSwitchEmployer.value) {
    containerFlag.value = !containerFlag.value
    employerContainerFlag.value = !employerContainerFlag.value
    return
  }
  if (flexSwitchEDU.value) {
    containerFlag.value = !containerFlag.value
    eduContainerFlag.value = !eduContainerFlag.value
    return
  }
}

const validateCompanyID = (event) => {
  employerData.value.company_id = event.target.value.replace(/[^\d]/g, '');
};

const fetchInstitutions = async(params) => {
  const response = await ToolsService.getEduInstitutions(params);
  return response;
};

</script>

<template>
  <TheHeader />
  <main>
    <div class="container container-pd52">
      <div v-if="containerFlag" class="sign-up-container container-all">
        <h1>Регистрация</h1>
        <div class="sign-up-form-group">
          <input
            class="form-control form-text-field sys-input-288"
            type="text form-text-field"
            placeholder="Фамилия"
            aria-label="Фамилия"
            v-model="userData.surname"
          >
          <input
            class="form-control form-text-field sys-input-288"
            type="text form-text-field"
            placeholder="Имя"
            aria-label="Имя"
            v-model="userData.name"
          >
          <input
            type="email"
            class="form-control form-text-field sys-input-288"
            id="FormControlEmailInput"
            placeholder="Электронная почта"
            v-model="userData.email"
          >
          <input
            type="password"
            id="SignInInputPassword"
            class="form-control form-text-field sys-input-288"
            placeholder="Пароль"
            v-model="userData.password"
          >
          <input
            type="password"
            id="SignInInputPassword"
            class="form-control form-text-field sys-input-288"
            placeholder="Подтверждение пароля"
            v-model="confirmPassword"
          >
          <div class="form-check form-switch">
            <input
              class="form-check-input form-switch-44px"
              type="checkbox"
              role="switch"
              id="flexSwitchEmployer"
              v-model="flexSwitchEmployer"
              @change="toggleSwitch(1)"
            >
            <label class="form-check-label" for="flexSwitchEmployer">
              Я работодатель
            </label>
          </div>
          <div class="form-check form-switch">
            <input
              class="form-check-input form-switch-44px"
              type="checkbox"
              role="switch"
              id="flexSwitchEDU"
              v-model="flexSwitchEDU"
              @change="toggleSwitch(2)"
            >
            <label class="form-check-label" for="flexSwitchEDU">
              Я работник ОУ
            </label>
          </div>
          <button
            v-if="flexSwitchEmployer || flexSwitchEDU"
            type="button"
            class="btn btn-primary sys-btn-288"
            @click="toggleContainer"
          >
            Далее
          </button>
          <button v-else type="button" class="btn btn-primary sys-btn-288" @click="registerApplicant">
            Зарегистрироваться
          </button>
        </div>
      </div>
      <div v-if="employerContainerFlag" class="sign-up-container container-employer">
        <h1>Компания</h1>
        <div class="sign-up-form-group">
          <input v-if="!flexSwitchCompany"
            class="form-control form-text-field sys-input-288"
            type="text form-text-field"
            placeholder="Наименование компании"
            aria-label="Наименование компании"
            v-model="employerData.company_name"
          >
          <input v-else
            class="form-control form-text-field sys-input-288"
            type="text form-text-field"
            placeholder="Идентификатор компании"
            aria-label="Идентификатор компании"
            v-model="employerData.company_id"
            @input="validateCompanyID"
          >
          <div class="form-check form-switch">
            <input
              class="form-check-input form-switch-44px"
              type="checkbox"
              role="switch"
              id="flexSwitchCompany"
              v-model="flexSwitchCompany"
            >
            <label class="form-check-label" for="flexSwitchCompany">
              По идентификатору
            </label>
          </div>
          <button type="button" class="btn btn-primary sys-btn-288" @click="toggleContainer">Назад</button>
          <button type="button" class="btn btn-primary sys-btn-288" @click="registerEmployer">
            Зарегистрироваться
          </button>
        </div>
      </div>
      <div v-if="eduContainerFlag" class="sign-up-container container-employer">
        <h1>Образовательное учреждение</h1>
        <div class="sign-up-form-group">
          <CatalogSearch class="institutions-search" :callback="fetchInstitutions" v-model="selectedInstitution"/>
          <button type="button" class="btn btn-primary sys-btn-288" @click="toggleContainer">Назад</button>
          <button type="button" class="btn btn-primary sys-btn-288" @click="registerEdu">
            Зарегистрироваться
          </button>
        </div>
      </div>
    </div>
  </main>
  <TheFooter />
</template>

<style scoped>

.sign-up-container {
  width: 382px;
  margin-left: auto;
  margin-right: auto;
  border-color: #DBE0E5;
  border-width: 1px;
  border-style: solid;
  border-radius: 10px;
  background-color: #FFFFFF;
}

.sign-up-container h1 {
  color: #5F666C;
  font-weight: 700;
  font-size: 32px;
  margin-top: 32px;
  margin-bottom: 46px;
  text-align: center;
}

.container-all {
  height: 659px;
  margin-top: 121px;
  margin-bottom: 121px;
}

.container-employer {
  height: 420px;
  margin-top: 266px;
  margin-bottom: 266px;
  margin-left: auto;
  margin-right: auto;
  border-color: #DBE0E5;
  border-width: 1px;
  border-style: solid;
  border-radius: 10px;
  background-color: #FFFFFF;
}

.sign-up-form-group {
  text-align: center;
}

.institutions-search {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0 auto;
  margin-bottom: 24px;
}

.form-text-field {
  margin: 0 auto;
  margin-bottom: 24px;
}

.sign-up-form-group select {
  width: 288px;
  height: 48px;
  margin: 0 auto;
  margin-bottom: 24px;
}

.form-check {
  text-align: left;
  width: 288px;
  height: 24px;
  margin: 0 auto;
  margin-bottom: 24px;
}

.form-check-label {
  margin-left: 8px;
  margin-top: 2px;
}

.form-switch-44px {
  width: 44px;
  height: 24px;
}

</style>