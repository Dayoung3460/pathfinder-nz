import type { Role } from './types'

export const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

export const ROLES: Record<Role, { label: string; emoji: string; description: string }> = {
  employer: {
    label: 'Employer / HR Manager',
    emoji: '🏢',
    description: 'Accreditation, Job Checks, and employer obligations',
  },
  applicant: {
    label: 'Visa Applicant',
    emoji: '🧳',
    description: 'Visa types, eligibility, and application procedures',
  },
}

export const SUGGESTED_QUESTIONS: Record<Role, string[]> = {
  employer: [
    'What type of accreditation do I need to hire overseas workers?',
    'Do I need to advertise the job before applying for a Job Check?',
    'What documents do I need to include in a Job Offer?',
  ],
  applicant: [
    'What visa do I need to work as a software engineer in NZ?',
    'How do I apply for the Skilled Migrant Category resident visa?',
    'What are the requirements for a partner visa?',
  ],
}

export const DISCLAIMER_TEXT =
  'This information is based on official Immigration New Zealand documents and is ' +
  'provided for general guidance only. It is not legal advice. For decisions that may ' +
  'significantly affect your visa status, please consult a licensed immigration adviser.'
