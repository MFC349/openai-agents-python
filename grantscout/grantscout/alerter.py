"""SMTP email and webhook (Slack/Discord) alert delivery."""

from __future__ import annotations

import json
import smtplib
from email.mime.text import MIMEText

import httpx

from grantscout.config import config
from grantscout.logger import log
from grantscout.models import Grant


def send_email_alert(grants: list[Grant], subject: str = "New Grant Opportunities") -> bool:
    """Send an email digest of new grants via SMTP. Returns True on success."""
    smtp = config.smtp
    if not smtp.is_configured:
        log.warning("SMTP not configured – skipping email alert")
        return False

    body_lines = [f"Found {len(grants)} new grant(s):\n"]
    for g in grants:
        body_lines.append(f"  • {g.title} ({g.agency})")
        body_lines.append(f"    Award: {g.award_range}  |  Status: {g.status.value}")
        if g.url:
            body_lines.append(f"    URL: {g.url}")
        body_lines.append("")

    msg = MIMEText("\n".join(body_lines), "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = smtp.alert_from
    msg["To"] = smtp.alert_to

    try:
        with smtplib.SMTP(smtp.host, smtp.port) as server:
            server.starttls()
            server.login(smtp.user, smtp.password)
            server.send_message(msg)
        log.info("Email alert sent to %s", smtp.alert_to)
        return True
    except Exception as exc:
        log.error("Email alert failed: %s", exc)
        return False


def send_webhook_alert(grants: list[Grant]) -> bool:
    """Post a summary to a Slack/Discord webhook. Returns True on success."""
    wh = config.webhook
    if not wh.is_configured:
        log.warning("Webhook not configured – skipping webhook alert")
        return False

    lines = [f"*GrantScout found {len(grants)} new opportunities*"]
    for g in grants[:10]:
        lines.append(f"• *{g.title}* – {g.agency} ({g.status.value})")
        if g.url:
            lines.append(f"  <{g.url}>")
    if len(grants) > 10:
        lines.append(f"_…and {len(grants) - 10} more._")

    payload = {"text": "\n".join(lines)}

    try:
        resp = httpx.post(wh.url, json=payload, timeout=15)
        resp.raise_for_status()
        log.info("Webhook alert sent successfully")
        return True
    except Exception as exc:
        log.error("Webhook alert failed: %s", exc)
        return False


def send_alerts(grants: list[Grant]) -> None:
    """Attempt all configured alert channels."""
    if not grants:
        log.info("No grants to alert on")
        return
    send_email_alert(grants)
    send_webhook_alert(grants)
