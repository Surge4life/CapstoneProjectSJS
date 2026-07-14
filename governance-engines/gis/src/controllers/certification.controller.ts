import { Request, Response } from 'express';
import { prisma } from '../config/database';

/**
 * CertificationController — Bronze/Silver/Gold/Platinum/Specialist tiers.
 * Document 00 §11.1 (GBS-SETHS Consolidated Super Framework), Document 04
 * (Skills Passport Technical Standard).
 *
 * This file, plus certification.routes.ts and the franchise pair alongside
 * it, were missing from the original package — index.ts imported both but
 * neither existed, so the service would not have started. Written to match
 * the existing controller pattern (see participant.controller.ts,
 * pledge.controller.ts) and the Certification/CertificationTier Prisma model
 * already defined in schema.prisma.
 */
export default class CertificationController {
  issue = async (req: Request, res: Response): Promise<void> => {
    try {
      const { participantId, tier, name, description, stream, gisDecisionId } = req.body;
      const validTiers = ['BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'SPECIALIST'];
      if (!validTiers.includes(tier)) {
        res.status(400).json({ error: `tier must be one of ${validTiers.join(', ')}` });
        return;
      }
      const cert = await prisma.certification.create({
        data: {
          participantId, tier, name, description: description || '', stream: stream || '',
          verified: Boolean(gisDecisionId), gisVerified: Boolean(gisDecisionId),
          gisDecisionId: gisDecisionId || null,
        },
      });
      res.status(201).json(cert);
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  };

  getByParticipant = async (req: Request, res: Response): Promise<void> => {
    try {
      const { participantId } = req.params;
      const certs = await prisma.certification.findMany({
        where: { participantId },
        orderBy: { issuedDate: 'asc' },
      });
      res.json(certs);
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  };

  verify = async (req: Request, res: Response): Promise<void> => {
    try {
      const { id } = req.params;
      const { verifiedBy, verificationHash } = req.body;
      const cert = await prisma.certification.update({
        where: { id },
        data: { verified: true, verifiedBy, verificationHash },
      });
      res.json(cert);
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  };

  getById = async (req: Request, res: Response): Promise<void> => {
    try {
      const { id } = req.params;
      const cert = await prisma.certification.findUnique({ where: { id } });
      if (!cert) {
        res.status(404).json({ error: 'certification not found' });
        return;
      }
      res.json(cert);
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  };
}
