<script setup>
import TheHeader from '@/components/global/TheHeader.vue'
import TheFooter from '@/components/global/TheFooter.vue'

//$('#formMultiselect').multiselect();
</script>

<template>
  <TheHeader />
  <main>
    <div class="container container-pd52">
      <div class="resume-container">
        <div class="editor-wrapper">
            <h1>Данные резюме</h1>
            <div class="row">
                <div class="col d-flex">
                    <div class="custom-form-floating">
                        <input type="text" class="form-control flex-grow-1 sys-input-900-flex" id="InputPosition" placeholder="Желаемая должность">
                        <label for="InputPosition">Желаемая должность</label>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col d-flex">
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
                <div class="col d-flex col-checkbox" style="flex-direction: column;">
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
                <div class="col d-flex col-checkbox" style="flex-direction: column;">
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
            </div>
            <div class="row">
                <div class="col d-flex">
                    <div class="resume-text-area">
                        <label for="formControlExtended" class="form-label">Расширенное описание</label>
                        <textarea class="form-control" id="formControlExtended" rows="15"></textarea>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col d-flex">
                    <div class="editor-buttons">
                        <button type="button" class="btn btn-primary sys-btn-288">
                            Скрыть резюме
                        </button>
                        <button type="button" class="btn btn-primary sys-btn-288">
                            Сохранить
                        </button>
                    </div>
                </div>
            </div>
        </div>
      </div>
    </div>
  </main>
  <TheFooter />
</template>

<style scoped>

.resume-container {
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

.editor-wrapper .row {
    margin-bottom: 24px;
}

.col-checkbox {
    flex-direction: column;
    min-width: 288px;
    max-width: 508px;
}

.resume-text-area {
    width: 100%;
}

.resume-text-area textarea {
    max-width: 900px;
    min-width: 288px;
    max-height: 370px;
    resize: none;
}

.editor-buttons {
    display: flex;
    flex-direction: column;
    margin-left: auto;
}

</style>