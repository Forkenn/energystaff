<script setup>
import { ref, onMounted } from 'vue';

import TheHeader from '@/components/global/TheHeader.vue'
import TheFooter from '@/components/global/TheFooter.vue'
import MultiUpload from '@/components/global/MultiUpload.vue';

const isLoading = ref(true);
const creatorMode = ref(true);

let recommendationData = {
  description: "Проверка связи",
  documents: [{
      "id": 1,
      "download_name": "Тестовый_файл.doc",
      "real_name": "555_Тестовый_файл.doc",
      "size": 500
  }]
}

const newRecommendationData = ref({
  description: "",
  documents: [],
  deleted_documents: []
})

const files = ref([]);

const prepareFiles = () => {
  if (!creatorMode) {
    recommendationData.documents.forEach(uploadedFile => {
      const exists = uploadedFile.id
        ? files.value.some(file => file.id === uploadedFile.id)
        : false;
      
      if (!exists) {
        newRecommendationData.value.deleted_documents.push(uploadedFile.real_name);
      }
    });
  }

  for (const uploadFile of files.value)
    if(uploadFile.data)
      newRecommendationData.value.documents.push(uploadFile.data);
}

const saveRecommendation = async() => {
  prepareFiles();
  files.value = [...recommendationData.documents]; // после запроса, если редактирование
  console.log(newRecommendationData.value);
}

onMounted(async () => {
  console.log(files.value); isLoading.value = false;
})

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
                <div class="col-auto" style="flex-direction: column;">
                  <label class="form-label">Подтверждающие документы</label>
                    <MultiUpload v-model="files" :isLoading="isLoading" />
                </div>
            </div>
            <div class="row">
                <div class="col d-flex">
                    <div class="editor-buttons">
                        <button type="button" class="btn btn-primary sys-btn-288">
                            Удалить рекомендацию
                        </button>
                        <button type="button" class="btn btn-primary sys-btn-288" @click="saveRecommendation">
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