<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import UserService from '@/services/user.service';

const props = defineProps({
    user: {
        type: Object,
        default: () => null,
    }
})

const router = useRouter()

const userRole = computed(() => {
    if(props.user.is_superuser)
        return 'Администратор'
    if(props.user.is_applicant)
        return 'Соискатель'
    if(props.user.is_employer)
        return 'Работодатель'
    if(props.user.is_edu)
        return 'Работник ОУ'
})

const userGender = computed(() => {
    if(props.user.sex == null)
        return 'пол не указан'

    if(props.user.sex)
        return 'Женский'

    return 'Мужской'
})

const verifyUser = async() => {
    try {
        if(props.user.is_applicant)
            await UserService.verifyApplicant(props.user.id)
        else if(props.user.is_employer)
            await UserService.verifyEmployer(props.user.id)
        else if(props.user.is_edu)
            await UserService.verifyEduWorker(props.user.id)
        props.user.is_verified = true;
    } catch(err) {}
}

const resetUser = async() => {
    try {
        if(props.user.is_applicant)
            await UserService.unverifyApplicant(props.user.id);
        else if(props.user.is_employer)
            await UserService.unverifyEmployer(props.user.id);
        else if(props.user.is_edu)
            await UserService.unverifyEduWorker(props.user.id);
        props.user.is_verified = false;
    } catch(err) {}
}

const activateUser = async() => {
    try {
        await UserService.activateUser(props.user.id);
        props.user.is_active = true;
    } catch(err) {}
}

const deactivateUser = async() => {
    try {
        await UserService.deactivateUser(props.user.id);
        props.user.is_active = false;
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
            {{ "ID: " + user.id + " | " + (user.location?.name || 'без города') + " | " + (user.birthdate || 'без д.р.') + " | " + userGender }}
        </div>
        <div class="user-info">
            {{ userRole }}
        </div>

        <button v-if="user.is_verified" type="button" class="btn btn-danger sys-btn-288" @click="resetUser">Сбросить</button>
        <button v-else type="button" class="btn btn-success sys-btn-288" @click="verifyUser">Подтвердить</button>
        <button v-if="user.is_active" type="button" class="btn btn-danger sys-btn-288" @click="deactivateUser">Деактивировать</button>
        <button v-else type="button" class="btn btn-success sys-btn-288" @click="activateUser">Активировать</button>
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