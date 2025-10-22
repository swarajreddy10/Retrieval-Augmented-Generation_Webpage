export interface Message {
  id: string
  text: string
  isUser: boolean
  timestamp: Date
}

export interface QueryResponse {
  answer: string
  sources: string[]
}