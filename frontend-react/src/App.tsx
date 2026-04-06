import { useState } from 'react'
import type { Role } from './types'
import { DISCLAIMER_TEXT } from './constants'
import RoleSelection from './components/RoleSelection'
import Chat from './components/Chat'

export default function App() {
  const [role, setRole] = useState<Role | null>(null)

  return (
    <div className="min-h-screen flex font-sans">
      {/* Sidebar */}
      <aside className="w-60 shrink-0 border-r border-notion bg-white flex flex-col">
        <div className="p-6 border-b border-notion">
          <div className="text-[22px] font-bold tracking-card-title text-notion-text">
            Pathfinder NZ
          </div>
          <div className="text-[13px] mt-0.5 text-notion-gray-500">
            NZ Visa Assistant
          </div>
        </div>

        <div className="p-6 mt-auto">
          <div className="rounded-xl p-4 border border-notion bg-notion-warm">
            <div className="text-[12px] font-semibold text-notion-text mb-2">
              ⚠️ Disclaimer
            </div>
            <p className="text-[12px] leading-relaxed text-notion-gray-500">
              {DISCLAIMER_TEXT}
            </p>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 flex flex-col bg-notion-warm">
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
