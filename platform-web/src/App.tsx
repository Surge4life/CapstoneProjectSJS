import { useState } from "react";
import { BrowserRouter, Routes, Route, NavLink, Navigate } from "react-router-dom";
import { getToken, setToken } from "./lib/api";
import { Login } from "./pages/Login";
import { AdminDash } from "./pages/AdminDash";
import { UDOCConsole } from "./pages/UDOCConsole";
import { SETHSConsole } from "./pages/SETHSConsole";
import { MADIBAConsole } from "./pages/MADIBAConsole";
import { TSConsole } from "./pages/TSConsole";
import { AuditConsole } from "./pages/AuditConsole";

const NAV = [
  { to: "/admin", label: "GODS Admin" },
  { to: "/udoc", label: "UDOC Governance" },
  { to: "/audit", label: "UDOC Audit (internal)" },
  { to: "/seths", label: "SETHS" },
  { to: "/madiba", label: "MADIBA" },
  { to: "/ts", label: "TS Industries" },
];

function Shell({ children }: { children: React.ReactNode }) {
  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand"><h1>G.O.D.S</h1><span>Holdings · Sovereign Platform</span></div>
        <nav className="nav">
          {NAV.map(n => <NavLink key={n.to} to={n.to}
            className={({ isActive }) => isActive ? "active" : ""}>{n.label}</NavLink>)}
          <a onClick={() => { setToken(null); location.href = "/"; }} style={{ cursor: "pointer", marginTop: 20, color: "var(--bad)" }}>Sign out</a>
        </nav>
      </aside>
      <main className="main">{children}</main>
    </div>
  );
}

export function App() {
  const [authed, setAuthed] = useState(!!getToken());
  if (!authed) return <Login onAuth={() => setAuthed(true)} />;
  return (
    <BrowserRouter>
      <Shell>
        <Routes>
          <Route path="/admin" element={<AdminDash />} />
          <Route path="/udoc" element={<UDOCConsole />} />
          <Route path="/audit" element={<AuditConsole />} />
          <Route path="/seths" element={<SETHSConsole />} />
          <Route path="/madiba" element={<MADIBAConsole />} />
          <Route path="/ts" element={<TSConsole />} />
          <Route path="*" element={<Navigate to="/admin" />} />
        </Routes>
      </Shell>
    </BrowserRouter>
  );
}
