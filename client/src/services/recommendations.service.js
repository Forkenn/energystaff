import getInstance from './apiInstance.js'

const instance = getInstance(true)
class RecommendationsService {
  async getApplicantRec(applicant_id) {
    return await instance
      .get('/recommendations', {
				params: {
					applicant_id: applicant_id
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
	async addRecommendation(applicant_id, data) {
		const formData = new FormData()
		formData.append('data', JSON.stringify({
			description: data.description
		}));
		if (Array.isArray(data.documents)) {
			Array.from(data.documents).forEach(file => {
				formData.append('documents', file);
			});
		}

    return await instance
      .post(`/recommendations`, formData, {
				params: {
					applicant_id: applicant_id
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
		const formData = new FormData()
		formData.append('data', JSON.stringify({
			description: data.description,
			deleted_documents: data.deleted_documents
		}));
		if (Array.isArray(data.documents)) {
			Array.from(data.documents).forEach(file => {
				formData.append('documents', file);
			});
		}

    return await instance
      .patch(`/recommendations/${id}`, formData)
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
      .delete(`/recommendations/${id}`)
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