<script setup>
import { useRouter } from 'vue-router';
import CompaniesService from '@/services/companies.service';

const props = defineProps({
    company: {
        type: Object,
        default: () => null,
    }
})

const router = useRouter()

const goToCompany = () => {
    router.push({ name: 'company_page', params: { id: props.company.id } })
}

const verifyCompany = async() => {
    try {
        await CompaniesService.verifyCompany(props.company.id);
    } catch(err) {}
    router.go(0);
}

const resetCompany = async() => {
    try {
        await CompaniesService.unverifyCompany(props.company.id);
    } catch(err) {}
    router.go(0);
}

</script>

<template>
  <div class="company-card">
    <div class="card-wrapper" style="align-items: center;" @click="goToCompany">
        <h1>
            {{ company.name }}
            <img v-if="company.is_verified" src="../../assets/icons/users/User_verified.svg">
            <img v-else src="../../assets/icons/users/User_unverified.svg">
        </h1>
        <div class="company-info">
            {{ "ID: " + company.id }}
        </div>
        <div class="company-info">
            {{ "Дата регистрации: " + (company.registration_date || "не указано") }}
        </div>
        <div class="company-info">
            {{ "Адрес регистрации: " + (company.address || "не указано") }}
        </div>
        <div class="company-info">
            {{ "ИНН: " + (company.inn || "не указано") }}
        </div>

        <button v-if="company.is_verified" type="button" class="btn btn-danger sys-btn-288" @click.stop="resetCompany">Сбросить</button>
        <button v-else type="button" class="btn btn-success sys-btn-288" @click.stop="verifyCompany">Подтвердить</button>
    </div>
  </div>
</template>

<style scoped>

.company-card {
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

.company-card:hover {
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

.card-wrapper .company-info {
    color: #343434;
    font-size: 20px;
    font-weight: 400;
}

</style>