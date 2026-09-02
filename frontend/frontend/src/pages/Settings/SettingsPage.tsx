import { useState } from 'react';
import { PageHeader } from '@/layouts/AppLayout';
import { Card, CardHeader, CardBody } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { SelectInput, TextInput } from '@/components/ui/FormField';

export function SettingsPage() {
  const [currency, setCurrency] = useState('INR');
  const [dateFormat, setDateFormat] = useState('dd-mmm-yyyy');
  const [name, setName] = useState('');
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    // No backend for settings yet — this simply confirms the form works.
    // Wire this to a real endpoint once one exists.
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="max-w-2xl">
      <PageHeader title="Settings" description="Preferences for how your data is displayed" />

      <Card className="mb-4">
        <CardHeader>
          <h2 className="text-base font-semibold">Profile</h2>
        </CardHeader>
        <CardBody className="flex flex-col gap-4">
          <TextInput id="settings-name" label="Display name" placeholder="Your name" value={name} onChange={(e) => setName(e.target.value)} />
        </CardBody>
      </Card>

      <Card className="mb-4">
        <CardHeader>
          <h2 className="text-base font-semibold">Display Preferences</h2>
        </CardHeader>
        <CardBody className="flex flex-col gap-4">
          <SelectInput
            id="settings-currency"
            label="Currency"
            value={currency}
            onChange={(e) => setCurrency(e.target.value)}
            options={[
              { label: 'Indian Rupee (₹)', value: 'INR' },
              { label: 'US Dollar ($)', value: 'USD' },
              { label: 'Euro (€)', value: 'EUR' },
            ]}
          />
          <SelectInput
            id="settings-date-format"
            label="Date format"
            value={dateFormat}
            onChange={(e) => setDateFormat(e.target.value)}
            options={[
              { label: '31-Dec-2026', value: 'dd-mmm-yyyy' },
              { label: '12/31/2026', value: 'mm/dd/yyyy' },
              { label: '2026-12-31', value: 'yyyy-mm-dd' },
            ]}
          />
        </CardBody>
      </Card>

      <div className="flex items-center gap-3">
        <Button onClick={handleSave}>Save Preferences</Button>
        {saved && <span className="text-sm font-medium text-emerald-600">Saved ✓</span>}
      </div>

      <p className="mt-6 text-xs text-ink-faint">
        Settings currently save only in local component state — there's no backend for user preferences yet. This page is
        wired up and ready to connect once one exists.
      </p>
    </div>
  );
}
