**Reproduce:** the verified environment uses Python 3.14; `pip install -r requirements.txt`, open this notebook
# Week 7 - Ioannis Tzalas

## Start here

Submit **W7_Portfolio_Clustering_Tzalas.ipynb**, the executed notebook required by
the brief. It contains all analysis code, outputs, written interpretation and inline
figures. Keep the `data/` folder with it for reproducibility. The HTML file is an
offline readable copy. `W7_Analysis_Report.pdf` is a shorter companion report, not a
substitute for the notebook.

This is the lecturer's PCA/K-Means portfolio assignment applied to **70 equities
previously selected by SephWide**. The brief permits “assets/tokens” although its
title says DeFi. This is explicitly an equity application; clarify with the lecturer
if tokens were intended exclusively. No trading project files are modified.

## Measured results

- 72 recorded BUY names through 1 September 2026, without filtering for winners.
- NESR excluded for insufficient history; GOLD excluded for unresolved issuer
  identity after ticker reuse. All candidates and reasons remain in the data audit.
- 70 assets, 787 price dates, 1 September 2023–21 October 2026.
- 751 formation returns; 35 later comparison returns, 2 September–21 October 2026.
- 3 PCs retain 82.71% of standardized asset-feature variation.
- k=2 selected; silhouette 0.3881. The elbow suggests k=3, but it creates a
  single-stock group and fails the declared three-asset minimum.
- Net later cumulative returns at 10 bps one-way costs: Cluster 1 **-1.84%**,
  Cluster 2 **-2.96%**, all-asset equal weights **-2.05%**, equal clusters **-2.22%**,
  SPY **+1.53%**. These are constructed historical portfolios, not funded P&L.
- Full first-BUY illustration: 24 positive and 46 negative adjusted-price changes,
  with different holding lengths, no strategy exits and no execution claim.
  Five positive examples are explicitly selected retrospectively; losses remain.
- 69 in-notebook structural checks and 439 separate numerical/submission checks.
  These do not establish predictive success or independent third-party assurance.

## Reproduce offline

Verified with Python 3.14; exact versions are in `requirements.txt`.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python execute_notebook.py
python audit_submission.py
```

Alternatively open the notebook with your Jupyter application, set this folder as
the working directory, and run all cells. Inputs are already frozen: no API key,
trading-project checkout, broker connection or network access is needed.
The public refresh script saves a different data vintage under a new filename;
it does not replace the frozen inputs. `prepare_data.py` documents the original
collection and owner-authorized read-only export. It is local-source dependent
and is not part of ordinary reproduction. It refuses to overwrite the declaration.

The optional PDF companion uses ReportLab. The original verified artifact runtime
had ReportLab 4.4.9 available; PDF recreation also works with a compatible installed
ReportLab. This optional package is unnecessary for the submitted notebook.

## Package map

| Item | Purpose |
|---|---|
| Executed `.ipynb` | Primary submission; all 100 rubric points addressed |
| `.html` | Read without installing Jupyter |
| `W7_Analysis_Report.pdf` | Concise analysis with charts and limitations |
| `data/` | Frozen prices, signal-date export, sector metadata, provenance |
| `declaration.json` | Timestamped original design before price calculation |
| `results/` | Every candidate k/seed, memberships, exact weights, metrics, plots |
| `validation/numerical_audit.json` | Separate calculation receipts |
| `validation/execution_attempts.jsonl` | Chronological execution log |
| `validation/attempt_01_before_identity_exclusion/` | Superseded 71-asset results, preserved |
| `validation/project_readonly_verification.json` | Comparison of repository file hashes |
| `AI_DISCLOSURE_AND_PROMPTS.md` | Assistance and user prompt disclosure |
| `STUDY_GUIDE.md` | Questions to prepare for discussion with the lecturer |
| `reference/assignment_brief.pdf` | Supplied brief, unchanged |

## Rubric coverage

| Requirement | Notebook section |
|---|---|
| Data collection/preprocessing (15) | Part 1.1 |
| PCA, variance threshold, loadings (15) | Part 1.2 |
| K-Means, elbow, silhouette, membership, plots (20) | Part 1.3 |
| Portfolio composition and weights (10) | Part 2.1 |
| Cumulative return, Sharpe with interval, drawdown, volatility, alpha/beta (15) | Part 2.2 |
| Equity, distribution, risk/return, composition visuals (5) | Parts 1.3 and 2.3 |
| Interpretation, insights and caveats (20) | Part 3.1–3.3 |

The cover gives conflicting Week 8/9 deadline wording; the body/final line say
before Week 8, so use that as the working deadline. The precise date is not supplied.
The brief mentions 30 bonus points but specifies no bonus tasks. No presentation or
Week 6 code-cell cap is required by this Week 7 document.

## Important evidence limits and corrections

The first version admitted 71 names and was executed before the GOLD issuer problem
was identified. The final 70-name version excludes it for identity, without mapping
the signal to another company or optimizing on its return. The first notebook/results
and timestamped identity receipt are retained. There are **two analytical data
versions**, each containing 28 declared fits with 50 initializations: 56 distinct
version-specific fits / 2,800 starts. Routine re-execution of the same fixed version
is recorded separately and is not a new research variant.

The later comparison is conditional and retrospective, and was inspected during
quality review. It is not an untouched or prospective holdout. No production candidate
is proposed. Selection/survivorship, data vintage, only 35 evaluation sessions,
model assumptions and simplified trading costs materially limit conclusions.
The exported project records are strategy signals, not proof of funded execution.
Source links and formulas are in the notebook and PDF. Review the AI disclosure
and understand the work before individual submission.
# Week 7 discussion guide

**What problem did you solve?** I used 70 stocks previously selected by SephWide
to ask whether price-derived risk and behaviour features produce interpretable
asset groups, then compared equal-weight portfolios over a later historical window.
I did not measure actual funded trading results or change the trading system.

**Why equities in a DeFi assignment?** The title says DeFi, but the data requirement
explicitly permits assets/tokens. I used the equity application to connect the
method to my own signal project and disclosed the scope. A token-only interpretation
would need the lecturer's agreement and a different dataset/calendar.

**Did you select only winners?** No. I froze all 72 distinct BUY names recorded by
1 September. Two failed data/identity checks, leaving 70. The requested five positive
examples are a separate retrospective table; 46 negative outcomes remain visible.

**Why exclude GOLD?** A ticker is not a permanent company identity. Barrick changed
from GOLD to B, and Gold.com later reused GOLD. I could not establish which issuer
the strategy intended from this export, so I excluded it rather than combine companies.
I retained the earlier result and disclosed that this correction followed inspection.

**What is a row in PCA?** One asset. Columns are eight features calculated from
formation-period daily returns. Clustering daily dates would classify market regimes,
not create groups of stocks.

**Why standardize?** Volatility, skewness and beta have different scales. Without
scaling, Euclidean distance can be dominated by large numerical units. Correlated
risk features still receive substantial collective influence, which is a limitation.

**What does 82.71% mean?** Three principal directions retain 82.71% of variation
in the standardized asset-feature matrix. It does not mean 82.71% of future returns
are explained, forecast correctly, or profitable.

**What do the PCs represent?** PC1 mainly separates higher-volatility, higher-beta,
larger-downside stocks from less risky stocks. PC2 and PC3 combine persistence,
market correlation, skewness and drawdown. Signs are arbitrary and economic labels
are descriptive, not causal laws.

**Why two clusters when the elbow suggests three?** The declared choice maximizes
training silhouette subject to at least three stocks per cluster. k=3 creates a
singleton and fails that constraint. The selected silhouette is 0.3881, a diagnostic
of separation, not proof of an optimal investment strategy.

**What are the groups?** Cluster 1 has 47 stocks and lower median formation-period
volatility/beta; Cluster 2 has 23 stocks and higher risk. These labels are relative
to this selected stock sample, not promises of low absolute risk.

**What happened later?** In 35 sessions after formation, net cumulative returns at
assumed 10 bps one-way costs were -1.84% and -2.96%, versus SPY +1.53%. The portfolio
test therefore does not demonstrate an advantage, despite individual successful signals.

**Why does the less negative-return cluster have a worse Sharpe?** Sharpe measures
mean excess return divided by variability, not cumulative return. A modest negative
excess mean divided by much smaller volatility can yield a more negative ratio.
Both cluster intervals include zero, and 35 sessions are far too short for confident
ranking. Always read the saved Sharpe together with its 85% interval.

**Why not call this a clean out-of-sample proof?** Features and model selection use
earlier dates, but membership comes from my later strategy history, prior project
knowledge exists, and the identity correction followed first-result inspection.
The split is chronologically separated but conditional and retrospective.

**Why MRNA as an example?** Its first recorded BUY predates a very large price rise,
and an issuer announcement gives dated clinical-trial context. This does not prove
the model anticipated the announcement. Its hypothetical holding starts after the
signal and ignores real strategy exits, costs and sizing.

**What do the checks prove?** They reconcile calculations and enforce the stated
rules. They do not prove the vendor data are flawless, the model has predictive
skill, the work is independently audited, or the approach should move real money.

**What would you do next?** Predeclare a genuinely future cohort, verify price and
issuer identity against independent records, include dead/rejected stocks, measure
execution costs and temporal cluster stability, and collect a much longer record.