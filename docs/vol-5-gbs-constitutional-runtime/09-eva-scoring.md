# Chapter 09 — EVA 6-Dimensional Sovereign Risk Scoring

## EVA: Evaluating Valiant Algorithms

The EVA engine is the probabilistic risk assessment component of the GBS Runtime. It produces a numerical risk score across six dimensions for every governance request. These scores are the primary input to the constitutional checker and policy engine.

---

## The Six Dimensions in Detail

### Dimension 1: Ethical Cooperation (EC)

**What it measures:** The degree to which the AI action aligns with cooperative ethical norms — specifically, does it exploit power imbalances, extract value from vulnerable parties, or violate established trust?

**Scoring model:**
- Input features: operator history, action category, affected subject demographic profile, declared purpose alignment
- Model type: Calibrated logistic regression on historical governance outcomes
- Training data: Historical governance decisions with human-verified outcomes (not the full decision corpus — only the subset reviewed by compliance officers)

**Key signals that lower the EC score:**
- Action by a high-power entity (employer, financial institution) affecting a low-power subject (jobseeker, borrower)
- Action category that historically correlates with exploitation in this jurisdiction
- Declared purpose does not match action category (e.g., "personalisation" used for "exclusion")

---

### Dimension 2: Societal Impact (SI)

**What it measures:** The likely societal effect if this action were applied at scale across the full population of similar requests.

**Scoring model:**
- Input features: action category, affected subject population, historical volume of similar actions, jurisdiction-specific social impact data
- Model type: Regression model calibrated against South African Human Development Index indicators

**Key signals that lower the SI score:**
- Action category with historically negative societal outcomes at scale
- Affected population overlapping with marginalised communities (without special inclusion safeguards)
- Volume trajectory: increasing volume of similar actions without corresponding compliance review

---

### Dimension 3: Regulatory Compliance (RC)

**What it measures:** The probability that this action complies with applicable law and regulation in the declared jurisdiction.

**Scoring model:**
- Input features: jurisdiction, action category, affected subject rights, operator licence status, applicable legislation flags
- Model type: Rule-based primary (explicit regulatory requirements) + statistical calibration for ambiguous cases

**South African legislative coverage:**
- Protection of Personal Information Act (POPIA) — data processing requirements
- Employment Equity Act — discrimination prohibition
- Basic Conditions of Employment Act — minimum terms
- National Qualifications Framework Act — qualification requirements
- Labour Relations Act — fair labour practices
- Financial Intelligence Centre Act (FICA) — financial sector AML/KYC
- Companies Act — governance requirements for registered entities

**Key signals that lower the RC score:**
- Action involves personal information without declared POPIA basis
- Action in the employment domain without equality impact assessment
- Operator lacks required licence for this action category in this jurisdiction

---

### Dimension 4: Fairness (FA)

**What it measures:** The consistency of this action across similarly situated individuals, regardless of protected characteristics.

**Protected characteristics monitored (per Employment Equity Act):**
- Race
- Gender
- Sex
- Pregnancy
- Marital status
- Family responsibility
- Ethnic or social origin
- Colour
- Sexual orientation
- Age
- Disability
- Religion
- HIV status
- Conscience, belief, political opinion
- Culture, language, birth

**Scoring model:**
- Input features: action category, affected subject characteristics, historical decisions for similar subjects, proxy feature detection
- Model type: Fairness-aware classifier using demographic parity + equal opportunity metrics

**Key signals that lower the FA score:**
- Action references protected characteristics explicitly
- Action involves features that historically proxy for protected characteristics
- Historical decisions show statistically significant disparity across demographic groups

---

### Dimension 5: Confidence Calibration (CC)

**What it measures:** Whether the AI model's declared confidence is appropriate and calibrated.

**Scoring model:**
- Input: Declared confidence score from the AI model, historical calibration data for this model, action category
- Model type: Calibration assessment (Expected Calibration Error comparison)

**Key signals that lower the CC score:**
- Declared confidence significantly above the model's historical calibration for this action category
- High-confidence action in a domain where this model has historically been overconfident
- No calibration history available for this model (new model, no track record)

---

### Dimension 6: Sovereignty Compliance (SC)

**What it measures:** Whether the action complies with the sovereignty declarations of the deployment jurisdiction.

**Scoring model:**
- Input: Jurisdiction declaration, data residency requirements, cross-border flow flags, subject consent status, operator authorisation scope
- Model type: Rule-based (sovereignty rules are explicit and deterministic)

**Key signals that lower the SC score:**
- Request involves data subject in a different jurisdiction to the deployment
- Data would transit a jurisdiction without cross-border authorisation
- Subject has not provided required consent for this action category
- Operator's authorisation scope does not cover this action in this jurisdiction

---

## Score Aggregation

The overall GBS score is a weighted combination of the six dimensions:

```
GBS_score = (
    w_EC * EC_score +
    w_SI * SI_score +
    w_RC * RC_score +
    w_FA * FA_score +
    w_CC * CC_score +
    w_SC * SC_score
) / sum(weights)
```

Default weights (configurable per deployment via PolicyPack):

| Dimension | Default Weight |
|-----------|---------------|
| Ethical Cooperation (EC) | 1.0 |
| Societal Impact (SI) | 0.8 |
| Regulatory Compliance (RC) | 1.5 (elevated — legal requirement) |
| Fairness (FA) | 1.5 (elevated — constitutional right) |
| Confidence Calibration (CC) | 0.7 |
| Sovereignty Compliance (SC) | 1.0 |

**The zero-score rule (hardcoded, not configurable):**
If any single dimension scores 0, the overall outcome is `BLOCK` regardless of the weighted score. A score of 0 means the EVA engine detected an absolute violation in that dimension — not a risk, not a concern, but a definitive violation. No weighted average can recover from an absolute violation.
