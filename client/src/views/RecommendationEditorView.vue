<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import TheHeader from '@/components/global/TheHeader.vue'
import TheFooter from '@/components/global/TheFooter.vue'
import MultiUpload from '@/components/global/MultiUpload.vue';

import RecommendationsService from '@/services/recommendations.service';

const router = useRouter();
const route = useRoute();
const applicantId = route.query.id;

const isLoading = ref(true);
const creatorMode = ref(true);
let errorMsg = '';

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

const validateFields = () => {
  errorMsg = '';

  if(
    newRecommendationData.value.documents.length < 1 ||
    newRecommendationData.value.documents.length > 10
  )
    errorMsg += '• Недопустимое кол-во документов (допустимо от 1 до 10 файлов)\n';

  if(10 < newRecommendationData.value.description.length > 5000 )
    errorMsg += '• Недопустимое описание (допустимо до 5000 символов)\n';
}

const prepareFiles = () => {
  if (!creatorMode.value) {
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
  validateFields();
  if(errorMsg != '') {
    alert(`Ошибка сохранения изменений:\n${errorMsg}`);
    return;
  }

  if(!creatorMode.value) {
    try {
      await RecommendationsService.editRecommendation(recommendationData.id, newRecommendationData.value)
      router.go(0);
    } catch(err) {
      console.log(err);
      alert('Ошибка сохранения!');
    }
  } else {
    try {
      await RecommendationsService.addRecommendation(applicantId, newRecommendationData.value)
      router.go(0);
    } catch(err) {
      console.log(err);
      alert('Ошибка сохранения!');
    }
  }
}

const deleteRecommendation = async() => {
  try {
    await RecommendationsService.deleteRecommendation(recommendationData.id);
    router.push({ name: 'edu_verification' });
  } catch(err) {
    alert('Ошибка удаления!');
  }
}

onMounted(async () => {
  if(!applicantId)
    router.push({ name: 'home' });

  try {
    const response = await RecommendationsService.getApplicantRec(applicantId);
    recommendationData = response.data;
    creatorMode.value = false;
  } catch(err) {
    if(err.response?.status != 404) {
      router.push({ name: 'home' });
    }
    isLoading.value = false;
  }
  if(!creatorMode.value) {
    files.value = [...recommendationData.documents];
    newRecommendationData.value.description = recommendationData.description;
    isLoading.value = false;
  }
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
                        <textarea class="form-control" id="formControlExtended" rows="15" v-model="newRecommendationData.description"></textarea>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col" style="flex-direction: column;">
                  <label class="form-label">Подтверждающие документы <span class="required-field">*</span></label>
                    <MultiUpload v-model="files" :isLoading="isLoading" />
                </div>
            </div>
            <div class="row">
                <div class="col d-flex">
                    <div class="editor-buttons">
                        <button v-if="!creatorMode" type="button" class="btn btn-danger sys-btn-288" @click="deleteRecommendation">
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