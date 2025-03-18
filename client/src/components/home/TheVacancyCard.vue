<script setup>
defineProps({
    vacancy: Object,
})
</script>

<template>
  <div class="vacancy-card">
    <div class="card-wrapper">
        <h1>
            {{ vacancy.name }}
        </h1>
        <div class="salary">
            от {{ vacancy.salary }} ₽, до вычета налогов
        </div>
        <div class="company">
            {{ vacancy.company }}
        </div>
        <div class="city">
            {{ vacancy.city }}
        </div>
        <button type="button" class="btn btn-primary sys-btn-288">Откликнуться</button>
    </div>
  </div>
</template>

<style scoped>

.vacancy-card {
  width: 100%;
  height: 344px;
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

.card-wrapper .salary {
    color: #343434;
    font-size: 24px;
    font-weight: 400;
    margin-bottom: 34px;
}

.card-wrapper .company {
    color: #343434;
    font-size: 20px;
    font-weight: 700;
}

.card-wrapper .city {
    color: #343434;
    font-size: 20px;
    font-weight: 400;
    margin-bottom: 34px;
}

</style>