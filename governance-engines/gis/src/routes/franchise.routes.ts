import express from 'express';
import FranchiseController from '../controllers/franchise.controller';

const router = express.Router();
const controller = new FranchiseController();

router.post('/franchise/violations', controller.reportViolation);
router.get('/franchise/violations/:id', controller.getById);
router.patch('/franchise/violations/:id/status', controller.updateStatus);
router.get('/franchise/employers/:employerId/violations', controller.getByEmployer);

export default router;
