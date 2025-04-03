import { useAttrs } from 'vue'
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
                console.log(err.response.headers)
            } else if (err.request) {
                console.log(err.request)
            } else {
                console.log('Error', err.message)
            }
            })
    }
  }
  
  export default new UserService()