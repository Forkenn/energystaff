<script setup>
import TheHeader from '../components/global/TheHeader.vue'
import TheFooter from '../components/global/TheFooter.vue'
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
            class="form-control"
            id="FormControlEmailInput"
            placeholder="Электронная почта"
          >
          <input
            type="password"
            id="SignInInputPassword"
            class="form-control"
            placeholder="Пароль"
          >
          <button type="button" class="btn btn-primary">Вход</button>
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
  width: 288px;
  height: 48px;
  margin-bottom: 24px;
}

.sign-in-form-group button {
  width: 288px;
  height: 48px;
  margin-bottom: 24px;
  border-radius: 40px;
}

.registration-link {
  color: #1775E4;
  font-family: 'Montserrat';
  font-weight: 700;
  font-size: 16px;
  text-decoration: none;
}

</style>