<script setup>
import { computed } from 'vue';

import TheHeader from '../components/global/TheHeader.vue'
import TheFooter from '../components/global/TheFooter.vue'
import { useUserStore } from '@/stores/user';
import UserService from '@/services/user.service';

const userStore = useUserStore();
const userData = computed(() => userStore.user.data);
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
  if(userData.value.applicant) {
    return "Соискатель"
  }
  return "Загрузка..."
})

const saveChanges = async() => {
  try{
    await UserService.editCurrent(userData.value)
    alert("Изменения сохранены!")
  } catch(err) {
    alert("Ошибка сохранения данных!")
  }
}

</script>

<template>
  <TheHeader />
  <main>
    <div class="container container-pd52">
      <div class="account-container account-data-container">
        <h1>Личные данные</h1>
        <div class="row form-row">
          <div class="col">
            <div class="custom-form-floating">
              <input type="text" class="form-control" id="InputSurname" placeholder="Фамилия" v-model="userData.surname">
              <label for="InputSurname">Фамилия</label>
            </div>
          </div>
          <div class="col">
            <div class="custom-form-floating">
              <input type="text" class="form-control" id="InputFirstname" placeholder="Имя" v-model="userData.name">
              <label for="InputFirstname">Имя</label>
            </div>
          </div>
          <div class="col">
            <div class="custom-form-floating">
              <input type="text" class="form-control" id="InputSecondname" placeholder="Отчество" v-model="userData.last_name">
              <label for="InputSecondname">Отчество</label>
            </div>
          </div>
        </div>
        <div class="row form-row">
            <div class="col">
              <div class="custom-form-floating">
                <input type="date" class="form-control" id="InputBirthdate" placeholder="Дата рождения" v-model="userData.birthdate">
                <label for="InputBirthdate">Дата рождения</label>
              </div>
            </div>
            <div class="col">
              <div class="custom-form-floating">
                <input type="text" class="form-control" id="InputEDUid" placeholder="Номер зачётной книжки">
                <label for="InputEDUid">Номер зачётной книжки</label>
              </div>
            </div>
            <div class="col">
              <div class="custom-form-floating">
                <input type="text" class="form-control" id="InputSystemID" placeholder="Идентификатор" v-model="userData.id">
                <label for="InputSystemID">Идентификатор</label>
              </div>
            </div>
        </div>
        <div class="row form-row">
            <div class="col">
              <select class="form-select" aria-label="Город">
                <option selected>Город</option>
                <option value="1">Москва</option>
                <option value="2">Смоленск</option>
                <option value="3">Санкт-Петербург</option>
              </select>
            </div>
            <div class="col">
              <select class="form-select" aria-label="Пол">
                <option selected>Пол</option>
                <option value="1">Мужской</option>
                <option value="2">Женский</option>
              </select>
            </div>
            <div class="col">
              <div class="custom-form-floating">
                <input type="text" class="form-control" id="InputSystemRole" placeholder="Соискатель" v-model="systemStatus">
                <label for="InputSystemRole">Статус в системе</label>
              </div>
            </div>
        </div>
        <div class="row form-row">
            <div class="col">
              <select class="form-select" aria-label="Образовательное учреждение">
                <option selected>Образовательное учреждение</option>
                <option value="1">МГУ</option>
                <option value="2">МГИМО</option>
                <option value="3">МЭИ</option>
              </select>
            </div>
            <div class="col">
              <select class="form-select" aria-label="Уровень образования">
                <option selected>Уровень образования</option>
                <option value="1">Бакалавриват</option>
                <option value="2">Специалитет</option>
                <option value="3">Магистратура</option>
              </select>
            </div>
            <div class="col">
              <select class="form-select" aria-label="Статус обучения">
                <option selected>Статус обучения</option>
                <option value="1">Студент</option>
                <option value="2">Выпускник</option>
              </select>
            </div>
        </div>
        <div class="btn-account-wrapper">
          <button type="button" class="btn btn-primary sys-btn-288 btn-account" @click="saveChanges">
            Сохранить изменения
          </button>
        </div>
      </div>
      <div class="account-container account-security-container">
        <h1>Аккаунт и безопасность</h1>
        <div class="row form-row-security">
          <div class="col">
            <div class="custom-form">
              <input type="text" class="form-control" id="InputPassword" placeholder="Текущий пароль">
            </div>
          </div>
          <div class="col">
            <div class="custom-form">
              <input type="text" class="form-control" id="InputNewPassword" placeholder="Новый пароль">
            </div>
          </div>
          <div class="col">
            <div class="custom-form">
              <input type="text" class="form-control" id="InputNewPassword2" placeholder="Подтверждение пароля">
            </div>
          </div>
          <div class="col">
            <button type="button" class="btn btn-primary sys-btn-288 btn-account">
              Сменить пароль
            </button>
          </div>
        </div>
        <div class="row form-row-security">
          <div class="col">
            <div class="custom-form">
              <input type="text" class="form-control" id="InputEmail" placeholder="Электронная почта">
            </div>
          </div>
          <div class="col">
            <div class="custom-form" style="visibility: hidden;">
              <input type="text" class="form-control" id="InputEmail2" placeholder="Электронная почта">
            </div>
          </div>
          <div class="col">
            <div class="custom-form" style="visibility: hidden;">
              <input type="text" class="form-control" id="InputEmail3" placeholder="Электронная почта">
            </div>
          </div>
          <div class="col">
            <button type="button" class="btn btn-primary sys-btn-288 btn-account">
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
  min-height: 500px;
  margin-top: 55px;
  margin-bottom: 37px;
}

.account-security-container {
  min-height: 284px;
  margin-bottom: 55px;
}

.form-row {
  margin-right: 360px;
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
}

.btn-account {
  margin-left: auto;
  margin-right: 48px;
}

</style>