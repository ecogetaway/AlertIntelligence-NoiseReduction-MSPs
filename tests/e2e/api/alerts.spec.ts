import { test, expect } from '@playwright/test';

/**
 * Backend Alert API Tests
 * 
 * Tests CRUD operations, filtering, pagination, and bulk operations.
 */

const API_BASE = process.env.API_BASE_URL || 'http://localhost:8000';

test.describe('Alert API Operations', () => {
  test('should list alerts with pagination', async ({ request }) => {
    const response = await request.get(`${API_BASE}/api/v1/alerts?page=1&page_size=20`);
    
    expect(response.ok()).toBeTruthy();
    
    const body = await response.json();
    expect(body).toHaveProperty('alerts');
    expect(body).toHaveProperty('total');
    expect(body).toHaveProperty('page');
    expect(body).toHaveProperty('page_size');
    expect(body).toHaveProperty('has_next');
    expect(body).toHaveProperty('has_previous');
    expect(Array.isArray(body.alerts)).toBeTruthy();
  });

  test('should filter alerts by severity', async ({ request }) => {
    const response = await request.get(`${API_BASE}/api/v1/alerts?severity=high`);
    
    expect(response.ok()).toBeTruthy();
    
    const body = await response.json();
    expect(Array.isArray(body.alerts)).toBeTruthy();
    
    // If alerts exist, verify they match severity
    if (body.alerts.length > 0) {
      body.alerts.forEach((alert: any) => {
        expect(alert.severity).toBe('high');
      });
    }
  });

  test('should filter alerts by status', async ({ request }) => {
    const response = await request.get(`${API_BASE}/api/v1/alerts?status=active`);
    
    expect(response.ok()).toBeTruthy();
    
    const body = await response.json();
    expect(Array.isArray(body.alerts)).toBeTruthy();
    
    // If alerts exist, verify they match status
    if (body.alerts.length > 0) {
      body.alerts.forEach((alert: any) => {
        expect(alert.status).toBe('active');
      });
    }
  });

  test('should search alerts by text', async ({ request }) => {
    const response = await request.get(`${API_BASE}/api/v1/alerts?search=cpu`);
    
    expect(response.ok()).toBeTruthy();
    
    const body = await response.json();
    expect(Array.isArray(body.alerts)).toBeTruthy();
    
    // If alerts exist, verify they contain search term
    if (body.alerts.length > 0) {
      body.alerts.forEach((alert: any) => {
        const searchText = `${alert.title} ${alert.description}`.toLowerCase();
        expect(searchText).toContain('cpu');
      });
    }
  });

  test('should create a new alert', async ({ request }) => {
    const newAlert = {
      title: 'Test Alert - E2E',
      description: 'This is a test alert created by Playwright',
      severity: 'medium',
      source: 'custom',
      source_id: `test-${Date.now()}`,
      fingerprint: `fp-test-${Date.now()}`,
      labels: { test: 'true', environment: 'e2e' },
      annotations: { created_by: 'playwright' },
      started_at: new Date().toISOString(),
    };

    const response = await request.post(`${API_BASE}/api/v1/alerts`, {
      data: newAlert,
    });

    expect(response.status()).toBe(200);
    
    const body = await response.json();
    expect(body).toHaveProperty('id');
    expect(body.title).toBe(newAlert.title);
    expect(body.severity).toBe(newAlert.severity);
    expect(body.fingerprint).toBe(newAlert.fingerprint);
  });

  test('should get alert by ID', async ({ request }) => {
    // First create an alert
    const newAlert = {
      title: 'Test Alert for Retrieval',
      severity: 'low',
      source: 'custom',
      source_id: `test-get-${Date.now()}`,
      fingerprint: `fp-get-${Date.now()}`,
      started_at: new Date().toISOString(),
    };

    const createResponse = await request.post(`${API_BASE}/api/v1/alerts`, {
      data: newAlert,
    });
    
    const created = await createResponse.json();
    const alertId = created.id;

    // Now retrieve it
    const getResponse = await request.get(`${API_BASE}/api/v1/alerts/${alertId}`);
    
    expect(getResponse.ok()).toBeTruthy();
    
    const body = await getResponse.json();
    expect(body.id).toBe(alertId);
    expect(body.title).toBe(newAlert.title);
  });

  test('should return 404 for non-existent alert', async ({ request }) => {
    const fakeId = '00000000-0000-0000-0000-000000000000';
    const response = await request.get(`${API_BASE}/api/v1/alerts/${fakeId}`);
    
    expect(response.status()).toBe(404);
  });

  test('should support advanced filtering', async ({ request }) => {
    const response = await request.get(
      `${API_BASE}/api/v1/alerts/advanced-filter?severity=high&status=active&page_size=10`
    );
    
    expect(response.ok()).toBeTruthy();
    
    const body = await response.json();
    expect(body).toHaveProperty('alerts');
    expect(Array.isArray(body.alerts)).toBeTruthy();
  });
});

