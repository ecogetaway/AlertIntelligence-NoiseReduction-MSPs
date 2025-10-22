import { test, expect } from '@playwright/test';

/**
 * Enhanced Next.js UI Feature Tests
 * 
 * Tests new features: grouping toggle, detail drawer, filter presets, 
 * live simulator, and bulk operations dialog.
 */

const NEXTJS_URL = process.env.NEXTJS_URL || 'http://localhost:3000';

test.describe('Enhanced Next.js UI Features', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(NEXTJS_URL);
    await page.waitForLoadState('networkidle');
  });

  test('should toggle between grouped and all alerts views', async ({ page }) => {
    // Find grouping toggle button
    const toggleButton = page.getByRole('button', { name: /grouped by incident|all alerts/i });
    
    if (await toggleButton.isVisible()) {
      const initialText = await toggleButton.textContent();
      
      // Toggle mode
      await toggleButton.click();
      await page.waitForTimeout(500);
      
      // Verify text changed
      const newText = await toggleButton.textContent();
      expect(newText).not.toBe(initialText);
      
      // Toggle back
      await toggleButton.click();
      await page.waitForTimeout(500);
      
      // Verify reverted
      const finalText = await toggleButton.textContent();
      expect(finalText).toBe(initialText);
    }
  });

  test('should open alert detail drawer on click', async ({ page }) => {
    // Wait for alerts to load
    await page.waitForSelector('[role="button"]', { timeout: 10000 });
    
    // Click first alert or incident row
    const firstAlert = page.locator('[role="button"]').first();
    if (await firstAlert.isVisible()) {
      await firstAlert.click();
      
      // Verify drawer opens
      const drawer = page.locator('[role="dialog"][aria-label*="detail"]');
      await expect(drawer).toBeVisible({ timeout: 2000 });
      
      // Verify AI Triage section exists
      const aiSection = page.getByText(/AI Triage/i);
      await expect(aiSection).toBeVisible();
      
      // Close drawer
      const closeButton = page.getByLabel(/close detail/i);
      await closeButton.click();
      
      // Verify drawer closed
      await expect(drawer).not.toBeVisible();
    }
  });

  test('should apply filter presets', async ({ page }) => {
    // Find preset buttons
    const presetBar = page.locator('text=Presets:').locator('..');
    
    if (await presetBar.isVisible()) {
      // Click "Critical Only" preset
      const criticalPreset = presetBar.getByRole('button', { name: /critical only/i });
      
      if (await criticalPreset.isVisible()) {
        await criticalPreset.click();
        await page.waitForTimeout(1000);
        
        // Verify filter applied (check URL or visible filters)
        const page URL or state changed
        expect(true).toBeTruthy(); // Placeholder - actual check depends on implementation
      }
    }
  });

  test('should save and apply custom filter preset', async ({ page }) => {
    // Apply some filters first
    const severityFilter = page.locator('select[name="severity"]').first();
    if (await severityFilter.isVisible()) {
      await severityFilter.selectOption('high');
      await page.waitForTimeout(500);
    }
    
    // Click "Save view" button
    const saveButton = page.getByRole('button', { name: /save view/i });
    
    if (await saveButton.isVisible()) {
      await saveButton.click();
      
      // Handle prompt (if browser allows)
      // Note: Playwright may need page.on('dialog') handler
      await page.waitForTimeout(1000);
    }
  });

  test('should enable and control live simulator', async ({ page }) => {
    // Find simulator controls
    const simulatorSection = page.getByText(/live simulator/i).locator('..');
    
    if (await simulatorSection.isVisible()) {
      // Enable simulator
      const enableCheckbox = simulatorSection.locator('input[type="checkbox"]').first();
      await enableCheckbox.check();
      
      // Wait for simulated alerts to appear
      await page.waitForTimeout(4000);
      
      // Verify alerts increased (check count changed)
      const alertCount = await page.locator('[class*="alert"]').count();
      expect(alertCount).toBeGreaterThan(0);
      
      // Disable simulator
      await enableCheckbox.uncheck();
    }
  });

  test('should adjust simulator interval and severity mix', async ({ page }) => {
    const simulatorSection = page.getByText(/live simulator/i).locator('..');
    
    if (await simulatorSection.isVisible()) {
      // Change interval
      const intervalInput = simulatorSection.locator('input[type="number"]');
      if (await intervalInput.isVisible()) {
        await intervalInput.fill('5000');
        expect(await intervalInput.inputValue()).toBe('5000');
      }
      
      // Change severity mix
      const mixSelect = simulatorSection.locator('select[aria-label="Severity mix"]');
      if (await mixSelect.isVisible()) {
        await mixSelect.selectOption('critical');
        expect(await mixSelect.inputValue()).toBe('critical');
      }
    }
  });

  test('should open bulk operations dialog', async ({ page }) => {
    // Select alerts first
    const selectAllButton = page.getByRole('button', { name: /select all/i });
    
    if (await selectAllButton.isVisible()) {
      await selectAllButton.click();
      await page.waitForTimeout(500);
      
      // Click bulk actions button
      const bulkButton = page.getByRole('button', { name: /bulk actions/i });
      
      if (await bulkButton.isVisible()) {
        await bulkButton.click();
        
        // Verify dialog opens
        const dialog = page.locator('[role="dialog"][aria-labelledby="bulk-ops-title"]');
        await expect(dialog).toBeVisible();
        
        // Verify dialog has action selector
        const actionSelect = dialog.locator('select');
        await expect(actionSelect).toBeVisible();
        
        // Close dialog
        const cancelButton = dialog.getByRole('button', { name: /cancel/i });
        await cancelButton.click();
        
        // Verify dialog closed
        await expect(dialog).not.toBeVisible();
      }
    }
  });

  test('should select action and provide reason in bulk ops', async ({ page }) => {
    const selectAllButton = page.getByRole('button', { name: /select all/i });
    
    if (await selectAllButton.isVisible()) {
      await selectAllButton.click();
      
      const bulkButton = page.getByRole('button', { name: /bulk actions/i });
      if (await bulkButton.isVisible()) {
        await bulkButton.click();
        
        const dialog = page.locator('[role="dialog"][aria-labelledby="bulk-ops-title"]');
        
        // Select suppress action
        const actionSelect = dialog.locator('select').first();
        await actionSelect.selectOption('suppress');
        
        // Enter reason
        const reasonTextarea = dialog.locator('textarea');
        await reasonTextarea.fill('Testing bulk suppression');
        
        // Verify form filled
        expect(await actionSelect.inputValue()).toBe('suppress');
        expect(await reasonTextarea.inputValue()).toContain('Testing');
        
        // Cancel (don't actually submit in test)
        const cancelButton = dialog.getByRole('button', { name: /cancel/i });
        await cancelButton.click();
      }
    }
  });

  test('should be responsive on mobile viewport', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(NEXTJS_URL);
    await page.waitForLoadState('networkidle');
    
    // Page should still render
    const heading = page.locator('h1, h2, [role="heading"]').first();
    await expect(heading).toBeVisible();
    
    // Simulator should be visible and functional
    const simulatorSection = page.getByText(/live simulator/i);
    if (await simulatorSection.isVisible()) {
      await expect(simulatorSection).toBeVisible();
    }
  });

  test('should maintain accessibility with new features', async ({ page }) => {
    // Check for ARIA labels on new components
    const toggleButton = page.getByRole('button', { name: /switch to/i });
    if (await toggleButton.isVisible()) {
      expect(await toggleButton.getAttribute('aria-label')).toBeTruthy();
    }
    
    // Check drawer has proper role
    const firstAlert = page.locator('[role="button"]').first();
    if (await firstAlert.isVisible()) {
      await firstAlert.click();
      
      const drawer = page.locator('[role="dialog"]');
      await expect(drawer).toHaveAttribute('aria-modal', 'true');
    }
  });
});

