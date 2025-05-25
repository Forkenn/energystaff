import { useAttrs } from 'vue'
import getInstance from './apiInstance.js'

const instance = getInstance(true)
class AuthService {
    async login(user) {
      await instance
        .post(
          'login',
          { username: user.email, password: user.password },
          {
            crossOrigin: true,
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
          }
        )
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
  
    async logout() {
      return await instance
        .post('logout', {})
        .then((response) => {
          return response
        })
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

    async changeEmail(data) {
      return await instance
        .post('/auth/change-email', {
          password: data.password,
          new_email: data.newEmail
        })
        .then((response) => {
          return response
        })
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

    async changePassword(data) {
      return await instance
        .post('/auth/change-password', {
          old_password: data.oldPassword,
          new_password: data.newPassword
        })
        .then((response) => {
          return response
        })
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
  
    async registerApplicant(user) {
      return await instance
        .post('auth/applicant/register', {
          surname: user.surname,
          name: user.name,
          email: user.email,
          password: user.password
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
    async registerEmployer(user) {
      return await instance
        .post('auth/employer/register', {
          surname: user.surname,
          name: user.name,
          email: user.email,
          password: user.password,
          company_id: user.company_id,
          company_name: user.company_name
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
    async registerEDU(user) {
      return await instance
        .post('auth/edu/register', {
          surname: user.surname,
          name: user.name,
          email: user.email,
          password: user.password,
          edu_institution_id: user.edu_institution_id
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
  
  export default new AuthService()