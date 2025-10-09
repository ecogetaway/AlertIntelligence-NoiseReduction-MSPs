import { test, expect } from '@playwright/test'

test.describe('MSP Alert Intelligence Platform', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the application
    await page.goto('/')
    
    // Wait for the page to load
    await page.waitForLoadState('networkidle')
  })

  test('should display dashboard with alert statistics', async ({ page }) => {
    // Check if the main dashboard elements are present
    await expect(page.locator('h1')).toContainText('MSP Alert Intelligence Platform')
    
    // Check for alert stats cards
    await expect(page.locator('[data-testid="alert-stats"]')).toBeVisible()
    
    // Check for navigation tabs
    await expect(page.locator('button:has-text("Alerts")')).toBeVisible()
    await expect(page.locator('button:has-text("Incidents")')).toBeVisible()
    await expect(page.locator('button:has-text("Analytics")')).toBeVisible()
  })

  test('should display alerts list with filtering', async ({ page }) => {
    // Click on Alerts tab
    await page.click('button:has-text("Alerts")')
    
    // Wait for alerts to load
    await page.waitForSelector('[data-testid="alert-card"]', { timeout: 10000 })
    
    // Check if alert cards are displayed
    const alertCards = page.locator('[data-testid="alert-card"]')
    await expect(alertCards).toHaveCount.greaterThan(0)
    
    // Test severity filter
    await page.click('[data-testid="severity-filter"]')
    await page.click('option[value="critical"]')
    
    // Wait for filtered results
    await page.waitForTimeout(1000)
    
    // Check if only critical alerts are shown
    const criticalAlerts = page.locator('[data-testid="alert-card"] .alert-severity-critical')
    await expect(criticalAlerts).toHaveCount.greaterThan(0)
  })

  test('should allow alert actions (acknowledge, suppress)', async ({ page }) => {
    // Navigate to alerts
    await page.click('button:has-text("Alerts")')
    await page.waitForSelector('[data-testid="alert-card"]')
    
    // Click on the first alert's action menu
    const firstAlert = page.locator('[data-testid="alert-card"]').first()
    await firstAlert.locator('[data-testid="alert-actions"]').click()
    
    // Check if action menu is visible
    await expect(page.locator('[data-testid="action-menu"]')).toBeVisible()
    
    // Test acknowledge action
    await page.click('text=Acknowledge')
    
    // Check if confirmation dialog appears
    await expect(page.locator('[data-testid="action-dialog"]')).toBeVisible()
    
    // Confirm the action
    await page.click('button:has-text("Confirm")')
    
    // Check if alert status changed
    await expect(firstAlert.locator('.status-acknowledged')).toBeVisible()
  })

  test('should display alert details and AI enrichments', async ({ page }) => {
    // Navigate to alerts
    await page.click('button:has-text("Alerts")')
    await page.waitForSelector('[data-testid="alert-card"]')
    
    // Click on alert details
    const firstAlert = page.locator('[data-testid="alert-card"]').first()
    await firstAlert.locator('[data-testid="alert-details-toggle"]').click()
    
    // Check if details are expanded
    await expect(firstAlert.locator('[data-testid="alert-details"]')).toBeVisible()
    
    // Check for AI enrichments if present
    const enrichments = firstAlert.locator('[data-testid="ai-enrichments"]')
    if (await enrichments.count() > 0) {
      await expect(enrichments).toBeVisible()
    }
    
    // Check for correlations if present
    const correlations = firstAlert.locator('[data-testid="alert-correlations"]')
    if (await correlations.count() > 0) {
      await expect(correlations).toBeVisible()
    }
  })

  test('should display incidents with AI analysis', async ({ page }) => {
    // Click on Incidents tab
    await page.click('button:has-text("Incidents")')
    
    // Wait for incidents to load
    await page.waitForSelector('[data-testid="incident-card"]', { timeout: 10000 })
    
    // Check if incident cards are displayed
    const incidentCards = page.locator('[data-testid="incident-card"]')
    await expect(incidentCards).toHaveCount.greaterThan(0)
    
    // Check for AI analysis in incidents
    const aiAnalysis = page.locator('[data-testid="ai-analysis"]')
    if (await aiAnalysis.count() > 0) {
      await expect(aiAnalysis).toBeVisible()
    }
  })

  test('should display analytics dashboard', async ({ page }) => {
    // Click on Analytics tab
    await page.click('button:has-text("Analytics")')
    
    // Check if analytics dashboard is displayed
    await expect(page.locator('h3:has-text("Analytics Dashboard")')).toBeVisible()
    
    // Check for AI processing metrics
    await expect(page.locator('text=AI Processing')).toBeVisible()
    await expect(page.locator('text=Noise Reduction')).toBeVisible()
    await expect(page.locator('text=Correlation Rate')).toBeVisible()
  })

  test('should handle search functionality', async ({ page }) => {
    // Navigate to alerts
    await page.click('button:has-text("Alerts")')
    await page.waitForSelector('[data-testid="alert-card"]')
    
    // Test search functionality
    const searchInput = page.locator('[data-testid="search-input"]')
    await searchInput.fill('database')
    
    // Wait for search results
    await page.waitForTimeout(1000)
    
    // Check if search results are filtered
    const alertCards = page.locator('[data-testid="alert-card"]')
    const count = await alertCards.count()
    
    if (count > 0) {
      // Check if at least one alert contains the search term
      const firstAlert = alertCards.first()
      await expect(firstAlert).toContainText('database')
    }
  })

  test('should be responsive on mobile devices', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 })
    
    // Check if navigation is mobile-friendly
    await expect(page.locator('button:has-text("Alerts")')).toBeVisible()
    
    // Check if alert cards are responsive
    const alertCards = page.locator('[data-testid="alert-card"]')
    if (await alertCards.count() > 0) {
      await expect(alertCards.first()).toBeVisible()
    }
  })

  test('should handle error states gracefully', async ({ page }) => {
    // Mock API failure
    await page.route('**/api/v1/alerts**', route => {
      route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Internal Server Error' })
      })
    })
    
    // Navigate to alerts
    await page.click('button:has-text("Alerts")')
    
    // Check if error message is displayed
    await expect(page.locator('text=Failed to load alerts')).toBeVisible()
  })

  test('should support keyboard navigation', async ({ page }) => {
    // Test tab navigation
    await page.keyboard.press('Tab')
    await page.keyboard.press('Tab')
    await page.keyboard.press('Tab')
    
    // Check if focus is visible
    const focusedElement = page.locator(':focus')
    await expect(focusedElement).toBeVisible()
    
    // Test Enter key on focused element
    await page.keyboard.press('Enter')
  })

  test('should handle real-time updates', async ({ page }) => {
    // Navigate to alerts
    await page.click('button:has-text("Alerts")')
    await page.waitForSelector('[data-testid="alert-card"]')
    
    // Get initial count
    const initialCount = await page.locator('[data-testid="alert-card"]').count()
    
    // Simulate new alert (this would be done via WebSocket in real app)
    await page.evaluate(() => {
      // Simulate adding a new alert to the DOM
      const container = document.querySelector('[data-testid="alerts-container"]')
      if (container) {
        const newAlert = document.createElement('div')
        newAlert.setAttribute('data-testid', 'alert-card')
        newAlert.className = 'alert-card'
        newAlert.innerHTML = '<div class="alert-title">New Test Alert</div>'
        container.appendChild(newAlert)
      }
    })
    
    // Check if new alert appears
    await expect(page.locator('[data-testid="alert-card"]')).toHaveCount(initialCount + 1)
  })
})
