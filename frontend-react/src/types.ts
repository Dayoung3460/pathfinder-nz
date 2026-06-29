export type Role = 'employer' | 'applicant'

export interface Source {
  url: string
  title: string
}

export interface Message {
  role: 'user' | 'assistant'
  content: string
  sources?: Source[]
}

export interface ChatResponse {
  answer: string
  sources: Source[]
}
