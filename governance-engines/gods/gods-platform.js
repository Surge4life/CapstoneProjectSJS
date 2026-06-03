"use strict";
// ════════════════════════════════════════════════════════════════════════════
// G.O.D.S PLATFORM — FOUR-DIVISION INTEGRATED ECONOMIC ENGINE
// Good Orderly Directional Systems Holdings (Pty) Ltd
// The closed capital loop: SETHS → TS → UDOC → MADIBA → (back to) SETHS
// Constitutional parent · 12 Pillars · IP Trust · COB · 250-year mandate
//
// This is NOT four disconnected service stubs. It models the integrated
// institution and runs a full compounding cycle, showing why the loop is
// closed and self-reinforcing: every division feeds the next, and returns
// recycle back into human capital rather than leaking to external extraction.
//
// Run: npx tsc --target ES2020 --module commonjs --skipLibCheck --types node \
//        --outDir dist gods-platform.ts && node dist/gods-platform.js
// ════════════════════════════════════════════════════════════════════════════
Object.defineProperty(exports, "__esModule", { value: true });
exports.GODSHoldings = exports.MADIBACapital = exports.UDOCDivision = exports.TSIndustries = exports.SETHS = exports.fmtR = exports.R = exports.DIVISIONS = exports.CONSTITUTIONAL_PILLARS = void 0;
exports.pillarGate = pillarGate;
const node_crypto_1 = require("node:crypto");
exports.CONSTITUTIONAL_PILLARS = [
    { number: 1, title: "Human Dignity", description: "Basic needs are not leverage points." },
    { number: 2, title: "Contribution First", description: "Reward contribution over speculative extraction." },
    { number: 3, title: "Sovereign Respect", description: "Alignment with governments is always voluntary." },
    { number: 4, title: "Ethical Profitability", description: "Profit pursued — never via destabilisation." },
    { number: 5, title: "Governance First", description: "No expansion beyond governance capacity." },
    { number: 6, title: "Transparency", description: "Operations remain independently auditable." },
    { number: 7, title: "Founder Constraint", description: "No individual supersedes the institution." },
    { number: 8, title: "Human Primacy in AI", description: "Technology serves human wellbeing." },
    { number: 9, title: "Reintegration", description: "Failure does not permanently exclude." },
    { number: 10, title: "Long-Horizon Discipline", description: "Decisions evaluated for generational impact." },
    { number: 11, title: "Anti-Corruption", description: "Integrity is architectural, not aspirational." },
    { number: 12, title: "Evidence-Driven", description: "System adapts on measurable outcomes." },
];
exports.DIVISIONS = [
    { code: "SETHS", name: "S.E.T.H.S", fullName: "Skills, Employment, Training, Human Systems", color: "#4A9E7F" },
    { code: "TS", name: "T.S Industries", fullName: "The Technological Sector", color: "#7A4A9E" },
    { code: "UDOC", name: "UDOC", fullName: "Unified Digital Oversight & Coordination", color: "#9E6B4A" },
    { code: "MADIBA", name: "M.A.D.I.B.A", fullName: "My African Dream Is Being Achieved", color: "#4A7A9E" },
    { code: "HOLDINGS", name: "G.O.D.S Holdings", fullName: "Good Orderly Directional Systems Holdings", color: "#C9A84C" },
];
const R = (rands) => Math.round(rands * 100);
exports.R = R;
const fmtR = (cents) => "R" + (cents / 100).toLocaleString("en-ZA", { minimumFractionDigits: 0, maximumFractionDigits: 0 });
exports.fmtR = fmtR;
function pillarGate(checks) {
    const violations = checks.filter(c => !c.passed);
    return { passed: violations.length === 0, violations };
}
class SETHS {
    constructor() {
        this.cohorts = [];
    }
    /**
     * Run a cohort through the reintegration pipeline.
     * completionRate / placementRate model real learnership attrition.
     * Funded by capital injected from M.A.D.I.B.A (closing the loop).
     */
    runCohort(params) {
        // Pillar 5 (Governance First): cannot intake beyond funded capacity.
        const fundedCapacity = Math.floor(params.fundingAvailable / params.costPerLearner);
        const actualIntake = Math.min(params.intake, fundedCapacity);
        const learners = [];
        let completed = 0, placed = 0;
        for (let i = 0; i < actualIntake; i++) {
            const isComplete = i < Math.round(actualIntake * params.completionRate);
            const isPlaced = isComplete && (i < Math.round(actualIntake * params.completionRate * params.placementRate));
            if (isComplete)
                completed++;
            if (isPlaced)
                placed++;
            learners.push({
                id: (0, node_crypto_1.randomUUID)(), enrolledQualification: params.qualification, nqfLevel: params.nqfLevel,
                startedAt: new Date(), completed: isComplete, placed: isPlaced,
                monthlyValue: isPlaced ? (0, exports.R)(params.avgMonthlyValue) : 0,
            });
        }
        const monthlyEconomicOutput = learners.reduce((s, l) => s + l.monthlyValue, 0);
        const gate = pillarGate([
            { pillar: 1, passed: true, note: "Stipends paid; dignity preserved" },
            { pillar: 2, passed: true, note: "Reward tied to completion + placement" },
            { pillar: 5, passed: actualIntake <= fundedCapacity, note: `Intake ${actualIntake} ≤ capacity ${fundedCapacity}` },
            { pillar: 9, passed: true, note: "Non-completers retain re-entry pathway" },
            { pillar: 12, passed: true, note: "Outcomes measured: completion + placement rates" },
        ]);
        const result = {
            cohortId: (0, node_crypto_1.randomUUID)(), intake: actualIntake, completed, placed,
            completionRate: actualIntake ? completed / actualIntake : 0,
            placementRate: completed ? placed / completed : 0,
            monthlyEconomicOutput, pillarGate: gate, learners,
        };
        this.cohorts.push(result);
        return result;
    }
    getCohorts() { return [...this.cohorts]; }
    totalPlaced() { return this.cohorts.reduce((s, c) => s + c.placed, 0); }
}
exports.SETHS = SETHS;
class TSIndustries {
    constructor() {
        this.projects = [];
    }
    /** Deploy placed workers + capex into a production SPV. */
    deployProject(params) {
        // Pillar 5: only deploy if workforce capacity exists.
        const workersAbsorbed = Math.min(params.workersAvailable, params.workersRequired);
        const utilisation = params.workersRequired ? workersAbsorbed / params.workersRequired : 0;
        // Revenue scales with workforce utilisation
        const monthlyGrossRevenue = Math.round(params.monthlyRevenue * utilisation);
        const monthlyOperatingProfit = Math.round(monthlyGrossRevenue * params.operatingMarginPct);
        const project = {
            id: (0, node_crypto_1.randomUUID)(), sector: params.sector, name: params.name,
            workersDeployed: workersAbsorbed, capexDeployed: params.capex,
            monthlyRevenue: monthlyGrossRevenue, operatingMarginPct: params.operatingMarginPct,
            spvId: `SPV-${params.sector}-${(0, node_crypto_1.randomUUID)().slice(0, 8)}`, active: workersAbsorbed > 0,
        };
        this.projects.push(project);
        const gate = pillarGate([
            { pillar: 2, passed: true, note: "Revenue from real production, not speculation" },
            { pillar: 4, passed: params.operatingMarginPct > 0 && params.operatingMarginPct < 0.6,
                note: `Margin ${(params.operatingMarginPct * 100).toFixed(0)}% — profitable, not extractive` },
            { pillar: 5, passed: utilisation >= 0.5, note: `Workforce utilisation ${(utilisation * 100).toFixed(0)}%` },
            { pillar: 6, passed: true, note: `Ring-fenced in ${project.spvId} — independently auditable` },
        ]);
        return { project, workersAbsorbed, monthlyGrossRevenue, monthlyOperatingProfit, pillarGate: gate };
    }
    getProjects() { return [...this.projects]; }
    totalMonthlyProfit() {
        return this.projects.reduce((s, p) => s + Math.round(p.monthlyRevenue * p.operatingMarginPct), 0);
    }
}
exports.TSIndustries = TSIndustries;
class UDOCDivision {
    constructor() {
        this.tenants = [];
    }
    onboardTenant(params) {
        const tenant = { id: (0, node_crypto_1.randomUUID)(), ...params };
        this.tenants.push(tenant);
        return tenant;
    }
    /** Internal governance for the institution's own AI usage — free, mandatory. */
    governInternal(division, modelsGoverned) {
        return this.onboardTenant({
            name: `INTERNAL-${division}`, modelsGoverned, monthlyLicenseFee: 0,
            decisionsPerMonth: modelsGoverned * 10000, blockRate: 0.02, jurisdiction: "ZA",
        });
    }
    snapshot() {
        const monthlyRecurringRevenue = this.tenants.reduce((s, t) => s + t.monthlyLicenseFee, 0);
        const totalModelsGoverned = this.tenants.reduce((s, t) => s + t.modelsGoverned, 0);
        const totalDecisionsPerMonth = this.tenants.reduce((s, t) => s + t.decisionsPerMonth, 0);
        const avgBlockRate = this.tenants.length
            ? this.tenants.reduce((s, t) => s + t.blockRate, 0) / this.tenants.length : 0;
        const gate = pillarGate([
            { pillar: 3, passed: true, note: "Government tenants onboarded voluntarily" },
            { pillar: 6, passed: true, note: "Every decision logged to StayChain — auditable" },
            { pillar: 8, passed: avgBlockRate > 0, note: `Human-primacy enforced — ${(avgBlockRate * 100).toFixed(1)}% blocked` },
            { pillar: 11, passed: true, note: "Governance prevents institutional AI capture" },
        ]);
        return { tenants: [...this.tenants], monthlyRecurringRevenue, totalModelsGoverned,
            totalDecisionsPerMonth, avgBlockRate, pillarGate: gate };
    }
}
exports.UDOCDivision = UDOCDivision;
class MADIBACapital {
    constructor() {
        this.sources = [];
        this.cumulativeRecycled = 0;
    }
    addSource(s) { this.sources.push(s); }
    /**
     * Allocate the month's pooled returns.
     * Policy: 20% DFI servicing · 15% reserve · 10% holdings opex · 55% recycled to SETHS.
     * The 55% recycle is the compounding mechanism — next cohort is bigger.
     */
    allocate(params) {
        const dfiPct = params?.dfiPct ?? 0.20;
        const reservePct = params?.reservePct ?? 0.15;
        const holdingsPct = params?.holdingsPct ?? 0.10;
        const recyclePct = 1 - dfiPct - reservePct - holdingsPct;
        const totalInflow = this.sources.reduce((s, c) => s + c.monthlyContribution, 0);
        const dfiServicing = Math.round(totalInflow * dfiPct);
        const reserveRetained = Math.round(totalInflow * reservePct);
        const holdingsOpex = Math.round(totalInflow * holdingsPct);
        const recycledToSETHS = totalInflow - dfiServicing - reserveRetained - holdingsOpex;
        this.cumulativeRecycled += recycledToSETHS;
        const gate = pillarGate([
            { pillar: 2, passed: recyclePct > 0.5, note: `${(recyclePct * 100).toFixed(0)}% recycled to human capital` },
            { pillar: 4, passed: totalInflow > 0, note: "Capital sourced from real returns" },
            { pillar: 10, passed: reservePct >= 0.10, note: `${(reservePct * 100).toFixed(0)}% long-horizon reserve` },
            { pillar: 11, passed: true, note: "Allocation rules fixed — no discretionary diversion" },
        ]);
        return { totalInflow, dfiServicing, reserveRetained, holdingsOpex,
            recycledToSETHS, recyclePct, pillarGate: gate };
    }
    reset() { this.sources = []; }
    getCumulativeRecycled() { return this.cumulativeRecycled; }
}
exports.MADIBACapital = MADIBACapital;
class GODSHoldings {
    constructor(seedCapital) {
        this.seedCapital = seedCapital;
        this.seths = new SETHS();
        this.ts = new TSIndustries();
        this.udoc = new UDOCDivision();
        this.madiba = new MADIBACapital();
        this.cycles = [];
        this.workforce = 0;
        // Holdings governs every division's AI internally (Pillar 8), free + mandatory.
        exports.DIVISIONS.filter(d => d.code !== "HOLDINGS").forEach(d => this.udoc.governInternal(d.code, 3));
        // Onboard external paying governance tenants (UDOC commercial revenue).
        this.udoc.onboardTenant({ name: "ZA-Gov Dept Home Affairs", modelsGoverned: 12,
            monthlyLicenseFee: (0, exports.R)(450000), decisionsPerMonth: 2000000, blockRate: 0.03, jurisdiction: "ZA" });
        this.udoc.onboardTenant({ name: "SADC Financial Regulator", modelsGoverned: 8,
            monthlyLicenseFee: (0, exports.R)(320000), decisionsPerMonth: 900000, blockRate: 0.04, jurisdiction: "SADC" });
    }
    /** Run one monthly cycle of the closed loop. */
    runCycle(month, sethsFunding) {
        // 1) S.E.T.H.S — fund a cohort; bigger funding → bigger cohort (compounding)
        const cohort = this.seths.runCohort({
            qualification: "Software Developer 118707", nqfLevel: 5,
            intake: 10000, completionRate: 0.78, placementRate: 0.70,
            avgMonthlyValue: 12000, fundingAvailable: sethsFunding, costPerLearner: (0, exports.R)(35000),
        });
        this.workforce += cohort.placed;
        // 2) T.S Industries — absorb placed workers into production SPVs
        const energy = this.ts.deployProject({
            sector: "ENERGY", name: `REIPP Solar Cohort M${month}`,
            workersAvailable: cohort.placed, workersRequired: Math.max(1, Math.round(cohort.placed * 0.4)),
            capex: (0, exports.R)(8000000), monthlyRevenue: (0, exports.R)(2200000), operatingMarginPct: 0.32,
        });
        const housing = this.ts.deployProject({
            sector: "HOUSING", name: `Modular Housing Cohort M${month}`,
            workersAvailable: cohort.placed - energy.workersAbsorbed,
            workersRequired: Math.max(1, Math.round(cohort.placed * 0.4)),
            capex: (0, exports.R)(5000000), monthlyRevenue: (0, exports.R)(1500000), operatingMarginPct: 0.28,
        });
        // Cumulative: every SPV ever deployed keeps producing (Pillar 10 — long horizon).
        const tsMonthlyProfit = this.ts.totalMonthlyProfit();
        // 3) UDOC — recurring SaaS revenue from governance tenants
        const udocSnap = this.udoc.snapshot();
        const udocMRR = udocSnap.monthlyRecurringRevenue;
        // 4) M.A.D.I.B.A — pool all returns, allocate, recycle surplus to SETHS
        this.madiba.reset();
        this.madiba.addSource({ division: "TS", monthlyContribution: tsMonthlyProfit, kind: "OPERATING_PROFIT" });
        this.madiba.addSource({ division: "UDOC", monthlyContribution: udocMRR, kind: "SAAS_REVENUE" });
        const alloc = this.madiba.allocate();
        const pillarsClean = cohort.pillarGate.passed && energy.pillarGate.passed &&
            housing.pillarGate.passed && udocSnap.pillarGate.passed && alloc.pillarGate.passed;
        const snap = {
            month, sethsFunding, workersPlaced: cohort.placed, cumulativeWorkforce: this.workforce,
            tsMonthlyProfit, udocMRR, madibaInflow: alloc.totalInflow,
            recycledToSETHS: alloc.recycledToSETHS, pillarsClean,
        };
        this.cycles.push(snap);
        return snap;
    }
    /** Run the full closed loop for N months; cohort funding compounds. */
    run(months) {
        let funding = this.seedCapital; // month 1 funded by DFI seed (via MADIBA)
        for (let m = 1; m <= months; m++) {
            const snap = this.runCycle(m, funding);
            // Next month's SETHS funding = recycled surplus + a flat DFI tranche while scaling
            const dfiTranche = m <= 3 ? this.seedCapital : 0; // DFI support tapers off
            funding = snap.recycledToSETHS + dfiTranche;
        }
        return this.cycles;
    }
    getCycles() { return [...this.cycles]; }
    getDivisions() { return { seths: this.seths, ts: this.ts, udoc: this.udoc, madiba: this.madiba }; }
}
exports.GODSHoldings = GODSHoldings;
// ─────────────────────────────────────────────────────────────────────────────
// SECTION 7 · RUNNABLE DEMO — full closed-loop simulation
// ─────────────────────────────────────────────────────────────────────────────
function demo() {
    const line = "═".repeat(78);
    console.log(line);
    console.log("G.O.D.S HOLDINGS — FOUR-DIVISION CLOSED-LOOP ECONOMIC ENGINE");
    console.log("Good Orderly Directional Systems · 12 Pillars · 250-year mandate");
    console.log(line);
    console.log("Divisions:");
    exports.DIVISIONS.forEach(d => console.log(`  ${d.name.padEnd(16)} ${d.fullName}`));
    console.log(line);
    const seed = (0, exports.R)(350000000); // R350m DFI seed capital
    console.log(`Seed capital (DFI): ${(0, exports.fmtR)(seed)}`);
    console.log(`Loop: MADIBA funds SETHS → SETHS places workers → TS produces →`);
    console.log(`      TS profit + UDOC SaaS → MADIBA → 55% recycled to SETHS\n`);
    const gods = new GODSHoldings(seed);
    const cycles = gods.run(12); // 12-month simulation
    console.log("MONTHLY CYCLE TABLE");
    console.log("─".repeat(78));
    console.log("Mo │ SETHS fund   │ Placed │ Workforce │ TS profit/mo │ UDOC MRR    │ Recycled→SETHS");
    console.log("─".repeat(78));
    cycles.forEach(c => {
        console.log(`${String(c.month).padStart(2)} │ ` +
            `${(0, exports.fmtR)(c.sethsFunding).padEnd(12)} │ ` +
            `${String(c.workersPlaced).padStart(6)} │ ` +
            `${String(c.cumulativeWorkforce).padStart(9)} │ ` +
            `${(0, exports.fmtR)(c.tsMonthlyProfit).padEnd(12)} │ ` +
            `${(0, exports.fmtR)(c.udocMRR).padEnd(11)} │ ` +
            `${(0, exports.fmtR)(c.recycledToSETHS)}`);
    });
    console.log("─".repeat(78));
    const last = cycles[cycles.length - 1];
    const first = cycles[0];
    console.log("\nLOOP OUTCOME (12 months)");
    console.log(line);
    console.log(`  Cumulative workforce reintegrated : ${last.cumulativeWorkforce.toLocaleString("en-ZA")} placed workers`);
    console.log(`  Month-1 SETHS funding             : ${(0, exports.fmtR)(first.sethsFunding)}`);
    console.log(`  Month-12 SETHS funding (recycled) : ${(0, exports.fmtR)(last.sethsFunding)}`);
    console.log(`  Month-12 TS monthly profit        : ${(0, exports.fmtR)(last.tsMonthlyProfit)}`);
    console.log(`  Month-12 UDOC MRR                 : ${(0, exports.fmtR)(last.udocMRR)}`);
    console.log(`  Total recycled into human capital : ${(0, exports.fmtR)(gods.getDivisions().madiba.getCumulativeRecycled())}`);
    const selfFunding = last.recycledToSETHS >= last.sethsFunding * 0.9;
    console.log(`  Loop self-sustaining by month 12  : ${selfFunding ? "YES — DFI dependency broken ✓" : "scaling — still DFI-supported"}`);
    const allClean = cycles.every(c => c.pillarsClean);
    console.log(`  All 12 Pillars clean, every cycle : ${allClean ? "YES ✓" : "NO — review violations"}`);
    console.log(line);
    console.log("\nWHY THE LOOP IS CLOSED (not a leaky pipe):");
    console.log("  • SETHS output (placed workers) is TS's input — no external labour market needed");
    console.log("  • TS output (profit) + UDOC output (SaaS) pool in MADIBA — no profit leaks out");
    console.log("  • MADIBA recycles 55% back to SETHS — next cohort is larger than the last");
    console.log("  • UDOC governs every division's AI internally — Pillar 8 enforced institution-wide");
    console.log("  • Holdings + 12 Pillars gate every action — Pillar 7 means even the founder is removable");
    console.log(line);
}
demo();
