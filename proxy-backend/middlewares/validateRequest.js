// middlewares/validateRequest.js
const logger = require('../utils/logger');

function validateRequestBody(req, res, next) {
  if (req.method !== 'POST') {
    return next();
  }

  if (!req.body || typeof req.body !== 'object') {
    logger.warn('Invalid request body format');
    return res.status(400).json({ error: 'Request body must be a JSON object' });
  }

  if (!req.body.chat) {
    logger.warn('Missing required field: chat');
    return res.status(400).json({ error: 'Missing required field: chat' });
  }

  next();
}

module.exports = validateRequestBody;