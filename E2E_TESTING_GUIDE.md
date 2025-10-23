# E2E Testing Guide - MSP Alert Intelligence

**Framework:** Playwright  
**Status:** ✅ Ready to Run  
**Coverage:** Backend API + Frontend UI + Integration Flows

---

## 🚀 Quick Start

### 1. Setup (One-Time)
```bash
# Run automated setup
./setup-e2e-tests.sh

# This installs:
# - Node dependencies
# - Playwright and browsers
# - Python dependencies
# - Test database
```

### 2. Run Tests
```bash
# Run all tests
npx playwright test

# Run with UI (interactive)
npx playwright test --ui

# Run in headed mode (watch browser)
npx playwright test --headed

# Run specific browser
npx playwright test --project=chromium
```

### 3. View Results
```bash
# Generate and open HTML report
npx playwright show-report
```

---

## 📁 Test Structure

```
tests/e2e/
├── api/
│   ├── health.spec.ts         # Backend health checks
│   ├── alerts.spec.ts         # Alert CRUD operations
│   └── webhook.spec.ts        # Keep webhook integration
├── frontend/
│   ├── dashboard.spec.ts      # Dashboard UI
│   └── filters.spec.ts        # Filter functionality
└── integration/
    └── full-flow.spec.ts      # End-to-end flows
```

---

## 🧪 Test Categories

### Backend API Tests (`tests/e2e/api/`)

#### Health Check Tests
**File:** `health.spec.ts`

**What it tests:**
- `/health` endpoint returns healthy status
- Root endpoint returns basic info
- OpenAPI docs are accessible
- Agents status endpoint works

**Run:**
```bash
npx playwright test tests/e2e/api/health.spec.ts
```

#### Alert API Tests
**File:** `alerts.spec.ts`

**What it tests:**
- List alerts with pagination
- Filter by severity, status, source
- Search alerts by text
- Create new alerts
- Get alert by ID
- Handle 404 errors
- Advanced filtering

**Run:**
```bash
npx playwright test tests/e2e/api/alerts.spec.ts
```

#### Webhook Tests
**File:** `webhook.spec.ts`

**What it tests:**
- HMAC signature verification
- Valid webhook acceptance
- Invalid signature rejection
- Missing signature handling
- Duplicate alert detection
- Noise filtering
- Sample payload generation
- cURL command generation

**Run:**
```bash
npx playwright test tests/e2e/api/webhook.spec.ts
```

### Frontend Tests (`tests/e2e/frontend/`)

#### Dashboard Tests
**File:** `dashboard.spec.ts`

**What it tests:**
- Page loads successfully
- Live Mode toggle visibility and functionality
- Alert statistics display
- Alert list/table rendering
- Filter controls presence
- Analytics/charts display
- Mobile responsiveness
- Navigation between views
- Version badge display

**Run:**
```bash
npx playwright test tests/e2e/frontend/dashboard.spec.ts
```

#### Filter Tests
**File:** `filters.spec.ts`

**What it tests:**
- Severity filtering
- Status filtering
- Source filtering
- Text search
- Clear/reset filters
- Multiple filter combinations

**Run:**
```bash
npx playwright test tests/e2e/frontend/filters.spec.ts
```

### Integration Tests (`tests/e2e/integration/`)

#### Full Flow Tests
**File:** `full-flow.spec.ts`

**What it tests:**
- Complete pipeline: Webhook → Backend → Database → API → Frontend
- Deduplication consistency
- Correlation enrichment
- Alert persistence
- API-Frontend data flow

**Run:**
```bash
npx playwright test tests/e2e/integration/full-flow.spec.ts
```

---

## 🎯 Test Scenarios

### Scenario 1: Basic Alert Flow
```
1. Send alert via Keep webhook
2. Verify HMAC signature accepted
3. Check alert persisted in database
4. Query via API
5. Verify enrichments added
6. Frontend displays alert
```

### Scenario 2: Deduplication
```
1. Send alert A
2. Send identical alert A
3. Verify only one persisted
4. Check duplicate status returned
5. Frontend shows single alert
```

### Scenario 3: Correlation
```
1. Send related alert A (same service)
2. Send related alert B (same service)
3. Send related alert C (same service)
4. Verify all correlated
5. Check incident ID assigned
6. Frontend groups by incident
```

---

## ⚙️ Configuration

### Environment Variables

Create `.env.test`:
```bash
API_BASE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
DATABASE_URL=sqlite:///./test_e2e.db
DEBUG=true
KEEP_WEBHOOK_SECRET=test-secret-e2e
BEDROCK_AGENTCORE_ENABLED=false
```

### Playwright Config

**File:** `playwright.config.ts`

**Key settings:**
- Timeout: 30 seconds per test
- Retry: 2 times on CI
- Browsers: Chromium, Firefox, WebKit, Mobile
- Screenshots: On failure
- Videos: On failure
- Traces: On retry

---

## 🌐 Browser Coverage

| Browser | Desktop | Mobile |
|---------|---------|--------|
| Chromium | ✅ | ✅ (Pixel 5) |
| Firefox | ✅ | ❌ |
| WebKit | ✅ | ✅ (iPhone 12) |
| Edge | ✅ | ❌ |
| Chrome | ✅ | ❌ |

---

## 🚀 Running Tests

### All Tests
```bash
npx playwright test
```

### Specific Browser
```bash
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit
```

### Specific Test File
```bash
npx playwright test tests/e2e/api/health.spec.ts
npx playwright test tests/e2e/frontend/dashboard.spec.ts
npx playwright test tests/e2e/integration/full-flow.spec.ts
```

### Headed Mode (Watch Tests Run)
```bash
npx playwright test --headed
```

### Debug Mode
```bash
npx playwright test --debug
```

### Interactive UI
```bash
npx playwright test --ui
```

### Specific Test by Name
```bash
npx playwright test -g "should accept webhook"
npx playwright test -g "deduplication"
```

---

## 📊 Viewing Results

### HTML Report
```bash
# Generate report
npx playwright show-report

# Opens in browser with:
# - Test results
# - Screenshots
# - Videos
# - Traces
```

### JSON Report
```bash
cat test-results/results.json | jq
```

### CI Summary
Automatically generated in GitHub Actions and posted to PR

---

## 🐛 Debugging Tests

### 1. Run in Headed Mode
```bash
npx playwright test --headed --project=chromium
```

### 2. Use Debug Mode
```bash
npx playwright test --debug tests/e2e/api/webhook.spec.ts
```

### 3. Open Playwright Inspector
```bash
PWDEBUG=1 npx playwright test
```

### 4. View Trace
```bash
npx playwright show-trace test-results/trace.zip
```

### 5. Take Screenshots
Already configured - screenshots saved on failure to `test-results/`

### 6. Record Video
Already configured - videos saved on failure to `test-results/`

---

## 📝 Writing New Tests

### Basic Test Template
```typescript
import { test, expect } from '@playwright/test';

test.describe('My Test Suite', () => {
  test('should do something', async ({ page, request }) => {
    // Arrange
    const data = { foo: 'bar' };
    
    // Act
    const response = await request.post('/api/endpoint', {
      data: data
    });
    
    // Assert
    expect(response.ok()).toBeTruthy();
    const body = await response.json();
    expect(body).toHaveProperty('id');
  });
});
```

### Frontend Test Template
```typescript
test('should interact with UI', async ({ page }) => {
  await page.goto('/frontend-demo.html');
  
  const button = page.getByRole('button', { name: 'Submit' });
  await button.click();
  
  await expect(page.getByText('Success')).toBeVisible();
});
```

### API Test Template
```typescript
test('should call API', async ({ request }) => {
  const response = await request.get('/api/v1/alerts');
  
  expect(response.status()).toBe(200);
  const body = await response.json();
  expect(Array.isArray(body.alerts)).toBeTruthy();
});
```

---

## 🔄 CI/CD Integration

### GitHub Actions Workflow

**File:** `.github/workflows/e2e-tests.yml`

**Triggers:**
- Push to main, develop, perf-benchmarks-evidence
- Pull requests
- Manual workflow dispatch

**Matrix:**
- Chromium
- Firefox
- WebKit

**Artifacts:**
- Test results (JSON/HTML)
- Screenshots
- Videos
- Traces

**Duration:** ~5-10 minutes

### Running on CI
Tests run automatically on push/PR. To run manually:
1. Go to Actions tab in GitHub
2. Select "E2E Tests with Playwright"
3. Click "Run workflow"

---

## 📋 Test Checklist

Before deploying or demoing:

- [ ] Run all tests: `npx playwright test`
- [ ] Check coverage: All test files pass
- [ ] Verify reports: `npx playwright show-report`
- [ ] Test on CI: Push to branch and check Actions
- [ ] Manual smoke test:
  - [ ] Backend health check
  - [ ] Send test webhook
  - [ ] Load frontend
  - [ ] Check filters work
  - [ ] Verify Live Mode

---

## 🔧 Troubleshooting

### Tests Fail with "Backend not running"
**Solution:**
```bash
# Start backend manually
./test-backend-locally.sh

# Then run tests in another terminal
npx playwright test
```

### Tests Timeout
**Solution:**
- Increase timeout in `playwright.config.ts`
- Check backend is healthy: `curl http://localhost:8000/health`
- Check database is writable

### Browser Installation Fails
**Solution:**
```bash
# Reinstall browsers
npx playwright install --with-deps
```

### Tests Pass Locally but Fail on CI
**Solution:**
- Check CI logs for specific error
- Verify environment variables set
- Check database initialization
- Ensure no hardcoded localhost URLs

### HMAC Signature Failures
**Solution:**
- Verify `KEEP_WEBHOOK_SECRET` matches in:
  - Backend `.env`
  - Test `.env.test`
  - Test scripts

---

## 📈 Coverage Goals

| Category | Target | Current |
|----------|--------|---------|
| API Endpoints | 90%+ | ~85% |
| Frontend UI | 80%+ | ~70% |
| Integration Flows | 100% | ~90% |
| Error Scenarios | 75%+ | ~60% |

**Next Priority:**
- Add more error scenario tests
- Increase frontend component coverage
- Add performance tests
- Add load tests

---

## 🎓 Learning Resources

- **Playwright Docs:** https://playwright.dev/
- **Best Practices:** https://playwright.dev/docs/best-practices
- **API Testing:** https://playwright.dev/docs/api-testing
- **Debugging:** https://playwright.dev/docs/debug
- **CI/CD:** https://playwright.dev/docs/ci

---

## 📞 Support

**Issues with tests?**
1. Check logs: `test-results/*.txt`
2. View screenshots: `test-results/*.png`
3. Watch videos: `test-results/*.webm`
4. Check traces: `test-results/trace.zip`

**Need help?**
- See `E2E_TESTING_PLAN.md` for architecture
- See `playwright.config.ts` for configuration
- See existing tests for examples

---

**Status:** ✅ Tests ready to run  
**Next:** Run `./setup-e2e-tests.sh` and `npx playwright test`

