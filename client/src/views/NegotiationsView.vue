<script setup>
import { onMounted, ref, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import TheHeader from '@/components/global/TheHeader.vue'
import TheFooter from '@/components/global/TheFooter.vue'
import TheNegotiationCard from '@/components/negotiations/TheNegotiationCard.vue';
import ThePaginator from '@/components/global/ThePaginator.vue';
import TheNotFoundSign from '@/components/global/TheNotFoundSign.vue';
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

const totalNegotiationsCount = ref(0)
const perPage = 6

// Pagination
const currentPage = computed(() => {
  const page = parseInt(route.query.page) || 1
  return page > 0 ? page : 1
});

const onPageChange = (newPage) => {
  router.push({ query: { ...route.query, page: newPage } })
}

const getNegotiationsCount = async() => {
  const filters = {status: filterBy.value};
  try {
      let response;
      if(userData.value.is_applicant) {
        response = await NegotiationsService.countAppNegotiations(filters);
      } else {
        response = await NegotiationsService.countEmplNegotiations(filters);
      }
      totalNegotiationsCount.value = response.data.count;
    } catch(err) {
      alert('Ошибка загрузки данных с сервера!');
  }
}

const getNegotiations = async() => {
  pagination.value.start = (currentPage.value - 1) * perPage;
  pagination.value.end = pagination.value.start + perPage
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
      alert('Ошибка загрузки данных с сервера!');
  }
}

watch(
  () => filterBy.value,
  () => {
    getNegotiationsCount();
    getNegotiations();
  }
)
watch(() => route.query.page, getNegotiations)

onMounted(async () => {
  getNegotiationsCount();
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
        <TheNotFoundSign v-else />
        <ThePaginator :total="totalNegotiationsCount" :per-page="perPage" :page="currentPage" @update:page="onPageChange" />
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