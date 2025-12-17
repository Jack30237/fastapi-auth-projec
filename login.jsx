import { useState } from "react";
import axios from "axios";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://127.0.0.1:8000/login", { username, password });
      localStorage.setItem("token", res.data.access_token);
      setMessage("登入成功！");
    } catch (err) {
      setMessage(err.response?.data?.detail || "登入失敗");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input placeholder="帳號" value={username} onChange={e => setUsername(e.target.value)} />
      <input placeholder="密碼" type="password" value={password} onChange={e => setPassword(e.target.value)} />
      <button type="submit">登入</button>
      <p>{message}</p>
    </form>
  );
}
