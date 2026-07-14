import { prisma } from '../config/database';
import { CET_CTE_STAGES } from '../config/constants';
import GISService from './gis.service';
import AuditService from './udoc.service';
import crypto from 'crypto';

export class CETCTEService {
  private gisService: GISService;
  private auditService: AuditService;

  constructor() {
    this.gisService = new GISService();
    this.auditService = new AuditService();
  }

  async getParticipantStage(participantId: string): Promise<any> {
    const participant = await prisma.participant.findUnique({ where: { id: participantId } });
    if (!participant) throw new Error(`Participant ${participantId} not found`);
    return { stage: participant.stage, phase: participant.phase };
  }

  async advanceStage(participantId: string, facilitatorId: string): Promise<any> {
    const participant = await prisma.participant.findUnique({
      where: { id: participantId },
      include: { certifications: true, employmentRecords: true }
    });
    if (!participant) throw new Error(`Participant ${participantId} not found`);

    const canAdvance = await this.checkStageCompletion(participantId, participant.stage);
    if (!canAdvance) throw new Error(`Stage ${participant.stage} not completed`);

    // Governance gate: every stage advance is itself a GIS decision (Document 00 §3's
    // "Digital Governor" function), not a bare data mutation. This was the intended
    // purpose of the gisService field already declared on this class (constructed but
    // never called in the original upload) — wiring it in here rather than leaving it
    // dead code or silencing the unused-field error.
    const gate = await this.gisService.makeDecision({
      type: 'GOVERNANCE_DECISION',
      domain: 'SETHS',
      data: { action: 'CETCTE_STAGE_ADVANCE', fromStage: participant.stage },
      participantId,
      requiresGovernanceGate: true
    });
    if (gate?.blocked) {
      throw new Error(`Stage advance blocked by GIS governance gate: ${gate.reasoning || 'fail-closed'}`);
    }

    const nextStage = participant.stage + 1;
    const updated = await prisma.participant.update({
      where: { id: participantId },
      data: { stage: nextStage, phase: CET_CTE_STAGES[nextStage]?.name || 'Unknown' }
    });

    if (nextStage >= 8) {
      await prisma.participant.update({ where: { id: participantId }, data: { status: 'ALUMNI' } });
    }

    await this.auditService.logAction({
      domain: 'CETCTE',
      entityId: participantId,
      entityType: 'Participant',
      action: 'STAGE_ADVANCE',
      performedBy: facilitatorId,
      beforeState: { stage: participant.stage },
      afterState: { stage: nextStage }
    });

    return updated;
  }

  async checkStageCompletion(participantId: string, stage: number): Promise<boolean> {
    const participant = await prisma.participant.findUnique({
      where: { id: participantId },
      include: { certifications: true, employmentRecords: true }
    });
    if (!participant) return false;

    switch (stage) {
      case 0: return !!participant.selfAffirmationContract;
      case 1: return true;
      case 2: return participant.certifications.length > 0;
      case 3: return participant.employmentRecords.length > 0;
      case 4: return participant.employmentVerified;
      case 5: return participant.employmentRecords.some((r: any) => r.isCurrent && r.startDate > new Date(Date.now() - 180 * 24 * 60 * 60 * 1000));
      case 6: return participant.employmentRecords.some((r: any) => r.isCurrent && r.startDate > new Date(Date.now() - 90 * 24 * 60 * 60 * 1000));
      case 7: return participant.isMentor;
      default: return true;
    }
  }

  async generateSkillsPassport(participantId: string): Promise<any> {
    const participant = await prisma.participant.findUnique({
      where: { id: participantId },
      include: { certifications: true, employmentRecords: true }
    });
    if (!participant) throw new Error(`Participant ${participantId} not found`);

    const existing = await prisma.skillsPassport.findUnique({ where: { participantId } });
    if (existing) return existing;

    return await prisma.skillsPassport.create({
      data: {
        participantId,
        certifications: participant.certifications.map((c: any) => ({ id: c.id, name: c.name, tier: c.tier })),
        aiReadinessScore: { baseline: 0.2, augmentation: 0.1, collaboration: 0.1, evolution: 0.1, updatedAt: new Date().toISOString() },
        employmentHistory: participant.employmentRecords.map((r: any) => ({ role: r.role, startDate: r.startDate, verified: r.verified })),
        skills: [],
        version: 1,
        verifiedHash: crypto.randomBytes(32).toString('hex')
      }
    });
  }

  async updateAIReadiness(participantId: string, scores: any): Promise<any> {
    const passport = await prisma.skillsPassport.findUnique({ where: { participantId } });
    if (!passport) throw new Error(`Skills Passport not found for ${participantId}`);
    
    return await prisma.skillsPassport.update({
      where: { participantId },
      data: {
        aiReadinessScore: { ...passport.aiReadinessScore as any, ...scores, updatedAt: new Date().toISOString() },
        version: passport.version + 1
      }
    });
  }

  async getParticipantProgress(participantId: string): Promise<any> {
    const participant = await prisma.participant.findUnique({ where: { id: participantId } });
    if (!participant) throw new Error(`Participant ${participantId} not found`);

    const stages = CET_CTE_STAGES.map(s => ({
      stage: s.stage,
      name: s.name,
      completed: s.stage < participant.stage,
      current: s.stage === participant.stage
    }));

    return { participantId, currentStage: participant.stage, stages, totalCompleted: stages.filter(s => s.completed).length };
  }
}

export default CETCTEService;