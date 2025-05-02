<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import VacanciesService from '@/services/vacancies.service';
import NegotiationsService from '@/services/negotiations.service';

const props = defineProps({
    vacancy: Object,
});

const router = useRouter();

const userStore = useUserStore();
const user = computed(() => userStore.user);

const goToVacancy = () => {
  router.push({ name: 'vacancy_page', params: { id: props.vacancy.id } })
}

const deleteVacancy = async() => {
    await VacanciesService.deleteVacancy(props.vacancy.id);
    router.go(0);
}

const editVacancy = async() => {
    router.push({ name: 'vacancy_editor', query: { id: props.vacancy.id } });
}

const applyVacancy = async() => {
    await NegotiationsService.createNegotiation(props.vacancy.id);
    router.go(0);
}

const deleteNegotiation = async() => {
    await NegotiationsService.deleteNegotiation(props.vacancy.negotiation?.id);
    router.go(0);
}

</script>

<template>
  <div class="vacancy-card" @click="goToVacancy">
    <div class="card-wrapper" style="align-items: center;">
        <h1>
            {{ vacancy.position }}
            <img v-if="vacancy.negotiation?.status == 'pending'" src="../../assets/icons/vacancies/Negotiation_process.svg">
            <img v-if="vacancy.negotiation?.status == 'accepted'" src="../../assets/icons/vacancies/Negotiation_success.svg">
            <img v-if="vacancy.negotiation?.status == 'rejected'" src="../../assets/icons/vacancies/Negotiation_reject.svg">
        </h1>
        <div class="salary">
            от {{ vacancy.salary }} ₽, до вычета налогов
        </div>
        <router-link @click.stop target="_blank" :to="{ name: 'company_page', params: { id: props.vacancy.company_id } }">
            <div class="company">
                {{ vacancy.company_name }}
            </div>
        </router-link>
        <div class="city">
            {{ vacancy.city }}
        </div>
        <button v-if="user.data.is_superuser" class="btn btn-danger sys-btn-200" @click.stop="deleteVacancy">Удалить</button>
        <button v-else-if="user.data.is_applicant && !vacancy.negotiation" class="btn btn-primary sys-btn-200" @click.stop="applyVacancy">Откликнуться</button>
        <button v-else-if="user.data.is_applicant && ['accepted', 'pending'].includes(vacancy.negotiation.status)" class="btn btn-danger sys-btn-200" @click.stop="deleteNegotiation">Отозвать отклик</button>
        <button v-if="user.data.is_employer && vacancy.author_id == user.data.id" class="btn btn-primary sys-btn-200" @click.stop="editVacancy">Редактировать</button>
        <button v-if="user.data.is_employer && vacancy.author_id == user.data.id" class="btn btn-danger sys-btn-200" @click.stop="deleteVacancy">Удалить</button>
    </div>
  </div>
</template>

<style scoped>

.vacancy-card {
  width: 100%;
  margin-bottom: 24px;
  border-color: #DBE0E5;
  border-width: 1px;
  border-style: solid;
  border-radius: 10px;
  background-color: #FFFFFF;
  font-family: "Montserrat";
  transition: box-shadow 0.3s ease, transform 0.3s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.vacancy-card:hover {
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
  transform: translateY(-4px);
}

.card-wrapper {
    margin-top: 48px;
    margin-left: 48px;
    margin-bottom: 48px;
}

.card-wrapper h1 {
    font-size: 32px;
    font-weight: 700;
    color: #343434;
}

.card-wrapper img {
    margin-bottom: 5px;
    margin-left: 2px;
}

.card-wrapper button {
    margin-bottom: 0;
    margin-right: 24px;
}

.card-wrapper .salary {
    color: #343434;
    font-size: 24px;
    font-weight: 400;
    margin-bottom: 34px;
}

.card-wrapper .company {
    color: #343434;
    font-size: 20px;
    font-weight: 700;
}

.card-wrapper .city {
    color: #343434;
    font-size: 20px;
    font-weight: 400;
    margin-bottom: 34px;
}

.card-wrapper a {
    color: #343434;
    text-decoration: none;
}

.card-wrapper a:hover {
  color: #B0B3B8;
}

</style>