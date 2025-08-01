import getInstance from './apiInstance.js'

const instance = getInstance(true)
class UserService {
    async getCurrent() {
      return await instance
        .get('/users/me')
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
        })
    }
    async editCurrent(data) {
      return await instance
        .post(`/users/me`, {
          name: data.name,
          surname: data.surname,
          last_name: data.last_name,
          birthdate: data.birthdate,
          sex: data.sex,
          location_id: data.location_id,
          applicant: data.applicant
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
    async getApplicants(data) {
      return await instance
        .get('/users/applicants', {
          params: {
            q: data.q,
            start: data.start,
            end: data.end,
            birthdate: data.birthdate,
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
        })
    }
    async countApplicants(data) {
      return await instance
        .get('/users/applicants/count', {
          params: {
            q: data.q,
            birthdate: data.birthdate,
            location_id: data.location_id,
            only_verified: data.only_verified,
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
        })
    }
    async getApplicantById(id) {
      return await instance
        .get(`/users/applicants/${id}`)
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
        })
    }
    async getApplicantByEdu(edu_num) {
      return await instance
        .get(`/users/applicants/by-edu-id/${edu_num}`)
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
        })
    }
    async getUsers(data) {
      return await instance
        .get('/users', {
          params: {
            q: data.q,
            start: data.start,
            end: data.end,
            birthdate: data.birthdate,
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
        })
    }
    async getUsersCount(data) {
      return await instance
        .get('/users/count', {
          params: {
            q: data.q,
            birthdate: data.birthdate,
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
        })
    }
    async getUserById(id) {
      return await instance
        .get(`/users/${id}`)
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
        })
    }
    async activateUser(id) {
      return await instance
        .post(`/users/${id}/activate`)
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
    async deactivateUser(id) {
      return await instance
        .post(`/users/${id}/deactivate`)
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
    async verifyApplicant(id) {
      return await instance
        .post(`/users/applicants/${id}/verify`)
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
    async unverifyApplicant(id) {
      return await instance
        .post(`/users/applicants/${id}/unverify`)
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
    async verifyEmployer(id) {
      return await instance
        .post(`/users/employers/${id}/verify`)
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
    async unverifyEmployer(id) {
      return await instance
        .post(`/users/employers/${id}/unverify`)
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
    async verifyEduWorker(id) {
      return await instance
        .post(`/users/edu-workers/${id}/verify`)
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
    async unverifyEduWorker(id) {
      return await instance
        .post(`/users/edu-workers/${id}/unverify`)
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

  export default new UserService()