import { Request, Response } from 'express';
import { prisma } from '../config/database';
import CETCTEService from '../services/cetcte.service';

export default class ParticipantController {
  private cetcteService: CETCTEService;

  constructor() {
    this.cetcteService = new CETCTEService();
  }

  create = async (req: Request, res: Response): Promise<void> => {
    try {
      const data = req.body;
      const participant = await prisma.participant.create({
        data: {
          gbsId: `GBS-${Date.now()}-${Math.random().toString(36).substr(2, 6)}`,
          firstName: data.firstName,
          lastName: data.lastName,
          email: data.email,
          phone: data.phone,
          dateOfBirth: new Date(data.dateOfBirth),
          nationalId: data.nationalId,
          country: data.country || 'South Africa',
          targetCohort: data.targetCohort || 1,
          status: 'INTAKE',
          stage: 0,
          phase: 'Intake'
        }
      });
      res.status(201).json(participant);
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  };

  getById = async (req: Request, res: Response): Promise<void> => {
    try {
      const participant = await prisma.participant.findUnique({
        where: { id: req.params.id },
        include: { certifications: true, employmentRecords: true }
      });
      if (!participant) { res.status(404).json({ error: 'Participant not found' }); return; }
      res.json(participant);
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  };

  update = async (req: Request, res: Response): Promise<void> => {
    try {
      const participant = await prisma.participant.update({
        where: { id: req.params.id },
        data: req.body
      });
      res.json(participant);
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  };

  delete = async (req: Request, res: Response): Promise<void> => {
    try {
      await prisma.participant.delete({ where: { id: req.params.id } });
      res.status(204).send();
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  };

  advanceStage = async (req: Request, res: Response): Promise<void> => {
    try {
      const result = await this.cetcteService.advanceStage(req.params.id, req.body.facilitatorId || 'system');
      res.json(result);
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  };

  getProgress = async (req: Request, res: Response): Promise<void> => {
    try {
      const result = await this.cetcteService.getParticipantProgress(req.params.id);
      res.json(result);
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  };

  signContract = async (req: Request, res: Response): Promise<void> => {
    try {
      const participant = await prisma.participant.update({
        where: { id: req.params.id },
        data: {
          selfAffirmationContract: req.body,
          status: 'ACTIVE'
        }
      });
      res.json(participant);
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  };

  getPassport = async (req: Request, res: Response): Promise<void> => {
    try {
      const result = await this.cetcteService.generateSkillsPassport(req.params.id);
      res.json(result);
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  };

  updateAIReadiness = async (req: Request, res: Response): Promise<void> => {
    try {
      const result = await this.cetcteService.updateAIReadiness(req.params.id, req.body);
      res.json(result);
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  };
}