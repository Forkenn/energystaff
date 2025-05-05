<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import TheHeader from '@/components/global/TheHeader.vue';
import TheFooter from '@/components/global/TheFooter.vue';
import VacanciesService from '@/services/vacancies.service';

const vacancy = ref({});
const loading = ref(true);

const route = useRoute();
const router = useRouter();
const vacancyId = route.params.id;

const userStore = useUserStore();
const user = computed(() => userStore.user);

const formattedSchedules = computed(() => {
const list = vacancy.value.vacancy_schedules

if (!list || list.length === 0) return 'не указано'
  const names = list.map(item => item.name.toLowerCase())

  if (names.length === 1) return names[0]
  if (names.length === 2) return `${names[0]} или ${names[1]}`

  const allButLast = names.slice(0, -1).join(', ')
  const last = names[names.length - 1]

  return `${allButLast} или ${last}`
})

const formattedTypes = computed(() => {
	const list = vacancy.value.vacancy_types

	if (!list || list.length === 0) return 'не указано'
  const names = list.map(item => item.name.toLowerCase())

  if (names.length === 1) return names[0]
  if (names.length === 2) return `${names[0]} или ${names[1]}`

  const allButLast = names.slice(0, -1).join(', ')
  const last = names[names.length - 1]

  return `${allButLast} или ${last}`
})

const formattedFormats = computed(() => {
	const list = vacancy.value.vacancy_formats

	if (!list || list.length === 0) return 'не указано'
  const names = list.map(item => item.name.toLowerCase())

  if (names.length === 1) return names[0]
  if (names.length === 2) return `${names[0]} или ${names[1]}`

  const allButLast = names.slice(0, -1).join(', ')
  const last = names[names.length - 1]

  return `${allButLast} или ${last}`
})

const deleteVacancy = async() => {
	if (user.value.data.is_superuser)
		await VacanciesService.forcedDeleteVacancy(vacancyId);
	else
		await VacanciesService.deleteVacancy(vacancyId);

		router.push({ name: 'home' });
}

const editVacancy = async() => {
    router.push({ name: 'vacancy_editor', query: { id: vacancyId } });
}

const applyVacancy = async() => {
    await NegotiationsService.createNegotiation(vacancyId);
    router.go(0);
}

const deleteNegotiation = async() => {
    await NegotiationsService.deleteNegotiation(vacancy.value.negotiation?.id);
    router.go(0);
}

onMounted(async() => {
  try {
		const response = await VacanciesService.getVacancy(vacancyId);
		vacancy.value = response.data;
	} catch(err) {
		router.push({ name: "home" });
	}
});
</script>

<template>
	<TheHeader />
  <main>
		<div class="container container-pd52">
			<div class="vacancy-container">
				<div class="row">
					<div class="col-7 column">
						<div class="vacancy-info">
							<div class="vacancy-info-container">
								<h1 class="mb-4">{{ vacancy.position }}</h1>
								<p class="mb-2 salary">от {{ vacancy.salary }} ₽, до вычета налогов</p>
								<p class="mb-2">{{ vacancy.specialization }}</p>
								<p class="mb-2">Регион: {{ vacancy.location?.name || "любой" }}</p>
								<p class="mb-2">Занятость: {{ formattedTypes }}</p>
								<p class="mb-2">График: {{ formattedSchedules }}</p>
								<p class="mb-2">Рабочие часы: {{ vacancy.work_hours || "не указано" }}</p>
								<p class="mb-4">Формат работы: {{ formattedFormats }}</p>
							</div>
						</div>
					</div>
					<div class="col column">
						<div class="vacancy-company">
							<div class="vacancy-company-container">
								<router-link @click.stop target="_blank" :to="{ name: 'company_page', params: { id: vacancy.company?.id } }">
									<p class="mb-2">{{ vacancy.company?.name }}</p>
								</router-link>
							</div>
						</div>
						<div class="vacancy-buttons">
							<button v-if="user.data.is_superuser" class="btn btn-danger sys-btn-288" @click="deleteVacancy">Удалить</button>
							<button v-else-if="user.is_applicant && !vacancy.negotiation" class="btn btn-primary sys-btn-288" @click.stop="applyVacancy">Откликнуться</button>
							<button v-else-if="user.is_applicant && ['accepted', 'pending'].includes(vacancy.negotiation?.status)"class="btn btn-danger sys-btn-288" @click.stop="deleteNegotiation">Отозвать отклик</button>
							<button v-if="user.data.id === vacancy.author_id" class="btn btn-primary sys-btn-288" @click.stop="editVacancy">Редактировать</button>
							<button v-if="user.data.id === vacancy.author_id" class="btn btn-danger sys-btn-288" @click="deleteVacancy">Удалить</button>
						</div>
					</div>
				</div>
				<div class="row">
					<div class="col-7 column">
						<div class="vacancy-description">
							<h1 class="mb-4">Описание</h1>
							<p>
								{{ vacancy.description }}
							</p>
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
	font-family: "Montserrat";
}

.vacancy-container .column {
	margin-bottom: 24px;
}

.vacancy-info {
	display: flex;
	border-color: #DBE0E5;
  border-width: 1px;
  border-style: solid;
  border-radius: 10px;
  background-color: #FFFFFF;
	width: 100%;
	min-width: 288px;
	padding: 48px;
}

.vacancy-company {
	display: flex;
	border-color: #DBE0E5;
  border-width: 1px;
  border-style: solid;
  border-radius: 10px;
  background-color: #FFFFFF;
	width: 100%;
	min-width: 288px;
	max-height: 75px;
	padding: 24px;
}

.vacancy-company-container p {
	color: #343434;
  font-size: 20px;
  font-weight: 700;
}

.vacancy-company-container a {
    color: #343434;
    text-decoration: none;
}

.vacancy-company-container a:hover {
  color: #B0B3B8;
}

.vacancy-info-container h1 {
	font-size: 32px;
	font-weight: 700;
	color: #343434;
}

.vacancy-info-container p {
	color: #343434;
  font-size: 20px;
  font-weight: 400;
}

.vacancy-info-container .salary {
  font-size: 24px !important;
}

.vacancy-buttons {
	display: grid;
	margin-top: 24px;
}

.vacancy-description h1 {
	font-size: 32px;
	font-weight: 700;
	color: #343434;
}

.vacancy-description p {
	text-align: justify;
	color: #343434;
  font-size: 20px;
  font-weight: 400;
}

</style>
