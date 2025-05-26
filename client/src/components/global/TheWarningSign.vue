<script setup>
const props = defineProps({
  red: {
    type: Boolean,
    default: () => false
  }
})
</script>

<template>
  <div class="warning-wrapper">
    <img :class="{ red_sign: red } " src="../../assets/icons/Warning.svg" width="200" height="200">
    <div :class="{ red_text: red } ">
      Учётная запись не подтверждёна
    </div>
    <div :class="{ red_text: red } ">
      Действия в системе ограничены
    </div>
  </div>
</template>

<style scoped>

.warning-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: "Montserrat";
  font-size: 20px;
  font-weight: 800;
  color: #343434;
  top: 27%;
  position: relative;
}

.red_sign {
  filter: invert(100%) sepia(2000%) saturate(5388%) hue-rotate(5deg) brightness(60%) contrast(110%)
}

.red_text {
  color: #770202;
}

</style>