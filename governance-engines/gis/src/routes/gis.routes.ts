import express from 'express';
import GISController from '../controllers/gis.controller';

const router = express.Router();
const controller = new GISController();

router.post('/decisions', controller.makeDecision);
router.get('/decisions/:decisionId', controller.getDecision);
router.get('/participant/:participantId/decisions', controller.getParticipantDecisions);
router.get('/decisions/type/:type', controller.getDecisionsByType);
router.get('/decisions/:decisionId/blocked', controller.isDecisionBlocked);
router.get('/status', controller.getSystemStatus);
router.post('/check-pillars', controller.checkPillars);

export default router;