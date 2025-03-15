<script setup>
import TheHeader from '../components/global/TheHeader.vue'
import TheFooter from '../components/global/TheFooter.vue'
import { ref } from 'vue'

const flexSwitchEmployer = ref(false)
const flexSwitchEDU = ref(false)

const toggleSwitch = (num) => {
    if (num == 1)
        flexSwitchEDU.value = false;
    else
        flexSwitchEmployer.value = false;
}
</script>

<template>
  <TheHeader />
  <main>
    <div class="container container-pd52">
      <div class="sign-up-container">
        <h1>Регистрация</h1>
        <div class="sign-up-form-group">
          <input
            class="form-control form-text-field"
            type="text form-text-field"
            placeholder="Фамилия"
            aria-label="Фамилия"
          >
          <input
            class="form-control form-text-field"
            type="text form-text-field"
            placeholder="Имя"
            aria-label="Имя"
          >
          <input
            type="email"
            class="form-control form-text-field"
            id="FormControlEmailInput"
            placeholder="Электронная почта"
          >
          <input
            type="password"
            id="SignInInputPassword"
            class="form-control form-text-field"
            placeholder="Пароль"
          >
          <input
            type="password"
            id="SignInInputPassword"
            class="form-control form-text-field"
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
          <button type="button" class="btn btn-primary">Далее</button>
        </div>
      </div>
    </div>
  </main>
  <TheFooter />
</template>

<style scoped>

.sign-up-container {
  width: 382px;
  height: 659px;
  margin-top: 121px;
  margin-bottom: 121px;
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

.sign-up-form-group {
  text-align: center;
}

.form-text-field {
  margin: 0 auto;
  width: 288px;
  height: 48px;
  margin-bottom: 24px;
}

.sign-up-form-group button {
  width: 288px;
  height: 48px;
  margin-bottom: 24px;
  border-radius: 40px;
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