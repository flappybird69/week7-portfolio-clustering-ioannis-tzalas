"""Create the concise PDF companion from measured outputs using ReportLab."""
from pathlib import Path
import json
from xml.sax.saxutils import escape
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

P = Path(__file__).resolve().parent
O = P / 'results'
s = json.loads((O / 'summary.json').read_text())
m = pd.read_csv(O / 'performance_metrics.csv', index_col=0)
profile = pd.read_csv(O / 'cluster_training_profiles.csv', index_col=0)
winners = pd.read_csv(O / 'retrospectively_selected_positive_examples.csv', index_col=0)
membership = pd.read_csv(O / 'asset_cluster_membership.csv', index_col=0)
audit = json.loads((P / 'validation/numerical_audit.json').read_text())
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyW7', fontName='Helvetica', fontSize=9.5, leading=13.4, spaceAfter=8, textColor=colors.HexColor('#253440')))
styles.add(ParagraphStyle(name='SmallW7', parent=styles['BodyW7'], fontSize=8, leading=10.6, spaceAfter=6))
styles.add(ParagraphStyle(name='TableW7', parent=styles['BodyW7'], fontSize=7.7, leading=10, spaceAfter=0))
styles.add(ParagraphStyle(name='HeaderW7', fontName='Helvetica-Bold', fontSize=19, leading=23, spaceAfter=12, textColor=colors.HexColor('#12636d')))
styles.add(ParagraphStyle(name='SubW7', fontName='Helvetica-Bold', fontSize=11, leading=14, spaceBefore=8, spaceAfter=7, textColor=colors.HexColor('#12636d')))
styles.add(ParagraphStyle(name='TitleW7', fontName='Helvetica-Bold', fontSize=29, leading=33, spaceAfter=18, textColor=colors.HexColor('#143542')))
story = []


def para(text, style='BodyW7'):
    story.append(Paragraph(text, styles[style]))


def title(text):
    para(text, 'HeaderW7')


def sub(text):
    para(text, 'SubW7')


def figure(name, width=500, maxheight=240):
    path = O / (name + '.png')
    w, h = ImageReader(str(path)).getSize()
    scale = min(width / w, maxheight / h)
    story.append(Image(str(path), width=w * scale, height=h * scale))
    story.append(Spacer(1, 7))


def table(data, widths):
    formatted = [[Paragraph(str(value), styles['TableW7']) for value in row] for row in data]
    t = Table(formatted, colWidths=widths, repeatRows=1, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e6f0f1')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEBELOW', (0, 0), (-1, 0), .7, colors.HexColor('#8fb3b8')),
        ('LINEBELOW', (0, 1), (-1, -1), .25, colors.HexColor('#dce2e5')),
        ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6), ('RIGHTPADDING', (0, 0), (-1, -1), 6)]))
    story.append(t); story.append(Spacer(1, 8))


def newpage():
    story.append(PageBreak())


para('FINTECH COURSE / WEEK 7', 'SubW7')
para('Portfolio clustering<br/>with SephWide signals', 'TitleW7')
para('PCA, K-Means and a transparent historical comparison', 'SubW7')
para('<b>Ioannis Tzalas</b> | MSc Banking &amp; Finance<br/>5 November 2026')
story.append(Spacer(1, 16))
table([['ASSETS', 'PRICE HISTORY', 'FORMATION / COMPARISON'],
       ['70 US-listed equities', '787 daily price dates<br/>Sep 2023 - Oct 2026', '751 formation returns<br/>35 later comparison returns'],
       ['PCA: 3 components', '82.71% feature variance retained', '2 clusters selected<br/>Silhouette 0.3881']], [150, 165, 185])
sub('Question and contribution')
para('Can price-derived features organize stocks selected by my algorithmic signal system into interpretable groups, and how did equal-weight portfolios of those groups behave later? The study connects the course methods to recorded SephWide BUY signals while keeping the trading project read-only.')
sub('Measured outcome')
para('<b>The portfolio comparison does not demonstrate a return advantage.</b> At assumed 10 bps one-way costs, Cluster 1 returned <b>-1.84%</b> and Cluster 2 <b>-2.96%</b> over 35 sessions; SPY returned <b>+1.53%</b>. Individual successful signal examples coexist with a weak aggregate comparison. Losses are retained.')
sub('Scope and evidence')
para('The brief permits "assets/tokens" despite its DeFi title. This is an explicitly disclosed <b>equity application</b>, not DeFi-token analysis. If the lecturer requires tokens exclusively, that scope needs agreement. The primary submission is the executed Jupyter notebook; this PDF is a concise companion.')
para('These are retrospectively constructed portfolios using strategy signal records and public adjusted prices. They are <b>not authenticated funded-account fills or funded P&amp;L</b>. The conditional historical split, short evaluation window and data correction prevent a claim of fresh prospective validation.', 'SmallW7')
newpage()

title('1 / Data and principal components')
para('Freeze all 72 distinct SephWide BUY tickers recorded through 1 September 2026, without filtering on gains. Download daily adjusted closes through yfinance; include SPY as market comparator. Fit on 1 September 2023 - 1 September 2026; compare on 2 September - 21 October 2026. Frozen CSVs and SHA-256 receipts support offline reproduction.')
table([['Quality rule', 'Measured treatment'],
       ['Fit coverage >=99%; exact endpoints; no nonpositive prices', 'NESR excluded: 212 missing fit prices / insufficient history.'],
       ['Issuer identity before economic interpretation', 'GOLD excluded: Barrick changed to B; Gold.com reused GOLD. Intended issuer is unresolved.'],
       ['SPY session calendar; past-only fill, maximum 2 sessions', '70 final assets have complete downloaded prices. No backfill or return-based exclusion.'],
       ['Large daily moves flagged, retained', 'WULF +59.52% (14 Aug 2025); MRNA +176.97% (19 Aug 2026). Vendor precision is not execution proof.']], [215, 285])
para('<b>Correction chronology:</b> the first 71-asset calculation preceded the GOLD identity finding. Its notebook and tables are preserved. The exclusion was a data-quality repair after initial result inspection; no claim of an untouched holdout is made.', 'SmallW7')
sub('Asset-by-feature matrix')
para('One row per stock; eight formation-period return features: annualized mean, volatility, downside deviation, skewness, maximum drawdown, SPY beta, SPY correlation and lag-one autocorrelation. Standardize each feature across assets. Price levels are avoided because share denominations are incomparable.')
figure('02_pca', maxheight=205)
para('<b>Variance rule:</b> retain the minimum PCs reaching 80%; three retain 82.71%. PC1 mainly combines volatility, downside risk and beta, opposed to signed drawdown. PC2/PC3 mix persistence, correlation and skewness. Coefficients describe standardized feature variation; they are neither return forecasts nor causal factors. PCA is linear, unwhitened and sign-indeterminate.', 'SmallW7')
newpage()

title('2 / Clusters and validation')
para('Fit K-Means on all three retained scores using k=2,...,8, 50 restarts and seed 42. Select the maximum training silhouette subject to at least three stocks in every cluster; smaller k breaks ties. The elbow is a separate diagnostic, never selected by later returns.')
figure('03_k_selection', maxheight=180)
para('<b>Result:</b> k=2 is selected (silhouette 0.3881). The chord elbow suggests k=3, but this and all higher-k partitions create a single-stock group and fail the declared size rule. The constraint is material; there is no claim of a unique natural number of economic groups.', 'SmallW7')
figure('04_clusters', maxheight=210)
table([['Group', 'Stocks', 'Median fit vol / beta', 'Economic interpretation'],
       ['Cluster 1', '47', '30.28% / 0.76', 'Relatively lower-risk, broad equities; utilities, consumer defensive and real estate are prominent.'],
       ['Cluster 2', '23', '57.99% / 1.68', 'Higher-risk equities; technology, materials and cyclical exposures, including event-sensitive names.']], [67, 42, 114, 277])
para('Twenty additional seed fits all have ARI=1 versus the selected partition. This supports optimizer consistency for this dataset, not stability across market regimes. Two analytical data versions are retained: 56 version-specific fits / 2,800 initialization starts in total. Routine reruns are logged separately.', 'SmallW7')
newpage()

title('3 / Portfolio design and measured performance')
para('Cluster 1 allocates 1/47 = <b>2.1277%</b> per constituent; Cluster 2 allocates 1/23 = <b>4.3478%</b>. Rebalance daily to fixed targets. The all-asset comparator allocates 1/70 = <b>1.4286%</b> per stock. The equal-cluster example allocates 50% to each group, or 1.0638% / 2.1739% per stock respectively. Exact memberships and all weights are in the notebook and CSVs.')
para('Charge 10 bps per one-way traded notional at entry, on drift-rebalancing and at final liquidation. Multiplicative wealth fees approximate financing of transaction costs. Fixed 0/25 bps sensitivity scenarios are retained; no outcome-based policy change is made. These portfolios do not replay SephWide sizing, exits or fills.', 'SmallW7')
data = [['Portfolio', 'Cum.<br/>return', 'Annual<br/>vol.', 'Max<br/>drawdown', 'Sharpe [85% interval]']]
for name, row in m.iterrows():
    data.append([name, f'{row.cumulative_return:.2%}', f'{row.vol_ann:.2%}', f'{row.max_drawdown:.2%}', f'{row.sharpe:.2f} [{row.sharpe_low85:.2f}, {row.sharpe_high85:.2f}]'])
table(data, [98, 63, 65, 71, 203])
figure('06_equity_and_distributions', maxheight=200)
sub('Metric definitions and uncertainty')
para('Cumulative return = product(1+r)-1. Volatility = sample daily standard deviation x sqrt(252). Sharpe uses daily excess returns against an assumed constant 3% annual cash rate. Maximum drawdown includes initial wealth 1, so a first-day loss counts. Alpha/beta use an intercept regression on gross adjusted SPY excess returns; all estimates and alpha intervals are supplied in the notebook.')
para('Each Sharpe interval is an 85% percentile circular-block bootstrap, block length five, 2,000 resamples. Alpha resamples paired portfolio/market dates. The intervals condition on fixed assets/clusters, omit selection uncertainty and are not multiplicity-adjusted or anytime-valid. All cluster intervals include zero. Annualization of 35 observations is a noisy scale conversion, not a year of demonstrated results.', 'SmallW7')
newpage()

title('4 / Successful signals in the complete record')
para('To show prior signals that rose, take each included stock\'s first recorded BUY and a hypothetical adjusted close <b>strictly after</b> that date; compare it with 21 October 2026. This is a separate retrospective illustration. It neither filters the main universe nor substitutes for the costed portfolio comparison.')
data = [['Ticker', 'Recorded BUY', 'Illustration entry', 'Price change', 'Matched SPY']]
for ticker, row in winners.iterrows():
    data.append([ticker, row.signal_date, row.illustration_entry_close, f'{row.adjusted_price_return:.2%}', f'{row.matched_spy_return:.2%}'])
table(data, [55, 110, 115, 110, 110])
para('<b>Selection disclosed:</b> these are the five largest positive outcomes, chosen after observation. Across all 70 names, <b>24 rose and 46 fell</b>. Holding lengths differ and overlap. These counts are not a calibrated win probability, and the illustration omits strategy exits, costs, sizing and funded-fill verification.', 'SmallW7')
figure('08_all_signal_outcomes', maxheight=205)
sub('Dated event context, with an evidence limit')
para('MRNA is the largest positive example in this provider series. On 19 August 2026, Merck and Moderna announced positive Phase 3 melanoma-trial endpoints. This issuer evidence supplies relevant context for the unusually large price move; it does not show that SephWide anticipated the announcement or isolate its causal effect. The event occurred before the September portfolio comparison.')
para('<link href="https://www.merck.com/news/merck-and-moderna-announce-phase-3-interpath-001-trial-of-intismeran-autogene-plus-keytruda-met-endpoints-of-recurrence-free-survival-rfs-and-distant-metastasis-free-survival-dmfs-in-patient/" color="#12636d">Source: Merck/Moderna issuer announcement, 19 August 2026.</link>', 'SmallW7')
newpage()

title('5 / Interpretation, insights and limits')
figure('07_risk_return', maxheight=240)
para('<b>Best/worst in this window:</b> Cluster 1 lost less than Cluster 2 in cumulative-return terms, but both lagged SPY. Cluster 2 carried substantially higher risk. A different Sharpe ordering can occur because Sharpe scales mean excess return by volatility; "least negative return" is not the same as "largest Sharpe". The wide intervals do not support a confident risk-adjusted ranking.')
para('<b>Economic meaning:</b> these groups summarize common risk and sector sensitivities. PCA/K-Means do not establish why an asset rose or fell. Later cross-cluster return correlation is only 0.087 in this window, but even some diversification did not deliver positive combined returns.')
sub('Actionable research use')
para('Use cluster membership to inspect repeated exposures before adding a name. Compare the predeclared all-asset and equal-cluster budgets: equal-cluster allocation raises the weights of stocks in the smaller, riskier cluster. A risk-constrained mandate should investigate training-based risk budgets and concentration limits using a new future evaluation. Do not buy the retrospectively best cluster or extrapolate the five winners from this evidence.')
sub('Material limitations')
para('<b>Selected survivors and historical knowledge:</b> later strategy membership and history requirements restrict representativeness. <b>Data:</b> adjusted-price revisions, symbol reuse and corporate actions; current sector labels; no original price vintage or certified fill record. <b>Inference:</b> 35 dependent sessions, one regime, selection uncertainty and unadjusted intervals. <b>Model:</b> linear PCA, correlated features, compact Euclidean groups and outlier sensitivity. <b>Execution:</b> fractional holdings, daily rebalancing, fixed costs/cash rate, no taxes, impact, liquidity or capacity model.', 'SmallW7')
para('Next: freeze a genuinely future cohort, verify issuer/price identities, retain delisted/rejected names, measure realistic costs and rolling cluster stability, and collect a much longer forward record. No live strategy change is proposed.', 'SmallW7')
newpage()

title('6 / Reproduction, checks and rubric coverage')
para('The executed notebook is self-contained and uses frozen CSVs offline. Install the pinned requirements, run the notebook in its folder, then run the separate audit script. The verified environment is Python 3.14. No project module is imported, no scheduler or trading agent is run, and no credentials are included.')
table([['Rubric item', 'Points', 'Evidence'],
       ['Data / preprocessing', '15', '787 dates, 72 candidates, complete exclusion/provenance audit'],
       ['PCA', '15', 'Scaling, minimal 80% rule, scree curve, loadings, interpretation'],
       ['Clustering', '20', 'All k/seeds, elbow/silhouette, 2D chart, sector/member tables'],
       ['Portfolio design', '10', 'Constituent weights, rebalancing, costs and comparators'],
       ['Performance', '15', 'Cumulative return, Sharpe + interval, volatility, drawdown, alpha/beta'],
       ['Visualizations', '5', 'Equity, distributions, risk-return and sector composition'],
       ['Written analysis', '20', 'Economic meaning, best/worst, allocation insights and caveats']], [127, 42, 331])
sub('Verification scope')
para(f'<b>{s["structural_checks"]} structural checks</b> pass inside the notebook; <b>{audit["checks_passed"]} separate numerical/submission checks</b> reconcile input hashes, chronology, PCA via SVD, beta/alpha via least squares, exact weights, fee/wealth calculations, drawdowns, bootstrap bounds, positive examples and notebook execution. These are same-assistant checks, not independent third-party assurance or evidence of profitability.')
para('The first analytical version and all execution attempts remain in validation/. A project hash comparison records the read-only boundary. The AI disclosure includes the user\'s original prompts and assistance description. Review and understand the work before individual submission.', 'SmallW7')
sub('References and source records')
para('Course brief, supplied PDF, pp. 1-4; Yahoo Finance adjusted closes via yfinance (download time/version and hashes in data/provenance.json); private authorized SephWide BUY-date/ticker snapshot; Yahoo sector metadata snapshot. The notebook contains direct source links and all formulas.', 'SmallW7')
para('<link href="https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html" color="#12636d">Scikit-learn PCA</link>; <link href="https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html" color="#12636d">KMeans</link>; <link href="https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html" color="#12636d">silhouette analysis</link>; <link href="https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html" color="#12636d">yfinance download</link>. Accessed 5 November 2026.', 'SmallW7')
para('Sharpe (1994), The Sharpe Ratio, Journal of Portfolio Management 21(1), 49-58. Kunsch (1989), The Jackknife and the Bootstrap for General Stationary Observations, Annals of Statistics 17(3), 1217-1241. NumPy, pandas, Matplotlib and Jupyter documentation; OpenAI Codex assistance disclosure included.', 'SmallW7')
para('<link href="https://www.barrick.com/English/news/news-details/2025/barrick-Is-now-B-on-the-NYSE/default.aspx" color="#12636d">Barrick ticker change</link>; <link href="https://ir.gold.com/news-events/press-releases/detail/212/gold-com-to-begin-trading-on-the-new-york-stock-exchange-under-ticker-symbol-gold" color="#12636d">Gold.com ticker reuse</link>; Merck/Moderna issuer announcement linked on page 5.', 'SmallW7')
para('<b>Brief ambiguities:</b> cover says before Week 8 or 9, body/final line say before Week 8; use the earlier working deadline and confirm the date. The +30 bonus has no tasks defined. No separate presentation is required by this brief.', 'SmallW7')


def footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setStrokeColor(colors.HexColor('#d4e1e5'))
    canvas.line(44, 38, w - 44, 38)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.HexColor('#506672'))
    canvas.drawString(44, 25, 'IOANNIS TZALAS / WEEK 7 / HISTORICAL COURSEWORK')
    canvas.drawRightString(w - 44, 25, str(doc.page))
    canvas.restoreState()


doc = SimpleDocTemplate(str(P / 'W7_Analysis_Report.pdf'), pagesize=A4,
                        rightMargin=44, leftMargin=44, topMargin=39, bottomMargin=50,
                        title='Week 7 - Portfolio Clustering with SephWide Signals',
                        author='Ioannis Tzalas', subject='PCA, K-Means and historical portfolio comparison')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print('Created PDF companion.')