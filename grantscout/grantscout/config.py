"""Environment-driven configuration with .env support."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv


def _load_env() -> None:
    """Load .env file from the project root if it exists."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)


_load_env()


def _env(key: str, default: str = "") -> str:
    return os.getenv(f"GRANTSCOUT_{key}", default)


def _env_int(key: str, default: int = 0) -> int:
    raw = _env(key)
    return int(raw) if raw else default


def _env_float(key: str, default: float = 0.0) -> float:
    raw = _env(key)
    return float(raw) if raw else default


@dataclass
class ScraperConfig:
    """Tuning knobs for HTTP requests."""

    request_timeout: int = field(default_factory=lambda: _env_int("REQUEST_TIMEOUT", 30))
    max_retries: int = field(default_factory=lambda: _env_int("MAX_RETRIES", 3))
    rate_limit_delay: float = field(default_factory=lambda: _env_float("RATE_LIMIT_DELAY", 1.0))


@dataclass
class SmtpConfig:
    """SMTP email alert settings."""

    host: str = field(default_factory=lambda: _env("SMTP_HOST", "smtp.gmail.com"))
    port: int = field(default_factory=lambda: _env_int("SMTP_PORT", 587))
    user: str = field(default_factory=lambda: _env("SMTP_USER"))
    password: str = field(default_factory=lambda: _env("SMTP_PASSWORD"))
    alert_from: str = field(default_factory=lambda: _env("ALERT_FROM"))
    alert_to: str = field(default_factory=lambda: _env("ALERT_TO"))

    @property
    def is_configured(self) -> bool:
        return bool(self.user and self.password and self.alert_from and self.alert_to)


@dataclass
class WebhookConfig:
    """Webhook (Slack / Discord) alert settings."""

    url: str = field(default_factory=lambda: _env("WEBHOOK_URL"))

    @property
    def is_configured(self) -> bool:
        return bool(self.url)


@dataclass
class Config:
    """Top-level application configuration."""

    scraper: ScraperConfig = field(default_factory=ScraperConfig)
    smtp: SmtpConfig = field(default_factory=SmtpConfig)
    webhook: WebhookConfig = field(default_factory=WebhookConfig)
    output_dir: str = field(default_factory=lambda: _env("OUTPUT_DIR", "./output"))
    log_file: str = field(default_factory=lambda: _env("LOG_FILE", "./grantscout.log"))

    def ensure_output_dir(self) -> Path:
        p = Path(self.output_dir)
        p.mkdir(parents=True, exist_ok=True)
        return p


# Singleton used across the application.
config = Config()
