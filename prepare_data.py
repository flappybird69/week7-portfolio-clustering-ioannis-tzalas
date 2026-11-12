"""Read-only SephWide export and public price collection, independent of its runtime."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parent
REPO = Path('/Users/john/SephianceAgents')
DECLARATION = {
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'purpose': 'Individual Week 7 coursework; no live strategy proposal',
    'universe': 'All distinct SephWide BUY tickers dated on or before 2026-09-01; no P&L filter',
    'prices_start': '2023-09-01', 'fit_end': '2026-09-01',
    'evaluation_start': '2026-09-02', 'evaluation_end': '2026-10-21',
    'features': ['mean_ann', 'vol_ann', 'downside_ann', 'skew', 'max_drawdown', 'beta_spy', 'corr_spy', 'autocorr1'],
    'pca_variance_threshold': 0.80,
    'k_grid': list(range(2, 9)),
    'selection': 'Maximum training silhouette among k with minimum cluster size 3; smaller k breaks ties; elbow diagnostic only',
    'kmeans_n_init': 50, 'seed': 42,
    'stability': '20 additional fixed seeds at chosen k, training only; no reselection',
    'weights': 'Equal weights within each cluster, rebalanced daily; equal budget across clusters as a separate illustration',
    'cost_one_way_bps': 10, 'cost_sensitivity_bps': [0, 25],
    'risk_free_annual': 0.03, 'annualization': 252,
    'interval': '85% percentile circular block bootstrap; block 5; 2000 samples; descriptive, not promotion evidence',
    'price_quality': 'SPY session calendar; exact endpoints; >=99% coverage; <=2 consecutive missing; past-only ffill limit 2; no bfill; no nonpositive prices',
    'winner_examples': 'Top 5 first-BUY-to-evaluation-end adjusted-price gains among positive cases; full first-BUY table retained; explicitly retrospective',
    'limitations': 'Historical selection from local strategy ledger, not funded fills; conditional retrospective split; no fresh prospective holdout or point-in-time vendor vintage',
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    declaration = ROOT / 'declaration.json'
    if declaration.exists():
        pass
    declaration.write_text(json.dumps(DECLARATION, indent=2))
    src = REPO / 'paper_trading/sephwide/trade_log.csv'
    raw = pd.read_csv(src)
    selected = raw[(raw.side == 'BUY') & (raw.date <= '2026-09-01')].copy()
    tickers = sorted(selected.ticker.unique())
    assert len(tickers) >= 50
    # Deliberately omit shares, notional, P&L and narrative fields from the submission.
    selected[['date', 'side', 'ticker', 'ts']].to_csv(ROOT / 'data/sephwide_buy_signals.csv', index=False)
    sector_map = json.loads((REPO / 'cache/sector_map.json').read_text())
    pd.DataFrame({'ticker': tickers, 'sector': [sector_map.get(t) or 'Unknown' for t in tickers]}).to_csv(ROOT / 'data/universe.csv', index=False)
    provenance = {'snapshot_utc': datetime.now(timezone.utc).isoformat(),
                  'repo_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO).decode().strip(),
                  'original_trade_log_sha256': digest(src), 'universe_count': len(tickers),
                  'data_origin': 'Yahoo Finance via yfinance download; auto_adjust=True; daily adjusted Close',
                  'yfinance_version': yf.__version__, 'requested_start': '2023-09-01',
                  'requested_end_exclusive': '2026-10-22', 'download_attempts': []}
    prices = []
    for i in range(0, len(tickers) + 1, 15):
        group = (tickers + ['SPY'])[i:i+15]
        print('Downloading', ', '.join(group), flush=True)
        frame = yf.download(group, start='2023-09-01', end='2026-10-22', auto_adjust=True,
                            progress=False, threads=False, timeout=20)
        close = frame['Close'].copy()
        if isinstance(close, pd.Series):
            close = close.to_frame(group[0])
        prices.append(close)
        provenance['download_attempts'].append({'tickers': group, 'rows': len(close)})
    prices = pd.concat(prices, axis=1).sort_index()
    prices.index = pd.to_datetime(prices.index).tz_localize(None)
    prices.index.name = 'Date'
    prices.to_csv(ROOT / 'data/adjusted_close_raw.csv', float_format='%.10f')
    provenance['completed_utc'] = datetime.now(timezone.utc).isoformat()
    provenance['files'] = {str(p.relative_to(ROOT)): digest(p) for p in (ROOT / 'data').glob('*')}
    (ROOT / 'data/provenance.json').write_text(json.dumps(provenance, indent=2))
    if not (ROOT / 'reference/assignment_brief.pdf').exists() and Path('/tmp/FinTechCourse_W7_assignment_v1.pdf').exists(): shutil.copyfile('/tmp/FinTechCourse_W7_assignment_v1.pdf', ROOT / 'reference/assignment_brief.pdf')
    print('Saved', prices.shape, 'missing per ticker', prices.isna().sum().to_dict(), flush=True)


if __name__ == '__main__':
    main()