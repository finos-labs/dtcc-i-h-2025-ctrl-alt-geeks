// routes/api.js
const express = require('express');
const router = express.Router();
const { proxyRequest } = require('../utils/httpClient');
const { proxyRequest1 } = require('../utils/httpClient');
const { proxyRequest2 } = require('../utils/httpClient');
const { proxyRequest3 } = require('../utils/httpClient');
const { proxyRequestN8n } = require('../utils/httpClient');

router.post('/getmessage', async (req, res) => {
  try {
    const response = await proxyRequest1({
      method: 'POST',
      headers: req.headers,
      body: req.body
    });
    
    res.status(response.status).json(response.data);
  } catch (error) {
    console.error('Proxy error:', error);
    
    const status = error.response?.status || 500;
    const errorData = error.response?.data || { error: error.message };
    
    res.status(status).json({
      error: 'Proxy request failed',
      details: errorData
    });
  }
});

router.post('/zerodha-agent-chat', async (req, res) => {
  try {
    const response = await proxyRequest2({
      method: 'POST',
      url: 'http://54.69.201.106:5678/webhook/zerodha-agent-chat',
      headers: req.headers,
      body: req.body
    });
    
    res.status(response.status).json(response.data);
  } catch (error) {
    console.error('Zerodha Agent Chat Proxy error:', error);
    
    const status = error.response?.status || 500;
    const errorData = error.response?.data || { error: error.message };
    
    res.status(status).json({
      error: 'Zerodha Agent Chat proxy request failed',
      details: errorData
    });
  }
});

router.get('/cors-proxy/clients', async (req, res) => {
  try {
    const response = await proxyRequest({
      method: 'GET',
      url: 'http://ec2-18-223-241-107.us-east-2.compute.amazonaws.com:3001/agentic-mcp-server/clients',
      headers: req.headers
    });
    res.status(response.status).json(response.data);
  } catch (error) {
    console.error('CORS Proxy error:', error);
    const status = error.response?.status || 500;
    const errorData = error.response?.data || { error: error.message };
    res.status(status).json({
      error: 'CORS proxy request failed',
      details: errorData
    });
  }
});

router.get('/leads', async (req, res) => {
  try {
    const response = await proxyRequest3({
      method: 'GET',
      url: 'http://54.70.91.219/leads',
      headers: req.headers
    });
    res.status(response.status).json(response.data);
  } catch (error) {
    console.error('Leads Proxy error:', error);
    const status = error.response?.status || 500;
    const errorData = error.response?.data || { error: error.message };
    res.status(status).json({
      error: 'Leads proxy request failed',
      details: errorData
    });
  }
});

router.post('/n8n-chat', async (req, res) => {
  try {
    const response = await proxyRequestN8n({
      method: 'POST',
      url: 'https://pawarpan.app.n8n.cloud/webhook/chat',
      headers: req.headers,
      body: req.body
    });

    res.status(response.status).json(response.data);
  } catch (error) {
    console.error('n8n Chat Proxy error:', error);

    const status = error.response?.status || 500;
    const errorData = error.response?.data || { error: error.message };

    res.status(status).json({
      error: 'n8n Chat proxy request failed',
      details: errorData
    });
  }
});

module.exports = router;