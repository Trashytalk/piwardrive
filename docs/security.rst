Security Guidance
-----------------
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.

Security Architecture
~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

   graph TB
       A[Security Module] --> B[Password Hashing]
       A --> C[Path Sanitization]
       A --> D[Service Validation]
       A --> E[API Authentication]
       
       B --> F[PBKDF2-HMAC-SHA256]
       B --> G[Random Salt]
       B --> H[Constant Time Comparison]
       
       C --> I[Path Validation]
       C --> J[Directory Traversal Protection]
       
       D --> K[Service Name Validation]
       D --> L[Command Injection Protection]
       
       E --> M[Bearer Token Authentication]
       E --> N[JWT Token Generation]
       E --> O[Route Protection]
       
       style A fill:#e1f5fe
       style B fill:#ffebee
       style C fill:#fff3e0
       style D fill:#fce4ec
       style E fill:#e8f5e8

Authentication Flow
~~~~~~~~~~~~~~~~~~~

.. mermaid::

   sequenceDiagram
       participant Client
       participant API
       participant Security
       participant Config
       
       Client->>API: POST /token (credentials)
       API->>Security: Verify Password
       Security->>Config: Get Password Hash
       Config-->>Security: Return Hash
       Security->>Security: Compare Hashes
       Security-->>API: Verification Result
       API->>API: Generate JWT Token
       API-->>Client: Bearer Token
       
       Client->>API: API Request + Bearer Token
       API->>Security: Validate Token
       Security-->>API: Token Valid
       API-->>Client: Protected Resource
       
       Note over Security: Constant-time comparison
       Note over API: Routes require authentication

The :mod:`security` module exposes helpers for sanitising paths, validating service names and hashing passwords. ``hash_password`` derives a PBKDF2‑HMAC‑SHA256 digest with a random salt while ``verify_password`` recomputes the hash and compares it in constant time. Store only the hashed value in ``config.json`` or the ``PW_ADMIN_PASSWORD_HASH`` environment variable. Never commit plain text passwords to version control.

To generate a hash run::

    python -c "import security,sys; print(security.hash_password(sys.argv[1]))" mypass

Keep the resulting string in a protected location such as ``~/.config/piwardrive/config.json`` or a secrets manager. The verification helper is tolerant of bad input and simply returns ``False`` on failure.

Store the digest in ``config.json`` using the ``admin_password_hash`` key::

    {
        "admin_password_hash": "$pbkdf2-sha256$..."
    }

Alternatively export it via ``PW_ADMIN_PASSWORD_HASH`` or place it in
``~/.config/piwardrive/.env``::

    export PW_ADMIN_PASSWORD_HASH="$pbkdf2-sha256$..."
    python -m piwardrive.main

For HTTP clients, obtain a bearer token by POSTing valid credentials to
``/token``. Include ``Authorization: Bearer <token>`` with requests to
routes that modify configuration or control services, as well as ``/status``.
When
``PW_API_PASSWORD_HASH`` is unset the API does not enforce authentication,
but running without a password is strongly discouraged.
