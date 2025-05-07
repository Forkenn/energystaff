<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';

import UserService from '@/services/user.service';

const props = defineProps({
    user: {
        type: Object,
        default: () => null,
    },
    edu_levels: {
        type: Array,
        default: () => [],
    },
})

const userEduInfo = computed(() => {
    const userEduLevel = props.edu_levels.find(
        obj => obj.id === props.user.applicant?.edu_level_id
    );

    if (props.user.applicant?.edu_status == "completed") {
        return userEduLevel.name + " (завершено)"
    }

    if (props.user.applicant?.edu_status == "progress") {
        return userEduLevel.name + " (в процессе)"
    }

    return "без образования"
})

const router = useRouter()

const editRecommendation = () => {
    router.push({ name: "edu_recommendation_editor", query: { id: props.user.id } });
}

const verifyUser = async() => {
    try {
        await UserService.verifyApplicant(props.user.id);
        props.user.is_verified = true;
    } catch(err) {}
}

const resetUser = async() => {
    try {
        await UserService.unverifyApplicant(props.user.id);
        props.user.is_verified = false;
    } catch(err) {}
}

</script>

<template>
  <div class="user-card">
    <div class="card-wrapper" style="align-items: center;">
        <h1>
            {{ user.surname }} {{ user.name }} {{ user.last_name }}
            <img v-if="user.is_verified" src="../../assets/icons/users/User_verified.svg">
            <img v-else src="../../assets/icons/users/User_unverified.svg">
        </h1>
        <div class="user-info">
            {{ "ID: " + user.id + " | " + (user.location?.name || 'без города') + " | " + (user.birthdate || 'без д.р.') + " | " + (user.sex ? "Женский" : "Мужской") }}
        </div>
        <div class="user-info">
            {{ "Зачётная книжка: " + (user.applicant?.edu_number || 'не указано') + " | " + userEduInfo }}
        </div>
        <button v-if="user.is_verified" type="button" class="btn btn-danger sys-btn-288" @click="resetUser">Сбросить</button>
        <button v-else type="button" class="btn btn-success sys-btn-288" @click="verifyUser">Подтвердить</button>
        <button type="button" class="btn btn-primary sys-btn-288" @click="editRecommendation">Рекомендация</button>
    </div>
  </div>
</template>

<style scoped>

.user-card {
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

.user-card:hover {
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
    margin-right: 24px;
    margin-top: 24px;
    margin-bottom: 0;
}

.card-wrapper .user-info {
    color: #343434;
    font-size: 20px;
    font-weight: 400;
}

</style>