import type { Role } from '../types'
import { ROLES, DISCLAIMER_TEXT } from '../constants'

interface Props {
  onSelectRole: (role: Role) => void
}

const ROLE_KEYS: Role[] = ['employer', 'applicant']

export default function RoleSelection({ onSelectRole }: Props) {
  return (
    <div className="flex-1 flex flex-col items-center justify-center px-8 py-16">
      <div className="w-full max-w-lg text-center">
        <h2 className="font-bold text-notion-text tracking-heading-xl leading-none mb-4 text-5xl">
          Your guide to<br />New Zealand visas
        </h2>

        <p className="font-semibold text-notion-gray-500 tracking-body-lg leading-snug mb-10 text-xl">
          Powered by official Immigration New Zealand documents.
        </p>

        <p className="text-[15px] font-semibold text-notion-text mb-5">
          Select your role to get started:
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {ROLE_KEYS.map(key => {
            const { emoji, label, description } = ROLES[key]
            return (
              <button
                key={key}
                onClick={() => onSelectRole(key)}
                className="bg-white rounded-xl p-6 text-left border border-notion transition-shadow hover:shadow-card focus:outline-none focus:ring-2 focus:ring-notion-blue-focus"
              >
                <div className="text-3xl mb-3">{emoji}</div>
                <div className="text-base font-bold text-notion-text mb-1">{label}</div>
                <div className="text-sm text-notion-gray-500">{description}</div>
              </button>
            )
          })}
        </div>

        <p className="mt-10 text-[13px] leading-relaxed text-notion-gray-300">
          {DISCLAIMER_TEXT}
        </p>
      </div>
    </div>
  )
}
