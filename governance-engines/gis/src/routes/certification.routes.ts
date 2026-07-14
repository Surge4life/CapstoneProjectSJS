import express from 'express';
import CertificationController from '../controllers/certification.controller';

const router = express.Router();
const controller = new CertificationController();

router.post('/certifications', controller.issue);
router.get('/certifications/:id', controller.getById);
router.post('/certifications/:id/verify', controller.verify);
router.get('/participants/:participantId/certifications', controller.getByParticipant);

export default router;
