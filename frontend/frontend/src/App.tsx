import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AppLayout } from './layouts/AppLayout';
import { DashboardPage } from './pages/Dashboard/DashboardPage';
import { ExpensesPage } from './pages/Expenses/ExpensesPage';
import { IncomePage } from './pages/Income/IncomePage';
import { RecurringPage } from './pages/Recurring/RecurringPage';
import { BudgetsPage } from './pages/Budgets/BudgetsPage';
import { GoalsPage } from './pages/Goals/GoalsPage';
import { ReportsPage } from './pages/Reports/ReportsPage';
import { NetWorthPage } from './pages/NetWorth/NetWorthPage';
import { SettingsPage } from './pages/Settings/SettingsPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/expenses" element={<ExpensesPage />} />
          <Route path="/income" element={<IncomePage />} />
          <Route path="/recurring" element={<RecurringPage />} />
          <Route path="/budgets" element={<BudgetsPage />} />
          <Route path="/goals" element={<GoalsPage />} />
          <Route path="/reports" element={<ReportsPage />} />
          <Route path="/net-worth" element={<NetWorthPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
