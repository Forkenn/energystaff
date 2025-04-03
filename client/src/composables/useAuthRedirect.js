import { computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';

export function useAuthRedirect(redirectRoute = { name: 'home' }) {
  const userStore = useUserStore();
  const router = useRouter();

  const user = computed(() => userStore.user);

  watch(user, (newUser) => {
    if (newUser?.status?.loggedIn) {
      router.push(redirectRoute);
    }
  }, { immediate: true });
}
