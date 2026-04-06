import { useState } from 'react'
import type { Role } from './types'
import { DISCLAIMER_TEXT } from './constants'
import RoleSelection from './components/RoleSelection'
import Chat from './components/Chat'

export default function App() {
  const [role, setRole] = useState<Role | null>(null)

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="sidebar-title">Pathfinder NZ</div>
          <div className="sidebar-subtitle">NZ Visa Assistant</div>
        </div>

        <div className="p-6 mt-auto">
          <div className="sidebar-disclaimer">
            <div className="sidebar-disclaimer-title">⚠️ Disclaimer</div>
            <p className="sidebar-disclaimer-text">{DISCLAIMER_TEXT}</p>
          </div>
        </div>
      </aside>

      <main className="main-content">
        {role === null ? (
          <RoleSelection onSelectRole={setRole} />
        ) : (
          <Chat
            key={role}
            role={role}
            onChangeRole={() => setRole(null)}
          />
        )}
      </main>
    </div>
  )
}
