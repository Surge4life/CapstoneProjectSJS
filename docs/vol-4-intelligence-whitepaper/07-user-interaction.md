# Chapter 07 — User Interaction Model

## How Users Experience G.O.D.S Intelligence

G.O.D.S Intelligence is embedded in the G.O.D.S platform — it is not a standalone product. Users encounter it in context, as a tool within their workflow, not as a general-purpose AI assistant they seek out.

---

## Interaction Points by Role

### Learner (SETHS)

A learner interacts with intelligence through the **Smart Application Advisor**:

- "How well does my profile match this opportunity?" → Intelligence compares learner profile against opportunity requirements using the corpus
- "What NQF level do I need for software developer roles?" → Intelligence retrieves from the regulatory and qualification corpus
- "What are my rights if my application is rejected?" → Intelligence retrieves from the relevant legislation and governance corpus

These are contextual queries — they happen within the application flow, not as a separate "chat" interface.

### Employer (SETHS)

- "What does the Employment Equity Act require for companies with more than 50 employees?" → Regulatory information
- "How should we document rejection reasons to ensure compliance?" → Compliance guidance

### Compliance Officer

- "Show me all policy rules that apply to employment decisions in South Africa" → Policy corpus retrieval
- "What are the EVA thresholds for this operator?" → Operational knowledge retrieval
- "Summarise the governance outcomes for this model over the last 90 days" → Analytics synthesis (uses operational data, not corpus)

### Administrator

- "What are the deployment requirements for an air-gapped UDOC node?" → Engineering Canon retrieval
- "What does POPIA require for data subject access requests?" → Regulatory retrieval

---

## Query Interface Design

The intelligence query interface in the G.O.D.S platform is minimal by design:

```
┌─────────────────────────────────────────────────┐
│  Ask a question about [context]                  │
│                                                 │
│  [ What NQF level is required for...          ] │
│                                    [Ask]         │
├─────────────────────────────────────────────────┤
│  Answer                                         │
│  ─────────────────────────────────────────────  │
│  NQF Level 6 (National Diploma equivalent) is   │
│  typically required for roles in this category. │
│                                                 │
│  Confidence: HIGH (0.87)                        │
│                                                 │
│  Sources:                                       │
│  ▸ NQF Act No. 67 of 2008 — Section 8          │
│  ▸ SAQA Framework — Tier 1                     │
│                                                 │
│  [Was this helpful?  👍  👎]                   │
└─────────────────────────────────────────────────┘
```

Key design choices:
1. **Contextual framing** — "about [context]" makes the scope clear
2. **Answer first** — the confidence and sources follow the answer, not precede it
3. **Confidence visible** — always shown, not hidden
4. **Sources expandable** — click to see the full excerpt
5. **Feedback mechanism** — thumbs up/down feeds calibration data

---

## Session Management

A query session is a sequence of related queries within one UI interaction. Within a session:
- Follow-up questions can reference the previous answer ("Tell me more about that")
- Context is maintained via the session's query history
- The system passes the previous query and response as context for the next query

A new session starts when the user navigates away or the session times out (30 minutes of inactivity).

Sessions are stored in the session database (Redis) with a TTL of 30 minutes. Session content (queries and responses) is also written to the audit log.

---

## External Consultation Flow

When the user triggers external consultation (if enabled):

```
User: "I need information on recent AI regulation in the EU — our corpus may not have this"
                          ↓
System: "Your query may require external information not in the institutional corpus.
         Would you like to consult an external AI service?
         Note: Your query will be sent to [service name]. No personal data will be included."
                          ↓
User: [Confirms]
                          ↓
System: Sanitises query (removes PII, sensitive terms)
        → Sends to configured external service
        → Receives response
        → Labels response as EXTERNAL_SOURCE, confidence: LOW
        → Delivers to user with clear external source attribution
                          ↓
Audit: External consultation logged with: service used, sanitised query, timestamp
```

The user must actively confirm before any query leaves the institutional boundary. This is the "user-initiated" requirement from the Constitutional Limits (Chapter 06, Limit 3).
