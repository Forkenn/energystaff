import { ref } from 'vue';
import { defineStore, acceptHMRUpdate } from 'pinia'

export const useUserStore = defineStore('user', () => {
    const user = ref({ status: {loggedIn: false}, data: null });
    const getUser = async() => {
        user.value = {
            status: {loggedIn: true},
            data: {is_admin: false, is_edu: false, is_employer: false} 
        }
    };

    return { user, getUser };
})

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useUserStore, import.meta.hot))
}
  