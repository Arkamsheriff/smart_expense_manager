import { InputHTMLAttributes, LabelHTMLAttributes, ReactNode, SelectHTMLAttributes } from 'react';

interface FieldWrapperProps {
  label: string;
  htmlFor: string;
  error?: string;
  children: ReactNode;
  labelProps?: LabelHTMLAttributes<HTMLLabelElement>;
}

function FieldWrapper({ label, htmlFor, error, children, labelProps }: FieldWrapperProps) {
  return (
    <div className="flex flex-col gap-1.5">
      <label htmlFor={htmlFor} className="text-sm font-medium text-ink" {...labelProps}>
        {label}
      </label>
      {children}
      {error && <span className="text-xs text-rose-500">{error}</span>}
    </div>
  );
}

const inputBase =
  'focus-ring w-full rounded-md border border-line bg-white px-3 py-2 text-sm text-ink placeholder:text-ink-faint disabled:bg-paper disabled:text-ink-faint';

interface TextInputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
}

export function TextInput({ label, error, id, className = '', ...props }: TextInputProps) {
  return (
    <FieldWrapper label={label} htmlFor={id!} error={error}>
      <input id={id} className={`${inputBase} ${className}`} {...props} />
    </FieldWrapper>
  );
}

export function NumberInput({ label, error, id, className = '', ...props }: TextInputProps) {
  return (
    <FieldWrapper label={label} htmlFor={id!} error={error}>
      <input id={id} type="number" inputMode="decimal" className={`${inputBase} font-mono ${className}`} {...props} />
    </FieldWrapper>
  );
}

interface SelectInputProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label: string;
  error?: string;
  options: { label: string; value: string }[];
}

export function SelectInput({ label, error, id, options, className = '', ...props }: SelectInputProps) {
  return (
    <FieldWrapper label={label} htmlFor={id!} error={error}>
      <select id={id} className={`${inputBase} ${className}`} {...props}>
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </FieldWrapper>
  );
}
