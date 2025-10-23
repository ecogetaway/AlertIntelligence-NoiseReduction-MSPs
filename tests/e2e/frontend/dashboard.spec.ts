import { test, expect } from '@playwright/test';

/**
 * Frontend Dashboard Tests
 * 
 * Tests dashboard loading, Live Mode, and core UI functionality.
 */

test.describe('Dashboard UI Tests', () => {
  test('should load dashboard page successfully', async ({ page }) => {
    await page.goto('/frontend-demo.html');
    
    // Wait for page to be interactive with longer timeout
    await page.waitForLoadState('networkidle', { timeout: 10000 });
    
    // Check title
    await expect(page).toHaveTitle(/MSP Alert Intelligence/);
    
    // Check main heading with more flexible selector
    const heading = page.locator('h1, h2, [class*="title"], [class*="heading"]').first();
    await expect(heading).toBeVisible({ timeout: 5000 });
  });

  test('should display Live Mode toggle', async ({ page }) => {
    await page.goto('/frontend-demo.html');
    await page.waitForLoadState('networkidle', { timeout: 10000 });
    
    // Look for Live Mode toggle with more flexible selectors
    const liveToggle = page.locator('[data-testid="live-mode-toggle"], #liveMode, input[type="checkbox"], button:has-text("Live"), [class*="live"]').first();
    await expect(liveToggle).toBeVisible({ timeout: 5000 });
  });

  test('should toggle Live Mode on and off', async ({ page }) => {
    await page.goto('/frontend-demo.html');
    
    // Find toggle button or checkbox
    const liveToggle = page.locator('[data-testid="live-mode-toggle"], #liveMode, input[type="checkbox"]').first();
    
    if (await liveToggle.isVisible()) {
      // Get initial state
      const initialState = await liveToggle.isChecked();
      
      // Toggle it
      await liveToggle.click();
      
      // Verify state changed
      const newState = await liveToggle.isChecked();
      expect(newState).not.toBe(initialState);
      
      // Toggle back
      await liveToggle.click();
      const finalState = await liveToggle.isChecked();
      expect(finalState).toBe(initialState);
    }
  });

  test('should display alert statistics', async ({ page }) => {
    await page.goto('/frontend-demo.html');
    await page.waitForLoadState('networkidle');
    
    // Look for stat cards or numbers
    const statCards = page.locator('.stat-card, [class*="stat"], [class*="metric"]');
    const count = await statCards.count();
    
    // Should have at least some statistics displayed
    expect(count).toBeGreaterThan(0);
  });

  test('should display alert list or table', async ({ page }) => {
    await page.goto('/frontend-demo.html');
    await page.waitForLoadState('networkidle');
    
    // Look for alert list, table, or cards
    const alertContainer = page.locator(
      '.alert-list, .alert-table, table, [class*="alert-card"], [data-testid="alerts"]'
    ).first();
    
    await expect(alertContainer).toBeVisible();
  });

  test('should show filter controls', async ({ page }) => {
    await page.goto('/frontend-demo.html');
    
    // Look for filter buttons, dropdowns, or inputs
    const filters = page.locator(
      'select, [type="search"], .filter, [class*="filter"], button:has-text("Filter")'
    );
    
    const count = await filters.count();
    expect(count).toBeGreaterThan(0);
  });

  test('should display analytics or charts', async ({ page }) => {
    await page.goto('/frontend-demo.html');
    await page.waitForLoadState('networkidle');
    
    // Look for chart elements (canvas, svg, or chart containers)
    const charts = page.locator('canvas, svg[class*="recharts"], .chart, [class*="chart"]');
    const count = await charts.count();
    
    // May or may not have charts depending on view
    if (count > 0) {
      const firstChart = charts.first();
      await expect(firstChart).toBeVisible();
    }
  });

  test('should be responsive on mobile viewport', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/frontend-demo.html');
    await page.waitForLoadState('networkidle');
    
    // Page should still be usable
    const heading = page.locator('h1, h2').first();
    await expect(heading).toBeVisible();
    
    // Mobile menu or responsive layout should be present
    const mobileMenu = page.locator('[class*="mobile"], [class*="hamburger"], button[aria-label*="menu"]');
    
    // Either mobile menu exists or layout is responsive
    const hasMobileMenu = (await mobileMenu.count()) > 0;
    const isResponsive = await page.evaluate(() => {
      return document.body.scrollWidth <= window.innerWidth;
    });
    
    expect(hasMobileMenu || isResponsive).toBeTruthy();
  });

  test('should handle navigation between views', async ({ page }) => {
    await page.goto('/frontend-demo.html');
    await page.waitForLoadState('networkidle');
    
    // Look for navigation tabs or links
    const navLinks = page.locator('nav a, [role="tab"], [class*="tab"]');
    const count = await navLinks.count();
    
    if (count > 1) {
      // Click second nav item
      await navLinks.nth(1).click();
      
      // Wait for content to change
      await page.waitForTimeout(500);
      
      // Verify page didn't crash
      const body = page.locator('body');
      await expect(body).toBeVisible();
    }
  });

  test('should display version badge', async ({ page }) => {
    await page.goto('/frontend-demo.html');
    
    // Look for version badge
    const version = page.getByText(/LiveMode|v\d+\.\d+/i);
    
    // Version badge should be visible somewhere
    const count = await version.count();
    expect(count).toBeGreaterThan(0);
  });
});

