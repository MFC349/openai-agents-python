"""Grants.gov REST API source."""

from __future__ import annotations

from datetime import date

from grantscout.logger import log
from grantscout.models import Grant, GrantStatus
from grantscout.sources.base import BaseSource


class GrantsGovSource(BaseSource):
    """Fetch opportunities from the Grants.gov REST API."""

    name = "grants_gov"
    base_url = "https://api.grants.gov/v1/api/opportunities"

    def fetch(self, keywords: list[str]) -> list[Grant]:
        keyword_str = ",".join(keywords) if keywords else ""
        log.info("[grants_gov] searching for: %s", keyword_str or "(all)")

        params: dict[str, str] = {"pageSize": "100"}
        if keyword_str:
            params["keyword"] = keyword_str

        data = self._get_json(self.base_url, params=params)
        raw_items = data.get("opportunities", data.get("items", []))
        grants: list[Grant] = []
        for item in raw_items:
            try:
                grants.append(self._parse(item))
            except Exception as exc:  # noqa: BLE001
                log.debug("[grants_gov] skipping item: %s", exc)
        log.info("[grants_gov] fetched %d grants", len(grants))
        return grants

    @staticmethod
    def _parse(item: dict) -> Grant:
        status_raw = (item.get("status") or item.get("oppStatus") or "posted").lower()
        status_map = {
            "forecasted": GrantStatus.FORECASTED,
            "posted": GrantStatus.POSTED,
            "closed": GrantStatus.CLOSED,
            "archived": GrantStatus.ARCHIVED,
        }
        status = status_map.get(status_raw, GrantStatus.POSTED)

        def _parse_date(val: str | None) -> date | None:
            if not val:
                return None
            for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
                try:
                    return date.fromisoformat(val) if "-" in val else date(
                        *map(int, val.split("/")[::-1])
                    )
                except (ValueError, TypeError):
                    continue
            return None

        opp_id = str(item.get("id") or item.get("opportunityId") or "")
        return Grant(
            id=f"grants_gov_{opp_id}",
            title=item.get("title") or item.get("opportunityTitle") or "",
            agency=item.get("agency") or item.get("agencyCode") or "",
            description=item.get("description") or item.get("synopsis") or "",
            status=status,
            award_ceiling=float(item.get("awardCeiling") or 0),
            award_floor=float(item.get("awardFloor") or 0),
            close_date=_parse_date(item.get("closeDate")),
            posted_date=_parse_date(item.get("postedDate")),
            url=f"https://www.grants.gov/search-results-detail/{opp_id}",
            source="grants_gov",
        )
