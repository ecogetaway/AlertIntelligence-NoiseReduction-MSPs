# Performance Benchmarks - Execution Guide

## 🚀 **Quick Start**

### Prerequisites
```bash
# Install Python dependencies
pip install psutil requests

# Install Node.js dependencies (if testing frontend)
cd frontend && npm install
```

### Running All Benchmarks
```bash
# 1. Start backend services
cd backend
python demo_main.py &

# 2. Start frontend (separate terminal)
cd frontend  
npm run dev &

# 3. Run benchmarks
python tests/performance/backend_benchmarks.py
python tests/performance/ai_benchmarks.py
python tests/performance/frontend_benchmarks.py
```

## 📊 **Results Location**
- **Backend Results**: `benchmarks/results/backend_benchmarks.json`
- **AI Results**: `benchmarks/results/ai_benchmarks.json`
- **Frontend Results**: `benchmarks/results/frontend_benchmarks.json`

## 🔍 **What Gets Measured**

### Backend Benchmarks
- API response times (10 endpoints)
- Database query performance
- Memory usage tracking
- Alert processing throughput
- Concurrent request handling

### AI/ML Benchmarks  
- Noise reduction effectiveness
- Deduplication accuracy
- Correlation analysis performance
- Agent processing speed
- Overall AI effectiveness

### Frontend Benchmarks
- Page load times (3 pages)
- Bundle size analysis
- Network request performance
- User experience metrics
- Performance scoring

## 📈 **Expected Results**

### Backend Performance
- API Response: 15-25ms average
- Database Queries: <3ms execution
- Memory Usage: ~45MB RSS
- Throughput: 1000+ alerts/second

### AI/ML Performance
- Noise Reduction: 75-80%
- Deduplication: 25-30%
- Correlation: 85-90% confidence
- Processing Speed: 200-300 alerts/second

### Frontend Performance
- Page Load: 1-2 seconds
- Bundle Size: 1-2MB
- Network Success: 100%
- Performance Grade: B+ to A-

## 🛠️ **Troubleshooting**

### Common Issues
1. **Backend not running**: Start with `python demo_main.py`
2. **Frontend not accessible**: Check `http://localhost:3000`
3. **Import errors**: Ensure backend is in Python path
4. **Network timeouts**: Increase timeout values in test scripts

### Debug Mode
```bash
# Run with verbose output
python tests/performance/backend_benchmarks.py --verbose
python tests/performance/ai_benchmarks.py --verbose
python tests/performance/frontend_benchmarks.py --verbose
```

## 📋 **Test Data**

### Sample Alerts (8 alerts)
- 2 Critical alerts (database, CPU)
- 1 High severity alert (memory)
- 1 Medium severity alert (disk)
- 1 Low severity alert (log level)
- 1 Duplicate alert (for deduplication testing)
- 2 Noise alerts (heartbeat, maintenance)

### Test Scenarios
- **Noise Reduction**: Filter out info-level alerts
- **Deduplication**: Detect duplicate database alerts
- **Correlation**: Group alerts by service
- **Performance**: Measure processing speed

## 🎯 **Success Criteria**

### Minimum Performance Targets
- API Response: <50ms average
- Noise Reduction: >70%
- Deduplication: >20%
- Frontend Load: <3 seconds
- Memory Usage: <100MB

### Excellent Performance Targets
- API Response: <25ms average
- Noise Reduction: >80%
- Deduplication: >30%
- Frontend Load: <2 seconds
- Memory Usage: <50MB

## 📊 **Benchmark Reports**

After running benchmarks, review:
1. **PERFORMANCE_BENCHMARKS.md** - Detailed technical report
2. **PERFORMANCE_SUMMARY_SLIDE.md** - Presentation-ready summary
3. **benchmarks/results/*.json** - Raw measurement data

## 🔄 **Re-running Benchmarks**

### Clean Results
```bash
# Clear previous results
rm -rf benchmarks/results/*.json

# Re-run all benchmarks
python tests/performance/backend_benchmarks.py
python tests/performance/ai_benchmarks.py  
python tests/performance/frontend_benchmarks.py
```

### Incremental Testing
```bash
# Run specific benchmark
python tests/performance/backend_benchmarks.py
python tests/performance/ai_benchmarks.py
python tests/performance/frontend_benchmarks.py
```

## 📈 **Performance Monitoring**

### Continuous Monitoring
- Run benchmarks after code changes
- Monitor performance regression
- Track improvement over time
- Document performance trends

### Production Monitoring
- Set up performance monitoring
- Track real-world metrics
- Compare with benchmark baselines
- Optimize based on actual usage

---

*Benchmark execution guide for MSP Alert Intelligence Platform*
*Last updated: 2024-12-19*
