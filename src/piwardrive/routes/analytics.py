"""Database analytics API routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from piwardrive import persistence
from piwardrive.api.auth import AUTH_DEP
from piwardrive.database_service import db_service
from piwardrive.models import ErrorResponse, NetworkAnalyticsRecord, NetworkFingerprint

router = APIRouter(prefix="/analytics-db", tags=["analytics-db"])


@router.get(
    "/fingerprints",
    response_model=list[NetworkFingerprint],
    responses={401: {"model": ErrorResponse}},
)
async def list_fingerprints(
    bssid: str | None = None,
    limit: int = 100,
    offset: int = 0,
    _auth: None = Depends(AUTH_DEP),
) -> list[NetworkFingerprint]:
    """Return stored network fingerprint rows."""
    query = (
        "SELECT id, bssid, fingerprint_hash, classification, risk_level, ",
        "tags, created_at FROM network_fingerprints"
    )
    params: list[object] = []
    if bssid:
        query += " WHERE bssid = ?"
        params.append(bssid)
    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    rows = await db_service.fetch(query, *params)
    return [NetworkFingerprint(**row) for row in rows]


@router.post(
    "/fingerprints",
    response_model=None,
    responses={401: {"model": ErrorResponse}},
)
async def add_fingerprint(
    rec: NetworkFingerprint,
    _auth: None = Depends(AUTH_DEP),
) -> None:
    """Insert a new fingerprint record."""
    await persistence.save_network_fingerprints([rec.model_dump(exclude_unset=True)])


@router.get(
    "/networks",
    response_model=list[NetworkAnalyticsRecord],
    responses={401: {"model": ErrorResponse}},
)
async def list_network_analytics(
    bssid: str | None = None,
    start: str | None = None,
    end: str | None = None,
    limit: int = 100,
    offset: int = 0,
    _auth: None = Depends(AUTH_DEP),
) -> list[NetworkAnalyticsRecord]:
    """Return rows from ``network_analytics`` filtered by parameters."""
    query = (
        "SELECT bssid, analysis_date, total_detections, suspicious_score ",
        "FROM network_analytics"
    )
    params: list[object] = []
    clauses: list[str] = []
    if bssid:
        clauses.append("bssid = ?")
        params.append(bssid)
    if start:
        clauses.append("analysis_date >= ?")
        params.append(start)
    if end:
        clauses.append("analysis_date <= ?")
        params.append(end)
    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    query += " ORDER BY analysis_date DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    rows = await db_service.fetch(query, *params)
    return [NetworkAnalyticsRecord(**row) for row in rows]
