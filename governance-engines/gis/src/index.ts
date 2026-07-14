import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import dotenv from 'dotenv';
import { prisma } from './config/database';
import { logger } from './utils/logger';

// Import routes
import gisRoutes from './routes/gis.routes';
import participantRoutes from './routes/participant.routes';
import franchiseRoutes from './routes/franchise.routes';
import certificationRoutes from './routes/certification.routes';
import pledgeRoutes from './routes/pledge.routes';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Security middleware
app.use(helmet());
app.use(cors({
  origin: process.env.CORS_ORIGIN || '*',
  credentials: true
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
});
app.use('/api', limiter);

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Health check
app.get('/health', (_req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    failClosed: process.env.GIS_FAIL_CLOSED === 'true'
  });
});

// API routes
app.use('/api/gis', gisRoutes);
app.use('/api/participants', participantRoutes);
app.use('/api/franchise', franchiseRoutes);
app.use('/api/certifications', certificationRoutes);
app.use('/api/pledges', pledgeRoutes);

// Error handling
app.use((err: any, _req: express.Request, res: express.Response, _next: express.NextFunction) => {
  logger.error(err.stack);
  res.status(err.status || 500).json({
    error: err.message || 'Internal Server Error',
    status: err.status || 500
  });
});

app.use((req, res) => {
  res.status(404).json({ error: 'Not Found', path: req.path });
});

app.listen(PORT, () => {
  logger.info(`G.O.D.S. Intelligence System running on port ${PORT}`);
  logger.info(`Environment: ${process.env.NODE_ENV}`);
  logger.info(`Fail-closed mode: ${process.env.GIS_FAIL_CLOSED === 'true'}`);
});

process.on('SIGTERM', async () => {
  logger.info('SIGTERM received, closing...');
  await prisma.$disconnect();
  process.exit(0);
});

process.on('SIGINT', async () => {
  logger.info('SIGINT received, closing...');
  await prisma.$disconnect();
  process.exit(0);
});

export default app;