"""SAM.gov opportunities API source."""

from __future__ import annotations

from datetime import date

from grantscout.logger import log
from grantscout.models import Grant, GrantStatus
from grantscout.sources.base import BaseSource


class SamGovSource(BaseSource):
    """Fetch grant opportunities from the SAM.gov public API."""

    name = "sam_gov"
    base_url = "https://api.sam.gov/opportunities/v2/search"

    def fetch(self, keywords: list[str]) -> list[Grant]:
        keyword_str = " ".join(keywords) if keywords else ""
        log.info("[sam_gov] searching for: %s", keyword_str or "(all)")

        params: dict[str, str] = {"limit": "100", "postedFrom": "01/01/2024"}
        if keyword_str:
            params["q"] = keyword_str

        data = self._get_json(self.base_url, params=params)
        raw_items = data.get("opportunitiesData", data.get("results", []))
        grants: list[Grant] = []
        for item in raw_items:
            try:
                grants.append(self._parse(item))
            except Exception as exc:  # noqa: BLE001
                log.debug("[sam_gov] skipping item: %s", exc)
        log.info("[sam_gov] fetched %d grants", len(grants))
        return grants

    @staticmethod
    def _parse(item: dict) -> Grant:
        status_raw = (item.get("type") or item.get("status") or "posted").lower()
        status_map = {
            "presolicitation": GrantStatus.FORECASTED,
            "o": GrantStatus.POSTED,
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
                    if "/" in val:
                        parts = val.split("/")
                        return date(int(parts[2]), int(parts[0]), int(parts[1]))
                    return date.fromisoformat(val)
                except (ValueError, TypeError, IndexError):
                    continue
            return None

        notice_id = str(item.get("noticeId") or item.get("id") or "")
        return Grant(
            id=f"sam_gov_{notice_id}",
            title=item.get("title") or "",
            agency=item.get("department") or item.get("agency") or "",
            description=item.get("description") or item.get("synopsis") or "",
            status=status,
            award_ceiling=float(item.get("awardCeiling") or 0),
            award_floor=float(item.get("awardFloor") or 0),
            close_date=_parse_date(item.get("responseDeadLine") or item.get("closeDate")),
            posted_date=_parse_date(item.get("postedDate")),
            url=f"https://sam.gov/opp/{notice_id}/view",
            source="sam_gov",
        )
