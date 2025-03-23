<script setup>
import { onMounted } from 'vue';
import { useUsersStore } from '@/stores/users';

import TheHeader from '@/components/global/TheHeader.vue'
import TheFooter from '@/components/global/TheFooter.vue'
import TheUserCard from '@/components/global/TheUserCard.vue';

const usersStore  = useUsersStore();
onMounted(usersStore.getUsers);

</script>

<template>
  <TheHeader />
  <main>
    <div class="container container-pd52">
      <div class="verification-wrapper">
        <div class="search-wrapper">
          <div class="row">
            <div class="col d-flex">
              <input type="text" class="form-control flex-grow-1 sys-input-1122-flex" id="InputSearch" placeholder="Фамилия, Имя, Отчество или идентификатор">
            </div>
            <div class="col-auto">
              <button type="button" class="btn btn-primary sys-btn-150">Поиск</button>
            </div>
          </div>
        </div>
        <div class="main-wrapper">
          <div class="row">
            <div class="col-auto">
              <div class="filter-wrapper">

              </div>
            </div>
            <div class="col d-flex w-100" style="flex-direction: column;">
              <div v-if="usersStore.users.count" class="vacancy-wrapper">
                <TheUserCard v-for="user in usersStore.users.items" :key="user.id" :user="user"/>
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
        </div>
      </div>
    </div>
  </main>
  <TheFooter />
</template>

<style scoped>

.search-wrapper {
  margin-top: 55px;
}

.verification-wrapper {
  margin-top: 55px;
  margin-bottom: 55px;
}

.filter-wrapper {
  width: 393px;
  height: 600px;
  border-color: #DBE0E5;
  border-width: 1px;
  border-style: solid;
  border-radius: 10px;
  background-color: #FFFFFF;
}

.vacancy-wrapper {
  min-width: 500px;
  max-width: 902px;
  min-height: 740px;
  width: 100%;
}

</style>