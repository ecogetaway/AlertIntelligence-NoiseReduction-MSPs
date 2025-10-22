# MSP Alert Intelligence - E2E Testing Plan

**Status:** 🚧 In Progress  
**Testing Framework:** Playwright  
**Integration:** KeepHQ/keep repository

---

## 🎯 Testing Objectives

### 1. Backend API Testing
- ✅ Health check and status endpoints
- ✅ Alert CRUD operations
- ✅ Keep webhook ingestion with HMAC
- ✅ Deduplication logic
- ✅ Correlation service
- ✅ AI enrichment flow

### 2. Frontend Testing
- ✅ Dashboard loads correctly
- ✅ Live Mode toggle functionality
- ✅ Alert filtering works
- ✅ Bulk operations execute
- ✅ Analytics display correctly
- ✅ Mobile responsiveness

### 3. Integration Testing
- ✅ Keep → Backend → Database flow
- ✅ Backend → Frontend API flow
- ✅ Alert enrichment end-to-end
- ✅ Deduplication consistency
- ✅ Correlation grouping

---

## 🏗️ Test Architecture

```
tests/
├── e2e/
│   ├── api/
│   │   ├── health.spec.ts           # Health check tests
│   │   ├── alerts.spec.ts           # Alert CRUD tests
│   │   ├── webhook.spec.ts          # Keep webhook tests
│   │   └── enrichment.spec.ts       # Enrichment flow tests
│   ├── frontend/
│   │   ├── dashboard.spec.ts        # Dashboard UI tests
│   │   ├── filters.spec.ts          # Filter functionality
│   │   ├── bulk-ops.spec.ts         # Bulk operations
│   │   └── analytics.spec.ts        # Analytics display
│   └── integration/
│       ├── keep-flow.spec.ts        # Keep → Backend flow
│       ├── api-frontend.spec.ts     # Backend → Frontend flow
│       └── deduplication.spec.ts    # Dedup consistency
├── fixtures/
│   ├── alerts.json                  # Sample alert data
│   ├── keep-webhooks.json           # Sample Keep payloads
│   └── enriched-alerts.json         # Expected enriched data
├── utils/
│   ├── api-helpers.ts               # API test utilities
│   ├── keep-simulator.ts            # Keep webhook simulator
│   └── data-generators.ts           # Test data factories
└── playwright.config.ts             # Playwright configuration
```

---

## 📋 Test Scenarios

### Scenario 1: Alert Ingestion via Keep Webhook
1. Simulate Keep sending alert via webhook
2. Verify HMAC signature validation
3. Check noise reduction filters applied
4. Confirm deduplication logic
5. Validate correlation assignment
6. Verify AI enrichment added
7. Check database persistence
8. Confirm API returns enriched alert

### Scenario 2: Frontend Dashboard Flow
1. Load dashboard page
2. Verify alerts display
3. Enable Live Mode
4. Confirm auto-refresh works
5. Test severity filter
6. Test status filter
7. Execute bulk acknowledge
8. Verify alert state updates

### Scenario 3: Deduplication Consistency
1. Send identical alert twice
2. Verify only one persisted
3. Send similar alerts within window
4. Check fingerprint matching
5. Confirm duplicate count tracked
6. Verify frontend shows deduplicated data

### Scenario 4: Correlation Grouping
1. Send related alerts (same service)
2. Verify Strands agents correlate
3. Check incident ID assigned
4. Confirm confidence score calculated
5. Verify frontend groups by incident
6. Check correlation metadata

---

## 🔧 Keep Repository Integration

### Setup Steps
```bash
# Clone Keep repository (as submodule or reference)
git submodule add https://github.com/keephq/keep.git external/keep

# Or clone alongside for reference
cd ..
git clone https://github.com/keephq/keep.git keep-reference
cd AlertIntelligence-NoiseReduction-MSPs
```

### Integration Points
1. **Alert Schema Mapping** - Use Keep's alert model as reference
2. **Webhook Format** - Match Keep's webhook payload structure
3. **Provider Patterns** - Study Keep's provider integration
4. **Workflow Engine** - Demonstrate compatibility with Keep workflows

---

## 🧪 Playwright Configuration

### Browser Coverage
- ✅ Chromium (primary)
- ✅ Firefox (compatibility)
- ✅ WebKit (Safari compatibility)
- ✅ Mobile Chrome (responsive)
- ✅ Mobile Safari (responsive)

### Test Environments
- **Local:** http://localhost:8000 (backend) + http://localhost:3000 (frontend)
- **Staging:** Backend on Render + Frontend on Netlify
- **Production:** Full deployed stack

---

## 📊 Test Coverage Goals

| Category | Target | Current |
|----------|--------|---------|
| API Routes | 90%+ | 0% |
| Frontend Components | 80%+ | 0% |
| Integration Flows | 100% | 0% |
| Error Scenarios | 75%+ | 0% |
| Mobile Responsive | 90%+ | 0% |

---

## 🚀 CI/CD Integration

### GitHub Actions Workflow
```yaml
name: E2E Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - Checkout code
      - Setup Node.js and Python
      - Install dependencies
      - Start backend
      - Run Playwright tests
      - Upload test artifacts
      - Generate coverage report
```

---

## 📝 Test Data Strategy

### Fixtures
- **alerts.json** - Various severity levels, sources, statuses
- **keep-webhooks.json** - Realistic Keep payloads
- **enriched-alerts.json** - Expected AI-enriched outputs

### Data Generators
- Alert factory with randomization
- Keep webhook builder
- HMAC signature generator
- Fingerprint calculator

---

## 🎯 Success Criteria

- [ ] All API endpoints have test coverage
- [ ] Frontend critical paths tested
- [ ] Integration flows pass consistently
- [ ] Tests run in < 5 minutes
- [ ] CI/CD pipeline automated
- [ ] Test documentation complete
- [ ] Keep integration demonstrated

---

## 📅 Implementation Timeline

**Phase 1: Setup (Day 1)**
- Install Playwright
- Configure test environment
- Clone Keep reference
- Create test structure

**Phase 2: API Tests (Day 1-2)**
- Health check tests
- Alert CRUD tests
- Webhook tests
- Enrichment tests

**Phase 3: Frontend Tests (Day 2-3)**
- Dashboard tests
- Filter tests
- Bulk operation tests
- Analytics tests

**Phase 4: Integration Tests (Day 3-4)**
- Keep flow tests
- API-Frontend tests
- Deduplication tests
- Correlation tests

**Phase 5: CI/CD (Day 4-5)**
- GitHub Actions setup
- Test automation
- Coverage reporting
- Documentation

---

## 🔗 Resources

- **Playwright Docs:** https://playwright.dev/
- **Keep Repository:** https://github.com/keephq/keep
- **Test Best Practices:** https://playwright.dev/docs/best-practices
- **CI/CD Examples:** https://playwright.dev/docs/ci

---

**Next Steps:** See implementation files being created...

