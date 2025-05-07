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
  async getCompanyByInn(inn) {
    return await instance
      .get(`/companies/by-inn/${inn}`)
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
      .get(`/companies`, {
        params: {
          q: data.q,
          start: data.start,
          end: data.end,
          registration_date: data.registration_date,
          location_id: data.location_id,
          only_verified: data.only_verified,
          desc: data.desc
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
  async getCompaniesCount(data) {
    return await instance
      .get(`/companies/count`, {
        params: {
          q: data.q,
          registration_date: data.registration_date,
          location_id: data.location_id,
          only_verified: data.only_verified
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
  async verifyCompany(id) {
    return await instance
      .post(`/companies/${id}/verify`)
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
  async unverifyCompany(id) {
    return await instance
      .post(`/companies/${id}/unverify`)
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