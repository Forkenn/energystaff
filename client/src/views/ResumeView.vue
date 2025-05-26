<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import TheHeader from '@/components/global/TheHeader.vue';
import TheFooter from '@/components/global/TheFooter.vue';
import ResumeService from '@/services/resume.service';
import RecommendationsService from '@/services/recommendations.service';
import ToolsService from '@/services/tools.service';
import TheFilesList from '@/components/global/TheFilesList.vue';

const resume = ref({});
const recommendation = ref({});

const route = useRoute();
const router = useRouter();
const applicantId = route.query.id;
const serverEduLevels = ref([]);
const serverEduInstitution = ref({});
const eduInstitution = ref('')
const dataLoading = ref(true);

const formattedTypes = computed(() => {
	const list = resume.value.resume_types

	if (!list || list.length === 0) return 'не указано'
  const names = list.map(item => item.name.toLowerCase())

  if (names.length === 1) return names[0]
  if (names.length === 2) return `${names[0]} или ${names[1]}`

  const allButLast = names.slice(0, -1).join(', ')
  const last = names[names.length - 1]

  return `${allButLast} или ${last}`
})

const formattedFormats = computed(() => {
	const list = resume.value.resume_formats

	if (!list || list.length === 0) return 'не указано'
  const names = list.map(item => item.name.toLowerCase())

  if (names.length === 1) return names[0]
  if (names.length === 2) return `${names[0]} или ${names[1]}`

  const allButLast = names.slice(0, -1).join(', ')
  const last = names[names.length - 1]

  return `${allButLast} или ${last}`
})

const edu_level = computed(() => {
  if(!serverEduLevels.value)
    return 'не загружено'

  let level = serverEduLevels.value.find(
        obj => obj.id === resume.value.applicant?.edu_level_id
  );

  if(!level)
    return 'не указано'

  if(resume.value.applicant?.edu_status == "progress") 
    return level?.name + ' (в процессе)'

  return level?.name
})

const updateEdu = () => {
  console.log(serverEduInstitution.value)
  if(!serverEduInstitution.value.id) {
    eduInstitution.value = 'не загружено';
    return;
  }

  if(resume.value.applicant?.edu_institution_id) {
    eduInstitution.value = serverEduInstitution.value.name;
    return;
  }

  eduInstitution.value = 'не указано';
}

watch(serverEduInstitution, updateEdu);

onMounted(async() => {
  try {
		const response = await ResumeService.getResumeByUserId(applicantId, true);
		resume.value = response.data;
    dataLoading.value = false;
	} catch(err) {
    if (window.history.state?.back) {
      alert('УПС!\nРезюме уже удалено...');
      router.go(-1);
    } else {
      router.push({ name: "home" });
    }
	}

  try {
		const response = await RecommendationsService.getApplicantRec(applicantId);
		recommendation.value = response.data;
	} catch(err) {}

  try {
    let response = await ToolsService.getEduLevels();
    serverEduLevels.value = response.data.items;
  } catch(err) {}

  try {
    const response = await ToolsService.getEduInstitutionbyId(resume.value.applicant.edu_institution_id);
    serverEduInstitution.value = response.data;
    dataLoading.value = false;
  } catch(err) {}
});
</script>

<template>
	<TheHeader />
  <main>
		<div class="container container-pd52">
			<div class="resume-container">
        <div class="resume-wrapper">
          <h1 class="mb-4">
            Резюме
          </h1>
          <p class="fio mt-4">
            {{ resume.applicant?.surname + ' ' + resume.applicant?.name + ' ' + resume.applicant?.last_name }}
          </p>
          <p>
            Дата рождения: 
            <span>{{ resume.applicant?.birthdate }}</span>
          </p>
          <p>
            Город: 
            <span>{{ resume.applicant?.location.name }}</span>
          </p>
          <p>
            Пол: 
            <span>{{ resume.applicant?.sex ? "Женский" : "Мужской" }}</span>
          </p>
          <p>
            Образовательное учреждение: 
            <span>{{ eduInstitution }}</span>
          </p>
          <p>
            Уровень образования: 
            <span>{{ edu_level }}</span>
          </p>
          <p class="mt-4">
            Желаемая позиция: 
            <span>{{ resume.position }}</span>
          </p>
          <p>
            Желаемая специальность: 
            <span>{{ resume.specialization }}</span>
          </p>
          <p>
            Ожидаемая зарплата: 
            <span v-if="!resume.salary || resume.salary == 0">не указано</span>
            <span v-else>{{ resume.salary }} ₽</span>
          </p>
          <p>
            Предпочитаемый тип занятости: 
            <span>{{ formattedTypes }}</span>
          </p>
          <p>
            Предпочитаемый формат работы: 
            <span>{{ formattedFormats }}</span>
          </p>
          <div v-if="resume.description" class="resume-description">
            <h1 class="mt-5 mb-4">Описание</h1>
            <p>
              {{ resume.description }}
            </p>
          </div>
        </div>
			</div>
      <div class="resume-container" v-if="recommendation.id">
        <div class="resume-wrapper">
          <div class="resume-description">
            <h1 class="mb-4">Рекомендации образовательного учреждения</h1>
            <p>
              {{ recommendation.description }}
            </p>
          </div>
          <p class="mt-4 mb-4">
            Подтверждающие документы
          </p>
          <TheFilesList :files="recommendation.documents"/>
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
	font-family: "Montserrat";
  border-color: #DBE0E5;
  border-width: 1px;
  border-style: solid;
  border-radius: 10px;
}

.resume-wrapper {
  margin: 48px;
}

.resume-wrapper h1 {
  font-size: 32px;
	font-weight: 700;
	color: #343434;
}

.resume-wrapper p {
	color: #343434;
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.resume-wrapper .fio {
	color: #343434;
  font-size: 25px;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.resume-wrapper span {
	color: #343434;
  font-size: 20px;
  font-weight: 400;
  margin-bottom: 0.5rem;
}

.resume-buttons {
	display: grid;
	margin-top: 24px;
}

.resume-description h1 {
	font-size: 32px;
	font-weight: 700;
	color: #343434;
}

.resume-description p {
	text-align: justify;
	color: #343434;
  font-size: 20px;
  font-weight: 400;
}

.control-buttons button {
  margin-right: 24px;
}

</style>
