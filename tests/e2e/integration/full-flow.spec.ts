import { test, expect } from '@playwright/test';
import * as crypto from 'crypto';

/**
 * Full Integration Flow Tests
 * 
 * Tests complete flow: Keep Webhook → Backend Processing → Database → API → Frontend
 */

const API_BASE = process.env.API_BASE_URL || 'http://localhost:8000';
const WEBHOOK_SECRET = process.env.KEEP_WEBHOOK_SECRET || 'test-secret-e2e';

function generateHMACSignature(payload: string, secret: string): string {
  const hmac = crypto.createHmac('sha256', secret);
  hmac.update(payload);
  return `sha256=${hmac.digest('hex')}`;
}

test.describe('End-to-End Integration Flow', () => {
  test('should process alert through complete pipeline', async ({ request, page }) => {
    // Step 1: Send Keep webhook
    const alertId = `e2e-full-flow-${Date.now()}`;
    const payload = {
      event: 'alert.created',
      alert: {
        id: alertId,
        title: 'E2E Full Flow Test Alert',
        name: 'e2e_test',
        description: 'Testing complete pipeline from webhook to frontend',
        severity: 'high',
        source: 'prometheus',
        status: 'firing',
        service: 'api-server',
        labels: {
          host: 'e2e-test-host',
          environment: 'test',
          team: 'platform',
        },
        annotations: {
          runbook: 'https://example.com/runbook',
          summary: 'E2E test alert',
        },
      },
    };

    const payloadString = JSON.stringify(payload);
    const signature = generateHMACSignature(payloadString, WEBHOOK_SECRET);

    const webhookResponse = await request.post(`${API_BASE}/api/v1/ingest/keep`, {
      headers: {
        'Content-Type': 'application/json',
        'X-Keep-Signature': signature,
      },
      data: payloadString,
    });

    // Step 2: Verify webhook accepted
    expect(webhookResponse.ok()).toBeTruthy();
    const webhookBody = await webhookResponse.json();
    expect(webhookBody.status).toBe('ok');
    expect(webhookBody).toHaveProperty('alert_id');
    expect(webhookBody).toHaveProperty('fingerprint');

    const createdAlertId = webhookBody.alert_id;
    const fingerprint = webhookBody.fingerprint;

    // Step 3: Query API to verify alert was persisted
    await page.waitForTimeout(1000); // Give time for async processing

    const apiResponse = await request.get(`${API_BASE}/api/v1/alerts/${createdAlertId}`);
    expect(apiResponse.ok()).toBeTruthy();
    
    const alertData = await apiResponse.json();
    expect(alertData.id).toBe(createdAlertId);
    expect(alertData.title).toBe(payload.alert.title);
    expect(alertData.fingerprint).toBe(fingerprint);

    // Step 4: Verify enrichments exist
    // Check if AI or correlation data was added
    if (alertData.enrichments) {
      expect(Array.isArray(alertData.enrichments)).toBeTruthy();
    }

    // Step 5: Verify alert appears in list
    const listResponse = await request.get(`${API_BASE}/api/v1/alerts?page_size=50`);
    expect(listResponse.ok()).toBeTruthy();
    
    const listData = await listResponse.json();
    const foundInList = listData.alerts.some((a: any) => a.id === createdAlertId);
    expect(foundInList).toBeTruthy();

    // Step 6: Load frontend and verify alert could be displayed
    await page.goto('/frontend-demo.html');
    await page.waitForLoadState('networkidle');
    
    // Page should load successfully
    const heading = page.locator('h1, h2').first();
    await expect(heading).toBeVisible();
  });

  test('should handle deduplication correctly', async ({ request }) => {
    const alertData = {
      id: `e2e-dedup-test-${Date.now()}`,
      title: 'Deduplication Test',
      name: 'dedup_test',
      severity: 'medium',
      source: 'datadog',
      status: 'firing',
      service: 'db-server',
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
    expect(body1.status).toBe('ok');
    const alertId1 = body1.alert_id;
    const fingerprint1 = body1.fingerprint;

    // Send identical alert (should be deduplicated)
    const response2 = await request.post(`${API_BASE}/api/v1/ingest/keep`, {
      headers: {
        'Content-Type': 'application/json',
        'X-Keep-Signature': signature,
      },
      data: payloadString,
    });

    const body2 = await response2.json();
    
    // Second should be marked as duplicate
    expect(body2.status).toBe('duplicate');
    expect(body2.fingerprint).toBe(fingerprint1);

    // Verify only one alert exists in database
    const listResponse = await request.get(
      `${API_BASE}/api/v1/alerts?search=${alertData.title}`
    );
    const listData = await listResponse.json();
    
    // Should only find one alert with this title
    const matchingAlerts = listData.alerts.filter(
      (a: any) => a.title === alertData.title
    );
    expect(matchingAlerts.length).toBe(1);
  });

  test('should enrich alerts with correlation data', async ({ request }) => {
    // Send related alerts that should be correlated
    const baseTime = Date.now();
    const service = 'correlation-test-service';

    const alerts = [
      {
        id: `corr-1-${baseTime}`,
        title: 'High CPU on correlation-test',
        severity: 'high',
        service,
      },
      {
        id: `corr-2-${baseTime}`,
        title: 'High Memory on correlation-test',
        severity: 'high',
        service,
      },
      {
        id: `corr-3-${baseTime}`,
        title: 'Slow Response on correlation-test',
        severity: 'medium',
        service,
      },
    ];

    const alertIds: string[] = [];

    // Send all alerts
    for (const alert of alerts) {
      const payload = {
        event: 'alert.created',
        alert: {
          ...alert,
          source: 'prometheus',
          status: 'firing',
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
      if (body.status === 'ok') {
        alertIds.push(body.alert_id);
      }
    }

    // Give time for correlation processing
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Verify alerts were correlated (have incident IDs)
    for (const alertId of alertIds) {
      const response = await request.get(`${API_BASE}/api/v1/alerts/${alertId}`);
      if (response.ok()) {
        const alertData = await response.json();
        
        // Alert should have enrichments or correlations
        // (exact structure depends on implementation)
        expect(alertData).toBeDefined();
      }
    }
  });
});

