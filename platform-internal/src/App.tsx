import { useEffect, useState, type ReactNode } from "react";
import { BrowserRouter, Routes, Route, NavLink, Navigate, useNavigate } from "react-router-dom";
import { api, getToken, setToken } from "./api";
import { Overview } from "./consoles/Overview";
import { SethsOps } from "./consoles/SethsOps";
import { MadibaOps } from "./consoles/MadibaOps";
import { TSOps } from "./consoles/TSOps";
import { UDOCGov } from "./consoles/UDOCGov";
import { Intelligence } from "./consoles/Intelligence";

/** Capstone profile — /auth/me may omit systems[] and is_admin */
type Profile = {
  sub?: string;
  email?: string;
  role?: string;
  division?: string;
  is_admin?: boolean;
  systems?: { key: string; label?: string }[];
  [k: string]: unknown;
};

function Login({ onAuth }: { onAuth: () => void }) {
  const [email, setEmail] = useState("admin@gods.local");
  const [pw, setPw] = useState("admin123");
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);
  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    setErr("");
    try {
      await api.login(email.trim().toLowerCase(), pw);
      onAuth();
    } catch (ex: any) {
      setErr(ex?.message || "Login failed");
    } finally {
      setBusy(false);
    }
  }
  function fill(e: string, p: string) {
    setEmail(e);
    setPw(p);
  }
  return (
    <div className="login">
      <div className="login-card">
        <h1>G.O.D.S Internal</h1>
        <p className="muted">Staff work environment · Holdings core · four divisions · UDOC across</p>
        <form onSubmit={submit}>
          <label>Email</label>
          <input value={email} onChange={(e) => setEmail(e.target.value)} autoComplete="username" />
          <label>Password</label>
          <input type="password" value={pw} onChange={(e) => setPw(e.target.value)} autoComplete="current-password" />
          <button type="submit" disabled={busy}>{busy ? "Signing in…" : "Sign in"}</button>
        </form>
        <div className="chips">
          <button type="button" onClick={() => fill("admin@gods.local", "admin123")}>admin@</button>
          <button type="button" onClick={() => fill("seths@gods.local", "staff123")}>seths@</button>
          <button type="button" onClick={() => fill("madiba@gods.local", "staff123")}>madiba@</button>
          <button type="button" onClick={() => fill("ts@gods.local", "staff123")}>ts@</button>
        </div>
        {err && <p className="err">{err}</p>}
        <p className="muted small">Not Client SaaS. Intelligence is one console — not the whole internal product.</p>
      </div>
    </div>
  );
}

function Launcher({ profile }: { profile: Profile }) {
  const nav = useNavigate();
  const cards = [
    { to: "/overview", title: "Holdings Overview", blurb: "GODS core · division loop" },
    { to: "/seths", title: "SETHS", blurb: "Develops · learners · placement" },
    { to: "/ts", title: "TS Industries", blurb: "Deploys · SPVs · workforce" },
    { to: "/madiba", title: "MADIBA", blurb: "Ledger · ≠ AUM · not_deployed" },
    { to: "/udoc", title: "UDOC Governance", blurb: "Across divisions · policy · EVA" },
    { to: "/intelligence", title: "Intelligence", blurb: "Corpus ask · one console" },
  ];
  return (
    <div className="main">
      <div className="top">
        <h2>G.O.D.S Internal · Launcher</h2>
        <span className="badge">{profile.role || "staff"} · {profile.division || "GODS"}</span>
      </div>
      <p className="muted">Four divisions under Holdings. UDOC is governance across them — not a fifth division and not the Holdings core.</p>
      <div className="launcher-grid">
        {cards.map((c) => (
          <button key={c.to} type="button" className="launch-card" onClick={() => nav(c.to)}>
            <strong>{c.title}</strong>
            <span>{c.blurb}</span>
          </button>
        ))}
      </div>
      <div className="launcher-grid" style={{ marginTop: 12 }}>
        <a className="launch-card" href="https://gods-platform-core.onrender.com/portals" target="_blank" rel="noreferrer">Portals · 24</a>
        <a className="launch-card" href="https://gods-platform-core.onrender.com/gbs" target="_blank" rel="noreferrer">GBS · Holdings freeze</a>
        <a className="launch-card" href="https://gods-platform-core.onrender.com/Sentinel" target="_blank" rel="noreferrer">Sentinel · EVA</a>
        <a className="launch-card" href="https://gods-platform-core.onrender.com/admin" target="_blank" rel="noreferrer">GODS Admin mainframe</a>
      </div>
    </div>
  );
}

function Guarded({ profile, sysKey, children }: { profile: Profile; sysKey: string; children: ReactNode }) {
  const systems = profile.systems || [];
  const role = (profile.role || "").toLowerCase();
  const isAdmin = !!profile.is_admin || role === "admin" || role === "superadmin";
  const openStaff = systems.length === 0 && (isAdmin || role === "staff" || !!profile.division);
  if (sysKey && systems.length > 0 && !systems.some((s) => s.key === sysKey) && !isAdmin) {
    return (
      <div className="main">
        <div className="top">
          <h2>Access denied</h2>
          <span className="badge">🔒 403</span>
        </div>
      </div>
    );
  }
  if (sysKey && systems.length === 0 && !openStaff && !isAdmin) {
    return (
      <div className="main">
        <div className="top">
          <h2>Access denied</h2>
          <span className="badge">🔒 403</span>
        </div>
      </div>
    );
  }
  return <>{children}</>;
}

function Shell({ profile, children }: { profile: Profile; children: ReactNode }) {
  const nav = useNavigate();
  const rawSystems = profile.systems || [];
  const DEFAULT_GODS_SYSTEMS = [
    { key: "holdings-overview", label: "Holdings Overview" },
    { key: "seths-ops", label: "SETHS Ops" },
    { key: "madiba-ops", label: "MADIBA Ops" },
    { key: "ts-ops", label: "TS Ops" },
    { key: "udoc-gov", label: "UDOC Governance" },
    { key: "intelligence", label: "Intelligence" },
  ];
  let systems = rawSystems.length ? rawSystems : DEFAULT_GODS_SYSTEMS;
  const role = (profile.role || "").toLowerCase();
  const div = (profile.division || "").toLowerCase();
  if (!rawSystems.length && role !== "admin" && role !== "superadmin") {
    if (div.includes("seths") || role.includes("seths"))
      systems = DEFAULT_GODS_SYSTEMS.filter((s) => ["holdings-overview", "seths-ops", "udoc-gov", "intelligence"].includes(s.key));
    else if (div.includes("madiba") || role.includes("madiba"))
      systems = DEFAULT_GODS_SYSTEMS.filter((s) => ["holdings-overview", "madiba-ops", "udoc-gov", "intelligence"].includes(s.key));
    else if (div.includes("ts") || role.includes("ts"))
      systems = DEFAULT_GODS_SYSTEMS.filter((s) => ["holdings-overview", "ts-ops", "udoc-gov", "intelligence"].includes(s.key));
  }
  return (
    <div className="shell">
      <aside className="side">
        <div className="brand">G.O.D.S <b>Internal</b></div>
        <div className="who">{profile.sub || profile.email || "staff"}</div>
        <div className="sec">Holdings · divisions</div>
        {systems.some((s) => s.key === "holdings-overview") && (
          <NavLink to="/overview" className={({ isActive }) => (isActive ? "active" : "")}>
            Holdings Overview
          </NavLink>
        )}
        {systems.some((s) => s.key === "seths-ops") && (
          <NavLink to="/seths" className={({ isActive }) => (isActive ? "active" : "")}>
            SETHS Ops
          </NavLink>
        )}
        {systems.some((s) => s.key === "madiba-ops") && (
          <NavLink to="/madiba" className={({ isActive }) => (isActive ? "active" : "")}>
            MADIBA Ops
          </NavLink>
        )}
        {systems.some((s) => s.key === "ts-ops") && (
          <NavLink to="/ts" className={({ isActive }) => (isActive ? "active" : "")}>
            TS Industries Ops
          </NavLink>
        )}
        {systems.some((s) => s.key === "udoc-gov") && (
          <>
            <div className="sec">Governance</div>
            <NavLink to="/udoc" className={({ isActive }) => (isActive ? "active" : "")}>
              UDOC Governance
            </NavLink>
          </>
        )}
        <div className="sec">Intelligence</div>
        <NavLink to="/intelligence" className={({ isActive }) => (isActive ? "active" : "")}>
          Intelligence · corpus
        </NavLink>
        <div className="sec">Core operators (live)</div>
        <a className="nav" href="https://gods-platform-core.onrender.com/portals" target="_blank" rel="noreferrer">Portals · 24</a>
        <a className="nav" href="https://gods-platform-core.onrender.com/gbs" target="_blank" rel="noreferrer">GBS · Holdings</a>
        <a className="nav" href="https://gods-platform-core.onrender.com/Sentinel" target="_blank" rel="noreferrer">Sentinel · EVA</a>
        <a className="nav" href="https://gods-platform-core.onrender.com/divisions" target="_blank" rel="noreferrer">Divisions loop</a>
        <a className="nav" href="https://gods-platform-core.onrender.com/admin" target="_blank" rel="noreferrer">GODS Admin mainframe</a>
        <button
          type="button"
          className="signout"
          onClick={() => {
            setToken(null);
            nav("/");
            window.location.reload();
          }}
        >
          Sign out
        </button>
      </aside>
      <div className="main-wrap">{children}</div>
    </div>
  );
}

export function App() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [booting, setBooting] = useState(true);
  async function boot() {
    if (!getToken()) {
      setBooting(false);
      return;
    }
    try {
      const me = await api.get("/auth/me");
      const role = (me.role || "").toLowerCase();
      setProfile({
        ...me,
        is_admin: !!(me as any).is_admin || role === "admin" || role === "superadmin",
        systems: (me as any).systems || [],
      });
    } catch {
      setToken(null);
      setProfile(null);
    } finally {
      setBooting(false);
    }
  }
  useEffect(() => {
    boot();
  }, []);
  if (booting) return <div className="login"><p className="muted">Booting G.O.D.S Internal…</p></div>;
  if (!getToken() || !profile) return <Login onAuth={() => { setBooting(true); boot(); }} />;
  return (
    <BrowserRouter>
      <Shell profile={profile}>
        <Routes>
          <Route path="/launcher" element={<Launcher profile={profile} />} />
          <Route path="/overview" element={<Guarded profile={profile} sysKey="holdings-overview"><Overview /></Guarded>} />
          <Route path="/seths" element={<Guarded profile={profile} sysKey="seths-ops"><SethsOps /></Guarded>} />
          <Route path="/madiba" element={<Guarded profile={profile} sysKey="madiba-ops"><MadibaOps /></Guarded>} />
          <Route path="/ts" element={<Guarded profile={profile} sysKey="ts-ops"><TSOps /></Guarded>} />
          <Route path="/udoc" element={<Guarded profile={profile} sysKey="udoc-gov"><UDOCGov /></Guarded>} />
          <Route path="/intelligence" element={<Intelligence />} />
          <Route path="/" element={<Navigate to="/launcher" />} />
          <Route path="*" element={<Navigate to="/launcher" />} />
        </Routes>
      </Shell>
    </BrowserRouter>
  );
}
export default App;
