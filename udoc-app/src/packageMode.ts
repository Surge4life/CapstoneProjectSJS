/** Capstone package identity for udoc-app / mobile.
 *  This build is the **Client** tenant SaaS shell.
 *  Staff Internal = udoc-desktop + udoc-internal (separate packages).
 */
export const UDOC_PACKAGE = "client" as const;

export type PackageRole =
  | "admin"
  | "exec"
  | "operator"
  | "gov"
  | "auditor"
  | "viewer"
  | "client";

/** True when UI should behave as tenant SaaS (no staff hardware plane). */
export function isTenantClientRole(role?: string | null, isAdmin?: boolean): boolean {
  if (isAdmin) return false;
  const r = String(role || "").toLowerCase();
  return r === "client";
}

/** Hardware plane is staff/forecast only — not the Client product surface. */
export function showHardwarePlane(role?: string | null, isAdmin?: boolean): boolean {
  if (isAdmin) return true;
  const r = String(role || "").toLowerCase();
  return r === "admin" || r === "exec" || r === "operator" || r === "gov";
}
