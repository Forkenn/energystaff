<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/stores/user';

const userStore = useUserStore()
const user = computed(() => userStore.user)
</script>

<template>
    <header class="wrapper">
        <div class="container container-pd52">
            <router-link class="logo" :to="{ name: 'home' }">
                ENERGY//STAFF
            </router-link>
            <nav class="nav-panel">
                <div v-if="!user.status.loggedIn">
                    <a href="#">Соискателям</a>
                    <a href="#">Работодателям</a>
                </div>
                <div v-else-if="user.data.is_superuser">
                    <a href="#">Управление</a>
                </div>
                <div v-else-if="user.data.is_edu">
                    <a href="#">Подтверждения</a>
                </div>
                <div v-else-if="user.data.is_employer">
                    <router-link :to="{ name: 'company_editor' }">
                        Компания
                    </router-link>
                    <router-link :to="{ name: 'vacancy_editor' }">
                        Добавить вакансию
                    </router-link>
                    <router-link :to="{ name: 'negotiations_page' }">
                        Отклики
                    </router-link>
                </div>
                <div v-else>
                    <a href="#">Моё резюме</a>
                    <router-link :to="{ name: 'negotiations_page' }">
                        Отклики и приглашения
                    </router-link>
                </div>
            </nav>
            <div class="right-nav">
                <div v-if="user.status.loggedIn" class="location-block">
                    <img src="../../assets/icons/Location.svg" width="24" height="24">
                    <span class="location-text">Местоположение</span>
                </div>
                <div class="unauth-user-icon">
                    <router-link :to="{ name: 'account_page' }">
                        <img src="../../assets/icons/Account.svg" width="48" height="48" alt="Личный кабинет">
                    </router-link>
                </div>
            </div>
        </div>
    </header>
</template>

<style scoped>

.wrapper {
    background: #27282A;
    height: 80px;
    font-size: 16px;
    font-family: 'Montserrat';
}

.container {
    display: flex;
    align-items: center;
    height: 100%;
}

.logo {
    color: #FFFFFF;
    font-weight: 600;
    text-decoration: none !important;
}

.nav-panel {
    display: flex;
    margin-left: 24px;
}

.nav-panel a {
    color: #FFFFFF;
    font-weight: 400;
    margin-right: 15px;
    text-decoration: none;
}

.nav-panel a:hover {
  color: #B0B3B8;
}

.right-nav {
    display: flex;
    margin-left: auto;
    align-items: center;
}

.location-block span {
    color: #FFFFFF;
    font-weight: 700;
    margin-right: 30px;
}

.location-block img {
    margin-right: 2px;
    margin-bottom: 5px;
}

</style>
