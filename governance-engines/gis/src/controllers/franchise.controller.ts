import { Request, Response } from 'express';
import { prisma } from '../config/database';

/**
 * FranchiseController — franchise/employer governance: reporting and
 * tracking compliance violations against the Absorption Commitment Clause
 * and the Twelve Constitutional Pillars (Document 05 §6.3, Document 08 Risk
 * & Failure Framework). Maps to the ComplianceViolation Prisma model — this
 * package does not define a separate FranchiseNode model; the live Python
 * backend (platform-core/app/services/gbs_engine.py) carries the full
 * franchise node registry. This controller stays scoped to what this
 * package's schema actually models: violations, not node CRUD.
 *
 * Missing from the original upload (index.ts imported it, the file did not
 * exist) — written to match the existing controller pattern.
 */
export default class FranchiseController {
  reportViolation = async (req: Request, res: Response): Promise<void> => {
    try {
      const { employerId, franchiseId, pillarId, violationType, description, severity, evidence } = req.body;
      const validTypes = [
        'OUTCOME_DATA_MANIPULATION', 'LEARNERSHIP_CREDIT_ABUSE', 'CONSTITUTIONAL_VIOLATION',
        'ABSORPTION_COMMITMENT_BREACH', 'GOVERNANCE_VIOLATION', 'ANTI_CORRUPTION_VIOLATION',
        'TRANSPARENCY_VIOLATION', 'HUMAN_DIGNITY_VIOLATION', 'AI_PRIMACY_VIOLATION',
      ];
      const validSeverities = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'];
      if (!validTypes.includes(violationType)) {
        res.status(400).json({ error: `violationType must be one of ${validTypes.join(', ')}` });
        return;
      }
      if (!validSeverities.includes(severity)) {
        res.status(400).json({ error: `severity must be one of ${validSeverities.join(', ')}` });
        return;
      }
      const violation = await prisma.complianceViolation.create({
        data: {
          violationId: `VIOL-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
          employerId, franchiseId: franchiseId || null, pillarId: pillarId || null,
          violationType, description, severity, evidence: evidence || undefined,
          status: 'REPORTED',
        },
      });
      res.status(201).json(violation);
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  };

  getByEmployer = async (req: Request, res: Response): Promise<void> => {
    try {
      const { employerId } = req.params;
      const violations = await prisma.complianceViolation.findMany({
        where: { employerId },
        orderBy: { reportedAt: 'desc' },
      });
      res.json(violations);
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  };

  updateStatus = async (req: Request, res: Response): Promise<void> => {
    try {
      const { id } = req.params;
      const { status, reviewedBy, resolution } = req.body;
      const validStatuses = ['REPORTED', 'UNDER_INVESTIGATION', 'CONFIRMED', 'REMEDIATED', 'RESOLVED', 'APPEALED'];
      if (!validStatuses.includes(status)) {
        res.status(400).json({ error: `status must be one of ${validStatuses.join(', ')}` });
        return;
      }
      const data: any = { status, reviewedBy, reviewedAt: new Date() };
      if (status === 'RESOLVED') {
        data.resolution = resolution;
        data.resolvedAt = new Date();
        data.resolvedBy = reviewedBy;
      }
      const violation = await prisma.complianceViolation.update({ where: { id }, data });
      res.json(violation);
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  };

  getById = async (req: Request, res: Response): Promise<void> => {
    try {
      const { id } = req.params;
      const violation = await prisma.complianceViolation.findUnique({ where: { id } });
      if (!violation) {
        res.status(404).json({ error: 'violation not found' });
        return;
      }
      res.json(violation);
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  };
}
