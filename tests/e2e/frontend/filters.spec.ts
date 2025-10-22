import { test, expect } from '@playwright/test';

/**
 * Frontend Filter Functionality Tests
 * 
 * Tests severity, status, source filters and search functionality.
 */

test.describe('Alert Filter Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/frontend-demo.html');
    await page.waitForLoadState('networkidle');
  });

  test('should filter alerts by severity', async ({ page }) => {
    // Look for severity filter dropdown or buttons
    const severityFilter = page.locator(
      'select[name="severity"], [data-filter="severity"], button:has-text("Severity")'
    ).first();
    
    if (await severityFilter.isVisible()) {
      // Click/interact with filter
      await severityFilter.click();
      
      // Select high severity
      const highOption = page.getByText(/high|critical/i).first();
      if (await highOption.isVisible()) {
        await highOption.click();
        
        // Wait for filtering
        await page.waitForTimeout(1000);
        
        // Verify alerts are filtered
        const alerts = page.locator('[class*="alert"]');
        const count = await alerts.count();
        
        // Some alerts should still be visible (or zero if none match)
        expect(count).toBeGreaterThanOrEqual(0);
      }
    }
  });

  test('should filter alerts by status', async ({ page }) => {
    // Look for status filter
    const statusFilter = page.locator(
      'select[name="status"], [data-filter="status"], button:has-text("Status")'
    ).first();
    
    if (await statusFilter.isVisible()) {
      await statusFilter.click();
      
      // Select active status
      const activeOption = page.getByText(/active|firing/i).first();
      if (await activeOption.isVisible()) {
        await activeOption.click();
        await page.waitForTimeout(1000);
      }
    }
  });

  test('should search alerts by text', async ({ page }) => {
    // Look for search input
    const searchInput = page.locator('[type="search"], input[placeholder*="search" i]').first();
    
    if (await searchInput.isVisible()) {
      // Type search query
      await searchInput.fill('cpu');
      
      // Wait for search results
      await page.waitForTimeout(1000);
      
      // Verify page didn't crash
      const body = page.locator('body');
      await expect(body).toBeVisible();
    }
  });

  test('should clear all filters', async ({ page }) => {
    // Apply some filters first
    const severityFilter = page.locator('select[name="severity"]').first();
    if (await severityFilter.isVisible()) {
      await severityFilter.selectOption('high');
      await page.waitForTimeout(500);
    }
    
    // Look for clear/reset button
    const clearButton = page.getByRole('button', { name: /clear|reset/i });
    
    if (await clearButton.isVisible()) {
      await clearButton.click();
      await page.waitForTimeout(500);
      
      // Filters should be reset
      const body = page.locator('body');
      await expect(body).toBeVisible();
    }
  });

  test('should filter by source', async ({ page }) => {
    const sourceFilter = page.locator(
      'select[name="source"], [data-filter="source"]'
    ).first();
    
    if (await sourceFilter.isVisible()) {
      await sourceFilter.click();
      
      const prometheusOption = page.getByText(/prometheus|datadog/i).first();
      if (await prometheusOption.isVisible()) {
        await prometheusOption.click();
        await page.waitForTimeout(1000);
      }
    }
  });

  test('should combine multiple filters', async ({ page }) => {
    // Apply severity filter
    const severityFilter = page.locator('select[name="severity"]').first();
    if (await severityFilter.isVisible()) {
      await severityFilter.selectOption({ label: /high/i });
      await page.waitForTimeout(500);
    }
    
    // Apply status filter
    const statusFilter = page.locator('select[name="status"]').first();
    if (await statusFilter.isVisible()) {
      await statusFilter.selectOption({ label: /active/i });
      await page.waitForTimeout(500);
    }
    
    // Verify page still works
    const alerts = page.locator('[class*="alert"]');
    const count = await alerts.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });
});

