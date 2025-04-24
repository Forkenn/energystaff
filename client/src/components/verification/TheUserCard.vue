<script setup>
import { useRouter } from 'vue-router';

const props = defineProps({
    user: Object,
})

const router = useRouter()

const editRecommendation = () => {
    router.push({ name: "edu_recommendation_editor", query: { id: props.user.id } });
}

const verifyUser = async() => {
    router.go(0);
}

const resetUser = async() => {
    router.go(0);
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
        <div class="city">
            {{ user.location }}, {{ user.birthdate }}
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
}

.card-wrapper .city {
    color: #343434;
    font-size: 20px;
    font-weight: 400;
    margin-bottom: 34px;
}

</style>