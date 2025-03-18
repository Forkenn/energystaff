import { ref } from 'vue';
import { defineStore, acceptHMRUpdate } from 'pinia'

export const useVacanciesStore = defineStore('vacancies', () => {
    const vacancies = ref({count: 0, items: [] });
    const getVacancies = async() => {
        vacancies.value = {
            count: 6,
            items: [
                {
                    id: 1,
                    name: "Вакансия 1",
                    salary: 15000,
                    city: "Смоленск",
                    company: "X5-Group"
                },
                {
                    id: 2,
                    name: "Вакансия 2",
                    salary: 15000,
                    city: "Смоленск",
                    company: "X5-Group"
                },
                {
                    id: 3,
                    name: "Вакансия 3",
                    salary: 15000,
                    city: "Смоленск",
                    company: "X5-Group"
                },
                {
                    id: 4,
                    name: "Вакансия 4",
                    salary: 15000,
                    city: "Смоленск",
                    company: "X5-Group"
                },
                {
                    id: 5,
                    name: "Вакансия 5",
                    salary: 15000,
                    city: "Смоленск",
                    company: "X5-Group"
                },
                {
                    id: 6,
                    name: "Вакансия 6",
                    salary: 15000,
                    city: "Смоленск",
                    company: "X5-Group"
                },
            ]
        }
    };

    return { vacancies, getVacancies };
})

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useVacanciesStore, import.meta.hot))
}