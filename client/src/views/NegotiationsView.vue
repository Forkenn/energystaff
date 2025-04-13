<script setup>
import { onMounted, ref, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import TheHeader from '@/components/global/TheHeader.vue'
import TheFooter from '@/components/global/TheFooter.vue'
import TheNegotiationCard from '@/components/negotiations/TheNegotiationCard.vue';
import NegotiationsService from '@/services/negotiations.service';

import { useUserStore } from '@/stores/user';

const userStore = useUserStore();
const userData = computed(() => userStore.user.data);

const route = useRoute();
const router = useRouter();

const filterBy = computed(() => route.query.filterBy);

const pagination = ref({
  "start": 0,
  "end": 50
});

const negotiations = ref({ "count": 0, "items": [] });

const getNegotiations = async() => {
  const filters = {...{status: filterBy.value}, ...pagination.value};
  try {
      let response;
      if(userData.value.is_applicant) {
        response = await NegotiationsService.getAppNegotiations(filters);
      } else {
        response = await NegotiationsService.getEmplNegotiations(filters);
      }
      negotiations.value = response.data;
    } catch(err) {
      alert('Нет инфы от сервера!');
  }
}

watch(
  () => filterBy.value,
  () => {
    getNegotiations();
  }
)

onMounted(async () => {
  getNegotiations();
});

</script>

<template>
  <TheHeader />
  <main>
    <div class="container container-pd52">
      <div class="negotiations-container">
        <div class="tabs-wrapper">
          <ul class="nav nav-pills">
            <li class="nav-item">
              <router-link
                class="nav-link"
                :to="{ name: 'negotiations_page' }"
                :class="{ active: !filterBy }"
              >
                Все
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                class="nav-link"
                :to="{ name: 'negotiations_page', query: {filterBy: 'pending'} }"
                :class="{ active: filterBy === 'pending' }"
              >
                В ожидании
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                class="nav-link"
                :to="{ name: 'negotiations_page', query: {filterBy: 'accepted'} }"
                :class="{ active: filterBy === 'accepted' }"
              >
                Приглашения
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                class="nav-link"
                :to="{ name: 'negotiations_page', query: {filterBy: 'rejected'} }"
                :class="{ active: filterBy === 'rejected' }"
              >
                Отказы
              </router-link>
            </li>
          </ul>
        </div>
        <div v-if="negotiations.count" class="negotiations-wrapper">
          <TheNegotiationCard v-for="negotiation in negotiations.items" :key="negotiation.id" :negotiation="negotiation"/>
        </div>
        <nav aria-label="Навигация" style="margin: 0 auto;">
          <ul class="pagination">
            <li class="page-item"><a class="page-link" href="#">1</a></li>
            <li class="page-item"><a class="page-link" href="#">2</a></li>
            <li class="page-item"><a class="page-link" href="#">3</a></li>
          </ul>
        </nav>
      </div>
    </div>
  </main>
  <TheFooter />
</template>

<style scoped>

.negotiations-container {
  margin-top: 55px;
  margin-bottom: 55px;
}

.tabs-wrapper {
  margin-bottom: 30px;
}

.negotiations-wrapper {
  display: flex;
  flex-direction: column;
}

</style>