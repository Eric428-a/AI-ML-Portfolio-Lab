import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  ArrowRight,
  BookOpen,
  Eye,
  EyeOff,
  LockKeyhole,
  Mail,
  ShieldCheck,
} from "lucide-react";

import Button from "../components/common/Button";

export default function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");

    if (!email.trim() || !password) {
      setError("Enter your email address and password.");
      return;
    }

    setError(
      "Authentication is not implemented in this frontend yet. Configure a backend authentication endpoint before enabling sign-in.",
    );
  }

  return (
    <main className="login-page">
      <section className="login-brand-panel">
        <Link to="/" className="login-brand">
          <span className="brand-mark">
            <BookOpen size={22} />
          </span>
          <span>
            <strong>DocuMind</strong>
            <small>DOCUMENT INTELLIGENCE</small>
          </span>
        </Link>

        <div className="login-brand-content">
          <span className="eyebrow">YOUR KNOWLEDGE, CONNECTED</span>

          <h1>
            Every document.
            <br />
            One intelligent workspace.
          </h1>

          <p>
            Bring information together, ask better questions, and explore
            answers with references to your original sources.
          </p>

          <div className="login-feature-list">
            <div>
              <span><BookOpen size={17} /></span>
              <div>
                <strong>Multi-document search</strong>
                <small>Explore information across multiple files.</small>
              </div>
            </div>

            <div>
              <span><ShieldCheck size={17} /></span>
              <div>
                <strong>Source-grounded answers</strong>
                <small>Inspect citations and retrieved excerpts.</small>
              </div>
            </div>
          </div>
        </div>

        <div className="login-brand-footer">
          Intelligent document research for your workflow.
        </div>
      </section>

      <section className="login-form-panel">
        <div className="login-form-container">
          <div className="login-mobile-brand">
            <span className="brand-mark">
              <BookOpen size={22} />
            </span>
            <strong>DocuMind</strong>
          </div>

          <span className="eyebrow">WELCOME BACK</span>
          <h2>Sign in to your workspace</h2>
          <p className="login-form-subtitle">
            Access your documents and continue your research.
          </p>

          <form className="login-form" onSubmit={handleSubmit}>
            <div className="form-field">
              <label htmlFor="login-email">Email address</label>

              <div className="login-input-wrap">
                <Mail size={17} />
                <input
                  id="login-email"
                  type="email"
                  autoComplete="username"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  required
                />
              </div>
            </div>

            <div className="form-field">
              <div className="login-password-label">
                <label htmlFor="login-password">Password</label>
              </div>

              <div className="login-input-wrap">
                <LockKeyhole size={17} />
                <input
                  id="login-password"
                  type={showPassword ? "text" : "password"}
                  autoComplete="current-password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  required
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={() =>
                    setShowPassword((previous) => !previous)
                  }
                  aria-label={
                    showPassword ? "Hide password" : "Show password"
                  }
                >
                  {showPassword ? (
                    <EyeOff size={17} />
                  ) : (
                    <Eye size={17} />
                  )}
                </button>
              </div>
            </div>

            {error && (
              <div className="inline-alert alert-error" role="alert">
                {error}
              </div>
            )}

            <Button type="submit" fullWidth>
              Sign in <ArrowRight size={16} />
            </Button>
          </form>

          <div className="login-security-note">
            <ShieldCheck size={16} />
            Authentication must be enabled on the backend before this page
            can securely sign users in.
          </div>

          <p className="login-back-link">
            <Link to="/">Return to workspace</Link>
          </p>
        </div>
      </section>
    </main>
  );
}