"""
MSP Alert Intelligence & Noise Reduction Platform
Main application entry point with AWS AgentCore and Strands Agents integration
"""

import asyncio
import logging
import os
from contextlib import asynccontextmanager
from typing import Dict, Any

import structlog
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from api.routes import alerts, incidents, workflows, agents
from core.config import settings
from core.database import init_db
from core.middleware import LoggingMiddleware, ErrorHandlingMiddleware
from agents.bedrock_agentcore import BedrockAgentCoreManager
from agents.strands_agents import StrandsAgentManager

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

# Global agent managers
bedrock_manager: BedrockAgentCoreManager = None
strands_manager: StrandsAgentManager = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown"""
    global bedrock_manager, strands_manager
    
    logger.info("Starting MSP Alert Intelligence Platform")
    
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    
    # Initialize AWS Bedrock AgentCore
    try:
        bedrock_manager = BedrockAgentCoreManager()
        await bedrock_manager.initialize()
        logger.info("Bedrock AgentCore initialized")
    except Exception as e:
        logger.error("Failed to initialize Bedrock AgentCore", error=str(e))
        bedrock_manager = None
    
    # Initialize Strands Agents
    try:
        strands_manager = StrandsAgentManager()
        await strands_manager.initialize()
        logger.info("Strands Agents initialized")
    except Exception as e:
        logger.error("Failed to initialize Strands Agents", error=str(e))
        strands_manager = None
    
    yield
    
    # Cleanup
    logger.info("Shutting down MSP Alert Intelligence Platform")
    if bedrock_manager:
        await bedrock_manager.cleanup()
    if strands_manager:
        await strands_manager.cleanup()


# Create FastAPI application
app = FastAPI(
    title="MSP Alert Intelligence Platform",
    description="Alert Intelligence & Noise Reduction for Managed Service Providers",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)
app.add_middleware(LoggingMiddleware)
app.add_middleware(ErrorHandlingMiddleware)

# Include routers
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["alerts"])
app.include_router(incidents.router, prefix="/api/v1/incidents", tags=["incidents"])
app.include_router(workflows.router, prefix="/api/v1/workflows", tags=["workflows"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])


@app.get("/")
async def root():
    """Root endpoint with basic information"""
    return {
        "name": "MSP Alert Intelligence Platform",
        "version": "1.0.0",
        "status": "operational",
        "features": [
            "Alert Deduplication",
            "Smart Filtering", 
            "Correlation Analysis",
            "Agentic AI Processing",
            "Real-time Dashboards",
            "Automated Workflows"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    status = {
        "status": "healthy",
        "database": "connected",
        "bedrock_agentcore": "connected" if bedrock_manager else "disconnected",
        "strands_agents": "connected" if strands_manager else "disconnected"
    }
    
    return JSONResponse(content=status)


@app.get("/api/v1/agents/status")
async def agents_status():
    """Get status of all AI agents"""
    if not bedrock_manager or not strands_manager:
        raise HTTPException(status_code=503, detail="AI agents not initialized")
    
    return {
        "bedrock_agentcore": await bedrock_manager.get_status(),
        "strands_agents": await strands_manager.get_status()
    }


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
