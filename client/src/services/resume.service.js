import getInstance from './apiInstance.js'

const instance = getInstance(true)
class ResumeService {
  async getMyResume() {
    return await instance
      .get('/resume/me')
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
  async editMyResume(data) {
    return await instance
      .patch('/resume/me', {
        position: data.position,
        specialization: data.specialization,
        salary: data.salary,
        description: data.description,
        resume_types_ids: data.resume_types_ids,
        resume_formats_ids: data.resume_formats_ids
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
  async addResume(data) {
    return await instance
      .post('/resume/me', {
        position: data.position,
        specialization: data.specialization,
        salary: data.salary,
        description: data.description,
        resume_types_ids: data.resume_types_ids,
        resume_formats_ids: data.resume_formats_ids
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
  async deleteMyResume() {
    return await instance
      .delete(`/resume/me`)
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
  async getResumeByUserId(id) {
    return await instance
      .get(`/resume`, {
				params: {
						applicant_id: id
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

export default new ResumeService()