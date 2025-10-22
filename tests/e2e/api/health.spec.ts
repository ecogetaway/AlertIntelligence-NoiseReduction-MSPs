import { test, expect } from '@playwright/test';

/**
 * Backend API Health Check Tests
 * 
 * Verifies backend is running and all systems operational.
 */

const API_BASE = process.env.API_BASE_URL || 'http://localhost:8000';

test.describe('Backend Health Checks', () => {
  test('should return healthy status from /health endpoint', async ({ request }) => {
    const response = await request.get(`${API_BASE}/health`);
    
    expect(response.ok()).toBeTruthy();
    expect(response.status()).toBe(200);
    
    const body = await response.json();
    expect(body).toHaveProperty('status');
    expect(body.status).toBe('healthy');
    expect(body).toHaveProperty('database');
    expect(body.database).toBe('connected');
  });

  test('should return basic info from root endpoint', async ({ request }) => {
    const response = await request.get(`${API_BASE}/`);
    
    expect(response.ok()).toBeTruthy();
    
    const body = await response.json();
    expect(body).toHaveProperty('name');
    expect(body.name).toContain('MSP Alert Intelligence');
    expect(body).toHaveProperty('version');
    expect(body).toHaveProperty('features');
    expect(Array.isArray(body.features)).toBeTruthy();
  });

  test('should have OpenAPI documentation available', async ({ request }) => {
    const response = await request.get(`${API_BASE}/docs`);
    
    expect(response.ok()).toBeTruthy();
    expect(response.status()).toBe(200);
    
    const html = await response.text();
    expect(html).toContain('swagger-ui');
  });

  test('should return agents status when available', async ({ request }) => {
    const response = await request.get(`${API_BASE}/api/v1/agents/status`);
    
    // May be 503 if agents not configured, or 200 if they are
    if (response.status() === 200) {
      const body = await response.json();
      expect(body).toHaveProperty('bedrock_agentcore');
      expect(body).toHaveProperty('strands_agents');
    } else {
      expect(response.status()).toBe(503);
    }
  });
});

