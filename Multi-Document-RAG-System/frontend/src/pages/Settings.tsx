import { useEffect, useState } from "react";
import {
  Check,
  Database,
  Globe,
  KeyRound,
  Palette,
  RefreshCw,
  Server,
  ShieldCheck,
  SlidersHorizontal,
} from "lucide-react";

import Button from "../components/common/Button";
import Loader from "../components/common/Loader";
import { apiClient } from "../api/client";
import { getAPIErrorMessage } from "../api/client";

type HealthState = "checking" | "connected" | "disconnected";

export default function Settings() {
  const [health, setHealth] = useState<HealthState>("checking");
  const [apiBaseUrl, setApiBaseUrl] = useState(
    apiClient.defaults.baseURL ?? "",
  );
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState("");
  const [testing, setTesting] = useState(false);

  async function checkHealth() {
    setTesting(true);
    setHealth("checking");
    setError("");

    try {
      const response = await apiClient.get("/health/ready");
      setHealth(
        response.data?.status === "ready"
          ? "connected"
          : "disconnected",
      );
    } catch {
      setHealth("disconnected");
    } finally {
      setTesting(false);
    }
  }

  useEffect(() => {
    void checkHealth();
  }, []);

  function saveEndpoint() {
    const normalized = apiBaseUrl.trim().replace(/\/+$/, "");

    if (!/^https?:\/\/.+/i.test(normalized)) {
      setError("Enter a valid HTTP or HTTPS API URL.");
      setSaved(false);
      return;
    }

    setError("");
    setSaved(false);

    try {
      const url = new URL(normalized);

      if (url.username || url.password) {
        setError("API URLs must not contain embedded credentials.");
        return;
      }

      apiClient.defaults.baseURL = normalized;
      setApiBaseUrl(normalized);
      setSaved(true);

      window.setTimeout(() => {
        setSaved(false);
      }, 2500);
    } catch {
      setError("The API URL is invalid.");
    }
  }

  return (
    <div className="settings-page">
      <div className="page-heading">
        <div>
          <span className="eyebrow">WORKSPACE CONFIGURATION</span>
          <h1>Settings</h1>
          <p>
            Configure your local workspace connection and inspect service
            availability.
          </p>
        </div>
      </div>

      <div className="settings-layout">
        <aside className="settings-navigation">
          <a href="#general" className="settings-nav-item settings-nav-active">
            <SlidersHorizontal size={17} />
            General
          </a>

          <a href="#connection" className="settings-nav-item">
            <Globe size={17} />
            API connection
          </a>

          <a href="#services" className="settings-nav-item">
            <Server size={17} />
            Services
          </a>

          <a href="#privacy" className="settings-nav-item">
            <ShieldCheck size={17} />
            Privacy
          </a>
        </aside>

        <div className="settings-sections">
          <section className="panel settings-panel" id="general">
            <div className="settings-section-heading">
              <div className="settings-section-icon">
                <Palette size={19} />
              </div>
              <div>
                <h2>General</h2>
                <p>Workspace information and interface preferences.</p>
              </div>
            </div>

            <div className="settings-field-row">
              <div>
                <strong>Application name</strong>
                <p>The name displayed throughout the interface.</p>
              </div>
              <span className="settings-readonly-value">
                DocuMind
              </span>
            </div>

            <div className="settings-field-row">
              <div>
                <strong>Environment</strong>
                <p>Frontend runtime configuration.</p>
              </div>
              <span className="settings-readonly-value">
                {import.meta.env.MODE}
              </span>
            </div>

            <div className="settings-field-row">
              <div>
                <strong>Language</strong>
                <p>Interface date and number formatting.</p>
              </div>
              <span className="settings-readonly-value">
                {navigator.language || "en-US"}
              </span>
            </div>
          </section>

          <section className="panel settings-panel" id="connection">
            <div className="settings-section-heading">
              <div className="settings-section-icon">
                <Globe size={19} />
              </div>
              <div>
                <h2>API connection</h2>
                <p>Configure the backend endpoint for this browser session.</p>
              </div>
            </div>

            <div className="form-field">
              <label htmlFor="api-base-url">Backend API URL</label>
              <input
                id="api-base-url"
                value={apiBaseUrl}
                onChange={(event) => {
                  setApiBaseUrl(event.target.value);
                  setSaved(false);
                }}
                placeholder="http://127.0.0.1:8000/api/v1"
              />
              <small>
                The new endpoint applies until the page is refreshed.
                To persist it, update the frontend environment file.
              </small>
            </div>

            {error && (
              <div className="inline-alert alert-error">
                {error}
              </div>
            )}

            <div className="settings-action-row">
              <Button
                variant="secondary"
                icon={<RefreshCw size={15} />}
                onClick={() => void checkHealth()}
                loading={testing}
              >
                Test connection
              </Button>

              <Button
                icon={<Check size={16} />}
                onClick={saveEndpoint}
              >
                Save for this session
              </Button>
            </div>

            {saved && (
              <div className="inline-alert alert-success">
                <Check size={16} />
                Endpoint updated for this browser session.
              </div>
            )}
          </section>

          <section className="panel settings-panel" id="services">
            <div className="settings-section-heading">
              <div className="settings-section-icon">
                <Database size={19} />
              </div>
              <div>
                <h2>Service status</h2>
                <p>Current availability reported by the backend.</p>
              </div>
            </div>

            <div className="service-status-row">
              <div className="service-status-icon">
                <Server size={18} />
              </div>

              <div className="service-status-info">
                <strong>Backend API</strong>
                <small>FastAPI application</small>
              </div>

              <span
                className={`service-status-badge service-${health}`}
              >
                <span />
                {health === "checking"
                  ? "Checking"
                  : health === "connected"
                    ? "Connected"
                    : "Unavailable"}
              </span>
            </div>

            <div className="service-status-row">
              <div className="service-status-icon">
                <Database size={18} />
              </div>

              <div className="service-status-info">
                <strong>Database</strong>
                <small>Database readiness endpoint</small>
              </div>

              <span
                className={`service-status-badge service-${health}`}
              >
                <span />
                {health === "connected"
                  ? "Ready"
                  : health === "checking"
                    ? "Checking"
                    : "Unavailable"}
              </span>
            </div>

            <div className="service-status-row">
              <div className="service-status-icon">
                <KeyRound size={18} />
              </div>

              <div className="service-status-info">
                <strong>Language model</strong>
                <small>
                  Provider configuration is managed by the backend.
                </small>
              </div>

              <span className="service-status-badge service-unknown">
                <span />
                Not verified
              </span>
            </div>

            {health === "disconnected" && (
              <div className="inline-alert alert-error">
                The backend could not be reached. Confirm that the server is
                running and that CORS permits this frontend origin.
              </div>
            )}
          </section>

          <section className="panel settings-panel" id="privacy">
            <div className="settings-section-heading">
              <div className="settings-section-icon">
                <ShieldCheck size={19} />
              </div>
              <div>
                <h2>Privacy and security</h2>
                <p>Important deployment and data handling details.</p>
              </div>
            </div>

            <div className="privacy-notice">
              <ShieldCheck size={21} />
              <div>
                <strong>Keep credentials on the server</strong>
                <p>
                  Never put LLM provider API keys in frontend environment
                  variables. Use backend environment variables and enable
                  authentication before exposing the API publicly.
                </p>
              </div>
            </div>

            <div className="privacy-notice">
              <Database size={21} />
              <div>
                <strong>Understand local storage</strong>
                <p>
                  Uploaded documents and vector indexes are stored by the
                  backend. Configure backups, access controls, and persistent
                  storage for production deployments.
                </p>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}