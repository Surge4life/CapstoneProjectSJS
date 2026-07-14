#!/bin/bash
# CORRECTED seed script for the live G.O.D.S API on Neon.
# Fixes vs the original: (1) login is form-encoded not JSON, (2) users via /auth/register
# not /admin/users, (3) models use operator_id/use_case/jurisdiction not vendor/description.
#
# PREREQUISITE: the .local register fix (RENDER_DEPLOY_backend.zip) must be DEPLOYED first,
# or /auth/register returns 422 on @gods.local emails. If you'd rather not push first, use
# Option A instead:  cd platform-core && DATABASE_URL="<neon-pooled-url>" python3 seed.py
set -e
API="${1:-https://gods-platform-core.onrender.com}"

echo "==> 1. Login as bootstrap admin (form-encoded)"
TOKEN=$(curl -s -X POST "$API/auth/login" \
  -d 'username=admin@gods.local&password=admin123' \
  | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
if [ ${#TOKEN} -lt 10 ]; then echo "   LOGIN FAILED — backend may be cold (wait 60s) or admin pw differs"; exit 1; fi
echo "   token: ${TOKEN:0:20}..."
H="Authorization: Bearer $TOKEN"

echo "==> 2. Create the 9 users (/auth/register)"
for u in \
  '{"email":"client.dsd@gods.local","password":"client123","role":"client","division":"DSD"}' \
  '{"email":"client.acme@gods.local","password":"client123","role":"client","division":"ACME"}' \
  '{"email":"seths.op@gods.local","password":"staff123","role":"operator","division":"SETHS"}' \
  '{"email":"madiba.op@gods.local","password":"staff123","role":"operator","division":"MADIBA"}' \
  '{"email":"ts.op@gods.local","password":"staff123","role":"operator","division":"TS"}' \
  '{"email":"cob@gods.local","password":"staff123","role":"exec","division":"GODS"}' \
  '{"email":"auditor@gods.local","password":"staff123","role":"auditor","division":"GODS"}' \
  '{"email":"exec@gods.local","password":"staff123","role":"exec","division":"GODS"}' \
  '{"email":"viewer@gods.local","password":"staff123","role":"viewer","division":"GODS"}'; do
  em=$(echo "$u" | python3 -c "import sys,json;print(json.load(sys.stdin)['email'])")
  code=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$API/auth/register" \
         -H "Content-Type: application/json" -d "$u")
  case "$code" in
    200|201) echo "   created  $em";;
    409)     echo "   exists   $em (ok)";;
    *)       echo "   FAILED   $em -> HTTP $code";;
  esac
done

echo "==> 3. Register 2 AI models (/registry/models — correct schema)"
curl -s -X POST "$API/registry/models" -H "$H" -H "Content-Type: application/json" \
  -d '{"model_id":"model-001","name":"ZA-CreditScorer","operator_id":"op-fnb","risk_tier":"HIGH","use_case":"South African credit scoring","jurisdiction":"ZA"}' \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print('   model-001 ->',d.get('status',d))" 2>/dev/null || echo "   model-001 (exists or check)"
curl -s -X POST "$API/registry/models" -H "$H" -H "Content-Type: application/json" \
  -d '{"model_id":"model-002","name":"Acme-FraudScore","operator_id":"op-acme","risk_tier":"MEDIUM","use_case":"fraud detection","jurisdiction":"ZA"}' \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print('   model-002 ->',d.get('status',d))" 2>/dev/null || echo "   model-002 (exists or check)"

echo "==> 4. Governance decisions through the gate (/engine/enforce)"
for m in model-001 model-002; do
  curl -s -X POST "$API/engine/enforce" -H "$H" -H "Content-Type: application/json" \
    -d "{\"action\":\"DEPLOY\",\"model_id\":\"$m\",\"risk_tier\":\"NOTABLE\"}" \
    | python3 -c "import sys,json;d=json.load(sys.stdin);print('   ',d.get('model_id','?'),'->',d.get('verdict','?'))" 2>/dev/null || echo "   $m enforce (check)"
done

echo "==> 5. Conformance scan (Sentinel)"
curl -s -X POST "$API/conformance/scan" -H "$H" -o /dev/null -w "   conformance/scan -> HTTP %{http_code}\n"

echo "==> Done. Log in with any account: client123 (clients) / staff123 (staff) / admin123 (admin)."
