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
            <h1>Рекомендации ОУ</h1>
            <div class="row">
                <div class="col d-flex">
                    <div class="resume-text-area">
                        <label for="formControlExtended" class="form-label">Описание рекомендации</label>
                        <textarea class="form-control" id="formControlExtended" rows="15"></textarea>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col d-flex" style="flex-direction: column;">
                    <label for="formFileMultiple" class="form-label">Подтверждающие документы</label>
                    <input class="form-control sys-input-900-flex" type="file" id="formFileMultiple" multiple>
                </div>
            </div>
            <div class="row">
                <div class="col d-flex">
                    <div class="editor-buttons">
                        <button type="button" class="btn btn-primary sys-btn-288">
                            Скрыть рекомендацию
                        </button>
                        <button type="button" class="btn btn-primary sys-btn-288">
                            Сохранить изменения
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

.form-control::file-selector-button {
  padding-top: 0.65rem;
  padding-bottom: 0.8rem;
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