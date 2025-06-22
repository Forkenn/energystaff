<script setup>
import { computed, ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'

import AuthService from '@/services/auth.service';
import { useUserStore } from '@/stores/user';

const userStore = useUserStore()
const user = computed(() => userStore.user)

const isMenuOpen = ref(false)
const router = useRouter()

const toggleMenu = () => {
  if((user.value.status.loggedIn && !isMenuOpen.value) || isMenuOpen.value)
    isMenuOpen.value = !isMenuOpen.value;
}

const logout = async() => {
  await AuthService.logout();
  isMenuOpen.value = false;
  router.push({ name: 'login_page' });
}

const handleClickOutside = (e) => {
  const dropdown = document.querySelector('.dropdown-menu-custom');
  const button = document.querySelector('.user-icon');
  if (dropdown && !dropdown.contains(e.target) && !button.contains(e.target))
    isMenuOpen.value = false;
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
  router.afterEach(() => {
    isMenuOpen.value = false;
  })
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
})

</script>

<template>
    <header class="wrapper">
        <div class="container container-pd52">
            <router-link class="logo" :to="{ name: 'home' }">
                ENERGY//STAFF
            </router-link>
            <nav class="nav-panel">
                <div v-if="!user.status.loggedIn">
                    <!--<a href="#">Соискателям</a>
                    <a href="#">Работодателям</a>-->
                </div>
                <div v-else-if="user.data.is_superuser">
                    <router-link :to="{ name: 'control_page' }">
                        Управление
                    </router-link>
                </div>
                <div v-else-if="user.data.is_edu">
                    <router-link :to="{ name: 'edu_verification' }">
                        Подтверждения
                    </router-link>
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
                    <router-link :to="{ name: 'resume_editor' }">
                        Моё резюме
                    </router-link>
                    <router-link :to="{ name: 'negotiations_page' }">
                        Отклики и приглашения
                    </router-link>
                </div>
            </nav>
            <div class="right-nav position-relative">
                <div v-if="user.status.loggedIn && user.data.location" class="location-block">
                    <img src="../../assets/icons/Location.svg" width="24" height="24">
                    <span class="location-text">{{ user.data.location.name }}</span>
                </div>
                <div class="unauth-user-icon" @click="toggleMenu">
                    <img class="user-icon" src="../../assets/icons/Account.svg" width="48" height="48" alt="Личный кабинет">
                </div>
                <transition name="fade">
                    <div v-if="isMenuOpen" class="dropdown-menu-custom">
                        <router-link class="dropdown-item" :to="{ name: 'account_page' }">
                            Личный кабинет
                        </router-link>
                        <a v-if="user.data.is_superuser" target="_blank" href="/api/docs" class="dropdown-item">API</a>
                        <a href="#" class="dropdown-item text-danger" @click.prevent="logout">Выход</a>
                    </div>
                </transition>
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
    height: 100%;
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

.dropdown-menu-custom {
  position: absolute;
  /*top: 89px;*/
  top: 100%;
  right: 0;
  background-color: #fff;
  border-radius: 8px;
  border-color: #DBE0E5;
  border-width: 1px;
  border-style: solid;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 180px;
  z-index: 1000;
  overflow: visible;
}

.dropdown-menu-custom::before {
  content: '';
  position: absolute;
  top: -9px; /* чуть выше из-за границы */
  right: 16px;
  width: 0;
  height: 0;
  border-left: 9px solid transparent;
  border-right: 9px solid transparent;
  border-bottom: 9px solid #fff;
  z-index: 1;
}

.dropdown-menu-custom::after {
  content: '';
  position: absolute;
  top: -10px;
  right: 15px;
  width: 0;
  height: 0;
  border-left: 10px solid transparent;
  border-right: 10px solid transparent;
  border-bottom: 10px solid rgba(0, 0, 0, 0.1); /* цвет тени/границы */
  z-index: 0;
}

.dropdown-item {
  padding: 12px 16px;
  height: 48px;
  display: flex;
  align-items: center;
  color: #212529;
  text-decoration: none;
  border-radius: 10px;
  font-size: 16px;
  font-family: 'Montserrat';
}

.dropdown-item:hover {
  background-color: #f8f9fa;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

</style>
