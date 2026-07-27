# Chapter 12 — Copyright Strategy

## The Copyright Challenge for Institutional Intelligence

Every AI knowledge system faces a copyright challenge: the knowledge it uses to answer questions comes from documents, and documents are copyrighted. G.O.D.S Intelligence has a deliberate strategy for navigating this challenge — not by ignoring copyright, but by building copyright governance into the corpus management process.

---

## The Declared Copyright Model

Every document uploaded to the G.O.D.S corpus must have a declared copyright status. The institution accepts responsibility for the accuracy of the declaration. The system records the declaration permanently.

| Status | Required Declaration | What It Means |
|--------|--------------------|--------------| 
| `institution_owned` | Nothing additional required | Created entirely by the institution |
| `licensed` | Licence reference number/URL | Used under a formal licence agreement |
| `public_domain` | Creative Commons identifier or legislation citation | Public domain in the applicable jurisdiction |
| `fair_use` | Legal basis document (internal) | Used under fair use / fair dealing |
| `government_publication` | Source URL and jurisdiction | Government publication |
| `open_access` | Open access licence identifier | Published under open access terms |

---

## Output Attribution — The Primary Copyright Mitigation

The most significant copyright mitigation in G.O.D.S Intelligence is source attribution. When the system cites the source of information, it:

1. Directs the user to the original for fuller context
2. Credits the original author/publisher
3. Creates a record showing the connection between the output and the source
4. Allows copyright holders to verify their work is being used appropriately

Attribution does not resolve all copyright questions. But a system that consistently attributes its sources is in a fundamentally better legal position than one that presents information as original without citing sources.

---

## The Synthesis Question

When G.O.D.S Intelligence synthesises a response from multiple sources, who owns the synthesis?

This is an evolving area of law. The G.O.D.S position is pragmatic and conservative:

1. **Verbatim quotations:** Copyright belongs to the original source. Quote sparingly, cite always.
2. **Close paraphrase:** Copyright situation is uncertain. Cite the source regardless. Let the institution's legal team advise on use.
3. **Original synthesis from multiple sources:** The institution may have a claim. Document the sources used in the audit record.
4. **AI-generated synthesis:** Copyright of AI-generated content is unsettled in most jurisdictions. Do not claim copyright over AI-generated synthesis without legal advice.

The system produces an audit record for every response including all sources. This record is the institution's primary evidence of how the response was produced.

---

## Copyright for Training Data (Future)

If G.O.D.S Holdings develops its own models (see Chapter 16), training data copyright becomes relevant. The position for in-house model training:

- Training data must be either institution-owned, licensed for training, or public domain
- No web scraping without explicit analysis of the resulting copyright situation
- Approved datasets (see Chapter 14) define the acceptable training data universe
- Training data provenance is permanently recorded

---

## Practical Guidance for Corpus Managers

**Safe to include:**
- Your own internal documents (policies, procedures, reports)
- Documents from government sources (legislation, gazettes, official guidance — verify jurisdiction)
- Documents licensed from publishers under a licence that covers this use
- Documents you have created from scratch

**Requires review:**
- Academic papers (check licence — many now open access, but not all)
- Industry reports (usually copyrighted — need licence)
- Third-party analysis or commentary (need licence or fair use basis)

**Do not include without legal advice:**
- Commercial publications (books, paywalled articles)
- Competitor materials
- Any material where the copyright situation is unclear
