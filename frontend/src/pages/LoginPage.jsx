import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { api } from "../services/api";

const initialRegisterState = {
  username: "",
  email: "",
  phone: "",
  password: "",
};

function LoginPage() {
  const navigate = useNavigate();
  const { setSession } = useAuth();
  const [mode, setMode] = useState("login");
  const [loginData, setLoginData] = useState({ username: "", password: "" });
  const [registerData, setRegisterData] = useState(initialRegisterState);
  const [formErrors, setFormErrors] = useState({});
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const validateForm = () => {
    if (mode === "login") return true;
    const errors = {};
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const phoneRegex = /^\+?[1-9]\d{1,14}$/;
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$/;

    if (!registerData.email || !emailRegex.test(registerData.email)) {
      errors.email = "Please enter a valid email address.";
    }
    if (registerData.phone && !phoneRegex.test(registerData.phone)) {
      errors.phone = "Please enter a valid phone number.";
    }
    if (!registerData.password || !passwordRegex.test(registerData.password)) {
      errors.password = "Password must be at least 8 chars, contain upper, lower, number, and special char.";
    }
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!validateForm()) return;
    setError("");
    setLoading(true);

    try {
      const endpoint = mode === "login" ? "/auth/login" : "/auth/register";
      const payload = mode === "login" ? loginData : registerData;
      const { data } = await api.post(endpoint, payload);
      setSession(data.access_token, data.user);
      navigate("/chat");
    } catch (requestError) {
      setError(requestError.response?.data?.detail || "Authentication failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div>
          <p className="eyebrow">AI + RAG</p>
          <h2>MPOnline FAQ Chatbot</h2>
          <p className="muted">
            Upload service documents, answer only from evidence, and escalate uncertain
            cases to human experts.
          </p>
        </div>

        <div className="tab-row">
          <button
            className={mode === "login" ? "tab active" : "tab"}
            onClick={() => setMode("login")}
            type="button"
          >
            Login
          </button>
          <button
            className={mode === "register" ? "tab active" : "tab"}
            onClick={() => setMode("register")}
            type="button"
          >
            Register
          </button>
        </div>

        <form onSubmit={handleSubmit} className="form-grid">
          {mode === "register" ? (
            <>
              <div className="input-group">
                <input
                  placeholder="Username"
                  value={registerData.username}
                  onChange={(event) =>
                    setRegisterData((current) => ({ ...current, username: event.target.value }))
                  }
                  required
                />
              </div>
              <div className="input-group">
                <input
                  className={formErrors.email ? "error-input" : ""}
                  placeholder="Email"
                  type="email"
                  value={registerData.email}
                  onChange={(event) =>
                    setRegisterData((current) => ({ ...current, email: event.target.value }))
                  }
                  required
                />
                {formErrors.email && <span className="field-error">{formErrors.email}</span>}
              </div>
              <div className="input-group">
                <input
                  className={formErrors.phone ? "error-input" : ""}
                  placeholder="Phone (Optional)"
                  type="tel"
                  value={registerData.phone}
                  onChange={(event) =>
                    setRegisterData((current) => ({ ...current, phone: event.target.value }))
                  }
                />
                {formErrors.phone && <span className="field-error">{formErrors.phone}</span>}
              </div>
              <div className="input-group">
                <input
                  className={formErrors.password ? "error-input" : ""}
                  placeholder="Password"
                  type="password"
                  value={registerData.password}
                  onChange={(event) =>
                    setRegisterData((current) => ({ ...current, password: event.target.value }))
                  }
                  required
                />
                {formErrors.password && <span className="field-error">{formErrors.password}</span>}
              </div>
            </>
          ) : (
            <>
              <input
                placeholder="Username"
                value={loginData.username}
                onChange={(event) =>
                  setLoginData((current) => ({ ...current, username: event.target.value }))
                }
                required
              />
              <input
                placeholder="Password"
                type="password"
                value={loginData.password}
                onChange={(event) =>
                  setLoginData((current) => ({ ...current, password: event.target.value }))
                }
                required
              />
            </>
          )}

          {error && <p className="error-text">{error}</p>}
          <button className="primary-button" disabled={loading} type="submit">
            {loading ? "Please wait..." : mode === "login" ? "Login" : "Create account"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;
