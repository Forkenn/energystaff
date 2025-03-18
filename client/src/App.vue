<script setup>
import { RouterView } from 'vue-router'
import { useUserStore } from '@/stores/user';
import { onMounted } from 'vue';

const currentUserStore = useUserStore();

onMounted(currentUserStore.getUser);
</script>

<template>
  <RouterView />
</template>
