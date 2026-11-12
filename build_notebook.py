"""Build the self-contained coursework notebook; run it separately in a fresh kernel."""
from pathlib import Path
import textwrap
import json

ROOT = Path(__file__).resolve().parent
cells = []


def md(text):
    cells.append({
        'cell_type': 'markdown',
        'metadata': {},
        'source': [l + chr(10) for l in textwrap.dedent(text).strip().splitlines()]
    })


def code(text):
    cells.append({
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [l + chr(10) for l in textwrap.dedent(text).strip().splitlines()]
    })


md('''
# Week 7 | Portfolio clustering with SephWide signals
## PCA, K-Means and a transparent historical portfolio comparison
**Ioannis Tzalas · MSc Banking & Finance · 5 November 2026**

### README and research question
Can price-derived risk and behaviour features organize stocks previously selected by
SephWide into economically interpretable groups, and how did equal-weight portfolios
of those groups behave over a later historical window?

The brief is titled *DeFi Portfolio Clustering & Analysis*, but its operative data
requirement permits at least 50 **assets/tokens**. This submission uses US-listed
equities previously selected by my SephWide algorithmic signal system. It is an
equity application of the required methods; it makes no DeFi-token claim. If the
lecturer intended tokens only, this scope needs their agreement.

**Design frozen before this calculation:** all distinct recorded BUY tickers dated
on or before **1 September 2026**, regardless of their subsequent performance.
Fit period: **1 September 2023–1 September 2026**. Later comparison:
**2 September–21 October 2026**. The complete declaration and download receipts
are included. Earlier knowledge of this project and later-selected signal membership
mean this is a **conditional retrospective study**, not a new prospective holdout.

SephWide's signals can influence real capital. Its exported strategy records and
the portfolios constructed here are **not authenticated funded-account fills or
funded P&L**. This assignment neither runs nor modifies SephWide.

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
had ReportLab 4.4.10 available; PDF recreation also works with a compatible installed
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
from this folder, and Run All. Frozen CSV inputs make the notebook work offline.
`prepare_data.py` documents the one-time public Yahoo Finance download and the
read-only project export; it is not needed to reproduce the submitted results.
`refresh_prices.py` can make a separately named public-data refresh without access
to SephWide. A refresh is a new data vintage and may change results.

**Integrity and attribution:** analysis/code drafted with OpenAI Codex assistance,
with numerical checks included. The prompt record is supplied. The submission is
individual; the student must understand and review it under the course's AI policy.
No claim is made that generated work was independently authored without assistance.
''')

md('''
## Part 1.1 | Data collection and preprocessing (15 points)
Yahoo Finance daily adjusted close prices are downloaded through `yfinance` with
`auto_adjust=True`: these are adjusted-price return proxies, not executable trade
quotes. SPY is an equity market comparator. Sector labels are a dated local metadata
snapshot used only to interpret the clusters. Signal timestamps establish recorded
membership, not original vendor availability or broker execution.

Rules: use SPY's observed session dates; require at least 99% **fit-period** price
coverage and exact first/last fit prices. Allow at most two consecutive missing
prices, filled forward using only earlier observations. Never backfill or interpolate.
Exclude invalid/insufficient fit histories with a reason; all admitted stocks must
then have usable later data or execution stops. No stock is admitted/excluded based
on later return. Large daily moves are flagged for review, never automatically erased.
''')
code('''
from pathlib import Path
import hashlib, json, platform, warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples, adjusted_rand_score
from IPython.display import display, Markdown

ROOT = Path.cwd()
assert (ROOT / 'declaration.json').exists(), 'Run from the submission folder.'
OUT = ROOT / 'results'; OUT.mkdir(exist_ok=True)
CFG = json.loads((ROOT / 'declaration.json').read_text())
SEED, ANN = CFG['seed'], CFG['annualization']
RF = (1 + CFG['risk_free_annual']) ** (1 / ANN) - 1
plt.rcParams.update({'figure.figsize': (10, 5), 'figure.dpi': 130,
                     'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.titlesize': 13, 'font.size': 10, 'savefig.bbox': 'tight'})
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 14)
checks = []
def check(name, condition):
    assert bool(condition), name
    checks.append({'check': name, 'passed': True})
def savefig(name):
    plt.savefig(OUT / (name + '.png'), dpi=160)
    plt.show()
def say(text):
    display(Markdown(text))
provenance = json.loads((ROOT / 'data/provenance.json').read_text())
for relative, expected in provenance['files'].items():
    check('Input hash: ' + relative,
          hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected)
versions = {'python': platform.python_version(), 'pandas': pd.__version__,
            'numpy': np.__version__, 'scikit-learn': sklearn.__version__}
(OUT / 'environment.json').write_text(json.dumps(versions, indent=2))
display(pd.Series(versions, name='Executed environment'))
''')
code('''
raw = pd.read_csv(ROOT / 'data/adjusted_close_raw.csv', index_col=0, parse_dates=True)
universe = pd.read_csv(ROOT / 'data/universe.csv').set_index('ticker')
signals = pd.read_csv(ROOT / 'data/sephwide_buy_signals.csv')
check('Dates unique and increasing', raw.index.is_unique and raw.index.is_monotonic_increasing)
check('Signals precede comparison', (pd.to_datetime(signals.date) <= pd.Timestamp(CFG['fit_end'])).all())
check('Universe is all frozen BUY names', set(universe.index) == set(signals.ticker.unique()))
sessions = raw.index[raw.SPY.notna()]
px = raw.reindex(sessions)
fit_mask = px.index <= CFG['fit_end']
audit, admitted = [], []
for ticker in universe.index:
    s = px[ticker]; f = s.loc[fit_mask]
    runs = f.isna().groupby(f.notna().cumsum()).sum()
    coverage = f.notna().mean()
    reasons = []
    identity_receipt = json.loads((ROOT / 'data/identity_exclusions.json').read_text())
    if ticker in identity_receipt['exclusions']:
        reasons.append(identity_receipt['exclusions'][ticker])
    if coverage < .99: reasons.append('fit coverage below 99%')
    if pd.isna(f.iloc[0]) or pd.isna(f.iloc[-1]): reasons.append('missing fit endpoint')
    if runs.max() > 2: reasons.append('fit gap exceeds 2 sessions')
    if (f.dropna() <= 0).any(): reasons.append('nonpositive fit price')
    audit.append({'ticker': ticker, 'fit_coverage': coverage, 'fit_missing': f.isna().sum(),
                  'status': 'excluded' if reasons else 'admitted', 'reason': '; '.join(reasons)})
    if not reasons: admitted.append(ticker)
audit = pd.DataFrame(audit).set_index('ticker')
audit.to_csv(OUT / 'data_quality.csv')
prices = px[admitted + ['SPY']].ffill(limit=2)
check('At least 50 admitted assets', len(admitted) >= 50)
check('Fit spans at least 24 months', prices.loc[fit_mask].index[-1] >= prices.index[0] + pd.DateOffset(months=24))
check('No unusable later price; no outcome-dependent removal', prices.notna().all().all())
check('Prices positive and finite', np.isfinite(prices).all().all() and (prices > 0).all().all())
check('Exact comparison end exists', str(prices.index[-1].date()) == CFG['evaluation_end'])
ret = prices.pct_change(fill_method=None).iloc[1:]
train = ret.loc[:CFG['fit_end']]
test = ret.loc[CFG['evaluation_start']:CFG['evaluation_end']]
check('Chronological disjoint return dates', train.index.max() < test.index.min())
check('No weekend return rows', (ret.index.dayofweek < 5).all())
flags = ret.stack()[ret.stack().abs() > .5].rename('daily_return').reset_index()
flags.to_csv(OUT / 'large_move_flags.csv', index=False)
say(f'**Measured coverage:** {len(admitted)} of {len(universe)} assets admitted; '
    f'{len(prices)} daily price rows, {prices.index[0].date()}–{prices.index[-1].date()}. '
    f'{len(train)} fit returns; **{len(test)} comparison returns**. '
    f'{len(flags)} daily moves above 50% flagged. Full inclusion/exclusion audit is supplied.')
display(audit)
''')

md('''
### Feature matrix: assets are the observations
Clustering dates would answer the wrong question. Here each **row is one asset**
and each column is a summary of its **fit-period daily adjusted-price returns**:
annualized mean, annualized sample volatility, downside deviation from zero,
sample skewness, maximum drawdown, SPY beta, SPY correlation and lag-one autocorrelation.
All eight features derive from the required prices. Downside deviation is
`sqrt(252 * mean(min(r,0)^2))`; beta is `cov(r,SPY)/var(SPY)`.
Price levels are not comparable across differently priced shares, so returns are
used instead. StandardScaler centers/scales each feature **across training assets**.
The correlated risk features deliberately permit economic interpretation, but may
overweight the common risk dimension. No later returns enter these features.
''')
code('''
def max_drawdown(r):
    wealth = np.r_[1., np.cumprod(1 + np.asarray(r, dtype=float))]
    return float(np.min(wealth / np.maximum.accumulate(wealth) - 1))

def asset_features(returns):
    market = returns['SPY']
    result = {}
    for ticker in admitted:
        r = returns[ticker]
        result[ticker] = {
            'mean_ann': r.mean() * ANN,
            'vol_ann': r.std(ddof=1) * np.sqrt(ANN),
            'downside_ann': np.sqrt(np.minimum(r, 0).pow(2).mean() * ANN),
            'skew': r.skew(), 'max_drawdown': max_drawdown(r),
            'beta_spy': r.cov(market) / market.var(ddof=1),
            'corr_spy': r.corr(market), 'autocorr1': r.autocorr(1)}
    return pd.DataFrame.from_dict(result, orient='index')[CFG['features']]

features = asset_features(train)
check('Eight finite price-derived features per asset', features.shape == (len(admitted), 8) and np.isfinite(features).all().all())
scaler = StandardScaler()
X = scaler.fit_transform(features)
check('Standardized feature means', np.allclose(X.mean(axis=0), 0, atol=1e-10))
check('Standardized feature variances', np.allclose(X.var(axis=0), 1, atol=1e-10))
features.to_csv(OUT / 'training_features.csv', index_label='ticker')
display(features.describe().round(3))
fig, ax = plt.subplots(figsize=(9, 6))
im = ax.imshow(features.corr(), vmin=-1, vmax=1, cmap='RdBu_r')
ax.set_xticks(range(8), features.columns, rotation=50, ha='right')
ax.set_yticks(range(8), features.columns)
ax.set_title('Training-feature correlation | shared risk information')
fig.colorbar(im, ax=ax, shrink=.8)
savefig('01_feature_correlation')
''')

md('''
## Part 1.2 | Principal component analysis (15 points)
Full-SVD PCA operates on the standardized asset-by-feature matrix. Retain the
**smallest number of components explaining at least 80%** of training cross-sectional
variance, a rule declared before performance evaluation. This balances compression
and information retention; it is not a claim of a unique optimal dimension.
PCA is centered, unwhitened and linear. K-Means uses all retained scores, so components
with more variance carry more weight. The charts may show only the first two/three.
Component signs are arbitrary; interpretations use joint feature directions.
''')
code('''
pca_full = PCA(svd_solver='full').fit(X)
cumulative = np.cumsum(pca_full.explained_variance_ratio_)
n_pc = int(np.searchsorted(cumulative, CFG['pca_variance_threshold']) + 1)
pca = PCA(n_components=n_pc, svd_solver='full')
Z = pca.fit_transform(X)
loadings = pd.DataFrame(pca.components_.T, index=features.columns,
                        columns=[f'PC{i+1}' for i in range(n_pc)])
variance = pd.DataFrame({'component': np.arange(1, 9),
                         'variance_ratio': pca_full.explained_variance_ratio_,
                         'cumulative': cumulative})
variance.to_csv(OUT / 'pca_variance.csv', index=False)
loadings.to_csv(OUT / 'pca_loadings.csv', index_label='feature')
check('PCA reaches threshold minimally', cumulative[n_pc-1] >= .8 and (n_pc == 1 or cumulative[n_pc-2] < .8))
check('PCA reconstruction identity', np.allclose(pca.inverse_transform(Z), Z @ pca.components_ + pca.mean_))
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
axes[0].bar(variance.component, variance.variance_ratio, color='#177e89', label='Individual')
axes[0].plot(variance.component, cumulative, 'o-', color='#d37627', label='Cumulative')
axes[0].axhline(.8, color='grey', linestyle='--', label='80% threshold')
axes[0].axvline(n_pc, color='grey', alpha=.5)
axes[0].set(xlabel='Principal component', ylabel='Explained variance', title=f'{n_pc} PCs retain {cumulative[n_pc-1]:.1%}')
axes[0].legend(fontsize=8)
im = axes[1].imshow(loadings, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
axes[1].set_xticks(range(n_pc), loadings.columns)
axes[1].set_yticks(range(8), loadings.index)
axes[1].set_title('Component direction coefficients')
fig.colorbar(im, ax=axes[1], shrink=.8)
plt.tight_layout(); savefig('02_pca')
display(loadings.round(3))
for pc in loadings:
    strongest = loadings[pc].abs().nlargest(3).index
    say(f'**{pc}:** ' + ', '.join(f'{f} ({loadings.loc[f, pc]:+.3f})' for f in strongest) +
        '. These are direction coefficients in standardized feature units, not forecasts or causal effects.')
''')

md('''
## Part 1.3 | K-Means clustering (20 points)
Test the declared grid **k=2,…,8**, `k-means++`, 50 initializations, seed 42.
The elbow is an inertia diagnostic: the largest normalized distance below the chord
joining k=1 and k=8. Selection uses **maximum silhouette among solutions with at
least three assets per cluster**, breaking ties toward smaller k. The size constraint
avoids presenting single-stock outliers as diversified portfolios. The elbow can
disagree; both are reported rather than selecting on later returns.
K-Means minimizes within-cluster squared Euclidean distance. It assumes roughly
compact groups, is sensitive to outliers and imposes a hard partition on continuous
financial characteristics. Silhouette separation is not investment performance.
''')
code('''
models, trials = {}, []
inertia1 = KMeans(n_clusters=1, n_init=50, random_state=SEED).fit(X=Z).inertia_
for k in CFG['k_grid']:
    model = KMeans(n_clusters=k, n_init=50, random_state=SEED).fit(Z)
    sizes = np.bincount(model.labels_, minlength=k)
    models[k] = model
    trials.append({'k': k, 'inertia': model.inertia_,
                   'silhouette': silhouette_score(Z, model.labels_),
                   'min_size': sizes.min(), 'eligible': sizes.min() >= 3})
trials = pd.DataFrame(trials)
eligible = trials[trials.eligible].sort_values(['silhouette', 'k'], ascending=[False, True])
check('An eligible clustering exists', not eligible.empty)
chosen_k = int(eligible.iloc[0].k)
model = models[chosen_k]
# Deterministic reporting labels, ordered by increasing median training volatility.
raw_labels = pd.Series(model.labels_, index=features.index)
order = features.vol_ann.groupby(raw_labels).median().sort_values().index
label_map = {old: new + 1 for new, old in enumerate(order)}
labels = raw_labels.map(label_map).rename('cluster')
elbow_points = pd.concat([pd.DataFrame([{'k': 1, 'inertia': inertia1}]), trials[['k', 'inertia']]])
x = (elbow_points.k.to_numpy() - 1) / 7
y = (elbow_points.inertia.to_numpy() - elbow_points.inertia.iloc[-1]) / (inertia1 - elbow_points.inertia.iloc[-1])
elbow_k = int(elbow_points.iloc[np.argmax(1 - x - y)].k)
trials.to_csv(OUT / 'k_selection_all_attempts.csv', index=False)
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].plot(elbow_points.k, elbow_points.inertia, 'o-', color='#177e89')
axes[0].axvline(elbow_k, color='grey', linestyle='--', label=f'Chord elbow k={elbow_k}')
axes[0].set(xlabel='k', ylabel='Within-cluster sum of squares', title='Elbow diagnostic'); axes[0].legend(fontsize=8)
axes[1].plot(trials.k, trials.silhouette, 'o-', color='#d37627')
axes[1].scatter(trials.loc[~trials.eligible, 'k'], trials.loc[~trials.eligible, 'silhouette'], marker='x', s=100, color='red', label='Size constraint fails')
axes[1].axvline(chosen_k, color='grey', linestyle='--', label=f'Chosen k={chosen_k}')
axes[1].set(xlabel='k', ylabel='Mean silhouette', title='Training separation'); axes[1].legend(fontsize=8)
plt.tight_layout(); savefig('03_k_selection')
display(trials.round(4))
say(f'**Selected k={chosen_k}; chord elbow k={elbow_k}.** '
    f'The selected training silhouette is {eligible.iloc[0].silhouette:.3f}. '
    'All seven candidate partitions are retained, including those refused by the size rule. '
    'No later-return ranking was used to choose k.')
''')
code('''
members = universe.loc[admitted].join(labels).join(features)
coords = pd.DataFrame(Z, index=admitted, columns=loadings.columns)
members.join(coords).to_csv(OUT / 'asset_cluster_membership.csv', index_label='ticker')
profile = features.join(labels).groupby('cluster').median()
profile.insert(0, 'n_assets', labels.value_counts().sort_index())
profile.to_csv(OUT / 'cluster_training_profiles.csv')
composition = pd.crosstab(members.cluster, members.sector)
composition.to_csv(OUT / 'cluster_sector_counts.csv')
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
colors = plt.get_cmap('tab10')
for group in range(1, chosen_k + 1):
    take = labels == group
    axes[0].scatter(Z[take, 0], Z[take, 1], s=45, alpha=.85,
                    color=colors(group-1), label=f'C{group} (n={take.sum()})')
    for ticker in labels[take].index:
        i = admitted.index(ticker)
        axes[0].annotate(ticker, Z[i, :2], fontsize=6, alpha=.8)
axes[0].set(xlabel='PC1', ylabel='PC2', title='Assets in the first two PCA directions')
axes[0].legend(fontsize=8)
samples = silhouette_samples(Z, model.labels_)
start = 0
for group in range(1, chosen_k + 1):
    s = np.sort(samples[labels.to_numpy() == group]); stop = start + len(s)
    axes[1].fill_betweenx(np.arange(start, stop), 0, s, color=colors(group-1), alpha=.8)
    axes[1].text(.01, (start + stop) / 2, f'C{group}', fontsize=8); start = stop + 3
axes[1].axvline(samples.mean(), color='black', linestyle='--')
axes[1].set(xlabel='Per-asset silhouette', ylabel='Assets grouped by cluster', title='Separation includes weak/negative assignments')
plt.tight_layout(); savefig('04_clusters')
composition.plot(kind='bar', stacked=True, figsize=(11, 5), colormap='tab20')
plt.title('Economic composition | sector counts, not causal labels')
plt.xlabel('Cluster'); plt.ylabel('Number of assets')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8)
savefig('05_sector_composition')
display(profile.round(3))
for group in range(1, chosen_k + 1):
    names = members.index[members.cluster == group].tolist()
    sector = members.loc[names, 'sector'].value_counts()
    say(f'**Cluster {group} — {len(names)} assets.** Leading sector: {sector.index[0]} '
        f'({sector.iloc[0]}/{len(names)}); median training volatility '
        f'{profile.loc[group, "vol_ann"]:.1%}, beta {profile.loc[group, "beta_spy"]:.2f}, '
        f'drawdown {profile.loc[group, "max_drawdown"]:.1%}. Constituents: ' + ', '.join(names) + '.')
''')
md('''
### Cluster validation and full attempt accounting
Twenty additional seeds at the selected k are fitted on the same training scores.
Adjusted Rand index (ARI) compares partitions independently of arbitrary label
numbers. This measures optimizer sensitivity, not stability across future regimes.
For this final data version the attempt ledger records one k=1 elbow baseline,
seven candidate-k fits and twenty seed checks: **28 fits, each with 50 initialization
restarts (1,400 starts)**. An earlier 71-asset version was calculated before the
`GOLD` identity exclusion; its notebook/results are retained under validation.
Across both data versions: **56 fits and 2,800 starts**. The data correction happened
after initial result inspection; this comparison is not an untouched holdout.
No failed/ineligible candidate is deleted. These unsupervised comparisons do not
constitute 28 independent tests of profitability.
''')
code('''
stability = []
for seed in range(20):
    other = KMeans(n_clusters=chosen_k, n_init=50, random_state=seed).fit(Z)
    stability.append({'seed': seed, 'ari_vs_selected': adjusted_rand_score(model.labels_, other.labels_),
                      'inertia': other.inertia_})
stability = pd.DataFrame(stability)
stability.to_csv(OUT / 'seed_stability_all_attempts.csv', index=False)
say(f'**Optimizer stability:** ARI median {stability.ari_vs_selected.median():.3f}, '
    f'minimum {stability.ari_vs_selected.min():.3f} across all 20 seed checks. '
    'A high value means these starts agree; it cannot establish stationary economic groups.')
display(stability.round(4))
''')

md('''
## Part 2.1 | Portfolio construction (10 points)
Each cluster starts with equal weights `1/n_cluster`. Equal weights avoid estimating
expected-return inputs from this small, selected sample. Holdings rebalance daily
to those fixed targets. We also show: (i) equal weights across all admitted assets;
(ii) equal capital across clusters, equal weights within each; (iii) SPY.
The equal-cluster allocation is fixed before later performance is inspected; it
overweights small clusters relative to the all-asset comparator. Every target
weight is supplied, including this concentration effect. These are educational
portfolios constructed here, not historical SephWide allocations or trade replay.

**Costs:** 10 basis points per unit of one-way traded notional, including initial
purchases, drift-rebalancing and final liquidation. One-way turnover is
`sum(abs(target_weight - drifted_weight))`, not half that sum. Costs are applied
multiplicatively to wealth. The small reduction in invested notional needed to pay
fees is approximated by the turnover charge; an exact self-financing impact model
is outside this exercise. Sensitivities of 0 and 25 bps are reported without changing
portfolio design. Taxes, spread variation, market impact, capacity and borrow are
not modeled. All positions are long-only with no leverage.
''')
code('''
weights = pd.DataFrame(0., index=admitted,
                       columns=[f'Cluster {g}' for g in range(1, chosen_k + 1)])
for g in range(1, chosen_k + 1):
    take = labels == g
    weights.loc[take, f'Cluster {g}'] = 1 / take.sum()
weights['All assets EW'] = 1 / len(admitted)
weights['Equal clusters'] = weights.filter(like='Cluster ').sum(axis=1) / chosen_k
check('All portfolio targets sum to one', np.allclose(weights.sum(), 1))
check('Long-only weights', (weights >= 0).all().all())
weights.to_csv(OUT / 'portfolio_target_weights.csv', index_label='ticker')
display(weights.round(4))

def simulate(asset_returns, target, cost_bps=10):
    target = np.asarray(target, dtype=float)
    r = np.asarray(asset_returns, dtype=float)
    check('Simulator input alignment and finite returns', r.shape[1] == len(target) and np.isfinite(r).all())
    check('Simulator weights valid', np.isclose(target.sum(), 1) and np.min(target) >= 0)
    gross = r @ target
    turnover = np.empty(len(r)); turnover[0] = np.abs(target).sum()
    for t in range(1, len(r)):
        drift = target * (1 + r[t-1]) / (1 + gross[t-1])
        turnover[t] = np.abs(target - drift).sum()
    fee = cost_bps / 10000
    net = (1 - fee * turnover) * (1 + gross) - 1
    net[-1] = (1 + net[-1]) * (1 - fee) - 1  # liquidate once, at the end
    return net, turnover

later, turns = {}, {}
for name in weights:
    later[name], turns[name] = simulate(test[admitted], weights[name], 10)
later['SPY'], turns['SPY'] = simulate(test[['SPY']], [1.], 10)
later = pd.DataFrame(later, index=test.index)
turns = pd.DataFrame(turns, index=test.index)
later.to_csv(OUT / 'comparison_net_daily_returns.csv', index_label='Date')
turns.to_csv(OUT / 'comparison_one_way_turnover.csv', index_label='Date')
''')

md('''
## Part 2.2 | Performance metrics and uncertainty (15 points)
For net simple daily returns `r`, equity is `cumprod(1+r)` and cumulative return
is final equity minus one. Annualized volatility uses sample standard deviation
times `sqrt(252)`. Sharpe is `sqrt(252) * mean(r-rf_daily) / std(r-rf_daily)`, with
**3% annual risk-free assumption** converted by `(1.03)^(1/252)-1`.
This is an explicit constant assumption, not a downloaded historical cash yield.
Maximum drawdown includes initial wealth 1, so a first-day loss is counted.

Beta is the sample covariance of portfolio and **gross adjusted SPY excess returns**
divided by benchmark variance. Alpha is `252 * (mean(portfolio excess) - beta *
mean(SPY excess))`, an arithmetic annualized regression intercept. It is reported
with an 85% circular-block-bootstrap interval, not interpreted as proven alpha.
SPY's net portfolio is shown for fair cost comparison; regression uses gross SPY.

Every displayed Sharpe includes an **85% percentile interval** from 2,000 circular
moving-block resamples of length five. Portfolio/market pairs are resampled together
for alpha. These intervals condition on the selected assets, fixed clusters and this
short regime; they ignore universe/model-selection uncertainty and are not
simultaneous or anytime-valid intervals. No annualized return extrapolation is used
to claim a year of observed profit.
''')
code('''
def performance(r, market):
    r = np.asarray(r, dtype=float); market = np.asarray(market, dtype=float)
    excess, mx = r - RF, market - RF
    sd = excess.std(ddof=1)
    beta = np.cov(excess, mx, ddof=1)[0, 1] / mx.var(ddof=1)
    return {'cumulative_return': np.prod(1 + r) - 1,
            'vol_ann': r.std(ddof=1) * np.sqrt(ANN),
            'max_drawdown': max_drawdown(r),
            'sharpe': np.sqrt(ANN) * excess.mean() / sd if sd > 0 else np.nan,
            'beta': beta, 'alpha_ann': ANN * (excess.mean() - beta * mx.mean())}

def block_intervals(r, market, seed=42, repetitions=2000, block=5):
    r, m = np.asarray(r), np.asarray(market)
    n = len(r); rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, (repetitions, int(np.ceil(n / block))))
    ix = ((starts[..., None] + np.arange(block)) % n).reshape(repetitions, -1)[:, :n]
    a, b = r[ix] - RF, m[ix] - RF
    sd = a.std(axis=1, ddof=1)
    sr = np.divide(a.mean(axis=1) * np.sqrt(ANN), sd,
                   out=np.full(repetitions, np.nan), where=sd > 0)
    ac, bc = a - a.mean(axis=1, keepdims=True), b - b.mean(axis=1, keepdims=True)
    beta = (ac * bc).sum(axis=1) / (bc * bc).sum(axis=1)
    alpha = ANN * (a.mean(axis=1) - beta * b.mean(axis=1))
    return np.nanquantile(sr, [.075, .925]), np.nanquantile(alpha, [.075, .925])

metrics = []
for name in later:
    row = performance(later[name], test.SPY)
    sr_ci, alpha_ci = block_intervals(later[name], test.SPY)
    row.update({'portfolio': name, 'sharpe_low85': sr_ci[0], 'sharpe_high85': sr_ci[1],
                'alpha_low85': alpha_ci[0], 'alpha_high85': alpha_ci[1],
                'one_way_notional_turnover': turns[name].sum() + 1, 'n_sessions': len(test)})
    metrics.append(row)
metrics = pd.DataFrame(metrics).set_index('portfolio')
metrics.to_csv(OUT / 'performance_metrics.csv')
readable = pd.DataFrame(index=metrics.index)
for col in ['cumulative_return', 'vol_ann', 'max_drawdown']:
    readable[col] = metrics[col].map(lambda x: f'{x:.2%}')
readable['Sharpe [85% interval]'] = [f'{r.sharpe:.2f} [{r.sharpe_low85:.2f}, {r.sharpe_high85:.2f}]' for r in metrics.itertuples()]
readable['beta'] = metrics.beta.round(2)
readable['alpha ann [85% interval]'] = [f'{r.alpha_ann:.1%} [{r.alpha_low85:.1%}, {r.alpha_high85:.1%}]' for r in metrics.itertuples()]
display(readable)
say(f'All metrics use the same **{len(test)} sessions**. Annualized Sharpe/alpha '
    'are noisy scale conversions from this window; the interval is conditional and '
    'does not turn a historical winner into an investable discovery.')
''')

md('''
## Part 2.3 | Portfolio visualizations (5 points)
All curves begin at one before the first return and include entry and exit charges.
The risk-return chart uses observed cumulative return and annualized volatility,
avoiding annualized-return extrapolation from the short comparison. Histograms
show realized daily distributions; they are not forecasts or normality tests.
''')
code('''
equity = (1 + later).cumprod()
anchor = pd.DataFrame(1., index=[pd.Timestamp(CFG['fit_end'])], columns=equity.columns)
equity = pd.concat([anchor, equity])
equity.to_csv(OUT / 'comparison_equity.csv', index_label='Date')
fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
for name in later:
    style = '--' if name in ['SPY', 'All assets EW'] else '-'
    axes[0].plot(equity.index, equity[name], style, label=name)
axes[0].set(title='Later historical window | net of assumed 10 bps costs', ylabel='Wealth from 1')
axes[0].tick_params(axis='x', rotation=30); axes[0].legend(fontsize=7)
for g in range(1, chosen_k + 1):
    axes[1].hist(later[f'Cluster {g}'] * 100, bins=12, alpha=.45, label=f'C{g}')
axes[1].set(title='Cluster daily net-return distributions', xlabel='Daily return (%)', ylabel='Sessions')
axes[1].legend(fontsize=8)
plt.tight_layout(); savefig('06_equity_and_distributions')
fig, ax = plt.subplots(figsize=(9, 5))
for name, row in metrics.iterrows():
    ax.scatter(row.vol_ann * 100, row.cumulative_return * 100, s=70)
    ax.annotate(name, (row.vol_ann * 100, row.cumulative_return * 100), xytext=(5, 5), textcoords='offset points', fontsize=8)
ax.axhline(0, color='grey', linewidth=.7)
ax.set(xlabel='Annualized daily volatility (%)', ylabel='Observed cumulative net return (%)',
       title=f'Risk versus realized return | {len(test)} comparison sessions')
savefig('07_risk_return')
''')
code('''
sensitivity = []
for bps in [0, 10, 25]:
    for name in weights:
        rr, _ = simulate(test[admitted], weights[name], bps)
        sensitivity.append({'cost_bps': bps, 'portfolio': name,
                            'cumulative_return': np.prod(1 + rr) - 1})
    rr, _ = simulate(test[['SPY']], [1.], bps)
    sensitivity.append({'cost_bps': bps, 'portfolio': 'SPY', 'cumulative_return': np.prod(1 + rr) - 1})
sensitivity = pd.DataFrame(sensitivity)
sensitivity.to_csv(OUT / 'cost_sensitivity_all_scenarios.csv', index=False)
display(sensitivity.pivot(index='portfolio', columns='cost_bps', values='cumulative_return').map(lambda x: f'{x:.2%}'))
say('Cost scenarios are the declared 0/10/25 bps alternatives. No cost setting or '
    'allocation is selected because its later result looks better.')
''')

md('''
## SephWide connection | Recorded signals that subsequently rose
This is a separate **retrospective illustration**, requested for the project link.
For every frozen BUY name, use the **first recorded BUY date**, then the first
available adjusted close **strictly after** that date (never the possibly partial
signal-day close), and compare it with the final adjusted close on 21 October.
The table retains positive and negative cases and records entry/end dates.

The top five positive returns are displayed as successful examples **chosen after
observing the outcome**. This selection is not evidence of overall predictive skill.
The baseline is a hypothetical close-to-end long position with matching SPY dates;
it ignores SephWide exits/top-ups/position sizing and is not its realized return.
The frozen main asset sample was not filtered using this table. Raw trade-log prices
are deliberately not treated as verified executions.
''')
code('''
first = signals.sort_values(['date', 'ts']).drop_duplicates('ticker').set_index('ticker')
cases = []
for ticker in admitted:
    signal_date = pd.Timestamp(first.loc[ticker, 'date'])
    entry_date = prices.index[prices.index > signal_date][0]
    end_date = prices.index[-1]
    gain = prices.loc[end_date, ticker] / prices.loc[entry_date, ticker] - 1
    market_gain = prices.loc[end_date, 'SPY'] / prices.loc[entry_date, 'SPY'] - 1
    cases.append({'ticker': ticker, 'signal_date': signal_date.date().isoformat(),
                  'illustration_entry_close': entry_date.date().isoformat(),
                  'end_close': end_date.date().isoformat(), 'cluster': int(labels[ticker]),
                  'adjusted_price_return': gain, 'matched_spy_return': market_gain,
                  'return_difference_pp': gain - market_gain})
cases = pd.DataFrame(cases).set_index('ticker')
cases.to_csv(OUT / 'all_signal_outcomes_including_losses.csv')
winners = cases[cases.adjusted_price_return > 0].nlargest(5, 'adjusted_price_return')
winners.to_csv(OUT / 'retrospectively_selected_positive_examples.csv')
display(winners.style.format({c: '{:.2%}' for c in ['adjusted_price_return', 'matched_spy_return', 'return_difference_pp']}))
say(f'**Complete record:** {(cases.adjusted_price_return > 0).sum()} positive, '
    f'{(cases.adjusted_price_return < 0).sum()} negative and '
    f'{(cases.adjusted_price_return == 0).sum()} flat price outcomes among {len(cases)} included names. '
    'Entries have different holding lengths and overlap. This is not a calibrated '
    'win probability, and transaction costs and actual strategy exits are absent here.')
fig, ax = plt.subplots(figsize=(11, 4.5))
ordered = cases.adjusted_price_return.sort_values()
ax.bar(range(len(ordered)), ordered * 100, color=np.where(ordered > 0, '#177e89', '#c35454'))
ax.set_xticks(range(len(ordered)), ordered.index, rotation=90, fontsize=6)
ax.set(ylabel='Adjusted-price change (%)', title='Every included first BUY | hypothetical next-close to final-close change')
ax.axhline(0, color='black', linewidth=.6)
savefig('08_all_signal_outcomes')
''')

md('''
## Part 3.1 | Results interpretation (8 points)
The following commentary is generated from the measured tables. Training profiles
explain economic grouping; later returns describe one realized market window.
Sector composition can support a mechanism hypothesis, but this dataset alone
cannot identify the news, valuation change or macro shock that caused a return.
''')
code('''
cluster_metrics = metrics.loc[[f'Cluster {g}' for g in range(1, chosen_k + 1)]]
best = cluster_metrics.cumulative_return.idxmax()
worst = cluster_metrics.cumulative_return.idxmin()
analysis = []
analysis.append(f'The {len(admitted)}-asset sample reduces from eight features to {n_pc} PCs, '
                f'retaining {cumulative[n_pc-1]:.1%} of training variance. The chosen '
                f'{chosen_k}-cluster partition has silhouette {eligible.iloc[0].silhouette:.3f}; '
                f'the inertia elbow suggests k={elbow_k}. These are training diagnostics, not a profit forecast.')
for g in range(1, chosen_k + 1):
    p = profile.loc[g]; names = members.index[members.cluster == g]
    top_sectors = members.loc[names, 'sector'].value_counts().head(2)
    sector_text = ', '.join(f'{sector} ({n})' for sector, n in top_sectors.items())
    row = metrics.loc[f'Cluster {g}']
    analysis.append(f'Cluster {g} contains {len(names)} stocks, led by {sector_text}. '
                    f'Its median training volatility is {p.vol_ann:.1%}, market beta {p.beta_spy:.2f}, '
                    f'and drawdown {p.max_drawdown:.1%}. In the later window its costed equal-weight '
                    f'portfolio returns {row.cumulative_return:.2%}, with annualized volatility '
                    f'{row.vol_ann:.1%}, maximum drawdown {row.max_drawdown:.1%}, and Sharpe '
                    f'{row.sharpe:.2f} [{row.sharpe_low85:.2f}, {row.sharpe_high85:.2f}] (85% interval). '
                    'The shared risk/sector exposures describe a plausible common sensitivity; '
                    'a causal explanation would require dated event and factor evidence.')
analysis.append(f'{best} is the realized return leader ({metrics.loc[best, "cumulative_return"]:.2%}); '
                f'{worst} is the laggard ({metrics.loc[worst, "cumulative_return"]:.2%}). '
                'These labels were assigned after the comparison and cannot justify picking the '
                'leader in advance. Portfolio diversification reduces idiosyncratic exposure, '
                'but clusters can remain correlated and a small group can concentrate sector risk.')
for paragraph in analysis: say(paragraph)
(OUT / 'measured_interpretation.json').write_text(json.dumps(analysis, indent=2))
''')

md('''
## Part 3.2 | Investment insights and allocation strategies (7 points)
1. **Use clusters as an exposure map.** Before adding another SephWide name, inspect
   whether it repeats an existing high-volatility/high-beta or sector exposure. This
   is a research interpretation, not a change to SephWide's production rules.
2. **Compare the two allocation policies already specified.** Equal capital across
   clusters reduces domination by the largest cluster but increases weights in small
   clusters. Equal weights across all stocks can be more balanced at the individual
   security level. The weight table makes this trade-off explicit.
3. **For a risk-constrained mandate**, investigate a lower-volatility cluster or
   explicit risk budgets using training data and a separate future validation. A
   low historical volatility estimate does not establish low future risk. Check
   individual-name and sector concentration, liquidity, and portfolio correlations.
4. **Do not chase the measured leader or the five successful signal examples.**
   Later ranking and conditional Sharpe intervals cannot establish a lasting
   risk-adjusted advantage. The actionable next step is to freeze this workflow and
   record future results before considering capital allocation or any strategy change.

The numerical equal-cluster and all-asset allocations are implementable research
examples. No live adoption is recommended from this short retrospective comparison.
''')
code('''
allocation_compare = readable.loc[['All assets EW', 'Equal clusters', 'SPY']]
display(allocation_compare)
corr_later = later.filter(like='Cluster ').corr()
corr_later.to_csv(OUT / 'later_cluster_return_correlations.csv')
say('**Observed cross-cluster correlations** show whether separate feature groups '
    'actually diversified this later window; unsupervised separation alone cannot answer that.')
display(corr_later.round(3))
''')

md('''
## Part 3.3 | Limitations and improvements (5 points)
- **Selection and survivorship:** these are stocks selected by a strategy in August/
  September 2026. Requiring sufficient price history also favors seasoned survivors.
  Results cannot describe the full historical opportunity set, dead stocks or the
  strategy's skill before these selections. Formation-date membership is fixed before
  later returns, but the overall study remains retrospective and informed by the project.
- **Data vintage/quality:** Yahoo adjusted closes may be revised and back-adjusted;
  no contemporaneous vendor vintage is claimed. SPY's observed dates are the calendar
  reference, not an independently certified exchange calendar. Forward fills can
  create zero returns and distort volatility. Corporate actions, symbol reuse and
  large moves need independent exchange/issuer verification. Sector labels are a
  snapshot and may be stale. No price or signal timestamp is a broker-fill receipt.
- **Short, dependent comparison:** only several weeks of later data, overlapping
  signal holding periods and one market regime. Annualization amplifies sampling
  noise. Five-session block bootstrap assumes locally repeatable dependence and does
  not capture every tail risk. Its 85% intervals condition on fixed selection/models;
  inspecting multiple clusters makes leader estimates optimistic. No multiplicity-
  adjusted alpha significance or strategy superiority is claimed.
- **Model assumptions:** linear PCA can miss nonlinear structure; scale choices and
  correlated features alter distances. K-Means assumes compact Euclidean groups,
  and outliers or small sample size can dominate. Silhouette and the elbow need not
  agree. Optimizer-seed stability is distinct from temporal stability. Features and
  cluster membership may change with market conditions.
- **Portfolio assumptions:** daily equal-weight rebalancing, fractional shares,
  adjusted-price return proxies, fixed friction and fixed risk-free rate. Execution
  timing, taxes, funding, liquidity, capacity, variable spread and market impact
  remain unmeasured. Alpha/beta use only SPY, so omitted factors can explain residuals.
- **Scope:** US equities demonstrate the asset workflow permitted by the text, not
  DeFi token behavior. Tokens would require 365-day annualization, 24/7 calendar,
  exchange/chain risks, staking/yield definitions, depegs and delisted-token coverage.
- **Next work:** freeze an independent future cohort; retain rejected/delisted names;
  verify corporate actions and data against another source; use a much longer forward
  record; assess rolling stability and robust scaling using training data; validate
  realistic execution costs and rebalance frequency. Any variants must be declared
  and counted rather than selected on this comparison window.

### Brief ambiguities recorded
The cover says “Before Week 8 or Week 9 Session,” whereas the body and final line
say “Before Week 8 Session.” Treat **before Week 8** as the working deadline and
confirm the calendar date with the lecturer. The brief states “100 (+30 bonus)”
but gives no bonus tasks or marking criteria. This notebook addresses the explicit
100-point rubric; it does not invent a bonus requirement or reuse Week 6's cell cap.
''')

md('''
## Verification and submission checklist
The independent audit script checks formulas with separate calculations, data hashes,
chronology, k-selection, exact weights, portfolio compounding, transaction costs,
and output completeness. The in-notebook policy checks below are **structural
checks**, not passed hypotheses of profitability. No project tests or agents run.
''')
code('''
check('Equity includes initial capital', np.allclose(equity.iloc[0], 1))
check('Equity reconciles to cumulative metric', np.allclose(equity.iloc[-1] - 1, metrics.cumulative_return))
check('Drawdown is nonpositive', (metrics.max_drawdown <= 0).all())
check('Sharpe intervals ordered', (metrics.sharpe_low85 <= metrics.sharpe_high85).all())
check('Alpha intervals ordered', (metrics.alpha_low85 <= metrics.alpha_high85).all())
check('Winner examples are subset, not universe filter', set(winners.index).issubset(set(cases.index)) and len(cases) == len(admitted))
check('Selected k satisfies declared selection', chosen_k == int(eligible.iloc[0].k))
check('Cluster weights do not depend on later returns', np.allclose(weights.filter(like='Cluster ').sum(), 1))
pd.DataFrame(checks).to_csv(OUT / 'notebook_structural_checks.csv', index=False)
summary = {'assets': len(admitted), 'price_rows': len(prices), 'train_returns': len(train),
           'comparison_returns': len(test), 'n_pc': n_pc, 'variance_retained': cumulative[n_pc-1],
           'k': chosen_k, 'elbow_k': elbow_k, 'silhouette': float(eligible.iloc[0].silhouette),
           'seed_ari_min': float(stability.ari_vs_selected.min()), 'fits_final_version': 28, 'initializations_final_version': 1400,
           'fits_including_superseded_data_version': 56, 'initializations_including_superseded_data_version': 2800,
           'structural_checks': len(checks), 'best_cluster': best, 'worst_cluster': worst,
           'positive_signal_cases': int((cases.adjusted_price_return > 0).sum()),
           'negative_signal_cases': int((cases.adjusted_price_return < 0).sum())}
(OUT / 'summary.json').write_text(json.dumps(summary, indent=2))
display(pd.Series(summary, name='Measured submission summary'))
''')

md('''
## References and source receipts
1. Course lecturer, *FinTechCourse_W7_assignment_v1.pdf*, supplied brief, pp. 1–4.
   Included under `reference/`; assignment requirements are treated as the rubric,
   not as authority to alter my trading project.
2. Yahoo Finance historical prices via yfinance, actual download time, requested
   span, version and SHA-256 receipts in `data/provenance.json`.
   [yfinance download documentation](https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html).
3. Scikit-learn: [StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html),
   [PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html),
   [KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html),
   [silhouette analysis](https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html).
   Documentation accessed 5 November 2026; executed versions are saved separately.
4. [NumPy](https://numpy.org/doc/stable/), [pandas](https://pandas.pydata.org/docs/),
   [Matplotlib](https://matplotlib.org/stable/) and [Jupyter](https://jupyter.org/):
   array/statistical calculations, tabular processing, plots and notebook presentation.
5. Sharpe, W. F. (1994), *The Sharpe Ratio*, Journal of Portfolio Management,
   21(1), 49–58. Ratio uses excess return divided by return variability.
6. Künsch, H. R. (1989), *The Jackknife and the Bootstrap for General Stationary
   Observations*, Annals of Statistics, 17(3), 1217–1241. Block resampling motivates
   dependence-aware uncertainty; the circular implementation and finite-sample
   limitations here are explicitly stated.
7. Private SephWide strategy BUY-date/ticker snapshot and sector metadata,
   read-only export authorized by the owner. Original log hash and project revision
   are in provenance; the portable notebook imports no project code or credentials.
8. OpenAI Codex, assisted Python drafting, rubric mapping and review, 5 November
   2026. Full available user-prompt wording and a workflow disclosure are supplied
   in `AI_DISCLOSURE_AND_PROMPTS.md`. This is not independent third-party validation.
''')

nb = {
    'cells': cells,
    'metadata': {
        'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
        'language_info': {'name': 'python', 'version': '3.14'},
    },
    'nbformat': 4,
    'nbformat_minor': 5
}
with open(ROOT / 'W7_Portfolio_Clustering_Tzalas.ipynb', 'w') as f:
    json.dump(nb, f, indent=2)
print('Built', len(cells), 'cells;', sum(c['cell_type'] == 'code' for c in cells), 'code cells')