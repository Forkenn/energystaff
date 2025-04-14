<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';

import NegotiationsService from '@/services/negotiations.service';

const props = defineProps({
    negotiation: Object,
});

const router = useRouter();

const userStore = useUserStore();
const user = computed(() => userStore.user.data);

const negotiationData = ref({
    negotiation_id: props.negotiation.id,
    desctiption: "Тестовое описание!"
})

const deleteNegotiation = async() => {
    try {
        await NegotiationsService.deleteNegotiation(props.negotiation.id);
        router.go(0);
    } catch(err) {
        alert('Ошибка удаления!');
    }
}

const showContacts = async() => {
    alert(negotiationData.value.desctiption);
}

const invite = async() => {
    try {
        await NegotiationsService.acceptNegotiation(negotiationData.value);
        router.go(0);
    } catch(err) {
        console.log(err)
        alert('Ошибка приглашения!');
    }
}

const reject = async() => {
    try {
        await NegotiationsService.regectNegotiation(negotiationData.value);
        router.go(0);
    } catch(err) {
        alert('Ошибка отказа!');
    }
}

const revokeAndInvite = async() => {
    try {
        await NegotiationsService.resetNegotiation(negotiationData.value);
        invite();
    } catch(err) {
        alert('Ошибка обработки!');
    }
}

const revokeAndReject = async() => {
    try {
        await NegotiationsService.resetNegotiation(negotiationData.value);
        reject();
    } catch(err) {
        alert('Ошибка обработки!');
    }
}

</script>

<template>
  <div class="negotiation-card">
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
        <button v-if="user.is_applicant && negotiation.status === 'accepted'" class="btn btn-primary sys-btn-288" @click="showContacts">Контакты</button>
        <button v-if="user.is_applicant && ['accepted', 'pending'].includes(negotiation.status)" class="btn btn-primary sys-btn-288" @click="deleteNegotiation">Отозвать и удалить</button>
        <button v-if="user.is_employer && negotiation.status === 'pending'" class="btn btn-primary sys-btn-288" @click="invite">Пригласить</button>
        <button v-if="user.is_employer && negotiation.status === 'pending'" class="btn btn-primary sys-btn-288" @click="reject">Отказать</button>
        <button v-if="user.is_employer && negotiation.status === 'accepted'" class="btn btn-primary sys-btn-288" @click="revokeAndReject">Отозвать и отказать</button>
        <button v-if="user.is_employer && negotiation.status === 'rejected'" class="btn btn-primary sys-btn-288" @click="revokeAndInvite">Отозвать и пригласить</button>
    </div>
  </div>
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

</style>