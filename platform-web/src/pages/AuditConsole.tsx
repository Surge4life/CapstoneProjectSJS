import { useEffect, useState } from "react";
import { api } from "../lib/api";
export function AuditConsole() {
  const [chain, setChain] = useState<any>(null);
  const [root, setRoot] = useState("");
  const [recs, setRecs] = useState<any[]>([]);
  useEffect(() => {
    api.get("/audit/chain/verify").then(setChain).catch(()=>{});
    api.get("/audit/chain/merkle-root").then(r=>setRoot(r.merkle_root)).catch(()=>{});
    api.get("/audit/records").then(setRecs).catch(()=>{});
  }, []);
  return (<>
    <div className="topbar"><h2>UDOC Audit (internal)</h2><span className="pill">immutable · hash-chained</span></div>
    <div className="grid">
      <div className="card"><h3>Chain Records</h3><div className="metric">{chain?.records ?? "—"}</div></div>
      <div className="card"><h3>Chain Intact</h3><div className="metric" style={{color: chain?.intact?"var(--ok)":"var(--bad)"}}>{chain ? String(chain.intact) : "—"}</div></div>
    </div>
    <div className="card"><h3>Published Merkle Root</h3>
      <p style={{fontFamily:"monospace",fontSize:".75rem",color:"var(--white)",wordBreak:"break-all"}}>{root || "—"}</p></div>
    <div className="card"><h3>Recent Audit Records</h3>
      <table><thead><tr><th>Seq</th><th>Event</th><th>Hash</th><th>Class</th></tr></thead>
      <tbody>{recs.map(r => <tr key={r.seq}><td>{r.seq}</td><td>{r.event_type}</td>
        <td style={{fontFamily:"monospace"}}>{r.event_hash}…</td><td>{r.classification}</td></tr>)}</tbody></table>
    </div>
  </>);
}
