import { useEffect, useState } from "react";
import { getBase, setBase, ping, getToken } from "./api";
import { StudentPortal } from "./portals/StudentPortal";
import { EmployerPortal } from "./portals/EmployerPortal";
import { EmployeePortal } from "./portals/EmployeePortal";

type Role = "student" | "employer" | "employee" | null;

export function App() {
  const [base, setBaseState] = useState(getBase());
  const [connected, setConnected] = useState<boolean | null>(null);
  const [role, setRole] = useState<Role>(null);

  async function checkConn() { setConnected(await ping()); }
  useEffect(() => { checkConn(); }, []);

  function saveBase() { setBase(base); setBaseState(getBase()); checkConn(); }

  if (role === "student") return <StudentPortal onBack={() => setRole(null)} />;
  if (role === "employer") return <EmployerPortal onBack={() => setRole(null)} />;
  if (role === "employee") return <EmployeePortal onBack={() => setRole(null)} />;

  return (
    <div className="connect">
      <span className="gods">G.O.D.S Holdings · Live Ecosystem</span>
      <h1>Connect to deployment</h1>
      <p style={{ fontSize: ".8rem", margin: "8px 0 14px" }}>
        Point this portal at your running G.O.D.S backend. Works from this web page to your
        local machine (same network) or via a public tunnel.
      </p>
      <input value={base} onChange={e => setBaseState(e.target.value)}
        placeholder="http://localhost:8000 or https://your-tunnel.ngrok-free.app" />
      <button className="btn" onClick={saveBase}>Connect</button>
      <div className={`status ${connected ? "ok" : "bad"}`}>
        {connected === null ? "checking…" : connected ? `✓ connected to ${getBase()}` : `✗ not reachable at ${getBase()}`}
      </div>

      {connected && (
        <>
          <p style={{ marginTop: 18, fontSize: ".8rem", color: "var(--white)" }}>Choose your portal:</p>
          <div className="roles">
            <div className="role student" onClick={() => setRole("student")}>
              <h3>Student</h3><p>SETHS learner</p></div>
            <div className="role employer" onClick={() => setRole("employer")}>
              <h3>Employer</h3><p>Post & hire</p></div>
            <div className="role employee" onClick={() => setRole("employee")}>
              <h3>Employee</h3><p>TS workforce</p></div>
          </div>
        </>
      )}
      <div className="foot">INSTALLABLE APP · CONNECTS LIVE TO YOUR G.O.D.S DEPLOYMENT</div>
    </div>
  );
}
