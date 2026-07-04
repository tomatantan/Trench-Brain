# Detection CALL API v0

Owner: nekotaro
Status: draft for UI/backend handoff

## Purpose

This adds a small box between external detection bots and the existing Brain CALL UI.

The bot finds a token. The backend records the event. The UI reads the recorded events and renders them in the CALL section. The UI should not own the detection or screening logic.

## Scope v0

In scope:

- Accept detection events from pumpfunbot, smart-wallet logic, or another detector.
- Store events as append-only JSONL under `brain/state/detections.jsonl`.
- Expose read APIs for UI.
- Keep screening fields optional so bundle/top-holder checks can be added later.

Out of scope for v0:

- Final bundle/top-holder suppression.
- Auto notification sending.
- Trading execution.
- Editing `sources/` or wiki synthesis pages.

## Endpoints

### POST `/api/detect`

Registers one detected token/call candidate.

If `DETECT_WEBHOOK_TOKEN` is set on the server, callers must send:

```text
Authorization: Bearer <DETECT_WEBHOOK_TOKEN>
```

Request body:

```json
{
  "source": "pumpfunbot",
  "chain": "solana",
  "symbol": "$TEST",
  "name": "Test Token",
  "ca": "CA...",
  "detected_at": "2026-07-03T10:00:00+09:00",
  "signal_type": "SMART DETECT",
  "verdict": "REVIEW",
  "risk_score": 42,
  "reasons": [
    "smart wallet multi-buy",
    "holders increasing"
  ],
  "metrics": {
    "mcap_usd": 32000,
    "volume_5m": 12000,
    "holders": 180,
    "bundle_ratio": null,
    "top_holder_ratio": null,
    "sell_pressure": null
  },
  "url": "https://pump.fun/..."
}
```

Response:

```json
{
  "ok": true,
  "id": "detect_20260703_100000_ab12cd",
  "status": "queued",
  "detection": {
    "id": "detect_20260703_100000_ab12cd",
    "source": "pumpfunbot",
    "ca": "CA...",
    "verdict": "REVIEW"
  }
}
```

Errors:

- `400` bad JSON or missing `ca`/`mint`
- `401` missing/wrong bearer token when configured
- `413` body too large
- `500` internal write failure

### GET `/api/detections`

Returns recent detection events for the CALL UI.

Query params:

- `n`: number of rows, default `50`, max `200`
- `include_avoids`: `1` to include `AVOID` events, default `1` in v0

Response:

```json
{
  "ok": true,
  "count": 1,
  "detections": [
    {
      "id": "detect_20260703_100000_ab12cd",
      "source": "pumpfunbot",
      "chain": "solana",
      "symbol": "$TEST",
      "name": "Test Token",
      "ca": "CA...",
      "mint": "CA...",
      "type": "SMART DETECT",
      "verdict": "REVIEW",
      "risk_score": 42,
      "reasons": ["smart wallet multi-buy"],
      "metrics": {"mcap_usd": 32000},
      "detected_at": "2026-07-03T10:00:00+09:00"
    }
  ],
  "calls": [
    {
      "id": "detect_20260703_100000_ab12cd",
      "source": "pumpfunbot",
      "symbol": "$TEST",
      "name": "Test Token",
      "ca": "CA...",
      "mint": "CA...",
      "type": "SMART DETECT",
      "verdict": "REVIEW",
      "reason": "smart wallet multi-buy",
      "mcap": 32000,
      "reply_count": 0,
      "first_seen": "2026-07-03T10:00:00+09:00"
    }
  ]
}
```

`calls` is shaped for the current `wiki/ui/app.js` CALL renderer.

### GET `/api/feed`

`/api/feed` should include the latest detection calls as `calls` so the existing UI can consume them without a large rewrite.

## Verdicts

- `APE`: display as actionable/positive.
- `REVIEW`: display with caution.
- `AVOID`: do not send user-facing notification once screening is active.
- `WATCH`: do not notify yet, keep observing.
- `RECOVERED`: previously blocked but improving; eligible to reappear.

## Screening v1 draft

Later PR:

- `bundle_ratio >= 40` -> `AVOID`
- `top_holder_ratio >= 40` -> `AVOID`
- `top10_holder_ratio >= 40` -> `REVIEW` or `AVOID`
- `WATCH -> RECOVERED` when holders and volume rise while sell pressure falls

The data model already has `metrics` for these fields.

## UI handoff

UI should display the `calls` array. Do not implement bundle/top-holder logic in UI. Backend owns `verdict`, `risk_score`, and `reasons`.

`/api/feed.calls` excludes `AVOID` rows for user-facing notifications. Use `/api/detections?include_avoids=1` when debugging rejected detections.

Minimal UI question:

```text
CALL UI can read /api/feed.calls or /api/detections.calls.
Please confirm whether the current fields are enough:
id, source, symbol, name, ca, type, verdict, risk_score, reasons, metrics, detected_at.
```
