import getInstance from './apiInstance.js'

const instance = getInstance(true)
class ToolsService {
  async getEduInstitutions(data) {
    return await instance
      .get('/tools/edu-institutions', {
          params: {
              q: data.q,
              start: data.start,
              end: data.end 
          },
        }
      )
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
  
export default new ToolsService()