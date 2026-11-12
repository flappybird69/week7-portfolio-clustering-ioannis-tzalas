"""Separate numerical audit; does not import or run the notebook's implementation."""
from pathlib import Path
import json
import math
import hashlib
from datetime import datetime, timezone
import numpy as np
import pandas as pd

P = Path(__file__).resolve().parent
O = P / 'results'
rows = []


def verify(name, value):
    rows.append({'check': name, 'passed': bool(value)})
    if not value:
        raise AssertionError(name)


def close(name, actual, expected, tol=1e-10):
    verify(name, np.allclose(actual, expected, rtol=tol, atol=tol, equal_nan=True))


raw = pd.read_csv(P / 'data/adjusted_close_raw.csv', index_col=0, parse_dates=True)
members = pd.read_csv(O / 'asset_cluster_membership.csv', index_col=0)
features = pd.read_csv(O / 'training_features.csv', index_col=0)
weights = pd.read_csv(O / 'portfolio_target_weights.csv', index_col=0)
metrics = pd.read_csv(O / 'performance_metrics.csv', index_col=0)
net = pd.read_csv(O / 'comparison_net_daily_returns.csv', index_col=0, parse_dates=True)
turnover = pd.read_csv(O / 'comparison_one_way_turnover.csv', index_col=0, parse_dates=True)
cfg = json.loads((P / 'declaration.json').read_text())
provenance = json.loads((P / 'data/provenance.json').read_text())
for file, expected in provenance['files'].items():
    verify('Frozen input SHA-256 ' + file, hashlib.sha256((P / file).read_bytes()).hexdigest() == expected)
verify('At least 50 assets', len(members) >= 50)
verify('Identity exclusion is retained', 'GOLD' not in members.index)
verify('Incomplete history exclusion retained', 'NESR' not in members.index)
verify('All original 72 candidates are audited', len(pd.read_csv(O / 'data_quality.csv')) == 72)
verify('No empty sector classification in final table', members.sector.notna().all())
verify('Fit/evaluation design is dated before collection completion',
       cfg['created_utc'] < provenance['completed_utc'])
prices = raw.loc[raw.SPY.notna(), members.index.tolist() + ['SPY']].ffill(limit=2)
verify('At least 24 months of prices', prices.index[-1] - prices.index[0] >= pd.Timedelta(days=730))
training = prices.loc[:cfg['fit_end']]
# Independent return calculation uses direct ratios rather than pct_change.
training_r = training.to_numpy()[1:] / training.to_numpy()[:-1] - 1
market_train = training_r[:, -1]
for ticker in members.index:
    j = prices.columns.get_loc(ticker); r = training_r[:, j]
    close('Mean feature ' + ticker, features.loc[ticker, 'mean_ann'], np.average(r) * 252)
    close('Volatility feature ' + ticker, features.loc[ticker, 'vol_ann'], np.std(r, ddof=1) * math.sqrt(252))
    beta = np.linalg.lstsq(np.column_stack([np.ones(len(r)), market_train]), r, rcond=None)[0][1]
    close('Training beta via regression ' + ticker, features.loc[ticker, 'beta_spy'], beta)

f = features.to_numpy()
x = (f - f.mean(axis=0)) / f.std(axis=0, ddof=0)
_, singular, _ = np.linalg.svd(x - x.mean(axis=0), full_matrices=False)
ratios = singular ** 2 / np.sum(singular ** 2)
variance = pd.read_csv(O / 'pca_variance.csv')
close('PCA variance via separate SVD', variance.variance_ratio, ratios)
verify('Minimal 80% component count', int(np.searchsorted(np.cumsum(ratios), .8) + 1) == 3)
trials = pd.read_csv(O / 'k_selection_all_attempts.csv')
verify('All seven candidate k retained', trials.k.tolist() == list(range(2, 9)))
best = trials[trials.min_size >= 3].sort_values(['silhouette', 'k'], ascending=[False, True]).iloc[0]
verify('Selection uses declared training-only rule', int(best.k) == members.cluster.nunique())
for col in weights:
    close('Weights fully allocated ' + col, weights[col].sum(), 1)
    verify('Weights nonnegative ' + col, weights[col].min() >= 0)
    if col.startswith('Cluster '):
        c = int(col.split()[-1]); take = members.cluster == c
        close('Equal weights on exact membership ' + col, weights[col], np.where(take, 1 / take.sum(), 0))
close('Equal-cluster allocation identity', weights['Equal clusters'], weights.filter(like='Cluster ').mean(axis=1))

evaluation_prices = prices.loc[cfg['fit_end']:cfg['evaluation_end']]
r = evaluation_prices.to_numpy()[1:] / evaluation_prices.to_numpy()[:-1] - 1
verify('Evaluation dates exact', list(net.index) == list(evaluation_prices.index[1:]))
rf = math.pow(1.03, 1 / 252) - 1
for name in net:
    if name == 'SPY':
        target = np.ones(1); data = r[:, -1:]
    else:
        target = weights[name].to_numpy(); data = r[:, :-1]
    day_returns, day_turnover = [], []
    current = np.zeros(len(target))
    for t, asset_day in enumerate(data):
        traded = math.fsum(abs(a - b) for a, b in zip(target, current))
        value_after_fee = 1 - traded / 1000
        gross_day = math.fsum(w * (1 + a) for w, a in zip(target, asset_day))
        ending = value_after_fee * gross_day
        if t == len(data) - 1:
            ending *= .999
        day_returns.append(ending - 1)
        day_turnover.append(traded)
        current = target * (1 + asset_day) / gross_day
    day_returns = np.array(day_returns)
    close('Daily fee/holdings reconciliation ' + name, net[name], day_returns)
    close('One-way turnover reconciliation ' + name, turnover[name], day_turnover)
    wealth, peak, worst = 1., 1., 0.
    for day in day_returns:
        wealth *= 1 + day; peak = max(peak, wealth); worst = min(worst, wealth / peak - 1)
    close('Compounded terminal return ' + name, metrics.loc[name, 'cumulative_return'], wealth - 1)
    close('Drawdown via wealth loop ' + name, metrics.loc[name, 'max_drawdown'], worst)
    close('Annual volatility ' + name, metrics.loc[name, 'vol_ann'], np.std(day_returns, ddof=1) * math.sqrt(252))
    sr = math.sqrt(252) * np.mean(day_returns - rf) / np.std(day_returns - rf, ddof=1)
    close('Excess-return Sharpe ' + name, metrics.loc[name, 'sharpe'], sr)
    regression = np.linalg.lstsq(np.column_stack([np.ones(len(r)), r[:, -1] - rf]), day_returns - rf, rcond=None)[0]
    close('Beta via least-squares intercept model ' + name, metrics.loc[name, 'beta'], regression[1])
    close('Alpha via least-squares intercept model ' + name, metrics.loc[name, 'alpha_ann'], regression[0] * 252)
    close('Total charged one-way turnover ' + name, metrics.loc[name, 'one_way_notional_turnover'], sum(day_turnover) + 1)
    # Same declared resamples; separate scalar statistics and least-squares alpha.
    rng = np.random.default_rng(42); n = len(r); bootstrap = []
    for repetition in range(2000):
        starts = rng.integers(0, n, math.ceil(n / 5))
        indexes = [(int(start) + j) % n for start in starts for j in range(5)][:n]
        a = day_returns[indexes] - rf; b = r[indexes, -1] - rf
        boot_sr = np.mean(a) / np.std(a, ddof=1) * math.sqrt(252)
        boot_alpha = np.linalg.lstsq(np.column_stack([np.ones(n), b]), a, rcond=None)[0][0] * 252
        bootstrap.append((boot_sr, boot_alpha))
    bounds = np.quantile(bootstrap, [.075, .925], axis=0)
    close('85% Sharpe bootstrap interval ' + name, metrics.loc[name, ['sharpe_low85', 'sharpe_high85']], bounds[:, 0])
    close('85% alpha bootstrap interval ' + name, metrics.loc[name, ['alpha_low85', 'alpha_high85']], bounds[:, 1])

cases = pd.read_csv(O / 'all_signal_outcomes_including_losses.csv', index_col=0)
signals = pd.read_csv(P / 'data/sephwide_buy_signals.csv')
for ticker in cases.index:
    first = pd.Timestamp(signals.loc[signals.ticker.eq(ticker), 'date'].min())
    entry = prices.index[prices.index > first][0]
    verify('Illustration price strictly after first BUY ' + ticker, str(entry.date()) == cases.loc[ticker, 'illustration_entry_close'])
    close('Signal outcome price ratio ' + ticker, cases.loc[ticker, 'adjusted_price_return'], prices.iloc[-1][ticker] / prices.loc[entry, ticker] - 1)
verify('All admitted signal outcomes retained', set(cases.index) == set(members.index))
verify('Losses remain visible', (cases.adjusted_price_return < 0).any())
winners = pd.read_csv(O / 'retrospectively_selected_positive_examples.csv', index_col=0)
verify('Positive illustrations accurately ranked', list(winners.index) == list(cases[cases.adjusted_price_return > 0].adjusted_price_return.nlargest(5).index))
nb = json.loads((P / 'W7_Portfolio_Clustering_Tzalas.ipynb').read_text())
code_cells = [c for c in nb['cells'] if c['cell_type'] == 'code']
verify('All code cells executed', all(c['execution_count'] is not None for c in code_cells))
verify('No notebook error outputs', not any(o.get('output_type') == 'error' for c in code_cells for o in c['outputs']))
verify('Inline image outputs exist', sum('image/png' in o.get('data', {}) for c in code_cells for o in c['outputs']) >= 8)
verify('HTML exported', (P / 'W7_Portfolio_Clustering_Tzalas.html').stat().st_size > 100000)
verify('Superseded analytical version preserved', (P / 'validation/attempt_01_before_identity_exclusion/summary.json').exists())
report = {'completed_utc': datetime.now(timezone.utc).isoformat(), 'checks_passed': len(rows),
          'scope': 'Separate numerical implementation by the same assistant; not independent third-party assurance or a predictive validation',
          'results': rows}
(P / 'validation/numerical_audit.json').write_text(json.dumps(report, indent=2))
print('Passed', len(rows), 'separate numerical and submission checks.')