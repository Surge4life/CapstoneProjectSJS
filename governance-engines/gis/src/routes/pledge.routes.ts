import express from 'express';
import PledgeController from '../controllers/pledge.controller';

const router = express.Router();
const controller = new PledgeController();

router.post('/pledges', controller.submit);
router.get('/pledges/count', controller.getCount);
router.get('/pledges', controller.getAll);
router.get('/pledges/:pledgeId', controller.getById);

export default router;