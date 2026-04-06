import type { Role } from '../types'
import { ROLES, DISCLAIMER_TEXT } from '../constants'

interface Props {
  onSelectRole: (role: Role) => void
}

const ROLE_KEYS: Role[] = ['employer', 'applicant']

export default function RoleSelection({ onSelectRole }: Props) {
  return (
    <div className="role-selection">
      <div className="role-selection-inner">
        <h2 className="role-selection-heading">
          Your guide to<br />New Zealand visas
        </h2>

        <p className="role-selection-tagline">
          Powered by official Immigration New Zealand documents.
        </p>

        <p className="role-selection-prompt">
          Select your role to get started:
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {ROLE_KEYS.map(key => {
            const { emoji, label, description } = ROLES[key]
            return (
              <button key={key} onClick={() => onSelectRole(key)} className="role-card">
                <div className="role-card-emoji">{emoji}</div>
                <div className="role-card-label">{label}</div>
                <div className="role-card-description">{description}</div>
              </button>
            )
          })}
        </div>

        <p className="role-selection-disclaimer">{DISCLAIMER_TEXT}</p>
      </div>
    </div>
  )
}
