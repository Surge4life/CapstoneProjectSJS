// ════════════════════════════════════════════════════════════════════════════
// UDOC EVA ENGINE — COMPLETE, SELF-CONTAINED BUILD
// Evaluating Valiant Algorithms · 6-Dimensional Sovereign Risk Scoring
// Claim 10 (6D scoring + JSD) · Claim 8 (Ethical Cooperation) · Part 7.1 (formulas)
// G.O.D.S Holdings (Pty) Ltd — v9.3 → v10.0 (gaps completed)
//
// This file CONSOLIDATES the v9.3 eva-engine and COMPLETES the five computations
// that were previously pass-through inputs:
//   1. CMAG Ethical Cooperation Score   ECS = C × A × I × F
//   2. Societal Impact via H-OS-56       I = entropy over 56 harm/benefit combos
//   3. MFCM 47-check compliance catalogue (full enumeration, ZA NAIFP + POPIA)
//   4. Fairness metrics (DI, SPD)        derived from confusion matrices
//   5. Temperature-scaled confidence     wired into the main pipeline
//
// Runs standalone with `ts-node eva-engine-complete.ts` (demo harness at bottom).
// ════════════════════════════════════════════════════════════════════════════

import { createHmac, randomBytes, timingSafeEqual } from "node:crypto";

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 1 · TYPES (self-contained — mirrors @udoc/types contracts)
// ─────────────────────────────────────────────────────────────────────────────

export enum GovernanceDecision {
  APPROVE  = "APPROVE",
  BLOCK    = "BLOCK",
  REVIEW   = "REVIEW",
  RESTRICT = "RESTRICT",
  ESCALATE = "ESCALATE",
}

export enum RiskTier {
  MINIMAL      = "MINIMAL",      // R = 0.0
  NOTABLE      = "NOTABLE",      // R = 0.2
  MEDIUM       = "MEDIUM",       // R = 0.5
  HIGH         = "HIGH",         // R = 0.8
  UNACCEPTABLE = "UNACCEPTABLE", // R = 1.0 — PERMANENT BLOCK
}

export enum CMAGArbitration {
  CONSENSUS    = "CONSENSUS",
  DISPUTE      = "DISPUTE",
  ESCALATE_IGA = "ESCALATE_IGA",
}

// 6-dimensional EVA score (full output contract)
export interface EVAScore {
  validity:        number;   // V  — [0,1] prediction vs ground-truth fidelity
  confidence:      number;   // Cf — [0,1] temperature-scaled
  risk:            number;   // R  — [0,1] SA tier mapped
  compliance:      number;   // Co — [0,1] MFCM 47-check weighted avg
  stability:       number;   // S  — [0,1] 1 − JSD(current‖baseline)
  societalImpact:  number;   // I  — [0,1] H-OS-56 entropy benefit ratio
  svs:             number;   // SVS = Σ(wᵢ·dimᵢ) aggregate, bounded [0,1]
  jsd:             number;   // Jensen-Shannon Divergence
  disparateImpact: number;   // DI — min(group rates)/max(group rates)
  spd:             number;   // Statistical Parity Difference
  ecs:             number;   // Ethical Cooperation Score (CMAG)
  cmag:            CMAGScore; // full CMAG breakdown
  decision:        GovernanceDecision;
  blockReasons:    string[];
  computedAt:      Date;
  latencyMs:       number;
}

export interface EVACoefficients {
  wValidity:       number;  // default 0.15
  wConfidence:     number;  // default 0.15
  wRisk:           number;  // default 0.25
  wCompliance:     number;  // default 0.20
  wStability:      number;  // default 0.10
  wSocietalImpact: number;  // default 0.15
}

export interface EVAThresholds {
  riskBlock:            number;  // R   > 0.80
  complianceBlock:      number;  // Co  < 0.70
  disparateImpactBlock: number;  // DI  < 0.80
  jsdBlock:             number;  // JSD > 0.40
  ecsBlock:             number;  // ECS < 0.65
  spdBlock:             number;  // |SPD| > 0.05
}

export interface CMAGScore {
  cooperation: number;      // [0,1] agent-to-agent agreement
  autonomy:    number;      // [0,1] preserved human autonomy
  integrity:   number;      // [0,1] data + provenance integrity
  fairness:    number;      // [0,1] cross-group fairness
  ecs:         number;      // ECS = C × A × I × F
  arbitration: CMAGArbitration;
}

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 2 · CONSTANTS — coefficients, thresholds, tier mapping
// ─────────────────────────────────────────────────────────────────────────────

// SA NAIFP-aligned default coefficients (Σ = 1.0)
export const SA_DEFAULT_COEFFICIENTS: EVACoefficients = {
  wValidity:       0.15,
  wConfidence:     0.15,
  wRisk:           0.25,
  wCompliance:     0.20,
  wStability:      0.10,
  wSocietalImpact: 0.15,
};

// Military profile — risk-dominant (Σ = 1.0)
export const MILITARY_COEFFICIENTS: EVACoefficients = {
  wValidity:       0.10,
  wConfidence:     0.10,
  wRisk:           0.40,
  wCompliance:     0.20,
  wStability:      0.10,
  wSocietalImpact: 0.10,
};

// Healthcare profile — compliance + societal dominant (Σ = 1.0)
export const HEALTHCARE_COEFFICIENTS: EVACoefficients = {
  wValidity:       0.15,
  wConfidence:     0.10,
  wRisk:           0.20,
  wCompliance:     0.25,
  wStability:      0.10,
  wSocietalImpact: 0.20,
};

export const DEFAULT_THRESHOLDS: EVAThresholds = {
  riskBlock:            0.80,
  complianceBlock:      0.70,
  disparateImpactBlock: 0.80,
  jsdBlock:             0.40,
  ecsBlock:             0.65,
  spdBlock:             0.05,
};

export const RISK_TIER_R: Record<RiskTier, number> = {
  [RiskTier.MINIMAL]:      0.0,
  [RiskTier.NOTABLE]:      0.2,
  [RiskTier.MEDIUM]:       0.5,
  [RiskTier.HIGH]:         0.8,
  [RiskTier.UNACCEPTABLE]: 1.0,
};

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 3 · DIMENSION 5 — STABILITY via Jensen-Shannon Divergence
// S = 1 − JSD(current ‖ baseline)
// ─────────────────────────────────────────────────────────────────────────────

/** KL divergence with zero-guard (bits). */
function klDivergence(p: number[], q: number[]): number {
  return p.reduce((sum, pi, i) => {
    if (pi === 0) return sum;
    const qi = q[i] === 0 ? 1e-10 : q[i];
    return sum + pi * Math.log2(pi / qi);
  }, 0);
}

/** Jensen-Shannon Divergence — symmetric, bounded [0,1] in bits. */
export function computeJSD(currentDist: number[], baselineDist: number[]): number {
  if (currentDist.length !== baselineDist.length) {
    throw new Error("EVA-JSD: Distribution length mismatch");
  }
  const M = currentDist.map((p, i) => (p + baselineDist[i]) / 2);
  return 0.5 * klDivergence(currentDist, M) + 0.5 * klDivergence(baselineDist, M);
}

/** Stability dimension: higher = more stable (less drift). */
export function computeStability(currentDist: number[], baselineDist: number[]): {
  stability: number; jsd: number;
} {
  const jsd = computeJSD(currentDist, baselineDist);
  return { stability: Math.max(0, 1 - jsd), jsd };
}

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 4 · DIMENSION 2 — CONFIDENCE with temperature scaling
// Cf = confidence_raw / (1 + ln(T + 1))     (Part 7.1)
// ─────────────────────────────────────────────────────────────────────────────

export function scaleConfidenceByTemperature(rawConfidence: number, temperature: number): number {
  if (temperature <= 0) return rawConfidence;
  return rawConfidence / (1 + Math.log(temperature + 1));
}

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 5 · DIMENSION 4 — COMPLIANCE: MFCM 47-CHECK CATALOGUE (COMPLETED)
// Co = Σ(wᵢ × MFCMᵢ) / Σwᵢ across 47 checks
// Full enumeration: ZA NAIFP pillars + POPIA + EU AI Act + sector overlays
// ─────────────────────────────────────────────────────────────────────────────

export interface MFCMCheck {
  checkId:   number;   // 1–47
  category:  string;
  passed:    boolean;
  weight:    number;
  reference: string;   // legal/regulatory citation
}

/**
 * The full 47-check MFCM (Multi-Framework Compliance Matrix) catalogue.
 * Each entry carries a default weight and legal reference. `evaluator`
 * is supplied at call-time to return pass/fail against a model's facts.
 */
export interface MFCMCatalogEntry {
  checkId:   number;
  category:  string;
  weight:    number;
  reference: string;
  description: string;
}

export const MFCM_CATALOG: MFCMCatalogEntry[] = [
  // ── POPIA — Data Protection (1–10) ──
  { checkId: 1,  category: "DATA_PROTECTION", weight: 1.0, reference: "POPIA s.4",   description: "Lawful processing conditions met" },
  { checkId: 2,  category: "DATA_PROTECTION", weight: 1.0, reference: "POPIA s.9",   description: "Processing limitation — minimality" },
  { checkId: 3,  category: "DATA_PROTECTION", weight: 1.0, reference: "POPIA s.10",  description: "Consent / lawful basis recorded" },
  { checkId: 4,  category: "DATA_PROTECTION", weight: 1.0, reference: "POPIA s.11",  description: "Purpose specification documented" },
  { checkId: 5,  category: "DATA_PROTECTION", weight: 0.8, reference: "POPIA s.13",  description: "Retention limitation enforced" },
  { checkId: 6,  category: "DATA_PROTECTION", weight: 1.0, reference: "POPIA s.18",  description: "Data-subject notification given" },
  { checkId: 7,  category: "DATA_PROTECTION", weight: 1.0, reference: "POPIA s.19",  description: "Security safeguards (integrity/confidentiality)" },
  { checkId: 8,  category: "DATA_PROTECTION", weight: 1.0, reference: "POPIA s.22",  description: "Breach notification capability present" },
  { checkId: 9,  category: "DATA_PROTECTION", weight: 0.9, reference: "POPIA s.71",  description: "Automated decision-making safeguards" },
  { checkId: 10, category: "DATA_PROTECTION", weight: 1.0, reference: "POPIA s.72",  description: "Cross-border transfer lawful (sovereignty)" },

  // ── SA NAIFP — National AI Framework Pillars (11–22) ──
  { checkId: 11, category: "NAIFP_FAIRNESS",   weight: 1.0, reference: "NAIFP P1",  description: "Fairness & non-discrimination" },
  { checkId: 12, category: "NAIFP_FAIRNESS",   weight: 1.0, reference: "NAIFP P1",  description: "Disparate-impact within tolerance" },
  { checkId: 13, category: "NAIFP_TRANSP",     weight: 0.9, reference: "NAIFP P2",  description: "Transparency & explainability" },
  { checkId: 14, category: "NAIFP_TRANSP",     weight: 0.8, reference: "NAIFP P2",  description: "Model card published" },
  { checkId: 15, category: "NAIFP_ACCOUNT",    weight: 1.0, reference: "NAIFP P3",  description: "Accountability — named operator" },
  { checkId: 16, category: "NAIFP_ACCOUNT",    weight: 0.9, reference: "NAIFP P3",  description: "Audit trail immutable (StayChain)" },
  { checkId: 17, category: "NAIFP_SAFETY",     weight: 1.0, reference: "NAIFP P4",  description: "Safety & robustness testing" },
  { checkId: 18, category: "NAIFP_SAFETY",     weight: 1.0, reference: "NAIFP P4",  description: "Adversarial robustness validated" },
  { checkId: 19, category: "NAIFP_PRIVACY",    weight: 1.0, reference: "NAIFP P5",  description: "Privacy-by-design verified" },
  { checkId: 20, category: "NAIFP_HUMAN",      weight: 1.0, reference: "NAIFP P6",  description: "Human oversight guaranteed" },
  { checkId: 21, category: "NAIFP_SOVEREIGN",  weight: 1.0, reference: "NAIFP P7",  description: "Data & compute sovereignty (ZA)" },
  { checkId: 22, category: "NAIFP_SOCIETAL",   weight: 0.9, reference: "NAIFP P8",  description: "Societal benefit demonstrated" },

  // ── EU AI Act overlay (23–32) ──
  { checkId: 23, category: "EU_AI_ACT", weight: 1.0, reference: "EU AI Act Art.5",  description: "No prohibited practices" },
  { checkId: 24, category: "EU_AI_ACT", weight: 1.0, reference: "EU AI Act Art.6",  description: "High-risk classification correct" },
  { checkId: 25, category: "EU_AI_ACT", weight: 0.9, reference: "EU AI Act Art.9",  description: "Risk-management system in place" },
  { checkId: 26, category: "EU_AI_ACT", weight: 0.9, reference: "EU AI Act Art.10", description: "Data governance — training quality" },
  { checkId: 27, category: "EU_AI_ACT", weight: 0.8, reference: "EU AI Act Art.11", description: "Technical documentation complete" },
  { checkId: 28, category: "EU_AI_ACT", weight: 0.8, reference: "EU AI Act Art.12", description: "Record-keeping / logging" },
  { checkId: 29, category: "EU_AI_ACT", weight: 0.9, reference: "EU AI Act Art.13", description: "Transparency to deployers" },
  { checkId: 30, category: "EU_AI_ACT", weight: 1.0, reference: "EU AI Act Art.14", description: "Human oversight measures" },
  { checkId: 31, category: "EU_AI_ACT", weight: 0.9, reference: "EU AI Act Art.15", description: "Accuracy / robustness / cybersecurity" },
  { checkId: 32, category: "EU_AI_ACT", weight: 0.8, reference: "EU AI Act Art.17", description: "Quality-management system" },

  // ── Security / cryptographic posture (33–40) ──
  { checkId: 33, category: "SECURITY", weight: 1.0, reference: "NIST PQC",        description: "Post-quantum signature (Dilithium) valid" },
  { checkId: 34, category: "SECURITY", weight: 0.9, reference: "NIST PQC",        description: "SPHINCS+ secondary signature valid" },
  { checkId: 35, category: "SECURITY", weight: 1.0, reference: "FIPS 140-3",      description: "HSM key custody verified" },
  { checkId: 36, category: "SECURITY", weight: 1.0, reference: "SHA-3-256",       description: "Model binary hash matches registry" },
  { checkId: 37, category: "SECURITY", weight: 0.9, reference: "PROV-ML",         description: "Provenance lineage intact" },
  { checkId: 38, category: "SECURITY", weight: 0.8, reference: "QKD",             description: "Key-distribution channel attested" },
  { checkId: 39, category: "SECURITY", weight: 1.0, reference: "Zero-Trust",      description: "Token TTL + scope enforced" },
  { checkId: 40, category: "SECURITY", weight: 0.9, reference: "BFT",             description: "Witness-node consensus reachable" },

  // ── Operational / lifecycle (41–47) ──
  { checkId: 41, category: "LIFECYCLE", weight: 0.8, reference: "MLOps",          description: "Calibration dataset registered" },
  { checkId: 42, category: "LIFECYCLE", weight: 0.8, reference: "MLOps",          description: "Bias-audit within due date" },
  { checkId: 43, category: "LIFECYCLE", weight: 0.7, reference: "MLOps",          description: "Drift monitoring active (JSD)" },
  { checkId: 44, category: "LIFECYCLE", weight: 0.7, reference: "MLOps",          description: "Rollback path defined" },
  { checkId: 45, category: "LIFECYCLE", weight: 0.9, reference: "Incident",       description: "Incident-response runbook linked" },
  { checkId: 46, category: "LIFECYCLE", weight: 0.8, reference: "DUO",            description: "DUO ontology tag assigned" },
  { checkId: 47, category: "LIFECYCLE", weight: 1.0, reference: "Sovereign Kill", description: "Hardware kill-switch reachable" },
];

/** Co = Σ(wᵢ × passᵢ) / Σwᵢ — weighted compliance over the 47-check catalogue. */
export function computeMFCMCompliance(checks: MFCMCheck[]): number {
  if (checks.length === 0) return 0;
  const totalWeight  = checks.reduce((s, c) => s + c.weight, 0);
  const passedWeight = checks.filter(c => c.passed).reduce((s, c) => s + c.weight, 0);
  return totalWeight > 0 ? passedWeight / totalWeight : 0;
}

/** Build a 47-check result set from a predicate over the catalogue. */
export function evaluateMFCM(predicate: (entry: MFCMCatalogEntry) => boolean): {
  checks: MFCMCheck[]; compliance: number; failed: MFCMCatalogEntry[];
} {
  const checks: MFCMCheck[] = MFCM_CATALOG.map(e => ({
    checkId: e.checkId, category: e.category, weight: e.weight,
    reference: e.reference, passed: predicate(e),
  }));
  const failed = MFCM_CATALOG.filter((e, i) => !checks[i].passed);
  return { checks, compliance: computeMFCMCompliance(checks), failed };
}

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 6 · FAIRNESS — DI & SPD derived from confusion matrices (COMPLETED)
// DI  = min(positiveRateₐ, positiveR_b) / max(positiveRateₐ, positiveRate_b)
// SPD = positiveRate_unprivileged − positiveRate_privileged
// ─────────────────────────────────────────────────────────────────────────────

export interface GroupOutcome {
  group:           string;   // e.g. "privileged" | "unprivileged" | demographic
  favorableCount:  number;   // positive/approved outcomes
  totalCount:      number;
}

export function positiveRate(g: GroupOutcome): number {
  return g.totalCount > 0 ? g.favorableCount / g.totalCount : 0;
}

/** Disparate Impact ratio across ≥2 groups — [0,1], 1.0 = perfect parity. */
export function computeDisparateImpact(groups: GroupOutcome[]): number {
  if (groups.length < 2) return 1.0;
  const rates = groups.map(positiveRate);
  const maxR = Math.max(...rates);
  const minR = Math.min(...rates);
  return maxR === 0 ? 1.0 : minR / maxR;
}

/** Statistical Parity Difference — unprivileged minus privileged positive rates. */
export function computeSPD(privileged: GroupOutcome, unprivileged: GroupOutcome): number {
  return positiveRate(unprivileged) - positiveRate(privileged);
}

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 7 · DIMENSION 6 — SOCIETAL IMPACT via H-OS-56 (COMPLETED)
// I = normalised benefit-weighted entropy over 56 harm/benefit-outcome states.
// 56 = 8 outcome-sectors × 7 severity bands (HO-OS = Harm/benefit Outcome —
// Outcome Sector). Fed by BFT-consensus weights and SAHRC harm flags.
// ─────────────────────────────────────────────────────────────────────────────

export const HOS56_SECTORS = [
  "EMPLOYMENT", "HEALTH", "JUSTICE", "FINANCE",
  "EDUCATION", "PRIVACY", "SECURITY", "ENVIRONMENT",
] as const;            // 8 outcome sectors

export const HOS56_SEVERITY_BANDS = [
  "CATASTROPHIC", "SEVERE", "MODERATE", "NEUTRAL",
  "BENEFICIAL", "STRONGLY_BENEFICIAL", "TRANSFORMATIVE",
] as const;            // 7 severity bands → 8 × 7 = 56 combinations

// Severity → signed valence in [-1, +1] (harm negative, benefit positive)
const SEVERITY_VALENCE: Record<string, number> = {
  CATASTROPHIC:        -1.0,
  SEVERE:              -0.66,
  MODERATE:            -0.33,
  NEUTRAL:              0.0,
  BENEFICIAL:           0.33,
  STRONGLY_BENEFICIAL:  0.66,
  TRANSFORMATIVE:       1.0,
};

export interface HOS56Cell {
  sector:   typeof HOS56_SECTORS[number];
  band:     typeof HOS56_SEVERITY_BANDS[number];
  weight:   number;     // BFT-consensus probability mass for this cell [0,1]
  sahrcFlag?: boolean;  // SAHRC harm flag — forces severe treatment
}

/**
 * Societal Impact I ∈ [0,1].
 * Combines (a) benefit-weighted valence across the 56-cell grid and
 * (b) an entropy penalty for dispersed/uncertain impact, then maps to [0,1].
 * A SAHRC flag on any cell caps the contribution of that cell at harm.
 */
export function computeSocietalImpact(cells: HOS56Cell[]): {
  societalImpact: number; valence: number; entropy: number; sahrcFlagged: boolean;
} {
  if (cells.length === 0) return { societalImpact: 0.5, valence: 0, entropy: 0, sahrcFlagged: false };

  const totalWeight = cells.reduce((s, c) => s + c.weight, 0) || 1;
  let valence = 0;
  let entropy = 0;
  let sahrcFlagged = false;

  for (const cell of cells) {
    const p = cell.weight / totalWeight;
    let v = SEVERITY_VALENCE[cell.band] ?? 0;
    if (cell.sahrcFlag) { v = Math.min(v, -0.66); sahrcFlagged = true; } // force severe harm
    valence += p * v;
    if (p > 0) entropy += -p * Math.log2(p);
  }

  // Normalise entropy by max possible (log2 of 56 cells)
  const maxEntropy = Math.log2(HOS56_SECTORS.length * HOS56_SEVERITY_BANDS.length);
  const normEntropy = maxEntropy > 0 ? entropy / maxEntropy : 0;

  // Map signed valence [-1,1] → [0,1], then penalise by dispersion uncertainty.
  const baseImpact = (valence + 1) / 2;
  const societalImpact = Math.max(0, Math.min(1, baseImpact * (1 - 0.25 * normEntropy)));

  return { societalImpact, valence, entropy: normEntropy, sahrcFlagged };
}

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 8 · CMAG — ETHICAL COOPERATION SCORE (COMPLETED)
// ECS = Cooperation × Autonomy × Integrity × Fairness  (Claim 8)
// Multi-agent arbitration: CONSENSUS / DISPUTE / ESCALATE_IGA
// ─────────────────────────────────────────────────────────────────────────────

export interface CMAGAgentVote {
  agentId:     string;
  cooperation: number;  // [0,1] willingness to align with peers
  autonomy:    number;  // [0,1] preserved human autonomy in this agent's path
  integrity:   number;  // [0,1] provenance + data integrity
  fairness:    number;  // [0,1] cross-group fairness for this agent
}

/**
 * Aggregate multi-agent votes into a single CMAG score.
 * ECS = C × A × I × F (geometric coupling — any zero collapses cooperation).
 * Arbitration: tight agreement → CONSENSUS; wide spread → DISPUTE/ESCALATE.
 */
export function computeCMAG(votes: CMAGAgentVote[]): CMAGScore {
  if (votes.length === 0) {
    return { cooperation: 0, autonomy: 0, integrity: 0, fairness: 0, ecs: 0,
             arbitration: CMAGArbitration.ESCALATE_IGA };
  }

  const mean = (xs: number[]) => xs.reduce((a, b) => a + b, 0) / xs.length;
  const cooperation = mean(votes.map(v => v.cooperation));
  const autonomy    = mean(votes.map(v => v.autonomy));
  const integrity   = mean(votes.map(v => v.integrity));
  const fairness    = mean(votes.map(v => v.fairness));

  const ecs = cooperation * autonomy * integrity * fairness;

  // Arbitration based on inter-agent cooperation variance
  const coopValues = votes.map(v => v.cooperation);
  const coopMean   = mean(coopValues);
  const variance   = mean(coopValues.map(c => (c - coopMean) ** 2));
  const spread     = Math.sqrt(variance);

  let arbitration: CMAGArbitration;
  if (spread < 0.10)      arbitration = CMAGArbitration.CONSENSUS;
  else if (spread < 0.25) arbitration = CMAGArbitration.DISPUTE;
  else                    arbitration = CMAGArbitration.ESCALATE_IGA;

  return { cooperation, autonomy, integrity, fairness, ecs, arbitration };
}

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 9 · DIMENSION 1 — VALIDITY
// V = validity(prediction, ground_truth) — accuracy-style fidelity in [0,1]
// ─────────────────────────────────────────────────────────────────────────────

export function computeValidity(correct: number, total: number): number {
  return total > 0 ? Math.max(0, Math.min(1, correct / total)) : 0;
}

// ════════════════════════════════════════════════════════════════════════════
// (Section 10 — the EVA scoring core + engine class — continues in part 2)
// ════════════════════════════════════════════════════════════════════════════

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 10 · EVA SCORING CORE — wires all six computed dimensions
// SVS = w₁V + w₂Cf + w₃(1−R) + w₄Co + w₅S + w₆I
// Hardware-equivalent BLOCK overrides applied before the soft decision.
// ─────────────────────────────────────────────────────────────────────────────

/** Raw evidence fed to the EVA engine — every dimension computed, not assumed. */
export interface EVAEvidence {
  modelId:   string;
  riskTier:  RiskTier;

  // Dimension 1 — Validity
  validityCorrect: number;
  validityTotal:   number;

  // Dimension 2 — Confidence (raw + temperature)
  rawConfidence: number;
  temperature:   number;

  // Dimension 4 — Compliance (predicate over MFCM catalogue)
  mfcmPredicate: (entry: MFCMCatalogEntry) => boolean;

  // Dimension 5 — Stability (distributions for JSD)
  currentDist:  number[];
  baselineDist: number[];

  // Dimension 6 — Societal impact (H-OS-56 grid)
  hos56Cells: HOS56Cell[];

  // Fairness — confusion-matrix group outcomes
  privilegedGroup:   GroupOutcome;
  unprivilegedGroup: GroupOutcome;
  fairnessGroups?:   GroupOutcome[];   // ≥2 for DI; defaults to the two above

  // CMAG — multi-agent ethical votes
  cmagVotes: CMAGAgentVote[];
}

/** Full EVA evaluation from raw evidence — the completed pipeline. */
export function evaluateEVA(
  ev: EVAEvidence,
  coefficients: EVACoefficients = SA_DEFAULT_COEFFICIENTS,
  thresholds:   EVAThresholds   = DEFAULT_THRESHOLDS,
): EVAScore {
  const startTime = Date.now();

  // Validate coefficient sum = 1.0
  const coeffSum = Object.values(coefficients).reduce((a, b) => a + b, 0);
  if (Math.abs(coeffSum - 1.0) > 0.001) {
    throw new Error(`EVA: Coefficient sum ${coeffSum.toFixed(4)} ≠ 1.000`);
  }

  // ── Compute all six dimensions ──
  const validity   = computeValidity(ev.validityCorrect, ev.validityTotal);
  const confidence = scaleConfidenceByTemperature(ev.rawConfidence, ev.temperature);
  const risk       = RISK_TIER_R[ev.riskTier];
  const { compliance } = evaluateMFCM(ev.mfcmPredicate);
  const { stability, jsd } = computeStability(ev.currentDist, ev.baselineDist);
  const { societalImpact } = computeSocietalImpact(ev.hos56Cells);

  // ── Fairness metrics ──
  const fairnessGroups = ev.fairnessGroups ?? [ev.privilegedGroup, ev.unprivilegedGroup];
  const disparateImpact = computeDisparateImpact(fairnessGroups);
  const spd             = computeSPD(ev.privilegedGroup, ev.unprivilegedGroup);

  // ── CMAG ethical cooperation ──
  const cmag = computeCMAG(ev.cmagVotes);
  const ecs  = cmag.ecs;

  // ── MANDATORY BLOCK OVERRIDES (hardware-equivalent) ──
  const blockReasons: string[] = [];
  if (risk >= thresholds.riskBlock)
    blockReasons.push(`R=${risk.toFixed(3)} ≥ ${thresholds.riskBlock} (Risk threshold)`);
  if (compliance < thresholds.complianceBlock)
    blockReasons.push(`Co=${compliance.toFixed(3)} < ${thresholds.complianceBlock} (Compliance failure)`);
  if (disparateImpact < thresholds.disparateImpactBlock)
    blockReasons.push(`DI=${disparateImpact.toFixed(3)} < ${thresholds.disparateImpactBlock} (Disparate impact — SA NAIFP)`);
  if (jsd > thresholds.jsdBlock)
    blockReasons.push(`JSD=${jsd.toFixed(3)} > ${thresholds.jsdBlock} (Distribution drift)`);
  if (ecs < thresholds.ecsBlock)
    blockReasons.push(`ECS=${ecs.toFixed(3)} < ${thresholds.ecsBlock} (Ethical cooperation failure — CMAG)`);
  if (Math.abs(spd) > thresholds.spdBlock)
    blockReasons.push(`|SPD|=${Math.abs(spd).toFixed(3)} > ${thresholds.spdBlock} (Statistical parity — SAHRC)`);
  if (ev.riskTier === RiskTier.UNACCEPTABLE)
    blockReasons.push("UNACCEPTABLE risk tier — permanent block (SA NAIFP)");
  if (cmag.arbitration === CMAGArbitration.ESCALATE_IGA)
    blockReasons.push("CMAG arbitration ESCALATE_IGA — inter-agent dispute unresolved");

  // ── Weighted SVS aggregate ──
  const svsRaw =
    coefficients.wValidity       * validity +
    coefficients.wConfidence     * confidence +
    coefficients.wRisk           * (1 - risk) +     // inverse: low risk → high score
    coefficients.wCompliance     * compliance +
    coefficients.wStability      * stability +
    coefficients.wSocietalImpact * societalImpact;
  const svs = Math.min(Math.max(svsRaw, 0), 1);

  // ── Decision ──
  let decision: GovernanceDecision;
  if (blockReasons.length > 0)                          decision = GovernanceDecision.BLOCK;
  else if (cmag.arbitration === CMAGArbitration.DISPUTE) decision = GovernanceDecision.ESCALATE;
  else if (risk >= 0.6 || compliance < 0.80)            decision = GovernanceDecision.REVIEW;
  else if (risk >= 0.5)                                 decision = GovernanceDecision.RESTRICT;
  else                                                  decision = GovernanceDecision.APPROVE;

  return {
    validity, confidence, risk, compliance, stability, societalImpact,
    svs, jsd, disparateImpact, spd, ecs, cmag,
    decision, blockReasons,
    computedAt: new Date(), latencyMs: Date.now() - startTime,
  };
}

// ── Formula reference (Part 7.1) ──
export const EVAFormulas = {
  validity:       "V  = correct / total",
  confidence:     "Cf = confidence_raw / (1 + ln(T + 1))",
  risk:           "R  = RiskTierMap[tier]",
  compliance:     "Co = Σ(wᵢ × MFCMᵢ) / Σwᵢ   [47 checks]",
  stability:      "S  = 1 − JSD(current ‖ baseline)",
  societalImpact: "I  = H-OS-56(valence, entropy, SAHRC flags)",
  disparateImpact:"DI = min(groupRates) / max(groupRates)",
  spd:            "SPD = posRate(unpriv) − posRate(priv)",
  ecs:            "ECS = Cooperation × Autonomy × Integrity × Fairness",
  svs:            "SVS = w₁V + w₂Cf + w₃(1−R) + w₄Co + w₅S + w₆I",
  block:          "BLOCK if R≥0.80 | Co<0.70 | DI<0.80 | JSD>0.40 | ECS<0.65 | |SPD|>0.05 | tier=UNACCEPTABLE",
};

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 11 · EVA ENGINE CLASS — hot-reload, profiles, evaluation
// ─────────────────────────────────────────────────────────────────────────────

export class EVAEngine {
  private coefficients: EVACoefficients;
  private thresholds:   EVAThresholds;

  constructor(coefficients = SA_DEFAULT_COEFFICIENTS, thresholds = DEFAULT_THRESHOLDS) {
    this.coefficients = { ...coefficients };
    this.thresholds   = { ...thresholds };
  }

  /** Hot-reload coefficients (<5ms target). Validates Σ = 1.0. */
  hotReload(coefficients: Partial<EVACoefficients>): void {
    this.coefficients = { ...this.coefficients, ...coefficients };
    const sum = Object.values(this.coefficients).reduce((a, b) => a + b, 0);
    if (Math.abs(sum - 1.0) > 0.001) {
      throw new Error(`EVA hot-reload: coefficient sum ${sum.toFixed(4)} ≠ 1.000`);
    }
  }

  updateThresholds(thresholds: Partial<EVAThresholds>): void {
    this.thresholds = { ...this.thresholds, ...thresholds };
  }

  evaluate(evidence: EVAEvidence): EVAScore {
    return evaluateEVA(evidence, this.coefficients, this.thresholds);
  }

  applyMilitaryProfile():   void { this.coefficients = { ...MILITARY_COEFFICIENTS }; }
  applyHealthcareProfile(): void { this.coefficients = { ...HEALTHCARE_COEFFICIENTS }; }
  resetToSADefaults():      void {
    this.coefficients = { ...SA_DEFAULT_COEFFICIENTS };
    this.thresholds   = { ...DEFAULT_THRESHOLDS };
  }

  getCoefficients(): Readonly<EVACoefficients> { return { ...this.coefficients }; }
  getThresholds():   Readonly<EVAThresholds>   { return { ...this.thresholds }; }
}

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 11.5 · HARDENED SCORING — tamper-evident, signed EVA verdicts
// For scale + deployment: every EVA verdict is sealed with an HMAC over its full
// score vector, so the UDOC orchestrator (and any downstream system) can verify the
// score was produced by this engine and not forged or mutated in transit.
//
// PRODUCTION: the sovereign key is injected from a TPM/Secure Enclave; in the Rust
// data-plane port this becomes a BLAKE3 keyed hash computed in constant time with no
// heap allocation, and the sealed verdict is what the eBPF/XDP layer checks before it
// will pass an AI request's packets. A missing or invalid seal ⇒ XDP_DROP.
// ─────────────────────────────────────────────────────────────────────────────

/** EVA engine signing key. Production: hardware TPM, never in source. */
export const EVA_SOVEREIGN_KEY: Buffer = randomBytes(32);

export interface SealedEVAScore {
  score: EVAScore;
  seal: string;        // HMAC-SHA256 over the canonical score vector
  engineId: string;
}

const EVA_ENGINE_ID = "ZA-EVA-ENGINE-01";

/** Canonical serialisation of the score vector for signing (stable field order). */
function canonicaliseScore(s: EVAScore): string {
  return [
    s.validity, s.confidence, s.risk, s.compliance, s.stability, s.societalImpact,
    s.svs, s.jsd, s.disparateImpact, s.spd, s.ecs, s.decision,
  ].map(v => (typeof v === "number" ? v.toFixed(6) : String(v))).join("|");
}

/** Evaluate AND seal — returns a tamper-evident verdict. */
export function evaluateEVASealed(
  ev: EVAEvidence,
  coefficients: EVACoefficients = SA_DEFAULT_COEFFICIENTS,
  thresholds: EVAThresholds = DEFAULT_THRESHOLDS,
): SealedEVAScore {
  const score = evaluateEVA(ev, coefficients, thresholds);
  const seal = createHmac("sha256", EVA_SOVEREIGN_KEY)
    .update(`${EVA_ENGINE_ID}:${canonicaliseScore(score)}`).digest("hex");
  return { score, seal, engineId: EVA_ENGINE_ID };
}

/** Verify a sealed verdict (constant-time). Returns false on any mutation. */
export function verifyEVASeal(sealed: SealedEVAScore): boolean {
  const expected = createHmac("sha256", EVA_SOVEREIGN_KEY)
    .update(`${sealed.engineId}:${canonicaliseScore(sealed.score)}`).digest("hex");
  const a = Buffer.from(sealed.seal), b = Buffer.from(expected);
  if (a.length !== b.length) return false;
  return timingSafeEqual(a, b);
}

// ─────────────────────────────────────────────────────────────────────────────
// SECTION 12 · RUNNABLE DEMO HARNESS
// Run:  npx ts-node eva-engine-complete.ts
// ─────────────────────────────────────────────────────────────────────────────

function demo(): void {
  const engine = new EVAEngine();
  const line = "─".repeat(72);

  const print = (title: string, s: EVAScore) => {
    console.log(line);
    console.log(`SCENARIO: ${title}`);
    console.log(line);
    console.log(`  V=${s.validity.toFixed(3)}  Cf=${s.confidence.toFixed(3)}  R=${s.risk.toFixed(3)}  ` +
                `Co=${s.compliance.toFixed(3)}  S=${s.stability.toFixed(3)}  I=${s.societalImpact.toFixed(3)}`);
    console.log(`  JSD=${s.jsd.toFixed(3)}  DI=${s.disparateImpact.toFixed(3)}  SPD=${s.spd.toFixed(3)}  ` +
                `ECS=${s.ecs.toFixed(3)} (${s.cmag.arbitration})`);
    console.log(`  SVS=${s.svs.toFixed(3)}  →  DECISION: ${s.decision}   [${s.latencyMs}ms]`);
    if (s.blockReasons.length) {
      console.log(`  BLOCK REASONS:`);
      s.blockReasons.forEach(r => console.log(`    • ${r}`));
    }
    console.log();
  };

  // ── Scenario A: healthy model → APPROVE ──
  print("Healthy compliant model", engine.evaluate({
    modelId: "model-healthy-001", riskTier: RiskTier.NOTABLE,
    validityCorrect: 950, validityTotal: 1000,
    rawConfidence: 0.92, temperature: 0.7,
    mfcmPredicate: () => true,                       // all 47 pass
    currentDist:  [0.25, 0.25, 0.25, 0.25],
    baselineDist: [0.24, 0.26, 0.25, 0.25],
    hos56Cells: [
      { sector: "EMPLOYMENT", band: "STRONGLY_BENEFICIAL", weight: 0.5 },
      { sector: "EDUCATION",  band: "BENEFICIAL",          weight: 0.5 },
    ],
    privilegedGroup:   { group: "priv",   favorableCount: 480, totalCount: 1000 },
    unprivilegedGroup: { group: "unpriv", favorableCount: 470, totalCount: 1000 },
    cmagVotes: [
      { agentId: "A", cooperation: 0.92, autonomy: 0.95, integrity: 0.94, fairness: 0.93 },
      { agentId: "B", cooperation: 0.90, autonomy: 0.93, integrity: 0.95, fairness: 0.92 },
      { agentId: "C", cooperation: 0.91, autonomy: 0.94, integrity: 0.93, fairness: 0.94 },
    ],
  }));

  // ── Scenario B: biased model → BLOCK on DI/SPD ──
  print("Biased hiring model (disparate impact)", engine.evaluate({
    modelId: "model-biased-002", riskTier: RiskTier.HIGH,
    validityCorrect: 880, validityTotal: 1000,
    rawConfidence: 0.85, temperature: 1.0,
    mfcmPredicate: (e) => e.checkId !== 12,          // fails NAIFP disparate-impact check
    currentDist:  [0.25, 0.25, 0.25, 0.25],
    baselineDist: [0.25, 0.25, 0.25, 0.25],
    hos56Cells: [
      { sector: "EMPLOYMENT", band: "SEVERE", weight: 0.6, sahrcFlag: true },
      { sector: "FINANCE",    band: "MODERATE", weight: 0.4 },
    ],
    privilegedGroup:   { group: "priv",   favorableCount: 600, totalCount: 1000 },
    unprivilegedGroup: { group: "unpriv", favorableCount: 300, totalCount: 1000 },
    cmagVotes: [
      { agentId: "A", cooperation: 0.80, autonomy: 0.85, integrity: 0.88, fairness: 0.55 },
      { agentId: "B", cooperation: 0.78, autonomy: 0.82, integrity: 0.86, fairness: 0.50 },
      { agentId: "C", cooperation: 0.81, autonomy: 0.84, integrity: 0.87, fairness: 0.58 },
    ],
  }));

  // ── Scenario C: drifted model → BLOCK on JSD ──
  print("Drifted model (distribution shift)", engine.evaluate({
    modelId: "model-drift-003", riskTier: RiskTier.MEDIUM,
    validityCorrect: 700, validityTotal: 1000,
    rawConfidence: 0.70, temperature: 2.0,
    mfcmPredicate: () => true,
    currentDist:  [0.85, 0.05, 0.05, 0.05],          // heavy drift
    baselineDist: [0.25, 0.25, 0.25, 0.25],
    hos56Cells: [{ sector: "HEALTH", band: "NEUTRAL", weight: 1.0 }],
    privilegedGroup:   { group: "priv",   favorableCount: 500, totalCount: 1000 },
    unprivilegedGroup: { group: "unpriv", favorableCount: 490, totalCount: 1000 },
    cmagVotes: [
      { agentId: "A", cooperation: 0.85, autonomy: 0.88, integrity: 0.90, fairness: 0.86 },
      { agentId: "B", cooperation: 0.84, autonomy: 0.87, integrity: 0.89, fairness: 0.85 },
    ],
  }));

  // ── Scenario D: unacceptable tier → permanent BLOCK ──
  print("Prohibited use-case (UNACCEPTABLE tier)", engine.evaluate({
    modelId: "model-prohibited-004", riskTier: RiskTier.UNACCEPTABLE,
    validityCorrect: 999, validityTotal: 1000,
    rawConfidence: 0.99, temperature: 0.5,
    mfcmPredicate: () => true,
    currentDist:  [0.25, 0.25, 0.25, 0.25],
    baselineDist: [0.25, 0.25, 0.25, 0.25],
    hos56Cells: [{ sector: "JUSTICE", band: "CATASTROPHIC", weight: 1.0, sahrcFlag: true }],
    privilegedGroup:   { group: "priv",   favorableCount: 500, totalCount: 1000 },
    unprivilegedGroup: { group: "unpriv", favorableCount: 500, totalCount: 1000 },
    cmagVotes: [
      { agentId: "A", cooperation: 0.95, autonomy: 0.10, integrity: 0.95, fairness: 0.95 },
    ],
  }));

  console.log(line);
  console.log("EVA FORMULAE");
  console.log(line);
  Object.entries(EVAFormulas).forEach(([k, v]) => console.log(`  ${k.padEnd(16)} ${v}`));
  console.log(line);
  console.log(`MFCM CATALOGUE: ${MFCM_CATALOG.length} checks across ` +
              `${new Set(MFCM_CATALOG.map(c => c.category)).size} categories`);
  console.log(`H-OS-56 GRID:   ${HOS56_SECTORS.length} sectors × ${HOS56_SEVERITY_BANDS.length} bands = ` +
              `${HOS56_SECTORS.length * HOS56_SEVERITY_BANDS.length} cells`);
  console.log(line);

  // ── HARDENED SEALED-VERDICT DEMO ──
  console.log("");
  console.log(line);
  console.log("HARDENED EVA — tamper-evident sealed verdicts");
  console.log(line);
  const sealed = evaluateEVASealed({
    modelId: "model-001",
    riskTier: RiskTier.NOTABLE, validityCorrect: 950, validityTotal: 1000,
    rawConfidence: 0.92, temperature: 0.7, mfcmPredicate: () => true,
    currentDist: [0.25,0.25,0.25,0.25], baselineDist: [0.24,0.26,0.25,0.25],
    hos56Cells: [{ sector: "EMPLOYMENT", band: "STRONGLY_BENEFICIAL", weight: 0.5 },
                 { sector: "EDUCATION", band: "BENEFICIAL", weight: 0.5 }],
    privilegedGroup:   { group: "priv",   favorableCount: 480, totalCount: 1000 },
    unprivilegedGroup: { group: "unpriv", favorableCount: 470, totalCount: 1000 },
    cmagVotes: [{ agentId: "A", cooperation: 0.92, autonomy: 0.95, integrity: 0.94, fairness: 0.93 }],
  });
  console.log(`  Verdict   : ${sealed.score.decision}  (SVS ${sealed.score.svs.toFixed(3)})`);
  console.log(`  Seal      : ${sealed.seal.slice(0, 48)}…`);
  console.log(`  Verify    : ${verifyEVASeal(sealed) ? "VALID ✓" : "INVALID"}`);
  // Tamper: flip the decision after sealing → verification must fail.
  const forged: SealedEVAScore = { ...sealed, score: { ...sealed.score, decision: GovernanceDecision.APPROVE, risk: 0.01 } };
  console.log(`  Tampered  : ${verifyEVASeal(forged) ? "VALID (BAD!)" : "INVALID ✓ — forgery detected"}`);
  console.log(line);
}

// Execute demo when run directly
demo();
