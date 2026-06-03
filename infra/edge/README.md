# UDOC External Edge (NGINX)
The single public boundary. Deny-by-default; only external-safe paths reach platform-core
(which binds to the internal NIC only). Internal consoles and admin/oversight/sovereignty/
audit/analytics are never proxied here — they live on the internal network only.

Deploy on the edge/gateway node (see udoc-gateway/). Set TLS certs + the real internal
upstream IP. External apps (UDOC/SETHS/MADIBA/TS .apk) point their connect screen at this
edge's https URL; internal consoles point at the internal bind.
