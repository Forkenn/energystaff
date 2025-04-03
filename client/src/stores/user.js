import { ref } from 'vue';
import { defineStore, acceptHMRUpdate } from 'pinia'
import UserService from '@/services/user.service';

export const useUserStore = defineStore('user', () => {
    const user = ref({ status: {loggedIn: false}, data: null });
    const getUser = async() => {
        const response = await UserService.getCurrent()
        if (response.data) {
            user.value = {
                status: {loggedIn: true},
                data: response.data
            }
        }
    };

    return { user, getUser };
})

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useUserStore, import.meta.hot))
}
  