import axios from 'axios'
import { QueryResponse } from '../types'

const api = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}/api`
})

export const uploadFiles = async (files: FileList) => {
  const formData = new FormData()
  Array.from(files).forEach(file => {
    formData.append('files', file)
  })
  
  return api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export const queryDocuments = async (question: string, stream: boolean = false): Promise<QueryResponse> => {
  const response = await api.post('/query', { question, top_k: 3, stream })
  return response.data
}

export const getConversationHistory = async () => {
  const response = await api.get('/conversation')
  return response.data
}

export const clearConversationHistory = async () => {
  const response = await api.delete('/conversation')
  return response.data
}