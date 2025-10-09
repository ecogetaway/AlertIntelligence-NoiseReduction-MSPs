"""
Configuration management for MSP Alert Intelligence Platform
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "MSP Alert Intelligence Platform"
    DEBUG: bool = Field(default=False, env="DEBUG")
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql://user:password@localhost:5432/msp_alerts",
        env="DATABASE_URL"
    )
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        env="REDIS_URL"
    )
    
    # AWS Configuration
    AWS_REGION: str = Field(default="us-east-1", env="AWS_REGION")
    AWS_ACCESS_KEY_ID: Optional[str] = Field(default=None, env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, env="AWS_SECRET_ACCESS_KEY")
    
    # Bedrock AgentCore
    BEDROCK_AGENTCORE_ENABLED: bool = Field(default=True, env="BEDROCK_AGENTCORE_ENABLED")
    BEDROCK_AGENTCORE_RUNTIME_URL: Optional[str] = Field(
        default=None, env="BEDROCK_AGENTCORE_RUNTIME_URL"
    )
    
    # Strands Agents
    STRANDS_AGENTS_ENABLED: bool = Field(default=True, env="STRANDS_AGENTS_ENABLED")
    STRANDS_AGENTS_CONFIG_PATH: str = Field(
        default="./agents/strands_config.yaml", env="STRANDS_AGENTS_CONFIG_PATH"
    )
    
    # AI Models
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    DEFAULT_AI_MODEL: str = Field(default="claude-3-sonnet", env="DEFAULT_AI_MODEL")
    
    # Security
    SECRET_KEY: str = Field(default="your-secret-key-here", env="SECRET_KEY")
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:3001"],
        env="ALLOWED_ORIGINS"
    )
    ALLOWED_HOSTS: List[str] = Field(
        default=["localhost", "127.0.0.1"],
        env="ALLOWED_HOSTS"
    )
    
    # Alert Processing
    ALERT_DEDUPLICATION_WINDOW: int = Field(default=300, env="ALERT_DEDUPLICATION_WINDOW")  # 5 minutes
    ALERT_CORRELATION_WINDOW: int = Field(default=1800, env="ALERT_CORRELATION_WINDOW")  # 30 minutes
    MAX_ALERTS_PER_BATCH: int = Field(default=100, env="MAX_ALERTS_PER_BATCH")
    
    # Workflow Processing
    WORKFLOW_TIMEOUT: int = Field(default=300, env="WORKFLOW_TIMEOUT")  # 5 minutes
    MAX_CONCURRENT_WORKFLOWS: int = Field(default=10, env="MAX_CONCURRENT_WORKFLOWS")
    
    # Monitoring
    ENABLE_METRICS: bool = Field(default=True, env="ENABLE_METRICS")
    METRICS_PORT: int = Field(default=9090, env="METRICS_PORT")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(default="json", env="LOG_FORMAT")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings"""
    return settings
