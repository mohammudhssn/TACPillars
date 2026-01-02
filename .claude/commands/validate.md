# TAC Architecture Validator

Run comprehensive validation on the TAC Knowledge Architecture.

**Usage:** `/validate` or `/validate [pillar_number]`

**Argument:** $ARGUMENTS (optional pillar number, e.g., "1" or "all")

---

## VALIDATION PROTOCOL

### Step 1: Run Base Validation Script
Execute the existing validation script:
```bash
cd /home/user/TACPillars && python validate_pillars.py
```

Report the output including statistics, errors, and warnings.

---

### Step 2: Enhanced Checks

If a specific pillar number was provided, focus checks on that pillar. Otherwise, check all pillars in `data/pillars.json`.

#### A. SCOPE PURITY VERIFICATION
For each pillar being validated, check against the ontology rules in `/docs/3_ontology.txt`:

| Pillar | Scope Rule | Red Flags |
|--------|------------|-----------|
| 1 | Patient/physiology only | Workforce, compensation, laws, wellbeing topics |
| 2 | Role definitions only | Career transitions, economics, operations |
| 3 | Environment/tools only | Contracts, culture, career advice |
| 4 | Rules/compliance only | Business strategy, compensation |
| 5 | Money/contracts only | Education, wellbeing, clinical practice |
| 6 | Knowledge/teaching only | Workforce deployment, bedside decisions |
| 7 | Career/leadership only | Role definitions, culture, contracts |
| 8 | Human experience only | Research, clinical, economics, legal |

**Check each Topic Domain title and definition. Flag any that:**
- Contain concepts belonging to a different pillar
- Mix multiple pillar concerns
- Have ambiguous placement

---

#### B. EXCLUSIVE PLACEMENT DETECTION
Search for potential duplicate concepts across pillars:
1. Extract all Topic Domain titles
2. Identify semantically similar topics that might exist in multiple pillars
3. Flag any concept that appears to be duplicated

**Common overlap patterns to check:**
- "Training" (Pillar 2 role training vs Pillar 6 education methods)
- "Compliance" (Pillar 4 legal vs Pillar 3 operational)
- "Leadership" (Pillar 7 career vs Pillar 8 culture)

---

#### C. ATOMIC PRECISION ANALYSIS
For each Topic Domain, verify it's a single teachable unit:

**Flags for non-atomic topics:**
- Title contains "and" joining unrelated concepts
- Definition describes multiple distinct ideas
- Scope is too broad (could be split into 3+ subtopics)
- Scope is too narrow (should be a subtopic, not a domain)

**Size Reference (from Pillar 7):**
- Good Topic Domain: "W2 to 1099 Transition Planning"
- Too Broad: "All Career Transitions and Financial Planning"
- Too Narrow: "How to Fill Out IRS Form 1099-NEC"

---

#### D. STRUCTURAL INTEGRITY
Compare against Pillar 7 reference structure (`data/pillar_7_reference.json`):

1. **Hierarchy check:** Every Topic Domain has a Branch parent, every Branch has a Sub-Pillar parent
2. **ID format check:** IDs follow pattern `X.Y.Z.N` (Pillar.SubPillar.Branch.TopicDomain)
3. **Balance check:** Flag Sub-Pillars with <2 or >8 Branches, Branches with <3 or >12 Topic Domains
4. **Completeness check:** All required fields present and non-empty

---

### Step 3: Generate Report

Output a structured report:

```
============================================================
TAC ARCHITECTURE VALIDATION REPORT
============================================================
Pillar(s) Validated: [X or ALL]
Timestamp: [current time]

STATISTICS
------------------------------------------------------------
[Output from validate_pillars.py]

CRITICAL ERRORS (Must Fix Before Commit)
------------------------------------------------------------
[List any blocking issues]

SCOPE PURITY ISSUES
------------------------------------------------------------
[List any cross-pillar contamination with specific fix suggestions]

EXCLUSIVE PLACEMENT CONCERNS
------------------------------------------------------------
[List potential duplicates with recommended resolution]

ATOMIC PRECISION WARNINGS
------------------------------------------------------------
[List topics that should be split or merged]

STRUCTURAL ISSUES
------------------------------------------------------------
[List hierarchy, ID, or balance problems]

ACTIONABLE FIX SUGGESTIONS
------------------------------------------------------------
For each issue found, provide:
1. Issue ID and location
2. What's wrong
3. Specific fix recommendation
4. Example of correct approach

VALIDATION SUMMARY
============================================================
[ ] PASSED - Ready to commit
[ ] PASSED WITH WARNINGS - Review recommended
[ ] FAILED - Fix errors before proceeding
```

---

## NOTES
- Read `/docs/3_ontology.txt` for pillar boundary definitions
- Use `/data/pillar_7_reference.json` as the gold standard for structure
- When in doubt, apply the inclusion/exclusion tests from the ontology
