import { NavLink } from 'react-router-dom';
import { ReactNode } from 'react';

interface NavItem {
  to: string;
  label: string;
  icon: ReactNode;
}

const icon = (d: string) => (
  <svg
    width="18"
    height="18"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="1.75"
  >
    <path d={d} strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const navItems: NavItem[] = [
  {
    to: '/',
    label: 'Dashboard',
    icon: icon('M3 13h8V3H3v10Zm0 8h8v-6H3v6Zm10 0h8V11h-8v10Zm0-18v6h8V3h-8Z'),
  },
  {
    to: '/expenses',
    label: 'Expenses',
    icon: icon('M3 10h18M7 15h4M5 5h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2Z'),
  },
  {
    to: '/income',
    label: 'Income',
    icon: icon('M12 3v18M6 8l6-5 6 5M6 16l6 5 6-5'),
  },
  {
    to: '/recurring',
    label: 'Recurring',
    icon: icon('M4 4v6h6M20 20v-6h-6M4.5 15a8 8 0 0 0 14.5 3.5M19.5 9A8 8 0 0 0 5 5.5'),
  },
  {
    to: '/budgets',
    label: 'Budgets',
    icon: icon('M3 3h18v4H3zM3 10h12v11H3zM19 10h2v11h-2z'),
  },
  {
    to: '/goals',
    label: 'Financial Goals',
    icon: icon('M12 2 2 12l10 10 10-10L12 2Zm0 5 5 5-5 5-5-5 5-5Z'),
  },
  {
    to: '/reports',
    label: 'Reports',
    icon: icon('M4 19h16M7 19V9m5 10V4m5 15v-7'),
  },
  {
    to: '/net-worth',
    label: 'Net Worth',
    icon: icon('M12 21c4.97 0 9-4.03 9-9s-4.03-9-9-9-9 4.03-9 9 4.03 9 9 9Zm0-13v8m-3-3 3 3 3-3'),
  },
  {
    to: '/settings',
    label: 'Settings',
    icon: icon('M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm7.4-3a7.4 7.4 0 0 0-.15-1.5l2.1-1.6-2-3.5-2.5 1a7.6 7.6 0 0 0-2.6-1.5L13.8 2h-4l-.45 2.9a7.6 7.6 0 0 0-2.6 1.5l-2.5-1-2 3.5 2.1 1.6A7.4 7.4 0 0 0 4.2 12c0 .5.05 1 .15 1.5l-2.1 1.6 2 3.5 2.5-1c.75.65 1.63 1.16 2.6 1.5L9.8 22h4l.45-2.9c.97-.34 1.85-.85 2.6-1.5l2.5 1 2-3.5-2.1-1.6c.1-.5.15-1 .15-1.5Z'),
  },
];

export function Sidebar({ onNavigate }: { onNavigate?: () => void }) {
  return (
    <div className="flex h-full w-64 flex-col bg-ink text-white">
      <div className="flex items-center gap-2.5 px-5 py-6">
        <div className="flex h-8 w-8 items-center justify-center rounded-md bg-emerald-500 font-display text-base font-semibold text-white">
          $
        </div>

        <div>
          <div className="font-display text-base font-semibold leading-tight">
            Smart Expense
          </div>
          <div className="text-[11px] uppercase tracking-wider text-white/50">
            Manager
          </div>
        </div>
      </div>

      <nav className="flex-1 overflow-y-auto px-3 py-2">
        <ul className="flex flex-col gap-0.5">
          {navItems.map((item) => (
            <li key={item.to}>
              <NavLink
                to={item.to}
                end={item.to === '/'}
                onClick={onNavigate}
                className={({ isActive }) =>
                  `focus-ring flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-white/10 text-white'
                      : 'text-white/60 hover:bg-white/5 hover:text-white'
                  }`
                }
              >
                {item.icon}
                {item.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      <div className="border-t border-white/10 px-5 py-4 text-xs text-white/40">
        v1.0 · connected
      </div>
    </div>
  );
}