import getInstance from './apiInstance.js'

const instance = getInstance(true)
class RecommendationsService {
  async getApplicantRec() {
    return await instance
      .get('/recommendations', {
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
  async editRecommendation(id, data) {
    return await instance
      .patchForm(`/recommendations/${id}`, {
        description: data.description,
        documents: data.documents,
				deleted_documents: data.deleted_documents
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
  async deleteRecommendation(id) {
    return await instance
      .post(`/recommendations/${id}`)
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

export default new RecommendationsService()