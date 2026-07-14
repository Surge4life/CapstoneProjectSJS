import { Request, Response } from 'express';
import { prisma } from '../config/database';
import crypto from 'crypto';

export default class PledgeController {
  submit = async (req: Request, res: Response): Promise<void> => {
    try {
      const { firstName, lastName, email, country, message } = req.body;
      const pledge = await prisma.worldPledge.create({
        data: {
          pledgeId: `PLEDGE-${Date.now()}-${crypto.randomBytes(4).toString('hex')}`,
          firstName,
          lastName,
          email,
          country,
          message: message || '',
          count: 1
        }
      });
      res.status(201).json(pledge);
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  };

  getCount = async (_req: Request, res: Response): Promise<void> => {
    try {
      const count = await prisma.worldPledge.count();
      res.json({ count });
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  };

  getAll = async (_req: Request, res: Response): Promise<void> => {
    try {
      const pledges = await prisma.worldPledge.findMany({
        orderBy: { createdAt: 'desc' },
        take: 100
      });
      res.json(pledges);
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  };

  getById = async (req: Request, res: Response): Promise<void> => {
    try {
      const pledge = await prisma.worldPledge.findUnique({
        where: { pledgeId: req.params.pledgeId }
      });
      if (!pledge) { res.status(404).json({ error: 'Pledge not found' }); return; }
      res.json(pledge);
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  };
}