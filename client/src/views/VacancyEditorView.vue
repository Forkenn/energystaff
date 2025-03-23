<script setup>
import TheFooter from '@/components/global/TheFooter.vue';
import TheHeader from '@/components/global/TheHeader.vue';

</script>

<template>
  <TheHeader />
  <main>
    <div class="container container-pd52">
      <div class="vacancy-container">
        <div class="editor-wrapper">
          <h1>
            Данные вакансии
          </h1>
          <div class="row">
            <div class="col-auto sys-col-912-flex">
              <div class="custom-form-floating">
                <input type="text" class="form-control flex-grow-1 sys-input-912-flex" id="InputName" placeholder="Должность">
                <label for="InputName">Должность</label>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-auto sys-col-600-flex">
              <div class="custom-form-floating">
                <input type="text" class="form-control flex-grow-1 sys-input-600-flex" id="InputSpecialization" placeholder="Специализация">
                <label for="InputSpecialization">Специализация</label>
              </div>
            </div>
            <div class="col d-flex">
              <div class="floating-input-group">
                <div class="custom-form-floating">
                  <input type="text" class="form-control flex-grow-1 sys-input-group-250" id="InputSalary" placeholder="Зарплата">
                  <label for="InputSalary">Зарплата</label>
                </div>
                <span class="input-group-text sys-input-group-text-38">₽</span>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-auto">
              <div style="width: 80px;">
                  Занятость
              </div>
            </div>
            <div class="col-auto sys-col-184">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckEmploymentFull">
                <label class="form-check-label" for="flexCheckEmploymentFull">
                    Полная занятость
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckEmploymentPartial">
                <label class="form-check-label" for="flexCheckEmploymentPartial">
                    Частичная занятость
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckEmploymentProject">
                <label class="form-check-label" for="flexCheckEmploymentProject">
                    Проектная работа
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckEmploymentIntern">
                <label class="form-check-label" for="flexCheckEmploymentIntern">
                    Стажировка
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckEmploymentPractice">
                <label class="form-check-label" for="flexCheckEmploymentPractice">
                    Практика
                </label>
              </div>
            </div>
            <div class="col-auto">
              <select id="formMultiselect" class="form-select sys-input-288" aria-label="Рабочие часы">
                <option selected>Рабочие часы</option>
                <option value="1">5/2</option>
                <option value="2">2/2</option>
                <option value="3">4/2</option>
              </select>
            </div>
            <div class="col d-flex">
              <select id="formMultiselect" class="form-select sys-input-288" aria-label="Навыки">
                <option selected>Навыки</option>
                <option value="1">SQL</option>
                <option value="2">Python</option>
                <option value="3">Git</option>
              </select>
            </div>
          </div>
          <div class="row">
            <div class="col-auto">
              <div style="width: 80px;">
                  График
              </div>
            </div>
            <div class="col-auto sys-col-184" style="flex-direction: column;">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDayFull">
                <label class="form-check-label" for="flexCheckDayFull">
                    Полный день
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDayShift">
                <label class="form-check-label" for="flexCheckDayShift">
                    Сменный день
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDayFlex">
                <label class="form-check-label" for="flexCheckDayFlex">
                    Гибкий график
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckRemote">
                <label class="form-check-label" for="flexCheckRemote">
                    Удалённая работа
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault">
                <label class="form-check-label" for="flexCheckDefault">
                    Вахтовый метод
                </label>
              </div>
            </div>
            <div class="col-auto">
              <select id="formMultiselect" class="form-select sys-input-288" aria-label="График">
                <option selected>График</option>
                <option value="1">5/2</option>
                <option value="2">2/2</option>
                <option value="3">4/2</option>
              </select>
            </div>
          </div>
          <div class="row">
            <div class="col d-flex">
              <div class="vacancy-text-area">
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

.vacancy-container {
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

.col-checkbox {
  flex-direction: column;
  min-width: 288px;
  max-width: 508px;
}

.vacancy-text-area {
    width: 100%;
}

.vacancy-text-area textarea {
    max-width: 912px;
    min-width: 288px;
    max-height: 370px;
    resize: none;
}

</style>