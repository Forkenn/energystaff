<script setup>
import { ref, computed, onMounted } from 'vue';

import TheFooter from '@/components/global/TheFooter.vue';
import TheHeader from '@/components/global/TheHeader.vue';
import TheBlockPage from '@/components/global/TheBlockPage.vue';
import CompaniesService from '@/services/companies.service';
import { useUserStore } from '@/stores/user';

const userStore = useUserStore();
const editorMode = ref(false)
const companyData = ref({
  id: null,
  name: "",
  registration_date: "2025-01-01",
  inn: null,
  address: null,
  description: null, 
  is_verified: false
})
const companyStatus = computed(() => {
  return companyData.value.is_verified ? 'Подтверждено' : 'Не подтверждено'
})
let errorMsg = '';

const validateFields = () => {
  errorMsg = '';
  if(
    !companyData.value.name ||
    companyData.value.name?.length < 5 ||
    companyData.value.name?.length > 120
  )
    errorMsg += '• Недопустимое наименование (допустимо от 5 до 120 символов)\n';

  if(!companyData.value.inn || companyData.value.inn?.length < 10)
    errorMsg += '• Недопустимый ИНН (допустимо от 10 до 12 символов)\n';

  if(companyData.value.description?.length > 5000)
    errorMsg += '• Недопустимое описание (допустимо до 5000 символов)\n';

  if(companyData.value.address?.length > 120)
    errorMsg += '• Недопустимый адрес (допустимо до 120 символов)\n';

  if(companyData.value.registration_date == '' || !companyData.value.registration_date)
    errorMsg += '• Недопустимая дата\n';
}

const validateINN = (event) => {
  let value = event.target.value.replace(/[^\d]/g, '');
  if (value.length > 12)
    value = value.slice(0, 12);

  companyData.value.inn = value;
};

const editCompany = async() => {
  validateFields();
  if(errorMsg != '') {
    alert(`Ошибка сохранения изменений:\n${errorMsg}`);
    return;
  }

  try {
    companyData.value.inn = String(companyData.value.inn);
    await CompaniesService.editCompany(companyData.value.id, companyData.value)
  } catch (err) {
    alert("Ошибка сохранения изменений!");
  }
}

onMounted(async () => {
  if(!userStore.user.data.is_verified)
    return;

  const companyId = userStore.user.data.employer?.company_id;
  if(companyId) {
    try {
      const response = await CompaniesService.getCompany(companyId);
      companyData.value = response.data;
      console.log(companyData.value)
    } catch(err) {
      alert("Ошибка получения данных компании!");
    } finally {
      editorMode.value = true
    }
  }
})

</script>

<template>
  <TheHeader />
  <TheBlockPage v-if="!userStore.user.data.is_verified"/>
  <main>
    <div class="container container-pd52">
      <div class="company-container">
        <div class="editor-wrapper">
          <h1>
            Данные компании
          </h1>
          <div class="row">
            <div class="col-auto sys-col-600-flex">
              <div class="custom-form-floating">
                <input type="text" class="form-control flex-grow-1 sys-input-600-flex" id="InputName" placeholder="Наименование" v-model="companyData.name">
                <label for="InputName">Наименование <span class="required-field">*</span></label>
              </div>
            </div>
            <div class="col d-flex">
              <div class="custom-form-floating">
                <input type="text" class="form-control sys-input-288" id="InputCompanyID" placeholder="Отсутсвует" v-model="companyData.id" readonly>
                <label for="InputCompanyID">Идентификатор</label>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-auto">
              <div class="custom-form-floating">
                <input type="date" class="form-control sys-input-288" id="InputCompanyDate" placeholder="Дата регистрации" v-model="companyData.registration_date">
                <label for="InputCompanyDate">Дата регистрации <span class="required-field">*</span></label>
              </div>
            </div>
            <div class="col-auto">
              <div class="custom-form-floating">
                <input
                  type="text"
                  class="form-control sys-input-288"
                  id="InputCompanyINN"
                  placeholder="ИНН"
                  v-model="companyData.inn"
                  @input="validateINN"
                >
                <label for="InputCompanyINN">ИНН <span class="required-field">*</span></label>
              </div>
            </div>
            <div class="col-auto">
              <div class="custom-form-floating">
                <input type="text" class="form-control sys-input-288" id="InputCompanyStatus" placeholder="Статус в системе" v-model="companyStatus" readonly>
                <label for="InputCompanyStatus">Статус в системе</label>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-auto sys-col-912-flex">
              <div class="custom-form-floating">
                <input type="text" class="form-control flex-grow-1 sys-input-912-flex" id="InputCompanyAddress" placeholder="Юридический адрес" v-model="companyData.address">
                <label for="InputCompanyAddress">Юридический адрес</label>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col d-flex">
              <div class="company-text-area">
                <label for="formControlExtended" class="form-label">Описание</label>
                <textarea class="form-control" id="formControlExtended" rows="15" v-model="companyData.description"></textarea>
              </div>
            </div>
          </div>
          <div class="col d-flex">
            <div style="margin-left: auto;">
              <button type="button" class="btn btn-primary sys-btn-264" @click="editCompany">
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

.company-container {
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

.company-text-area {
    width: 100%;
}

.company-text-area textarea {
    max-width: 912px;
    min-width: 288px;
    max-height: 370px;
    resize: none;
}

</style>