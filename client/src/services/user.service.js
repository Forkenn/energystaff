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
          birthdate: data.birthdate
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
        })
    }
    async getUsers() {
      return await instance
        .get('/users', {
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
        })
    }
  }

  export default new UserService()