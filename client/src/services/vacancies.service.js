import getInstance from './apiInstance.js'

const instance = getInstance(true)
class VacanciesService {
  async getVacancies(data) {
    return await instance
      .get('/vacancies', {
        params: {
          q: data.q,
          start: data.start,
          end: data.end 
        },
      })
      .then((response) => response)
      .catch((err) => {
        if (err.response) {
          console.log(err.response.data)
          console.log(err.response.status)
        } else if (err.request) {
          console.log(err.request)
        } else {
          console.log('Error', err.message)
        }
        throw err;
      })
  }
  async countVacancies(data) {
    return await instance
      .get('/vacancies/count', {
        params: {
          q: data.q
        },
      })
      .then((response) => response)
      .catch((err) => {
        if (err.response) {
          console.log(err.response.data)
          console.log(err.response.status)
        } else if (err.request) {
          console.log(err.request)
        } else {
          console.log('Error', err.message)
        }
        throw err;
      })
  }
  async editVacancy(id, data) {
    return await instance
      .post(`/vacancies/${id}`, {
        position: data.position,
        specialization: data.specialization,
        salary: data.salary,
        work_hours: data.work_hours,
        description: data.description,
        location_id: data.location_id,
        vacancy_types_ids: data.vacancy_types_ids,
        vacancy_formats_ids: data.vacancy_formats_ids,
        vacancy_schedules_ids: data.vacancy_schedules_ids
      })
      .then((response) => response)
      .catch((err) => {
        if (err.response) {
          console.log(err.response.data)
          console.log(err.response.status)
        } else if (err.request) {
          console.log(err.request)
        } else {
          console.log('Error', err.message)
        }
        throw err;
      })
  }
  async addVacancy(data) {
    return await instance
      .post('/vacancies', {
        position: data.position,
        specialization: data.specialization,
        salary: data.salary,
        description: data.description,
        vacancy_types_ids: data.vacancy_types_ids,
        vacancy_formats_ids: data.vacancy_formats_ids,
        vacancy_schedules_ids: data.vacancy_schedules_ids
      })
      .then((response) => response)
      .catch((err) => {
        if (err.response) {
          console.log(err.response.data)
          console.log(err.response.status)
        } else if (err.request) {
          console.log(err.request)
        } else {
          console.log('Error', err.message)
        }
        throw err;
      })
  }
  async deleteVacancy(id) {
    return await instance
      .delete(`/vacancies/${id}`)
      .then((response) => response)
      .catch((err) => {
        if (err.response) {
          console.log(err.response.data)
          console.log(err.response.status)
        } else if (err.request) {
          console.log(err.request)
        } else {
          console.log('Error', err.message)
        }
        throw err;
      })
  }
  async forcedDeleteVacancy(id) {
    return await instance
      .delete(`/vacancies/${id}/force`)
      .then((response) => response)
      .catch((err) => {
        if (err.response) {
          console.log(err.response.data)
          console.log(err.response.status)
        } else if (err.request) {
          console.log(err.request)
        } else {
          console.log('Error', err.message)
        }
        throw err;
      })
  }
  async getVacancy(id) {
    return await instance
      .get(`/vacancies/${id}`)
      .then((response) => response)
      .catch((err) => {
        if (err.response) {
          console.log(err.response.data)
          console.log(err.response.status)
        } else if (err.request) {
          console.log(err.request)
        } else {
          console.log('Error', err.message)
        }
        throw err;
      })
  }
  async getVacanciesSchedules() {
    return await instance
      .get('/vacancies/schedules')
      .then((response) => response)
      .catch((err) => {
        if (err.response) {
          console.log(err.response.data)
          console.log(err.response.status)
        } else if (err.request) {
          console.log(err.request)
        } else {
          console.log('Error', err.message)
        }
        throw err;
      })
  }
  async getVacanciesFormats() {
    return await instance
      .get('/vacancies/formats')
      .then((response) => response)
      .catch((err) => {
        if (err.response) {
          console.log(err.response.data)
          console.log(err.response.status)
        } else if (err.request) {
          console.log(err.request)
        } else {
          console.log('Error', err.message)
        }
        throw err;
      })
  }
  async getVacanciesTypes() {
    return await instance
      .get('/vacancies/types')
      .then((response) => response)
      .catch((err) => {
        if (err.response) {
          console.log(err.response.data)
          console.log(err.response.status)
        } else if (err.request) {
          console.log(err.request)
        } else {
          console.log('Error', err.message)
        }
        throw err;
      })
  }
}
  
  export default new VacanciesService()