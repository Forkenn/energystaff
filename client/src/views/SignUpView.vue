<script setup>
import { ref, reactive  } from 'vue'
import { useRouter } from 'vue-router';

import TheHeader from '../components/global/TheHeader.vue'
import TheFooter from '../components/global/TheFooter.vue'
import AuthService from '@/services/auth.service'
import { useAuthRedirect } from '@/composables/useAuthRedirect';
import { errorMessages } from 'vue/compiler-sfc';

useAuthRedirect();
const router = useRouter();

const userData= ref({
  surname: "",
  name: "",
  email: "",
  password: "",
})

const employerData = ref({
  company_id: null,
  company_name: null,
})

const eduData = ref({
  edu_institution_id: null
})

const flexSwitchEmployer = ref(false)
const flexSwitchEDU = ref(false)
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

const registerApplicant = async() => {
  try {
    await AuthService.registerApplicant(userData.value)
    router.push({ name: 'login_page' });
  } catch(err) {
    if (err.response?.status == 400) {
      alert("Данный E-mail уже занят");
    }
  }
}

const registerEmployer = async() => {
  const userEmployerData = reactive({
    ...userData.value,
    ...employerData.value
  });

  try {
    await AuthService.registerEmployer(userEmployerData)
    router.push({ name: 'login_page' });
  } catch(err) {
    if (err.response?.status == 400) {
      alert("Данный E-mail уже занят");
    }
  }
}

const registerEdu = async() => {
  const userEduData = reactive({
    ...userData.value,
    ...eduData.value
  });

  try {
    await AuthService.registerEDU(userEduData.value)
    router.push({ name: 'login_page' });
  } catch(err) {
    if (err.response?.status == 400) {
      alert("Данный E-mail уже занят");
    }
  }
}

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
          <input
            class="form-control form-text-field sys-input-288"
            type="text form-text-field"
            placeholder="Наименование компании"
            aria-label="Наименование компании"
            v-model="employerData.company_name"
          >
          <select class="form-select" aria-label="Город">
            <option selected>Город</option>
            <option value="1">Москва</option>
            <option value="2">Смоленск</option>
            <option value="3">Санкт-Петербург</option>
          </select>
          <button type="button" class="btn btn-primary sys-btn-288" @click="toggleContainer">Назад</button>
          <button type="button" class="btn btn-primary sys-btn-288" @click="registerEmployer">
            Зарегистрироваться
          </button>
        </div>
      </div>
      <div v-if="eduContainerFlag" class="sign-up-container container-employer">
        <h1>Образовательное учреждение</h1>
        <div class="sign-up-form-group">
          <input
            class="form-control form-text-field sys-input-288"
            type="text form-text-field"
            placeholder="Наименование ОУ"
            aria-label="Наименование ОУ"
          >
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