# Chapter 16 — Future In-House Model Roadmap

## The Strategic Direction

The current G.O.D.S Intelligence architecture relies on external embedding and synthesis models (OpenAI, sentence-transformers, Llama, Mistral). This is pragmatic for the current stage — these models are excellent, and building from scratch would delay deployment by years.

However, the long-term vision is institutional sovereignty over the full model stack — including the models themselves. An institution that governs its AI using models owned by another institution is only partially sovereign.

This chapter describes the roadmap for developing G.O.D.S-specific models.

---

## Phase 1: Current State (Years 0–2)

**Status:** Operational

- External embedding models (Sentence Transformers for air-gap; OpenAI for cloud)
- External synthesis models (Llama 3 for air-gap; GPT-4o-mini for cloud)
- All models governed by the constitutional runtime
- No in-house model training

**Goal:** Prove the governance architecture. Build the corpus. Collect calibration data.

---

## Phase 2: Fine-Tuning (Years 2–4)

**Goal:** Fine-tune existing open-source models on G.O.D.S-specific governance tasks.

**Embedding model fine-tuning:**
- Fine-tune `e5-large-v2` on institutional governance queries
- Training data: anonymised query-source pairs from the platform corpus
- Evaluation: improved retrieval accuracy on governance-specific queries

**Synthesis model fine-tuning:**
- Fine-tune Llama 3 on constitutional compliance tasks
- Training data: curated examples of correct constitutional refusals, correct source attribution, correct evidence-bounded responses
- Evaluation: improved constitutional compliance test scores

**Data governance for fine-tuning:**
- Training data must be approved under the approved datasets framework
- No user query content used for training without explicit consent
- Training process audited (what data was used, when, by whom)
- Fine-tuned models registered in the UDOC model registry like any other AI model

---

## Phase 3: Purpose-Built Embedding (Years 4–7)

**Goal:** Train a G.O.D.S-specific embedding model optimised for governance and regulatory retrieval.

**What makes a governance-specific embedding model different:**
- Trained on governance, legislative, and regulatory text (not general web text)
- Optimised for semantic similarity within governance domains (finding relevant legislation, not just similar-sounding text)
- Calibrated for the evidence tier system (Tier 1 documents should be semantically distinct from Tier 5)

**Training data (planned):**
- South African legislative corpus (approved dataset)
- Commonwealth governance publications (public domain)
- International governance frameworks (public domain, selected)
- G.O.D.S operational knowledge (institution-owned)

**Governance of the training:**
- Full training data provenance recorded
- Model registered with UDOC before deployment
- Conformance scan run on the trained model
- Third-party evaluation of model bias

---

## Phase 4: In-House Synthesis (Years 7–15)

**Goal:** A G.O.D.S-trained synthesis model that operates entirely within the institutional boundary, is trained only on approved data, and has constitutional compliance baked into its training (not just enforced post-hoc).

**Constitutional training objective:**
Rather than training a general model and then checking its outputs against constitutional limits, the Phase 4 model is trained with the constitutional framework as a training objective. This means:
- Constitutional refusals are trained in, not just enforced as post-checks
- Evidence attribution is a learned behaviour, not an instruction
- Confidence calibration is trained against the evidence tier system

**This is research-stage work.** The technical approach will be determined based on the state of the art in AI alignment and constitutional AI at the time.

---

## Governance of In-House Models

All in-house models, at every phase, are subject to:
- UDOC registration before deployment
- Conformance scanning
- Third-party bias evaluation before production deployment
- Ongoing governance monitoring (EVA scoring of model outputs)
- The same constitutional limits as any external model

Building the model in-house does not create an exemption from governance. If anything, in-house models are held to a higher standard — the institution cannot claim ignorance of a model's behaviour when it trained the model.
