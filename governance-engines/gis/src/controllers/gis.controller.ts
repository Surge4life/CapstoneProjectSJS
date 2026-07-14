import { Request, Response } from 'express';
import GISService from '../services/gis.service';

export default class GISController {
  private gisService: GISService;

  constructor() {
    this.gisService = new GISService();
  }

  makeDecision = async (req: Request, res: Response): Promise<void> => {
    try {
      const result = await this.gisService.makeDecision(req.body);
      res.json(result);
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  };

  getDecision = async (req: Request, res: Response): Promise<void> => {
    try {
      const result = await this.gisService.getDecision(req.params.decisionId);
      res.json(result);
    } catch (error: any) {
      res.status(404).json({ error: error.message });
    }
  };

  getParticipantDecisions = async (req: Request, res: Response): Promise<void> => {
    try {
      const result = await this.gisService.getParticipantDecisions(req.params.participantId);
      res.json(result);
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  };

  getDecisionsByType = async (_req: Request, res: Response): Promise<void> => {
    // Simplified - in production, add proper service method
    res.json({ message: 'Get decisions by type' });
  };

  isDecisionBlocked = async (_req: Request, res: Response): Promise<void> => {
    res.json({ blocked: false });
  };

  getSystemStatus = async (_req: Request, res: Response): Promise<void> => {
    res.json({
      status: 'operational',
      failClosed: process.env.GIS_FAIL_CLOSED === 'true',
      pillars: 12,
      version: '1.0.0'
    });
  };

  checkPillars = async (_req: Request, res: Response): Promise<void> => {
    // Simplified - in production, use the GIS service
    res.json({ allPassed: true });
  };
}