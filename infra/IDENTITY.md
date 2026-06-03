# Identity Federation path (assessment gap #7)
Today: JWT (bcrypt) issued by platform-core /auth. Enterprise federation path:
- Deploy Keycloak as IdP; configure OIDC clients for each portal + platform.
- platform-core validates Keycloak-issued OIDC tokens (swap the JWT verify for JWKS).
- SAML for government/university SSO via Keycloak brokering.
Hook point: app/core/security.py decode_token() → replace with JWKS verification.
