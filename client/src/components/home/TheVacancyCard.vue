<script setup>
defineProps({
    vacancy: Object,
})
</script>

<template>
  <div class="vacancy-card">
    <div class="card-wrapper" style="align-items: center;">
        <h1>
            {{ vacancy.position }}
            <img v-if="vacancy.negotiations && vacancy.negotiations.id == 1" src="../../assets/icons/vacancies/Negotiation_process.svg">
            <img v-if="vacancy.negotiations && vacancy.negotiations.id == 2" src="../../assets/icons/vacancies/Negotiation_success.svg">
            <img v-if="vacancy.negotiations && vacancy.negotiations.id == 3" src="../../assets/icons/vacancies/Negotiation_reject.svg">
        </h1>
        <div class="salary">
            от {{ vacancy.salary }} ₽, до вычета налогов
        </div>
        <div class="company">
            {{ vacancy.company_name }}
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

.card-wrapper img {
    margin-bottom: 5px;
    margin-left: 2px;
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