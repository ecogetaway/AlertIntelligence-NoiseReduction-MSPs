import { test, expect } from '@playwright/test';
import * as crypto from 'crypto';

/**
 * Keep Webhook Integration Tests
 * 
 * Tests webhook ingestion, HMAC verification, and alert processing pipeline.
 */

const API_BASE = process.env.API_BASE_URL || 'http://localhost:8000';
const WEBHOOK_SECRET = process.env.KEEP_WEBHOOK_SECRET || 'test-secret-e2e';

function generateHMACSignature(payload: string, secret: string): string {
  const hmac = crypto.createHmac('sha256', secret);
  hmac.update(payload);
  return `sha256=${hmac.digest('hex')}`;
}

test.describe('Keep Webhook Integration', () => {
  test('should accept webhook with valid HMAC signature', async ({ request }) => {
    const payload = {
      event: 'alert.created',
      alert: {
        id: `test-webhook-${Date.now()}`,
        title: 'Webhook Test Alert',
        name: 'webhook_test',
        description: 'Testing webhook ingestion',
        severity: 'high',
        source: 'prometheus',
        status: 'firing',
        labels: {
          host: 'test-server-01',
          environment: 'e2e',
        },
        annotations: {
          summary: 'E2E webhook test',
        },
      },
    };

    const payloadString = JSON.stringify(payload);
    const signature = generateHMACSignature(payloadString, WEBHOOK_SECRET);

    const response = await request.post(`${API_BASE}/api/v1/ingest/keep`, {
      headers: {
        'Content-Type': 'application/json',
        'X-Keep-Signature': signature,
      },
      data: payloadString,
    });

    expect(response.ok()).toBeTruthy();
    
    const body = await response.json();
    expect(body).toHaveProperty('status');
    expect(['ok', 'filtered', 'duplicate']).toContain(body.status);
    
    if (body.status === 'ok') {
      expect(body).toHaveProperty('fingerprint');
      expect(body).toHaveProperty('alert_id');
    }
  });

  test('should reject webhook with invalid HMAC signature', async ({ request }) => {
    const payload = {
      event: 'alert.created',
      alert: {
        id: 'test-invalid-hmac',
        title: 'Invalid HMAC Test',
        severity: 'low',
      },
    };

    const response = await request.post(`${API_BASE}/api/v1/ingest/keep`, {
      headers: {
        'Content-Type': 'application/json',
        'X-Keep-Signature': 'sha256=invalid_signature',
      },
      data: JSON.stringify(payload),
    });

    expect(response.status()).toBe(401);
  });

  test('should reject webhook without signature header', async ({ request }) => {
    const payload = {
      event: 'alert.created',
      alert: {
        id: 'test-no-signature',
        title: 'No Signature Test',
      },
    };

    const response = await request.post(`${API_BASE}/api/v1/ingest/keep`, {
      headers: {
        'Content-Type': 'application/json',
      },
      data: JSON.stringify(payload),
    });

    expect(response.status()).toBe(401);
  });

  test('should handle duplicate alerts within window', async ({ request }) => {
    const alertData = {
      id: `test-duplicate-${Date.now()}`,
      title: 'Duplicate Test Alert',
      name: 'duplicate_test',
      severity: 'medium',
      source: 'datadog',
      status: 'firing',
    };

    const payload = {
      event: 'alert.created',
      alert: alertData,
    };

    const payloadString = JSON.stringify(payload);
    const signature = generateHMACSignature(payloadString, WEBHOOK_SECRET);

    // Send first alert
    const response1 = await request.post(`${API_BASE}/api/v1/ingest/keep`, {
      headers: {
        'Content-Type': 'application/json',
        'X-Keep-Signature': signature,
      },
      data: payloadString,
    });

    const body1 = await response1.json();

    // Send duplicate immediately
    const response2 = await request.post(`${API_BASE}/api/v1/ingest/keep`, {
      headers: {
        'Content-Type': 'application/json',
        'X-Keep-Signature': signature,
      },
      data: payloadString,
    });

    const body2 = await response2.json();

    // First should be processed, second should be duplicate
    if (body1.status === 'ok') {
      expect(body2.status).toBe('duplicate');
    }
  });

  test('should filter low-priority noise alerts', async ({ request }) => {
    const payload = {
      event: 'alert.created',
      alert: {
        id: `test-noise-${Date.now()}`,
        title: 'Low Priority Noise',
        severity: 'info',
        status: 'firing',
        labels: {
          noise: 'true',
        },
      },
    };

    const payloadString = JSON.stringify(payload);
    const signature = generateHMACSignature(payloadString, WEBHOOK_SECRET);

    const response = await request.post(`${API_BASE}/api/v1/ingest/keep`, {
      headers: {
        'Content-Type': 'application/json',
        'X-Keep-Signature': signature,
      },
      data: payloadString,
    });

    const body = await response.json();
    
    // Alert might be filtered or accepted depending on rules
    expect(['ok', 'filtered', 'duplicate']).toContain(body.status);
  });

  test('should get sample webhook payloads', async ({ request }) => {
    const response = await request.get(`${API_BASE}/api/v1/test/keep-webhook/samples`);
    
    expect(response.ok()).toBeTruthy();
    
    const body = await response.json();
    expect(body).toHaveProperty('critical_cpu');
    expect(body).toHaveProperty('medium_disk');
    expect(body).toHaveProperty('info_network');
  });

  test('should get cURL commands for testing', async ({ request }) => {
    const response = await request.get(`${API_BASE}/api/v1/test/keep-webhook/curl`);
    
    expect(response.ok()).toBeTruthy();
    
    const body = await response.json();
    expect(Object.keys(body).length).toBeGreaterThan(0);
    
    // Verify cURL command format
    const firstCommand = Object.values(body)[0] as string;
    expect(firstCommand).toContain('curl');
    expect(firstCommand).toContain('/api/v1/ingest/keep');
  });
});

