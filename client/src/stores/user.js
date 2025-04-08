import { ref, watch } from 'vue';
import { defineStore, acceptHMRUpdate } from 'pinia'
import UserService from '@/services/user.service';

export const useUserStore = defineStore('user', () => {
    const initialUser = JSON.parse(localStorage.getItem('user')) || { 
        status: { loggedIn: false }, 
        data: null 
    };

    const isLoading = ref(false);
    const user = ref(initialUser);

    watch(
        () => user.value, (newUser) => {
            localStorage.setItem('user', JSON.stringify(newUser));
        }, { deep: true }
    );

    const getUser = async() => {
        isLoading.value = true;
        const response = await UserService.getCurrent()
        if (response && response.data) {
            user.value = {
                status: {loggedIn: true},
                data: response.data
            };
            isLoading.value = false;
            return;
        }
        if (user.value.status.loggedIn) {
            user.value = { status: {loggedIn: false}, data: null };
        }
        isLoading.value = false;
    };

    return { isLoading, user, getUser };
})

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useUserStore, import.meta.hot))
}
  