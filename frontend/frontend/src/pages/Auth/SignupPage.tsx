import { FormEvent, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { supabase } from '../../lib/supabase';

export function SignupPage() {
  const navigate = useNavigate();

  const [fullName, setFullName] = useState('');
  const [age, setAge] = useState('');
  const [profession, setProfession] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const handleSignup = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    setError('');
    setMessage('');

    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    const numericAge = Number(age);

    if (!Number.isInteger(numericAge) || numericAge < 13 || numericAge > 120) {
      setError('Please enter a valid age between 13 and 120.');
      return;
    }

    setLoading(true);

    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          full_name: fullName,
          age: numericAge,
          profession,
        },
      },
    });

    if (error) {
      setError(error.message);
      setLoading(false);
      return;
    }

    setLoading(false);

    if (!data.session) {
      setMessage(
        'Account created successfully. Please check your email to verify your account before logging in.'
      );
      return;
    }

    navigate('/');
  };

  return (
    <div className="auth-page">
      <div className="auth-card auth-card-large">
        <div className="auth-logo">
           <img
            src="/smart-expense-manager-logo.png"
            alt="Smart Expense Manager"
            className="auth-logo-image"
          />
        </div>

        <h2>Create Account</h2>
        <p className="auth-subtitle">
          Create your personal expense management account.
        </p>

        {error && (
          <div className="auth-error">
            {error}
          </div>
        )}

        {message && (
          <div className="auth-message">
            {message}
          </div>
        )}

        <form onSubmit={handleSignup}>
          <div className="auth-field">
            <label htmlFor="fullName">Full Name</label>
            <input
              id="fullName"
              type="text"
              value={fullName}
              onChange={(event) => setFullName(event.target.value)}
              placeholder="Enter your full name"
              required
              autoComplete="name"
            />
          </div>

          <div className="auth-field">
            <label htmlFor="age">Age</label>
            <input
              id="age"
              type="number"
              value={age}
              onChange={(event) => setAge(event.target.value)}
              placeholder="Enter your age"
              min="13"
              max="120"
              required
            />
          </div>

          <div className="auth-field">
            <label htmlFor="profession">Profession</label>
            <input
              id="profession"
              type="text"
              value={profession}
              onChange={(event) => setProfession(event.target.value)}
              placeholder="e.g. Software Engineer"
              required
            />
          </div>

          <div className="auth-field">
            <label htmlFor="signup-email">Email</label>
            <input
              id="signup-email"
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="Enter your email"
              required
              autoComplete="email"
            />
          </div>

          <div className="auth-field">
            <label htmlFor="signup-password">Password</label>
            <input
              id="signup-password"
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Create a password"
              minLength={6}
              required
              autoComplete="new-password"
            />
          </div>

          <div className="auth-field">
            <label htmlFor="confirm-password">Confirm Password</label>
            <input
              id="confirm-password"
              type="password"
              value={confirmPassword}
              onChange={(event) =>
                setConfirmPassword(event.target.value)
              }
              placeholder="Confirm your password"
              minLength={6}
              required
              autoComplete="new-password"
            />
          </div>

          <button
            type="submit"
            className="auth-button"
            disabled={loading}
          >
            {loading ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>

        <p className="auth-footer">
          Already have an account?{' '}
          <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
}