import { ref } from 'vue';
import { defineStore, acceptHMRUpdate } from 'pinia'

export const useUsersStore = defineStore('users', () => {
    const users = ref({count: 0, items: [] });
    const getUsers = async() => {
        users.value = {
            count: 6,
            items: [
                {
                    id: 1,
                    name: "Иван",
                    secondname: "Иванов",
                    surname: "Иванович",
                    city: "Смоленск",
                    is_verified: true,
                },
                {
                    id: 2,
                    name: "Иван",
                    secondname: "Иванов",
                    surname: "Иванович",
                    city: "Смоленск",
                    is_verified: true,
                },
                {
                    id: 3,
                    name: "Иван",
                    secondname: "Иванов",
                    surname: "Иванович",
                    city: "Смоленск",
                    is_verified: false,
                },
                {
                    id: 4,
                    name: "Иван",
                    secondname: "Иванов",
                    surname: "Иванович",
                    city: "Смоленск",
                    is_verified: false,
                },
                {
                    id: 5,
                    name: "Иван",
                    secondname: "Иванов",
                    surname: "Иванович",
                    city: "Смоленск",
                    is_verified: true,
                },
                {
                    id: 6,
                    name: "Иван",
                    secondname: "Иванов",
                    surname: "Иванович",
                    city: "Смоленск",
                    is_verified: true,
                },
            ]
        }
    };

    return { users, getUsers };
})

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useUsersStore, import.meta.hot))
}