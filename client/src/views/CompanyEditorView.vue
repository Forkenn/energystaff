<script setup>
import TheFooter from '@/components/global/TheFooter.vue';
import TheHeader from '@/components/global/TheHeader.vue';

</script>

<template>
  <TheHeader />
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
                <input type="text" class="form-control flex-grow-1 sys-input-600-flex" id="InputName" placeholder="Наименование">
                <label for="InputName">Наименование</label>
              </div>
            </div>
            <div class="col d-flex">
              <div class="custom-form-floating">
                <input type="text" class="form-control sys-input-288" id="InputCompanyID" placeholder="Отсутсвует">
                <label for="InputCompanyID">Идентификатор</label>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-auto">
              <div class="custom-form-floating">
                <input type="date" class="form-control sys-input-288" id="InputCompanyDate" placeholder="Дата регистрации">
                <label for="InputCompanyDate">Дата регистрации</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="custom-form-floating">
                <input type="text" class="form-control sys-input-288" id="InputCompanyID" placeholder="Отсутсвует">
                <label for="InputCompanyID">Место</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="custom-form-floating">
                <input type="text" class="form-control sys-input-288" id="InputCompanyINN" placeholder="ИНН">
                <label for="InputCompanyINN">ИНН</label>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-auto sys-col-600-flex">
              <div class="custom-form-floating">
                <input type="text" class="form-control flex-grow-1 sys-input-600-flex" id="InputCompanyAddress" placeholder="Юридический адрес">
                <label for="InputCompanyAddress">Юридический адрес</label>
              </div>
            </div>
            <div class="col d-flex">
              <div class="custom-form-floating">
                <input type="text" class="form-control sys-input-288" id="InputCompanyStatus" placeholder="Статус в системе">
                <label for="InputCompanyStatus">Статус в системе</label>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col d-flex">
              <div class="company-text-area">
                <label for="formControlExtended" class="form-label">Описание</label>
                <textarea class="form-control" id="formControlExtended" rows="15"></textarea>
              </div>
            </div>
          </div>
          <div class="col d-flex">
            <div style="margin-left: auto;">
              <button type="button" class="btn btn-primary sys-btn-264">
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