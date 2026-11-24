import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../../services/authService";

function LoginPage() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");

  const handleLogin = async (
    e: React.FormEvent
  ) => {

    e.preventDefault();

    setError("");

    try {

      await login({
        username,
        password,
      });

      navigate("/dashboard");

    } catch {

      setError("Invalid username or password.");

    }

  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
      }}
    >
      <form
        onSubmit={handleLogin}
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "15px",
          width: "300px",
        }}
      >
        <h2>Login</h2>

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) =>
            setUsername(e.target.value)
          }
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
        />

        <button type="submit">
          Login
        </button>

        {error && (
          <p style={{ color: "red" }}>
            {error}
          </p>
        )}

      </form>
    </div>
  );
}

export default LoginPage;