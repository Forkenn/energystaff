import getInstance from './apiInstance.js'

const instance = getInstance(true)
class CompaniesService {
  async editCompany(id, data) {
    return await instance
      .post(`/companies/${id}`, {
        name: data.name,
        registration_date: data.registration_date,
        inn: data.inn,
        address: data.address,
        description: data.description
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
  async getCompany(id) {
    return await instance
      .get(`/companies/${id}`)
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
  async getCompanies(data) {
    return await instance
      .get(`/companies/search`, {
        params: {
          q: data.q,
          start: data.start,
          end: data.end 
        }
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
}
  
  export default new CompaniesService()