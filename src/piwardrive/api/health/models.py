from __future__ import annotations

from typing import TypedDict


class TokenResponse(TypedDict):
    access_token: str
    token_type: str


class AuthLoginResponse(TokenResponse):
    role: str


class LogoutResponse(TypedDict):
    logout: bool


class HealthRecordDict(TypedDict):
    timestamp: str
    cpu_temp: float | None
    cpu_percent: float
    memory_percent: float
    disk_percent: float


class BaselineAnalysisResult(TypedDict):
    recent: dict[str, float]
    baseline: dict[str, float]
    delta: dict[str, float]
    anomalies: list[str]


class SyncResponse(TypedDict):
    uploaded: int
