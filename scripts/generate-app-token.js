#!/usr/bin/env node
/**
 * GitHub App Installation Token Generator
 *
 * Usage: node scripts/generate-app-token.js
 * Output: Installation access token (stdout)
 */

const crypto = require('crypto');
const https = require('https');
const fs = require('fs');
const path = require('path');

// Configuration
const APP_ID = '2639463';
const INSTALLATION_ID = '103780638';
const PRIVATE_KEY_PATH = path.join(__dirname, '..', 'seven-poker-agent.2026-01-11.private-key.pem');

function base64url(data) {
  return Buffer.from(data)
    .toString('base64')
    .replace(/=/g, '')
    .replace(/\+/g, '-')
    .replace(/\//g, '_');
}

function generateJWT(appId, privateKey) {
  const now = Math.floor(Date.now() / 1000);

  const header = {
    alg: 'RS256',
    typ: 'JWT'
  };

  const payload = {
    iat: now - 60,        // Issued 60 seconds ago (clock drift)
    exp: now + (10 * 60), // Expires in 10 minutes
    iss: appId
  };

  const encodedHeader = base64url(JSON.stringify(header));
  const encodedPayload = base64url(JSON.stringify(payload));
  const signatureInput = `${encodedHeader}.${encodedPayload}`;

  const sign = crypto.createSign('RSA-SHA256');
  sign.update(signatureInput);
  const signature = sign.sign(privateKey, 'base64')
    .replace(/=/g, '')
    .replace(/\+/g, '-')
    .replace(/\//g, '_');

  return `${signatureInput}.${signature}`;
}

function httpsRequest(options, postData = null) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(JSON.parse(data));
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${data}`));
        }
      });
    });
    req.on('error', reject);
    if (postData) req.write(postData);
    req.end();
  });
}

async function getInstallationToken(jwt, installationId) {
  const options = {
    hostname: 'api.github.com',
    path: `/app/installations/${installationId}/access_tokens`,
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${jwt}`,
      'Accept': 'application/vnd.github+json',
      'User-Agent': 'seven-poker-agent',
      'X-GitHub-Api-Version': '2022-11-28'
    }
  };

  return httpsRequest(options, '');
}

async function main() {
  try {
    // Read private key
    if (!fs.existsSync(PRIVATE_KEY_PATH)) {
      console.error(`Error: Private key not found at ${PRIVATE_KEY_PATH}`);
      process.exit(1);
    }

    const privateKey = fs.readFileSync(PRIVATE_KEY_PATH, 'utf8');

    // Generate JWT
    const jwt = generateJWT(APP_ID, privateKey);

    // Get installation token
    const response = await getInstallationToken(jwt, INSTALLATION_ID);

    // Output only the token
    console.log(response.token);
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

main();
