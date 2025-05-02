<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import TheHeader from '@/components/global/TheHeader.vue';
import TheFooter from '@/components/global/TheFooter.vue';
import CompaniesService from '@/services/companies.service';

const company = ref({});

const route = useRoute();
const router = useRouter();
const companyId = route.params.id;

const userStore = useUserStore();
const user = computed(() => userStore.user);

onMounted(async() => {
  try {
		const response = await CompaniesService.getCompany(companyId);
		company.value = response.data;
	} catch(err) {
		router.push({ name: "home" });
	}
});
</script>

<template>
	<TheHeader />
  <main>
		<div class="container container-pd52">
			<div class="company-container">
        <div class="company-wrapper">
          <h1 class="mb-4">
            {{ "Компания «" + company.name + "»" }}
            <img v-if="company.is_verified" src="../assets/icons/companies/Company_verified.svg">
            <img v-else src="../assets/icons/companies/Company_unverified.svg">
          </h1>
          <p>
            Дата регистрации: 
            <span>{{ company.registration_date }}</span>
          </p>
          <p>
            Адрес регистрации: 
            <span>{{ company.address }}</span>
          </p>
          <p>
            ИНН: 
            <span>{{ company.inn }}</span>
          </p>
          <div class="company-description">
            <h1 class="mt-5 mb-4">Описание</h1>
            <p>
              {{ company.description }}
            </p>
          </div>
          <div class="control-buttons mt-5">
            <button v-if="user.data.is_superuser && !company.is_verified" class="btn btn-primary sys-btn-288">Подтвердить</button>
            <button v-if="user.data.is_superuser && company.is_verified" class="btn btn-primary sys-btn-288">Сбросить</button>
            <button v-if="user.data.is_superuser" class="btn btn-danger sys-btn-288">Удалить</button>
					  <button v-else-if="user.data.employer?.company_id == company.id" class="btn btn-primary sys-btn-288">Редактировать</button>
          </div>
        </div>
			</div>
		</div>
	</main>
	<TheFooter />
</template>

<style scoped>

.company-container {
  margin-top: 55px;
  margin-bottom: 55px;
  width: 100%;
	font-family: "Montserrat";
  border-color: #DBE0E5;
  border-width: 1px;
  border-style: solid;
  border-radius: 10px;
}

.company-wrapper {
  margin: 48px;
}

.company-wrapper h1 {
  font-size: 32px;
	font-weight: 700;
	color: #343434;
}

.company-wrapper p {
	color: #343434;
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.company-wrapper span {
	color: #343434;
  font-size: 20px;
  font-weight: 400;
  margin-bottom: 0.5rem;
}

.company-buttons {
	display: grid;
	margin-top: 24px;
}

.company-description h1 {
	font-size: 32px;
	font-weight: 700;
	color: #343434;
}

.company-description p {
	text-align: justify;
	color: #343434;
  font-size: 20px;
  font-weight: 400;
}

.control-buttons button {
  margin-right: 24px;
}

</style>
