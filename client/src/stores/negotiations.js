import { ref } from 'vue';
import { defineStore, acceptHMRUpdate } from 'pinia'

export const useNegotiationsStore = defineStore('negotiations', () => {
    const negotiations = ref({count: 0, items: [] });
    const getNegotiations = async() => {
        negotiations.value = {
            count: 3,
            items: [
                {
                    id: 1,
                    name: "Вакансия 1",
                    salary: 15000,
                    city: "Смоленск",
                    company: "X5-Group",
                    negotiations: {
                        id: 1,
                        name: "В ожидании"
                    }
                },
                {
                    id: 2,
                    name: "Вакансия 2",
                    salary: 15000,
                    city: "Смоленск",
                    company: "X5-Group",
                    negotiations: {
                        id: 2,
                        name: "Приглашение"
                    }
                },
                {
                    id: 3,
                    name: "Вакансия 3",
                    salary: 15000,
                    city: "Смоленск",
                    company: "X5-Group",
                    negotiations: {
                        id: 3,
                        name: "Отказ"
                    }
                },
            ]
        }
    };

    return { negotiations, getNegotiations };
})

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useNegotiationsStore, import.meta.hot))
}