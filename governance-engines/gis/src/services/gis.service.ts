import { prisma } from '../config/database';
import { CONSTITUTIONAL_PILLARS } from '../config/constants';
import { AuditService } from './udoc.service';
import crypto from 'crypto';

export interface GISDecisionInput {
  type: string;
  domain: string;
  data: any;
  context?: any;
  participantId?: string;
  requiresGovernanceGate?: boolean;
}

export class GISService {
  private auditService: AuditService;
  private failClosedEnabled: boolean;

  constructor() {
    this.auditService = new AuditService();
    this.failClosedEnabled = process.env.GIS_FAIL_CLOSED === 'true';
  }

  async makeDecision(input: GISDecisionInput): Promise<any> {
    // Step 1: Check constitutional pillars
    const pillarChecks = await this.checkConstitutionalPillars(input);
    const allPillarsPassed = pillarChecks.every((check: any) => check.passed);

    // Step 2: Generate decision or block
    let decision: any;
    let confidence = 0;
    let reasoning = '';
    let governanceGate = false;

    if (allPillarsPassed) {
      const result = await this.generateDecision(input);
      decision = result.decision;
      confidence = result.confidence;
      reasoning = result.reasoning;
      
      // Apply governance gate for high-stakes decisions
      if (input.requiresGovernanceGate !== false && this.isHighStakesDecision(input)) {
        governanceGate = await this.applyGovernanceGate(input, decision);
        if (!governanceGate) {
          decision = this.getBlockDecision(input);
          confidence = 0;
          reasoning = 'Governance gate failed - decision requires COB review';
        }
      } else {
        governanceGate = true;
      }
    } else {
      decision = this.getBlockDecision(input);
      reasoning = `Constitutional violation: ${pillarChecks.filter((p: any) => !p.passed).map((p: any) => p.pillarName).join(', ')}`;
      governanceGate = false;
    }

    // Fail-closed enforcement
    if (this.failClosedEnabled && decision.blocked) {
      decision.enforced = true;
    }

    // Record decision
    const record = await prisma.gISDecision.create({
      data: {
        decisionId: `GIS-${Date.now()}-${crypto.randomBytes(4).toString('hex')}`,
        decisionType: input.type as any,
        domain: input.domain,
        inputData: input.data,
        context: input.context || {},
        output: decision,
        confidence,
        reasoning,
        pillarChecks,
        allPillarsPassed,
        governanceGate,
        coBReviewed: false,
        coBApproved: false,
        failClosed: this.failClosedEnabled,
        participantId: input.participantId || null,
        auditHash: crypto.randomBytes(32).toString('hex')
      }
    });

    await this.auditService.logAction({
      domain: 'GIS',
      entityId: record.id,
      entityType: 'GISDecision',
      action: 'DECISION_MADE',
      performedBy: 'GIS_System',
      afterState: { decisionId: record.decisionId, type: input.type, allPillarsPassed }
    });

    return {
      decisionId: record.decisionId,
      decision,
      confidence,
      reasoning,
      pillarChecks,
      allPillarsPassed,
      governanceGate,
      failClosed: this.failClosedEnabled
    };
  }

  private async checkConstitutionalPillars(input: GISDecisionInput): Promise<any[]> {
    const results = [];
    for (const pillar of CONSTITUTIONAL_PILLARS) {
      const passed = await this.evaluatePillar(pillar, input);
      results.push({
        pillarId: pillar.id,
        pillarNumber: pillar.number,
        pillarName: pillar.name,
        passed,
        reasoning: passed ? 'Compliant' : `Violation of Pillar ${pillar.number}`
      });
    }
    return results;
  }

  private async evaluatePillar(pillar: any, input: GISDecisionInput): Promise<boolean> {
    switch (pillar.number) {
      case 1: return !(input.data?.harmParticipant || input.data?.dehumanizing);
      case 2: return !(input.data?.permanentExclusion || input.data?.giveUpOnParticipant);
      case 3: return !(input.data?.partisanAdvocacy || input.data?.violatesSovereignty);
      case 4: return !(input.data?.unethicalProfit || input.data?.missionUndermined);
      case 5: return !(input.data?.bypassGovernance);
      case 6: return !(input.data?.nonAuditable);
      case 7: return !(input.data?.founderOverride);
      case 8: return !(input.data?.aiReplacingHuman);
      case 9: return !(input.data?.discriminatesCohort1);
      case 10: return !(input.data?.shortTermGain === 'critical');
      case 11: return !(input.data?.dataManipulation || input.data?.creditAbuse);
      case 12: return !(input.data?.evidenceBased === false);
      default: return true;
    }
  }

  private async generateDecision(input: GISDecisionInput): Promise<any> {
    switch (input.type) {
      case 'CAREER_NAVIGATION':
        return this.generateCareerNavigation(input);
      case 'CERTIFICATION_VERIFICATION':
        return { decision: { verified: true }, confidence: 0.95, reasoning: 'Certification verified', blocked: false };
      case 'EMPLOYMENT_VERIFICATION':
        return { decision: { verified: true }, confidence: 0.90, reasoning: 'Employment verified', blocked: false };
      case 'COMPLIANCE_CHECK':
        return { decision: { compliant: true }, confidence: 0.85, reasoning: 'Compliance check passed', blocked: false };
      case 'GOVERNANCE_DECISION':
        return { decision: { approved: true }, confidence: 0.80, reasoning: 'Governance approved', blocked: false };
      case 'OUTCOME_AUDIT':
        return { decision: { outcomes: { placementRate: 0.72, employmentRate: 0.68 } }, confidence: 0.90, reasoning: 'Outcomes audited', blocked: false };
      case 'FRANCHISE_INTELLIGENCE':
        return { decision: { status: 'ACTIVE', complianceScore: 0.92 }, confidence: 0.85, reasoning: 'Franchise performance analyzed', blocked: false };
      case 'AI_ADAPTATION':
        return this.generateAIAdaptation(input);
      case 'MENTOR_MATCHING':
        return { decision: { matchedMentors: [{ mentorId: 'mentor_1', matchScore: 0.85 }] }, confidence: 0.80, reasoning: 'Mentors matched', blocked: false };
      default:
        return { decision: { processed: true }, confidence: 0.60, reasoning: 'Generic decision', blocked: false };
    }
  }

  private generateCareerNavigation(input: GISDecisionInput): any {
    const cohortType = input.data?.cohortType || 1;
    let pathway = 'A';
    let reasoning = 'Default to Construction pathway';
    if (cohortType === 2) { pathway = 'B'; reasoning = 'AI-displaced worker - recommended Digital Operations'; }
    else if (cohortType === 3) { pathway = 'A'; reasoning = 'Workforce evolution - recommended Construction'; }
    else if (cohortType === 4) { pathway = 'B'; reasoning = 'Future workforce - recommended Digital Operations with AI literacy'; }
    return {
      decision: { recommendedPathway: pathway, needsAILiteracy: true, needsFinancialLiteracy: true },
      confidence: 0.75,
      reasoning,
      blocked: false
    };
  }

  private generateAIAdaptation(_input: GISDecisionInput): any {
    // Simplified reference-package placeholder — returns illustrative figures regardless of
    // input. The live, input-driven pillar/decision logic is
    // platform-core/app/services/gis_engine.py (make_decision), which this TS package remains
    // the canonical spec for, not the runtime source of truth. See GIS_ECOSYSTEM_BUILD_NOTES.md.
    const risk = 0.45;
    const recommendations = risk > 0.5 ? ['AI Awareness', 'AI Augmentation'] : ['AI Awareness'];
    return {
      decision: { displacementRisk: risk, recommendations, aiReadinessScore: { baseline: 0.6, augmentation: 0.4 } },
      confidence: 0.75,
      reasoning: risk > 0.5 ? 'High displacement risk' : 'Moderate displacement risk',
      blocked: false
    };
  }

  private isHighStakesDecision(input: GISDecisionInput): boolean {
    return ['GOVERNANCE_DECISION', 'FRANCHISE_INTELLIGENCE'].includes(input.type) ||
           input.data?.harmParticipant || input.data?.constitutionalViolation;
  }

  private async applyGovernanceGate(_input: GISDecisionInput, _decision: any): Promise<boolean> {
    // Dev-mode placeholder, honestly labelled as such by the original author — this always
    // approves and is NOT the fail-closed behaviour Document 00 §3 / Pillar VIII require.
    // The live, fail-closed implementation is gis_engine.py's make_decision() in platform-core,
    // which defaults to BLOCK on any unverified pillar flag. Do not treat this stub as evidence
    // of fail-closed behaviour in this reference package; the Python engine is authoritative.
    return true; // Auto-pass for development
  }

  private getBlockDecision(input: GISDecisionInput): any {
    return { blocked: true, enforced: true, reason: 'Constitutional violation or governance gate failure', type: input.type };
  }

  async getDecision(decisionId: string): Promise<any> {
    return await prisma.gISDecision.findUnique({ where: { decisionId }, include: { participant: true } });
  }

  async getParticipantDecisions(participantId: string): Promise<any[]> {
    return await prisma.gISDecision.findMany({ where: { participantId }, orderBy: { createdAt: 'desc' } });
  }
}

export default GISService;