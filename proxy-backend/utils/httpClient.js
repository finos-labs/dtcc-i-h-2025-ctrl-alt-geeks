// utils/httpClient.js
const axios = require('axios');
const logger = require('./logger');

const TARGET_API = process.env.TARGET_API;

async function proxyRequest1({ method, headers, body }) {
  const config = {
    method: method.toLowerCase(),
    url: TARGET_API,
    headers: {
      'Content-Type': 'application/json'
    },
    data: body
  };

  logger.debug(`Proxying request to: ${TARGET_API}`);
  logger.debug(`Request body: ${JSON.stringify(body)}`);

  try {
    const response = await axios(config);
    logger.debug(`Proxy response status: ${response.status}`);
    return response;
  } catch (error) {
    logger.error(`Proxy request failed: ${error.message}`);
    
    if (error.response) {
      // Server responded with non-2xx status
      logger.error(`Target API response: ${error.response.status} - ${JSON.stringify(error.response.data)}`);
      throw error;
    } else if (error.request) {
      // No response received
      throw new Error('No response received from target API');
    } else {
      // Request setup error
      throw new Error(`Request setup error: ${error.message}`);
    }
  }
}

async function proxyRequest({ method, url, headers, body }) {
  const axios = require('axios');
  const targetUrl = url || 'DEFAULT_URL_HERE';
  return axios({
    method,
    url: targetUrl,
    headers,
    data: body
  });
}

async function proxyRequest3({ method, url, headers, body }) {
  const axios = require('axios');
  const targetUrl = url;
  return axios({
    method,
    url: targetUrl,
    headers: {
      'Content-Type': 'application/json'
    }
  });
}

async function proxyRequest2({ method, url, headers, body }) {
  const axios = require('axios');
  const targetUrl = url;
  return axios({
    method: method.toLowerCase(),
    url: targetUrl,
    headers,
    data: body
  });
}

async function proxyRequestN8n({ method, url, headers, body }) {
  try {
    const response = await axios({
      method,
      url,
      headers: {
      'Content-Type': 'application/json'
    },
      data: body,
    });
    return {
      status: response.status,
      data: response.data
    };
  } catch (error) {
    throw error;
  }
}

module.exports = { proxyRequest, proxyRequest1, proxyRequest2, proxyRequest3, proxyRequestN8n };