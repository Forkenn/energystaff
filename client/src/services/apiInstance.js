import axios from 'axios'

const API_URL = '/api' 

export default function getInstance(withCredentials) {
  return axios.create({
    withCredentials,
    baseURL: API_URL 
  }) 
}
