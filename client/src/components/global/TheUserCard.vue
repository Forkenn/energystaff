<script setup>
defineProps({
    user: Object,
})
</script>

<template>
  <div class="user-card">
    <div class="card-wrapper" style="align-items: center;">
        <h1>
            {{ user.secondname }} {{ user.name }} {{ user.surname }}
            <img v-if="user.is_verified" src="../../assets/icons/users/User_verified.svg">
            <img v-else src="../../assets/icons/users/User_unverified.svg">
        </h1>
        <div class="city">
            {{ user.city }}
        </div>
        <button v-if="user.is_verified" type="button" class="btn btn-primary sys-btn-288">Сбросить</button>
        <button v-else type="button" class="btn btn-primary sys-btn-288">Подтвердить</button>
        <button type="button" class="btn btn-primary sys-btn-288">Дополнить</button>
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