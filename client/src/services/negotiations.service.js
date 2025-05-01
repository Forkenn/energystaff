import getInstance from './apiInstance.js'

const instance = getInstance(true)
class NegotiationsService {
  async getAppNegotiations(data) {
    return await instance
      .get('/negotiations/applicant', {
        params: {
          status: data.status,
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
  async countAppNegotiations(data) {
    return await instance
      .get('/negotiations/applicant/count', {
        params: {
          status: data.status,
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
  async getEmplNegotiations(data) {
    return await instance
      .get('/negotiations/employer', {
        params: {
          status: data.status,
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
  async countEmplNegotiations(data) {
    return await instance
      .get('/negotiations/employer/count', {
        params: {
          status: data.status,
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
  async regectNegotiation(data) {
    return await instance
      .post('/negotiations/employer/reject', {
        negotiation_id: data.negotiation_id,
        desctiption: data.desctiption
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
  async acceptNegotiation(data) {
    return await instance
    .post('/negotiations/employer/accept', {
        negotiation_id: data.negotiation_id,
        desctiption: data.desctiption
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
  async resetNegotiation(data) {
    return await instance
      .post('/negotiations/employer/reset', {
        negotiation_id: data.negotiation_id
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
  async createNegotiation(vacancy_id) {
    return await instance
      .post('/negotiations/applicant', {},
        {
          params: {
            vacancy_id: vacancy_id
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
  async deleteNegotiation(id) {
    return await instance
      .delete(`/negotiations/${id}`)
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
  
  export default new NegotiationsService()