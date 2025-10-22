import { test, expect } from '@playwright/test';

/**
 * Smoke Tests - Basic functionality checks
 * 
 * These tests verify that the basic infrastructure is working
 * without requiring complex setup or external dependencies.
 */

test.describe('Smoke Tests', () => {
  test('should serve frontend demo page', async ({ page }) => {
    await page.goto('/frontend-demo.html');
    
    // Check that page loads without errors
    await expect(page).toHaveTitle(/MSP Alert Intelligence/);
    
    // Check that React components are rendering
    const body = page.locator('body');
    await expect(body).toBeVisible();
  });

  test('should serve static demo page', async ({ page }) => {
    await page.goto('/frontend-simple.html');
    
    // Check that page loads
    await expect(page).toHaveTitle(/MSP Alert Intelligence/);
    
    const body = page.locator('body');
    await expect(body).toBeVisible();
  });

  test('should serve keep integration demo', async ({ page }) => {
    await page.goto('/keep-integration-demo.html');
    
    // Check that page loads
    await expect(page).toHaveTitle(/Keep Integration/);
    
    const body = page.locator('body');
    await expect(body).toBeVisible();
  });

  test('should serve main index page', async ({ page }) => {
    await page.goto('/index.html');
    
    // Check that page loads
    await expect(page).toHaveTitle(/MSP Alert Intelligence/);
    
    const body = page.locator('body');
    await expect(body).toBeVisible();
  });
});
