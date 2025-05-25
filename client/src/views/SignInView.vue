<script setup>

import { ref } from 'vue'
import { useRouter } from 'vue-router';

import TheHeader from '../components/global/TheHeader.vue'
import TheFooter from '../components/global/TheFooter.vue'
import AuthService from '@/services/auth.service'

const router = useRouter();

const userLogin = ref({ email: "", password: "" });

const login = async() => {
  try {
    await AuthService.login(userLogin.value);
    router.push({ name: 'home' });
  } catch(err) {
    if (err.response?.status == 400) {
      alert("Неверный логин или пароль");
    } else {
      alert(`Ошибка сервера (${err.response?.status || '500'})`);
    }
  }
}

</script>

<template>
  <TheHeader />
  <main>
    <div class="container container-pd52">
      <div class="sign-in-container">
        <h1>Личный кабинет</h1>
        <div class="sign-in-form-group">
          <input
            type="email"
            class="form-control sys-input-288"
            id="FormControlEmailInput"
            placeholder="Электронная почта"
            v-model="userLogin.email"
          >
          <input
            type="password"
            id="SignInInputPassword"
            class="form-control sys-input-288"
            placeholder="Пароль"
            v-model="userLogin.password"
          >
          <button type="button" class="btn btn-primary sys-btn-288" @click="login">Вход</button>
          <div>
            <router-link class="registration-link" to="/registration">
              <img src="../assets/icons/Chevron.svg" width="24" height="24">
              Регистрация
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </main>
  <TheFooter />
</template>

<style scoped>

.sign-in-container {
  width: 382px;
  height: 390px;
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

.sign-in-container h1 {
  color: #5F666C;
  font-weight: 700;
  font-size: 32px;
  margin-top: 32px;
  margin-bottom: 46px;
  text-align: center;
}

.sign-in-form-group {
  text-align: center;
}

.sign-in-form-group input {
  margin: 0 auto;
  margin-bottom: 24px;
}

.registration-link {
  color: #1775E4;
  font-family: 'Montserrat';
  font-weight: 700;
  font-size: 16px;
  text-decoration: none;
}

</style>