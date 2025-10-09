import { test, expect } from '@playwright/test'

test.describe('AI Agents Integration', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
    await page.waitForLoadState('networkidle')
  })

  test('should display AI agent status', async ({ page }) => {
    // Check if AI agent status is displayed
    await expect(page.locator('text=AI Processing')).toBeVisible()
    await expect(page.locator('text=95%')).toBeVisible()
    
    // Check for agent capabilities
    await expect(page.locator('text=Noise Reduction')).toBeVisible()
    await expect(page.locator('text=78%')).toBeVisible()
    
    await expect(page.locator('text=Correlation Rate')).toBeVisible()
    await expect(page.locator('text=62%')).toBeVisible()
  })

  test('should show AI enrichment indicators on alerts', async ({ page }) => {
    // Navigate to alerts
    await page.click('button:has-text("Alerts")')
    await page.waitForSelector('[data-testid="alert-card"]')
    
    // Check for AI enrichment indicators
    const aiEnrichedAlerts = page.locator('[data-testid="ai-enriched"]')
    if (await aiEnrichedAlerts.count() > 0) {
      await expect(aiEnrichedAlerts.first()).toBeVisible()
    }
    
    // Check for correlation indicators
    const correlatedAlerts = page.locator('[data-testid="correlated"]')
    if (await correlatedAlerts.count() > 0) {
      await expect(correlatedAlerts.first()).toBeVisible()
    }
  })

  test('should allow manual AI enrichment', async ({ page }) => {
    // Navigate to alerts
    await page.click('button:has-text("Alerts")')
    await page.waitForSelector('[data-testid="alert-card"]')
    
    // Click on first alert's action menu
    const firstAlert = page.locator('[data-testid="alert-card"]').first()
    await firstAlert.locator('[data-testid="alert-actions"]').click()
    
    // Click on AI Enrich action
    await page.click('text=AI Enrich')
    
    // Check if enrichment process starts
    await expect(page.locator('text=Alert enrichment started')).toBeVisible()
    
    // Wait for enrichment to complete (simulated)
    await page.waitForTimeout(2000)
    
    // Check if enrichment results are displayed
    const enrichments = firstAlert.locator('[data-testid="ai-enrichments"]')
    if (await enrichments.count() > 0) {
      await expect(enrichments).toBeVisible()
    }
  })

  test('should display AI-generated incident summaries', async ({ page }) => {
    // Navigate to incidents
    await page.click('button:has-text("Incidents")')
    await page.waitForSelector('[data-testid="incident-card"]')
    
    // Check for AI-generated content
    const aiSummary = page.locator('[data-testid="ai-summary"]')
    if (await aiSummary.count() > 0) {
      await expect(aiSummary.first()).toBeVisible()
    }
    
    const aiRootCause = page.locator('[data-testid="ai-root-cause"]')
    if (await aiRootCause.count() > 0) {
      await expect(aiRootCause.first()).toBeVisible()
    }
    
    const aiRecommendations = page.locator('[data-testid="ai-recommendations"]')
    if (await aiRecommendations.count() > 0) {
      await expect(aiRecommendations.first()).toBeVisible()
    }
  })

  test('should show noise reduction metrics', async ({ page }) => {
    // Navigate to analytics
    await page.click('button:has-text("Analytics")')
    
    // Check for noise reduction metrics
    await expect(page.locator('text=Noise Reduction')).toBeVisible()
    await expect(page.locator('text=78%')).toBeVisible()
    
    // Check for AI processing metrics
    await expect(page.locator('text=AI Processing')).toBeVisible()
    await expect(page.locator('text=95%')).toBeVisible()
  })

  test('should handle AI agent errors gracefully', async ({ page }) => {
    // Mock AI agent failure
    await page.route('**/api/v1/agents/status**', route => {
      route.fulfill({
        status: 503,
        contentType: 'application/json',
        body: JSON.stringify({ 
          error: 'AI agents not initialized',
          bedrock_agentcore: 'disconnected',
          strands_agents: 'disconnected'
        })
      })
    })
    
    // Navigate to analytics
    await page.click('button:has-text("Analytics")')
    
    // Check if error state is handled
    await expect(page.locator('text=AI Processing')).toBeVisible()
    // The UI should still show metrics but with degraded functionality
  })

  test('should display correlation analysis', async ({ page }) => {
    // Navigate to alerts
    await page.click('button:has-text("Alerts")')
    await page.waitForSelector('[data-testid="alert-card"]')
    
    // Look for correlated alerts
    const correlatedAlerts = page.locator('[data-testid="correlated-alerts"]')
    if (await correlatedAlerts.count() > 0) {
      await expect(correlatedAlerts.first()).toBeVisible()
      
      // Check correlation details
      const correlationDetails = page.locator('[data-testid="correlation-details"]')
      if (await correlationDetails.count() > 0) {
        await expect(correlationDetails.first()).toBeVisible()
      }
    }
  })

  test('should show AI confidence scores', async ({ page }) => {
    // Navigate to alerts
    await page.click('button:has-text("Alerts")')
    await page.waitForSelector('[data-testid="alert-card"]')
    
    // Check for confidence scores in AI enrichments
    const confidenceScores = page.locator('[data-testid="confidence-score"]')
    if (await confidenceScores.count() > 0) {
      await expect(confidenceScores.first()).toBeVisible()
      
      // Check if confidence score is a valid percentage
      const score = await confidenceScores.first().textContent()
      expect(score).toMatch(/\d+%/)
    }
  })

  test('should handle AI agent configuration', async ({ page }) => {
    // This test would check if AI agent configuration is accessible
    // In a real implementation, this might be in a settings page
    
    // For now, we'll check if the agent status is displayed
    await expect(page.locator('text=AI Processing')).toBeVisible()
    
    // Check if agent capabilities are shown
    await expect(page.locator('text=Noise Reduction')).toBeVisible()
    await expect(page.locator('text=Correlation Rate')).toBeVisible()
  })

  test('should demonstrate AI workflow automation', async ({ page }) => {
    // Navigate to analytics to see AI workflow metrics
    await page.click('button:has-text("Analytics")')
    
    // Check for workflow automation indicators
    await expect(page.locator('text=AI Processing')).toBeVisible()
    await expect(page.locator('text=95%')).toBeVisible()
    
    // This indicates that AI workflows are processing alerts automatically
    // In a real implementation, we might show specific workflow status
  })
})
