"use strict";
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
Object.defineProperty(exports, "__esModule", { value: true });
exports.EVA_SOVEREIGN_KEY = exports.EVAEngine = exports.EVAFormulas = exports.HOS56_SEVERITY_BANDS = exports.HOS56_SECTORS = exports.MFCM_CATALOG = exports.RISK_TIER_R = exports.DEFAULT_THRESHOLDS = exports.HEALTHCARE_COEFFICIENTS = exports.MILITARY_COEFFICIENTS = exports.SA_DEFAULT_COEFFICIENTS = exports.CMAGArbitration = exports.RiskTier = exports.GovernanceDecision = void 0;
exports.computeJSD = computeJSD;
exports.computeStability = computeStability;
exports.scaleConfidenceByTemperature = scaleConfidenceByTemperature;
exports.computeMFCMCompliance = computeMFCMCompliance;
exports.evaluateMFCM = evaluateMFCM;
exports.positiveRate = positiveRate;
exports.computeDisparateImpact = computeDisparateImpact;
exports.computeSPD = computeSPD;
exports.computeSocietalImpact = computeSocietalImpact;
exports.computeCMAG = computeCMAG;
exports.computeValidity = computeValidity;
exports.evaluateEVA = evaluateEVA;
exports.evaluateEVASealed = evaluateEVASealed;
exports.verifyEVASeal = verifyEVASeal;
const node_crypto_1 = require("node:crypto");
// ─────────────────────────────────────────────────────────────────────────────
// SECTION 1 · TYPES (self-contained — mirrors @udoc/types contracts)
// ─────────────────────────────────────────────────────────────────────────────
var GovernanceDecision;
(function (GovernanceDecision) {
    GovernanceDecision["APPROVE"] = "APPROVE";
    GovernanceDecision["BLOCK"] = "BLOCK";
    GovernanceDecision["REVIEW"] = "REVIEW";
    GovernanceDecision["RESTRICT"] = "RESTRICT";
    GovernanceDecision["ESCALATE"] = "ESCALATE";
})(GovernanceDecision || (exports.GovernanceDecision = GovernanceDecision = {}));
var RiskTier;
(function (RiskTier) {
    RiskTier["MINIMAL"] = "MINIMAL";
    RiskTier["NOTABLE"] = "NOTABLE";
    RiskTier["MEDIUM"] = "MEDIUM";
    RiskTier["HIGH"] = "HIGH";
    RiskTier["UNACCEPTABLE"] = "UNACCEPTABLE";
})(RiskTier || (exports.RiskTier = RiskTier = {}));
var CMAGArbitration;
(function (CMAGArbitration) {
    CMAGArbitration["CONSENSUS"] = "CONSENSUS";
    CMAGArbitration["DISPUTE"] = "DISPUTE";
    CMAGArbitration["ESCALATE_IGA"] = "ESCALATE_IGA";
})(CMAGArbitration || (exports.CMAGArbitration = CMAGArbitration = {}));
// ─────────────────────────────────────────────────────────────────────────────
// SECTION 2 · CONSTANTS — coefficients, thresholds, tier mapping
// ─────────────────────────────────────────────────────────────────────────────
// SA NAIFP-aligned default coefficients (Σ = 1.0)
exports.SA_DEFAULT_COEFFICIENTS = {
    wValidity: 0.15,
    wConfidence: 0.15,
    wRisk: 0.25,
    wCompliance: 0.20,
    wStability: 0.10,
    wSocietalImpact: 0.15,
};
// Military profile — risk-dominant (Σ = 1.0)
exports.MILITARY_COEFFICIENTS = {
    wValidity: 0.10,
    wConfidence: 0.10,
    wRisk: 0.40,
    wCompliance: 0.20,
    wStability: 0.10,
    wSocietalImpact: 0.10,
};
// Healthcare profile — compliance + societal dominant (Σ = 1.0)
exports.HEALTHCARE_COEFFICIENTS = {
    wValidity: 0.15,
    wConfidence: 0.10,
    wRisk: 0.20,
    wCompliance: 0.25,
    wStability: 0.10,
    wSocietalImpact: 0.20,
};
exports.DEFAULT_THRESHOLDS = {
    riskBlock: 0.80,
    complianceBlock: 0.70,
    disparateImpactBlock: 0.80,
    jsdBlock: 0.40,
    ecsBlock: 0.65,
    spdBlock: 0.05,
};
exports.RISK_TIER_R = {
    [RiskTier.MINIMAL]: 0.0,
    [RiskTier.NOTABLE]: 0.2,
    [RiskTier.MEDIUM]: 0.5,
    [RiskTier.HIGH]: 0.8,
    [RiskTier.UNACCEPTABLE]: 1.0,
};
// ─────────────────────────────────────────────────────────────────────────────
// SECTION 3 · DIMENSION 5 — STABILITY via Jensen-Shannon Divergence
// S = 1 − JSD(current ‖ baseline)
// ─────────────────────────────────────────────────────────────────────────────
/** KL divergence with zero-guard (bits). */
function klDivergence(p, q) {
    return p.reduce((sum, pi, i) => {
        if (pi === 0)
            return sum;
        const qi = q[i] === 0 ? 1e-10 : q[i];
        return sum + pi * Math.log2(pi / qi);
    }, 0);
}
/** Jensen-Shannon Divergence — symmetric, bounded [0,1] in bits. */
function computeJSD(currentDist, baselineDist) {
    if (currentDist.length !== baselineDist.length) {
        throw new Error("EVA-JSD: Distribution length mismatch");
    }
    const M = currentDist.map((p, i) => (p + baselineDist[i]) / 2);
    return 0.5 * klDivergence(currentDist, M) + 0.5 * klDivergence(baselineDist, M);
}
/** Stability dimension: higher = more stable (less drift). */
function computeStability(currentDist, baselineDist) {
    const jsd = computeJSD(currentDist, baselineDist);
    return { stability: Math.max(0, 1 - jsd), jsd };
}
// ─────────────────────────────────────────────────────────────────────────────
// SECTION 4 · DIMENSION 2 — CONFIDENCE with temperature scaling
// Cf = confidence_raw / (1 + ln(T + 1))     (Part 7.1)
// ─────────────────────────────────────────────────────────────────────────────
function scaleConfidenceByTemperature(rawConfidence, temperature) {
    if (temperature <= 0)
        return rawConfidence;
    return rawConfidence / (1 + Math.log(temperature + 1));
}
exports.MFCM_CATALOG = [
    // ── POPIA — Data Protection (1–10) ──
    { checkId: 1, category: "DATA_PROTECTION", weight: 1.0, reference: "POPIA s.4", description: "Lawful processing conditions met" },
    { checkId: 2, category: "DATA_PROTECTION", weight: 1.0, reference: "POPIA s.9", description: "Processing limitation — minimality" },
    { checkId: 3, category: "DATA_PROTECTION", weight: 1.0, reference: "POPIA s.10", description: "Consent / lawful basis recorded" },
    { checkId: 4, category: "DATA_PROTECTION", weight: 1.0, reference: "POPIA s.11", description: "Purpose specification documented" },
    { checkId: 5, category: "DATA_PROTECTION", weight: 0.8, reference: "POPIA s.13", description: "Retention limitation enforced" },
    { checkId: 6, category: "DATA_PROTECTION", weight: 1.0, reference: "POPIA s.18", description: "Data-subject notification given" },
    { checkId: 7, category: "DATA_PROTECTION", weight: 1.0, reference: "POPIA s.19", description: "Security safeguards (integrity/confidentiality)" },
    { checkId: 8, category: "DATA_PROTECTION", weight: 1.0, reference: "POPIA s.22", description: "Breach notification capability present" },
    { checkId: 9, category: "DATA_PROTECTION", weight: 0.9, reference: "POPIA s.71", description: "Automated decision-making safeguards" },
    { checkId: 10, category: "DATA_PROTECTION", weight: 1.0, reference: "POPIA s.72", description: "Cross-border transfer lawful (sovereignty)" },
    // ── SA NAIFP — National AI Framework Pillars (11–22) ──
    { checkId: 11, category: "NAIFP_FAIRNESS", weight: 1.0, reference: "NAIFP P1", description: "Fairness & non-discrimination" },
    { checkId: 12, category: "NAIFP_FAIRNESS", weight: 1.0, reference: "NAIFP P1", description: "Disparate-impact within tolerance" },
    { checkId: 13, category: "NAIFP_TRANSP", weight: 0.9, reference: "NAIFP P2", description: "Transparency & explainability" },
    { checkId: 14, category: "NAIFP_TRANSP", weight: 0.8, reference: "NAIFP P2", description: "Model card published" },
    { checkId: 15, category: "NAIFP_ACCOUNT", weight: 1.0, reference: "NAIFP P3", description: "Accountability — named operator" },
    { checkId: 16, category: "NAIFP_ACCOUNT", weight: 0.9, reference: "NAIFP P3", description: "Audit trail immutable (StayChain)" },
    { checkId: 17, category: "NAIFP_SAFETY", weight: 1.0, reference: "NAIFP P4", description: "Safety & robustness testing" },
    { checkId: 18, category: "NAIFP_SAFETY", weight: 1.0, reference: "NAIFP P4", description: "Adversarial robustness validated" },
    { checkId: 19, category: "NAIFP_PRIVACY", weight: 1.0, reference: "NAIFP P5", description: "Privacy-by-design verified" },
    { checkId: 20, category: "NAIFP_HUMAN", weight: 1.0, reference: "NAIFP P6", description: "Human oversight guaranteed" },
    { checkId: 21, category: "NAIFP_SOVEREIGN", weight: 1.0, reference: "NAIFP P7", description: "Data & compute sovereignty (ZA)" },
    { checkId: 22, category: "NAIFP_SOCIETAL", weight: 0.9, reference: "NAIFP P8", description: "Societal benefit demonstrated" },
    // ── EU AI Act overlay (23–32) ──
    { checkId: 23, category: "EU_AI_ACT", weight: 1.0, reference: "EU AI Act Art.5", description: "No prohibited practices" },
    { checkId: 24, category: "EU_AI_ACT", weight: 1.0, reference: "EU AI Act Art.6", description: "High-risk classification correct" },
    { checkId: 25, category: "EU_AI_ACT", weight: 0.9, reference: "EU AI Act Art.9", description: "Risk-management system in place" },
    { checkId: 26, category: "EU_AI_ACT", weight: 0.9, reference: "EU AI Act Art.10", description: "Data governance — training quality" },
    { checkId: 27, category: "EU_AI_ACT", weight: 0.8, reference: "EU AI Act Art.11", description: "Technical documentation complete" },
    { checkId: 28, category: "EU_AI_ACT", weight: 0.8, reference: "EU AI Act Art.12", description: "Record-keeping / logging" },
    { checkId: 29, category: "EU_AI_ACT", weight: 0.9, reference: "EU AI Act Art.13", description: "Transparency to deployers" },
    { checkId: 30, category: "EU_AI_ACT", weight: 1.0, reference: "EU AI Act Art.14", description: "Human oversight measures" },
    { checkId: 31, category: "EU_AI_ACT", weight: 0.9, reference: "EU AI Act Art.15", description: "Accuracy / robustness / cybersecurity" },
    { checkId: 32, category: "EU_AI_ACT", weight: 0.8, reference: "EU AI Act Art.17", description: "Quality-management system" },
    // ── Security / cryptographic posture (33–40) ──
    { checkId: 33, category: "SECURITY", weight: 1.0, reference: "NIST PQC", description: "Post-quantum signature (Dilithium) valid" },
    { checkId: 34, category: "SECURITY", weight: 0.9, reference: "NIST PQC", description: "SPHINCS+ secondary signature valid" },
    { checkId: 35, category: "SECURITY", weight: 1.0, reference: "FIPS 140-3", description: "HSM key custody verified" },
    { checkId: 36, category: "SECURITY", weight: 1.0, reference: "SHA-3-256", description: "Model binary hash matches registry" },
    { checkId: 37, category: "SECURITY", weight: 0.9, reference: "PROV-ML", description: "Provenance lineage intact" },
    { checkId: 38, category: "SECURITY", weight: 0.8, reference: "QKD", description: "Key-distribution channel attested" },
    { checkId: 39, category: "SECURITY", weight: 1.0, reference: "Zero-Trust", description: "Token TTL + scope enforced" },
    { checkId: 40, category: "SECURITY", weight: 0.9, reference: "BFT", description: "Witness-node consensus reachable" },
    // ── Operational / lifecycle (41–47) ──
    { checkId: 41, category: "LIFECYCLE", weight: 0.8, reference: "MLOps", description: "Calibration dataset registered" },
    { checkId: 42, category: "LIFECYCLE", weight: 0.8, reference: "MLOps", description: "Bias-audit within due date" },
    { checkId: 43, category: "LIFECYCLE", weight: 0.7, reference: "MLOps", description: "Drift monitoring active (JSD)" },
    { checkId: 44, category: "LIFECYCLE", weight: 0.7, reference: "MLOps", description: "Rollback path defined" },
    { checkId: 45, category: "LIFECYCLE", weight: 0.9, reference: "Incident", description: "Incident-response runbook linked" },
    { checkId: 46, category: "LIFECYCLE", weight: 0.8, reference: "DUO", description: "DUO ontology tag assigned" },
    { checkId: 47, category: "LIFECYCLE", weight: 1.0, reference: "Sovereign Kill", description: "Hardware kill-switch reachable" },
];
/** Co = Σ(wᵢ × passᵢ) / Σwᵢ — weighted compliance over the 47-check catalogue. */
function computeMFCMCompliance(checks) {
    if (checks.length === 0)
        return 0;
    const totalWeight = checks.reduce((s, c) => s + c.weight, 0);
    const passedWeight = checks.filter(c => c.passed).reduce((s, c) => s + c.weight, 0);
    return totalWeight > 0 ? passedWeight / totalWeight : 0;
}
/** Build a 47-check result set from a predicate over the catalogue. */
function evaluateMFCM(predicate) {
    const checks = exports.MFCM_CATALOG.map(e => ({
        checkId: e.checkId, category: e.category, weight: e.weight,
        reference: e.reference, passed: predicate(e),
    }));
    const failed = exports.MFCM_CATALOG.filter((e, i) => !checks[i].passed);
    return { checks, compliance: computeMFCMCompliance(checks), failed };
}
function positiveRate(g) {
    return g.totalCount > 0 ? g.favorableCount / g.totalCount : 0;
}
/** Disparate Impact ratio across ≥2 groups — [0,1], 1.0 = perfect parity. */
function computeDisparateImpact(groups) {
    if (groups.length < 2)
        return 1.0;
    const rates = groups.map(positiveRate);
    const maxR = Math.max(...rates);
    const minR = Math.min(...rates);
    return maxR === 0 ? 1.0 : minR / maxR;
}
/** Statistical Parity Difference — unprivileged minus privileged positive rates. */
function computeSPD(privileged, unprivileged) {
    return positiveRate(unprivileged) - positiveRate(privileged);
}
// ─────────────────────────────────────────────────────────────────────────────
// SECTION 7 · DIMENSION 6 — SOCIETAL IMPACT via H-OS-56 (COMPLETED)
// I = normalised benefit-weighted entropy over 56 harm/benefit-outcome states.
// 56 = 8 outcome-sectors × 7 severity bands (HO-OS = Harm/benefit Outcome —
// Outcome Sector). Fed by BFT-consensus weights and SAHRC harm flags.
// ─────────────────────────────────────────────────────────────────────────────
exports.HOS56_SECTORS = [
    "EMPLOYMENT", "HEALTH", "JUSTICE", "FINANCE",
    "EDUCATION", "PRIVACY", "SECURITY", "ENVIRONMENT",
]; // 8 outcome sectors
exports.HOS56_SEVERITY_BANDS = [
    "CATASTROPHIC", "SEVERE", "MODERATE", "NEUTRAL",
    "BENEFICIAL", "STRONGLY_BENEFICIAL", "TRANSFORMATIVE",
]; // 7 severity bands → 8 × 7 = 56 combinations
// Severity → signed valence in [-1, +1] (harm negative, benefit positive)
const SEVERITY_VALENCE = {
    CATASTROPHIC: -1.0,
    SEVERE: -0.66,
    MODERATE: -0.33,
    NEUTRAL: 0.0,
    BENEFICIAL: 0.33,
    STRONGLY_BENEFICIAL: 0.66,
    TRANSFORMATIVE: 1.0,
};
/**
 * Societal Impact I ∈ [0,1].
 * Combines (a) benefit-weighted valence across the 56-cell grid and
 * (b) an entropy penalty for dispersed/uncertain impact, then maps to [0,1].
 * A SAHRC flag on any cell caps the contribution of that cell at harm.
 */
function computeSocietalImpact(cells) {
    if (cells.length === 0)
        return { societalImpact: 0.5, valence: 0, entropy: 0, sahrcFlagged: false };
    const totalWeight = cells.reduce((s, c) => s + c.weight, 0) || 1;
    let valence = 0;
    let entropy = 0;
    let sahrcFlagged = false;
    for (const cell of cells) {
        const p = cell.weight / totalWeight;
        let v = SEVERITY_VALENCE[cell.band] ?? 0;
        if (cell.sahrcFlag) {
            v = Math.min(v, -0.66);
            sahrcFlagged = true;
        } // force severe harm
        valence += p * v;
        if (p > 0)
            entropy += -p * Math.log2(p);
    }
    // Normalise entropy by max possible (log2 of 56 cells)
    const maxEntropy = Math.log2(exports.HOS56_SECTORS.length * exports.HOS56_SEVERITY_BANDS.length);
    const normEntropy = maxEntropy > 0 ? entropy / maxEntropy : 0;
    // Map signed valence [-1,1] → [0,1], then penalise by dispersion uncertainty.
    const baseImpact = (valence + 1) / 2;
    const societalImpact = Math.max(0, Math.min(1, baseImpact * (1 - 0.25 * normEntropy)));
    return { societalImpact, valence, entropy: normEntropy, sahrcFlagged };
}
/**
 * Aggregate multi-agent votes into a single CMAG score.
 * ECS = C × A × I × F (geometric coupling — any zero collapses cooperation).
 * Arbitration: tight agreement → CONSENSUS; wide spread → DISPUTE/ESCALATE.
 */
function computeCMAG(votes) {
    if (votes.length === 0) {
        return { cooperation: 0, autonomy: 0, integrity: 0, fairness: 0, ecs: 0,
            arbitration: CMAGArbitration.ESCALATE_IGA };
    }
    const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
    const cooperation = mean(votes.map(v => v.cooperation));
    const autonomy = mean(votes.map(v => v.autonomy));
    const integrity = mean(votes.map(v => v.integrity));
    const fairness = mean(votes.map(v => v.fairness));
    const ecs = cooperation * autonomy * integrity * fairness;
    // Arbitration based on inter-agent cooperation variance
    const coopValues = votes.map(v => v.cooperation);
    const coopMean = mean(coopValues);
    const variance = mean(coopValues.map(c => (c - coopMean) ** 2));
    const spread = Math.sqrt(variance);
    let arbitration;
    if (spread < 0.10)
        arbitration = CMAGArbitration.CONSENSUS;
    else if (spread < 0.25)
        arbitration = CMAGArbitration.DISPUTE;
    else
        arbitration = CMAGArbitration.ESCALATE_IGA;
    return { cooperation, autonomy, integrity, fairness, ecs, arbitration };
}
// ─────────────────────────────────────────────────────────────────────────────
// SECTION 9 · DIMENSION 1 — VALIDITY
// V = validity(prediction, ground_truth) — accuracy-style fidelity in [0,1]
// ─────────────────────────────────────────────────────────────────────────────
function computeValidity(correct, total) {
    return total > 0 ? Math.max(0, Math.min(1, correct / total)) : 0;
}
/** Full EVA evaluation from raw evidence — the completed pipeline. */
function evaluateEVA(ev, coefficients = exports.SA_DEFAULT_COEFFICIENTS, thresholds = exports.DEFAULT_THRESHOLDS) {
    const startTime = Date.now();
    // Validate coefficient sum = 1.0
    const coeffSum = Object.values(coefficients).reduce((a, b) => a + b, 0);
    if (Math.abs(coeffSum - 1.0) > 0.001) {
        throw new Error(`EVA: Coefficient sum ${coeffSum.toFixed(4)} ≠ 1.000`);
    }
    // ── Compute all six dimensions ──
    const validity = computeValidity(ev.validityCorrect, ev.validityTotal);
    const confidence = scaleConfidenceByTemperature(ev.rawConfidence, ev.temperature);
    const risk = exports.RISK_TIER_R[ev.riskTier];
    const { compliance } = evaluateMFCM(ev.mfcmPredicate);
    const { stability, jsd } = computeStability(ev.currentDist, ev.baselineDist);
    const { societalImpact } = computeSocietalImpact(ev.hos56Cells);
    // ── Fairness metrics ──
    const fairnessGroups = ev.fairnessGroups ?? [ev.privilegedGroup, ev.unprivilegedGroup];
    const disparateImpact = computeDisparateImpact(fairnessGroups);
    const spd = computeSPD(ev.privilegedGroup, ev.unprivilegedGroup);
    // ── CMAG ethical cooperation ──
    const cmag = computeCMAG(ev.cmagVotes);
    const ecs = cmag.ecs;
    // ── MANDATORY BLOCK OVERRIDES (hardware-equivalent) ──
    const blockReasons = [];
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
    const svsRaw = coefficients.wValidity * validity +
        coefficients.wConfidence * confidence +
        coefficients.wRisk * (1 - risk) + // inverse: low risk → high score
        coefficients.wCompliance * compliance +
        coefficients.wStability * stability +
        coefficients.wSocietalImpact * societalImpact;
    const svs = Math.min(Math.max(svsRaw, 0), 1);
    // ── Decision ──
    let decision;
    if (blockReasons.length > 0)
        decision = GovernanceDecision.BLOCK;
    else if (cmag.arbitration === CMAGArbitration.DISPUTE)
        decision = GovernanceDecision.ESCALATE;
    else if (risk >= 0.6 || compliance < 0.80)
        decision = GovernanceDecision.REVIEW;
    else if (risk >= 0.5)
        decision = GovernanceDecision.RESTRICT;
    else
        decision = GovernanceDecision.APPROVE;
    return {
        validity, confidence, risk, compliance, stability, societalImpact,
        svs, jsd, disparateImpact, spd, ecs, cmag,
        decision, blockReasons,
        computedAt: new Date(), latencyMs: Date.now() - startTime,
    };
}
// ── Formula reference (Part 7.1) ──
exports.EVAFormulas = {
    validity: "V  = correct / total",
    confidence: "Cf = confidence_raw / (1 + ln(T + 1))",
    risk: "R  = RiskTierMap[tier]",
    compliance: "Co = Σ(wᵢ × MFCMᵢ) / Σwᵢ   [47 checks]",
    stability: "S  = 1 − JSD(current ‖ baseline)",
    societalImpact: "I  = H-OS-56(valence, entropy, SAHRC flags)",
    disparateImpact: "DI = min(groupRates) / max(groupRates)",
    spd: "SPD = posRate(unpriv) − posRate(priv)",
    ecs: "ECS = Cooperation × Autonomy × Integrity × Fairness",
    svs: "SVS = w₁V + w₂Cf + w₃(1−R) + w₄Co + w₅S + w₆I",
    block: "BLOCK if R≥0.80 | Co<0.70 | DI<0.80 | JSD>0.40 | ECS<0.65 | |SPD|>0.05 | tier=UNACCEPTABLE",
};
// ─────────────────────────────────────────────────────────────────────────────
// SECTION 11 · EVA ENGINE CLASS — hot-reload, profiles, evaluation
// ─────────────────────────────────────────────────────────────────────────────
class EVAEngine {
    constructor(coefficients = exports.SA_DEFAULT_COEFFICIENTS, thresholds = exports.DEFAULT_THRESHOLDS) {
        this.coefficients = { ...coefficients };
        this.thresholds = { ...thresholds };
    }
    /** Hot-reload coefficients (<5ms target). Validates Σ = 1.0. */
    hotReload(coefficients) {
        this.coefficients = { ...this.coefficients, ...coefficients };
        const sum = Object.values(this.coefficients).reduce((a, b) => a + b, 0);
        if (Math.abs(sum - 1.0) > 0.001) {
            throw new Error(`EVA hot-reload: coefficient sum ${sum.toFixed(4)} ≠ 1.000`);
        }
    }
    updateThresholds(thresholds) {
        this.thresholds = { ...this.thresholds, ...thresholds };
    }
    evaluate(evidence) {
        return evaluateEVA(evidence, this.coefficients, this.thresholds);
    }
    applyMilitaryProfile() { this.coefficients = { ...exports.MILITARY_COEFFICIENTS }; }
    applyHealthcareProfile() { this.coefficients = { ...exports.HEALTHCARE_COEFFICIENTS }; }
    resetToSADefaults() {
        this.coefficients = { ...exports.SA_DEFAULT_COEFFICIENTS };
        this.thresholds = { ...exports.DEFAULT_THRESHOLDS };
    }
    getCoefficients() { return { ...this.coefficients }; }
    getThresholds() { return { ...this.thresholds }; }
}
exports.EVAEngine = EVAEngine;
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
exports.EVA_SOVEREIGN_KEY = (0, node_crypto_1.randomBytes)(32);
const EVA_ENGINE_ID = "ZA-EVA-ENGINE-01";
/** Canonical serialisation of the score vector for signing (stable field order). */
function canonicaliseScore(s) {
    return [
        s.validity, s.confidence, s.risk, s.compliance, s.stability, s.societalImpact,
        s.svs, s.jsd, s.disparateImpact, s.spd, s.ecs, s.decision,
    ].map(v => (typeof v === "number" ? v.toFixed(6) : String(v))).join("|");
}
/** Evaluate AND seal — returns a tamper-evident verdict. */
function evaluateEVASealed(ev, coefficients = exports.SA_DEFAULT_COEFFICIENTS, thresholds = exports.DEFAULT_THRESHOLDS) {
    const score = evaluateEVA(ev, coefficients, thresholds);
    const seal = (0, node_crypto_1.createHmac)("sha256", exports.EVA_SOVEREIGN_KEY)
        .update(`${EVA_ENGINE_ID}:${canonicaliseScore(score)}`).digest("hex");
    return { score, seal, engineId: EVA_ENGINE_ID };
}
/** Verify a sealed verdict (constant-time). Returns false on any mutation. */
function verifyEVASeal(sealed) {
    const expected = (0, node_crypto_1.createHmac)("sha256", exports.EVA_SOVEREIGN_KEY)
        .update(`${sealed.engineId}:${canonicaliseScore(sealed.score)}`).digest("hex");
    const a = Buffer.from(sealed.seal), b = Buffer.from(expected);
    if (a.length !== b.length)
        return false;
    return (0, node_crypto_1.timingSafeEqual)(a, b);
}
// ─────────────────────────────────────────────────────────────────────────────
// SECTION 12 · RUNNABLE DEMO HARNESS
// Run:  npx ts-node eva-engine-complete.ts
// ─────────────────────────────────────────────────────────────────────────────
function demo() {
    const engine = new EVAEngine();
    const line = "─".repeat(72);
    const print = (title, s) => {
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
        mfcmPredicate: () => true, // all 47 pass
        currentDist: [0.25, 0.25, 0.25, 0.25],
        baselineDist: [0.24, 0.26, 0.25, 0.25],
        hos56Cells: [
            { sector: "EMPLOYMENT", band: "STRONGLY_BENEFICIAL", weight: 0.5 },
            { sector: "EDUCATION", band: "BENEFICIAL", weight: 0.5 },
        ],
        privilegedGroup: { group: "priv", favorableCount: 480, totalCount: 1000 },
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
        mfcmPredicate: (e) => e.checkId !== 12, // fails NAIFP disparate-impact check
        currentDist: [0.25, 0.25, 0.25, 0.25],
        baselineDist: [0.25, 0.25, 0.25, 0.25],
        hos56Cells: [
            { sector: "EMPLOYMENT", band: "SEVERE", weight: 0.6, sahrcFlag: true },
            { sector: "FINANCE", band: "MODERATE", weight: 0.4 },
        ],
        privilegedGroup: { group: "priv", favorableCount: 600, totalCount: 1000 },
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
        currentDist: [0.85, 0.05, 0.05, 0.05], // heavy drift
        baselineDist: [0.25, 0.25, 0.25, 0.25],
        hos56Cells: [{ sector: "HEALTH", band: "NEUTRAL", weight: 1.0 }],
        privilegedGroup: { group: "priv", favorableCount: 500, totalCount: 1000 },
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
        currentDist: [0.25, 0.25, 0.25, 0.25],
        baselineDist: [0.25, 0.25, 0.25, 0.25],
        hos56Cells: [{ sector: "JUSTICE", band: "CATASTROPHIC", weight: 1.0, sahrcFlag: true }],
        privilegedGroup: { group: "priv", favorableCount: 500, totalCount: 1000 },
        unprivilegedGroup: { group: "unpriv", favorableCount: 500, totalCount: 1000 },
        cmagVotes: [
            { agentId: "A", cooperation: 0.95, autonomy: 0.10, integrity: 0.95, fairness: 0.95 },
        ],
    }));
    console.log(line);
    console.log("EVA FORMULAE");
    console.log(line);
    Object.entries(exports.EVAFormulas).forEach(([k, v]) => console.log(`  ${k.padEnd(16)} ${v}`));
    console.log(line);
    console.log(`MFCM CATALOGUE: ${exports.MFCM_CATALOG.length} checks across ` +
        `${new Set(exports.MFCM_CATALOG.map(c => c.category)).size} categories`);
    console.log(`H-OS-56 GRID:   ${exports.HOS56_SECTORS.length} sectors × ${exports.HOS56_SEVERITY_BANDS.length} bands = ` +
        `${exports.HOS56_SECTORS.length * exports.HOS56_SEVERITY_BANDS.length} cells`);
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
        currentDist: [0.25, 0.25, 0.25, 0.25], baselineDist: [0.24, 0.26, 0.25, 0.25],
        hos56Cells: [{ sector: "EMPLOYMENT", band: "STRONGLY_BENEFICIAL", weight: 0.5 },
            { sector: "EDUCATION", band: "BENEFICIAL", weight: 0.5 }],
        privilegedGroup: { group: "priv", favorableCount: 480, totalCount: 1000 },
        unprivilegedGroup: { group: "unpriv", favorableCount: 470, totalCount: 1000 },
        cmagVotes: [{ agentId: "A", cooperation: 0.92, autonomy: 0.95, integrity: 0.94, fairness: 0.93 }],
    });
    console.log(`  Verdict   : ${sealed.score.decision}  (SVS ${sealed.score.svs.toFixed(3)})`);
    console.log(`  Seal      : ${sealed.seal.slice(0, 48)}…`);
    console.log(`  Verify    : ${verifyEVASeal(sealed) ? "VALID ✓" : "INVALID"}`);
    // Tamper: flip the decision after sealing → verification must fail.
    const forged = { ...sealed, score: { ...sealed.score, decision: GovernanceDecision.APPROVE, risk: 0.01 } };
    console.log(`  Tampered  : ${verifyEVASeal(forged) ? "VALID (BAD!)" : "INVALID ✓ — forgery detected"}`);
    console.log(line);
}
// Execute demo when run directly
demo();
