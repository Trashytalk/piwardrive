# Security Configuration

The API enforces authentication when `PW_API_PASSWORD_HASH` is set. The username defaults to `admin` and can be overridden with `PW_API_USER`.

Rate limiting is enabled via `PIWARDRIVE_RATE_LIMIT_REQUESTS` and `PIWARDRIVE_RATE_LIMIT_WINDOW`.

CORS origins can be specified in `PW_CORS_ORIGINS`.

Content Security Policy can be customised with `PW_CONTENT_SECURITY_POLICY`.

The service adds HTTP security headers (HSTS, CSP, X-Frame-Options, X-Content-Type-Options).

Automated security scanning runs in CI (`.github/workflows/security.yml`).
