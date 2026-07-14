import { prisma } from '../config/database';
import crypto from 'crypto';

export class AuditService {
  async logAction(action: any): Promise<any> {
    const recordId = `UDOC-${Date.now()}-${crypto.randomBytes(4).toString('hex')}`;
    const sealable = JSON.stringify({ recordId, ...action, timestamp: new Date().toISOString() });
    const sealHash = crypto.createHash('sha256').update(sealable + process.env.JWT_SECRET).digest('hex');

    return await prisma.auditRecord.create({
      data: {
        recordId,
        domain: action.domain,
        entityId: action.entityId,
        entityType: action.entityType,
        action: action.action,
        performedBy: action.performedBy,
        beforeState: action.beforeState || {},
        afterState: action.afterState || {},
        pillarId: action.pillarId || null,
        pillarCompliant: action.pillarCompliant || null,
        gisDecisionId: action.gisDecisionId || null,
        sealHash
      }
    });
  }

  async sealRecord(recordId: string, sealedBy: string): Promise<any> {
    const record = await prisma.auditRecord.findUnique({ where: { recordId } });
    if (!record) throw new Error(`Record ${recordId} not found`);
    
    const sealable = JSON.stringify({ ...record, sealedAt: new Date().toISOString() });
    const sealHash = crypto.createHash('sha256').update(sealable + process.env.JWT_SECRET).digest('hex');

    return await prisma.auditRecord.update({
      where: { recordId },
      data: { isSealed: true, sealedAt: new Date(), sealedBy, sealHash }
    });
  }

  async verifySeal(recordId: string): Promise<boolean> {
    const record = await prisma.auditRecord.findUnique({ where: { recordId } });
    if (!record || !record.isSealed) return false;
    const sealable = JSON.stringify({ ...record, sealedAt: record.sealedAt?.toISOString() });
    const calculated = crypto.createHash('sha256').update(sealable + process.env.JWT_SECRET).digest('hex');
    return record.sealHash === calculated;
  }

  async getEntityAuditTrail(entityId: string, entityType: string): Promise<any[]> {
    return await prisma.auditRecord.findMany({
      where: { entityId, entityType },
      orderBy: { createdAt: 'desc' }
    });
  }

  async issueComplianceWarning(employerId: string, violationType: string, description: string, severity: string, evidence?: any): Promise<any> {
    return await prisma.complianceViolation.create({
      data: {
        violationId: `VIOL-${Date.now()}-${crypto.randomBytes(4).toString('hex')}`,
        employerId,
        violationType: violationType as any,
        description,
        severity: severity as any,
        evidence: evidence || {},
        status: 'REPORTED'
      }
    });
  }

  async getEmployerViolations(employerId: string): Promise<any[]> {
    return await prisma.complianceViolation.findMany({
      where: { employerId },
      orderBy: { createdAt: 'desc' }
    });
  }
}

export default AuditService;