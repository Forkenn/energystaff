import { computed } from 'vue'
import { useUserStore } from '@/stores/user';

export function useRoles() {
  const userStore = useUserStore()
  const roles = computed(() => ({
    is_active: userStore.user.data.is_active,
    is_applicant: userStore.user.data.is_applicant,
    is_edu: userStore.user.data.is_edu,
    is_employer: userStore.user.data.is_employer,
    is_superuser: userStore.user.data.is_superuser,
    is_verified: userStore.user.data.is_verified
  }))

  return roles
}