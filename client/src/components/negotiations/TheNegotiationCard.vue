<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';

import TheModal from '../global/TheModal.vue';

import NegotiationsService from '@/services/negotiations.service';

const props = defineProps({
    negotiation: Object,
});

const router = useRouter();
let errorMsg = '';

const userStore = useUserStore();
const user = computed(() => userStore.user.data);

const showModalContacts = ref(false)
const showModalInfoSend = ref(false)

const negotiationData = ref({
    negotiation_id: props.negotiation.id,
    employer_description: ""
})

const deleteNegotiation = async() => {
    try {
        await NegotiationsService.deleteNegotiation(props.negotiation.id);
        router.go(0);
    } catch(err) {
        alert('Ошибка удаления!');
    }
}

const validateFields = () => {
    errorMsg = '';
    if(
        negotiationData.value.employer_description.length < 50 ||
        negotiationData.value.employer_description.length > 500
    )
        errorMsg += '• Недопустимое описание (допустимо от 50 до 500 символов)\n';
}

const invite = async() => {
    validateFields();
    if(errorMsg != '') {
        alert(`Ошибка переговоров:\n${errorMsg}`);
        return;
    }

    showModalInfoSend.value = false;
    try {
        await NegotiationsService.acceptNegotiation(negotiationData.value);
        router.go(0);
    } catch(err) {
        console.log(err)
        alert('Ошибка приглашения!');
    }
}

const reject = async() => {
    validateFields();
    if(errorMsg != '') {
        alert(`Ошибка переговоров:\n${errorMsg}`);
        return;
    }

    showModalInfoSend.value = false;
    try {
        await NegotiationsService.regectNegotiation(negotiationData.value);
        router.go(0);
    } catch(err) {
        alert('Ошибка отказа!');
    }
}

const revokeAndInvite = async() => {
    validateFields();
    if(errorMsg != '') {
        alert(`Ошибка переговоров:\n${errorMsg}`);
        return;
    }

    showModalInfoSend.value = false;
    try {
        await NegotiationsService.resetNegotiation(negotiationData.value);
        invite();
    } catch(err) {
        alert('Ошибка обработки');
    }
}

const revokeAndReject = async() => {
    validateFields();
    if(errorMsg != '') {
        alert(`Ошибка переговоров:\n${errorMsg}`);
        return;
    }

    showModalInfoSend.value = false;
    try {
        await NegotiationsService.resetNegotiation(negotiationData.value);
        reject();
    } catch(err) {
        alert('Ошибка обработки');
    }
}

const goToResume = () => {
  if(user.value.is_employer)
    router.push({ name: 'resume_page', query: {id: props.negotiation.applicant_id }})
  else
    router.push({ name: 'vacancy_page', params: { id: props.negotiation.vacancy_id } })
}

</script>

<template>
  <div class="negotiation-card" @click="goToResume">
    <div class="card-wrapper" style="align-items: center;">
        <h1>
            {{ negotiation.vacancy_position }}
            <img v-if="negotiation.status === 'pending'" src="../../assets/icons/vacancies/Negotiation_process.svg">
            <img v-if="negotiation.status === 'accepted'" src="../../assets/icons/vacancies/Negotiation_success.svg">
            <img v-if="negotiation.status === 'rejected'" src="../../assets/icons/vacancies/Negotiation_reject.svg">
        </h1>
        <div class="salary">
            от {{ negotiation.vacancy_salary }} ₽, до вычета налогов
        </div>
        <div v-if="user.is_applicant" class="company">
            {{ negotiation.company_name }}
        </div>
        <div v-if="user.is_employer" class="company">
            {{ negotiation.user_surname + ' ' + negotiation.user_name + ' ' + negotiation.user_last_name }}
        </div>
        <div v-if="user.is_applicant" class="city">
            {{ negotiation.vacancy_location }}
        </div>
        <div v-if="user.is_employer" class="city">
            {{ negotiation.user_location }}
        </div>
        <button v-if="user.is_applicant && ['accepted', 'rejected'].includes(negotiation.status)" class="btn btn-primary sys-btn-288" @click.stop="showModalContacts = true">Информация</button>
        <button v-if="user.is_applicant && ['accepted', 'pending'].includes(negotiation.status)" class="btn btn-danger sys-btn-288" @click="deleteNegotiation">Отозвать и удалить</button>
        <button v-if="user.is_employer && negotiation.status === 'pending'" class="btn btn-primary sys-btn-288" @click.stop="showModalInfoSend = true">Пригласить</button>
        <button v-if="user.is_employer && negotiation.status === 'pending'" class="btn btn-danger sys-btn-288" @click.stop="showModalInfoSend = true">Отказать</button>
        <button v-if="user.is_employer && negotiation.status === 'accepted'" class="btn btn-danger sys-btn-288" @click.stop="showModalInfoSend = true">Отозвать и отказать</button>
        <button v-if="user.is_employer && negotiation.status === 'rejected'" class="btn btn-primary sys-btn-288" @click.stop="showModalInfoSend = true">Отозвать и пригласить</button>
    </div>
  </div>

  <TheModal v-if="showModalContacts" @close="showModalContacts = false">
    <template #header>
      <h5 class="modal-title">Сообщение от работодателя</h5>
    </template>

    <p>{{ negotiation.employer_description }}</p>

    <template #footer>
      <button class="btn btn-secondary" @click="showModalContacts = false">Закрыть</button>
    </template>
  </TheModal>

  <TheModal v-if="showModalInfoSend" @close="showModalInfoSend = false">
    <template #header>
      <h5 class="modal-title">Сообщение для соискателя</h5>
    </template>

    <div class="negotiation-text-area">
        <label for="formControlExtended" class="form-label">Контакты, причины отказа и т.п.</label>
        <textarea class="form-control" id="formControlExtended" rows="5" v-model="negotiationData.employer_description"></textarea>
    </div>

    <template #footer>
      <button v-if="negotiation.status === 'pending'" class="btn btn-primary" @click.stop="invite">Пригласить</button>
      <button v-if="negotiation.status === 'pending'" class="btn btn-danger" @click.stop="reject">Отказать</button>
      <button v-if="negotiation.status === 'accepted'" class="btn btn-danger" @click.stop="revokeAndReject">Отозвать и отказать</button>
      <button v-if="negotiation.status === 'rejected'" class="btn btn-primary" @click.stop="revokeAndInvite">Отозвать и пригласить</button>
      <button class="btn btn-secondary" @click="showModalInfoSend = false">Закрыть</button>
    </template>
  </TheModal>
</template>

<style scoped>

.negotiation-card {
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

.negotiation-card:hover {
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

.modal-title {
  font-weight: 700 !important;
  color: #343434 !important;
}

</style>