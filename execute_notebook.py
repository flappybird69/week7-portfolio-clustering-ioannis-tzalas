"""Execute the submitted notebook in a clean kernel using this Python environment."""
from pathlib import Path
from datetime import datetime, timezone
import os
import json
import sys
import tempfile
import traceback
import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter

ROOT = Path(__file__).resolve().parent
kernel_root = Path(tempfile.mkdtemp(prefix='w7-jupyter-'))
kernel_dir = kernel_root / 'kernels/w7-local'
kernel_dir.mkdir(parents=True)
(kernel_dir / 'kernel.json').write_text(json.dumps({
    'argv': [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
    'display_name': 'Week 7 local execution', 'language': 'python'}))
os.environ['JUPYTER_PATH'] = str(kernel_root)
notebook = ROOT / 'W7_Portfolio_Clustering_Tzalas.ipynb'
nb = nbformat.read(notebook, as_version=4)
attempt = {'started_utc': datetime.now(timezone.utc).isoformat()}
try:
    NotebookClient(nb, timeout=600, kernel_name='w7-local',
                   resources={'metadata': {'path': str(ROOT)}}).execute()
    attempt['status'] = 'completed'
except Exception:
    attempt['status'] = 'failed'
    attempt['error'] = traceback.format_exc()
    raise
finally:
    attempt['ended_utc'] = datetime.now(timezone.utc).isoformat()
    with (ROOT / 'validation/execution_attempts.jsonl').open('a') as stream:
        stream.write(json.dumps(attempt) + '\n')
    nbformat.write(nb, notebook)
body, resources = HTMLExporter(template_name='lab').from_notebook_node(nb)
(ROOT / 'W7_Portfolio_Clustering_Tzalas.html').write_text(body)
print('Fresh-kernel execution and standalone HTML export completed.')
"""Optional public-data refresh. Never overwrites the frozen submission inputs."""
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
import yfinance as yf

root = Path(__file__).resolve().parent
tickers = pd.read_csv(root / 'data/universe.csv').ticker.tolist() + ['SPY']
target = root / 'data' / ('refresh_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '.csv')
if target.exists():
    raise FileExistsError(target)
frame = yf.download(tickers, start='2023-09-01', end='2026-10-22',
                    auto_adjust=True, threads=False, progress=False, timeout=20)
if frame is None or frame.empty:
    raise RuntimeError('No public prices returned; frozen inputs are unchanged.')
frame['Close'].to_csv(target)
print('New data vintage saved separately:', target)
# AI assistance and prompt record

Date: 5 November 2026. Student: Ioannis Tzalas.

OpenAI Codex assisted with reading the brief, choosing and implementing a transparent
coursework design, drafting Python/Markdown, downloading public data, executing the
notebook, checking calculations, and preparing the submission package. No claim of
independent student-only code authorship or independent third-party assurance is made.
Review this disclosure against the lecturer's policy and understand the code before
submitting or presenting it.

## User prompts (verbatim, including subsequent correction)

> ok so listen to me carefully, do not change anything on my code here, on my project, i have an assigment that i need to do , something like my other assigments for my professor from week1,2,3,4,5,6 and now this is week 7, complete this assigment like you did all my previous ones, but now i want to use this project for previous signals that did go up, like use signals from my algotraders, maybe put sephwide

> and output the folder on the weekstop

> desktop

The user supplied `FinTechCourse_W7_assignment_v1.pdf`. Its contents were used as the
rubric, rather than as an instruction to modify the trading project.

## Assistant's declared design and safeguards

- Save the work on the Desktop, outside the project; project access is read-only.
- Use all recorded SephWide BUY tickers through 1 September 2026 without a winner filter.
- Fit price-derived features, scaling, PCA and K-Means before evaluating later returns.
- Keep the requested positive examples explicitly retrospective and retain losses.
- Record all k candidates, seeds, exclusions, execution failures and cost scenarios.
- Supply frozen data, provenance, formulas, uncertainty limits and readable exports.

`declaration.json` is the timestamped design before the price download/calculation.
`validation/execution_attempts.jsonl` records notebook execution attempts and errors.
`results/k_selection_all_attempts.csv` and `results/seed_stability_all_attempts.csv`
retain every model fit. The independent audit is a separate calculation by the same
assistant, not an audit by another person or an independent AI agent.

This file is a transparent record of the available user prompts and workflow; it is
not a purported verbatim export of hidden model reasoning or every internal tool call.