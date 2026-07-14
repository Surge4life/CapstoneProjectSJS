import express from 'express';
import ParticipantController from '../controllers/participant.controller';

const router = express.Router();
const controller = new ParticipantController();

router.post('/participants', controller.create);
router.get('/participants/:id', controller.getById);
router.put('/participants/:id', controller.update);
router.delete('/participants/:id', controller.delete);
router.post('/participants/:id/advance', controller.advanceStage);
router.get('/participants/:id/progress', controller.getProgress);
router.post('/participants/:id/contract', controller.signContract);
router.get('/participants/:id/passport', controller.getPassport);
router.put('/participants/:id/ai-readiness', controller.updateAIReadiness);

export default router;