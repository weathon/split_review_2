from __future__ import annotations

import argparse
import asyncio
import csv
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

from deepreview.runner import run_text_job_async
from deepreview.state import ensure_artifact_paths, fail_job, load_job_state, save_job_state
from deepreview.storage import append_event, write_text_atomic
from deepreview.types import JobState, JobStatus


CSV_FIELDS = [
    'paper_id',
    'title',
    'status',
    'pred_score',
    'gt_avg_score',
    'abs_error',
    'cost_usd',
    'openrouter_calls',
    'input_tokens',
    'output_tokens',
    'total_tokens',
    'job_id',
    'review_path',
    'error',
]
SCORE_PATTERN = re.compile(r'Final\s+Score\s*:\s*(\d+(?:\.\d+)?)\s*/\s*10', re.IGNORECASE)


def load_manifest(dataset: Path) -> list[dict[str, Any]]:
    ratings_path = dataset / 'ratings.csv'
    ratings = {}
    if ratings_path.exists():
        with ratings_path.open('r', encoding='utf-8', newline='') as f:
            for row in csv.DictReader(f):
                paper_id = row['paper_id'].strip()
                ratings[paper_id] = {
                    'title': row['title'].strip(),
                    'avg_score': float(row['avg_score']) if row['avg_score'].strip() else None,
                }
    papers_dir = dataset / 'papers'
    if not papers_dir.exists():
        raise FileNotFoundError(f'papers dir missing: {papers_dir}')
    rows = []
    for paper_path in sorted(papers_dir.glob('*.txt')):
        paper_id = paper_path.stem
        rating = ratings[paper_id] if paper_id in ratings else {'title': paper_id, 'avg_score': None}
        rows.append(
            {
                'paper_id': paper_id,
                'title': rating['title'],
                'avg_score': rating['avg_score'],
                'paper_path': paper_path,
            }
        )
    if not rows:
        raise RuntimeError(f'no paper txt files found: {papers_dir}')
    return rows


def load_finished(csv_path: Path, reviews_dir: Path) -> set[str]:
    finished = set()
    if not csv_path.exists():
        return finished
    with csv_path.open('r', encoding='utf-8', newline='') as f:
        for row in csv.DictReader(f):
            if row['status'] != 'completed':
                continue
            review_path = Path(row['review_path'])
            if not review_path.is_absolute():
                review_path = reviews_dir / review_path
            if not review_path.exists():
                raise FileNotFoundError(f'completed CSV row has missing review file: {review_path}')
            finished.add(row['paper_id'])
    return finished


def create_text_job(paper: dict[str, Any]) -> str:
    paper_id = paper['paper_id']
    paper_path = paper['paper_path']
    paper_text = paper_path.read_text(encoding='utf-8')
    if not paper_text.strip():
        raise RuntimeError(f'paper text is empty: {paper_path}')

    job = JobState(
        title=paper['title'] or paper_id,
        source_pdf_name=f'{paper_id}.txt',
        metadata={
            'benchmark': 'iclr2026_new',
            'paper_id': paper_id,
            'paper_path': str(paper_path),
            'input_mode': 'text',
        },
    )
    artifacts = ensure_artifact_paths(job.id)
    write_text_atomic(Path(artifacts['mineru_markdown']), paper_text)
    job.artifacts.mineru_markdown_path = str(artifacts['mineru_markdown'])
    job.artifacts.annotations_path = str(artifacts['annotations'])
    save_job_state(job)
    append_event(job.id, 'created_text_benchmark', paper_id=paper_id, paper_path=str(paper_path))
    return str(job.id)


def parse_score(review_text: str) -> float:
    match = SCORE_PATTERN.search(review_text)
    if not match:
        raise RuntimeError('Final Score: X/10 not found in final review.')
    return float(match.group(1))


async def write_event(log_path: Path, lock: asyncio.Lock, payload: dict[str, Any]) -> None:
    row = {'ts': time.strftime('%Y-%m-%dT%H:%M:%S'), **payload}
    text = json.dumps(row, ensure_ascii=False)
    async with lock:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open('a', encoding='utf-8') as f:
            f.write(text + '\n')
        print(text, flush=True)


async def write_csv(csv_path: Path, lock: asyncio.Lock, row: dict[str, Any]) -> None:
    async with lock:
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with csv_path.open('a', encoding='utf-8', newline='') as f:
            csv.DictWriter(f, fieldnames=CSV_FIELDS).writerow(row)


async def run_one(
    paper: dict[str, Any],
    reviews_dir: Path,
    csv_path: Path,
    csv_lock: asyncio.Lock,
    log_path: Path,
    log_lock: asyncio.Lock,
) -> dict[str, Any]:
    paper_id = paper['paper_id']
    await write_event(log_path, log_lock, {'event': 'sample_start', 'paper_id': paper_id})
    job_id = ''
    review_path = reviews_dir / f'{paper_id}.md'
    try:
        job_id = create_text_job(paper)
        await run_text_job_async(job_id)
        state = load_job_state(job_id)
        if state is None:
            raise RuntimeError(f'job state missing after run: {job_id}')
        final_path = Path(state.artifacts.final_markdown_path or '')
        if not final_path.exists():
            raise RuntimeError(f'final markdown missing: {final_path}')
        review_text = final_path.read_text(encoding='utf-8')
        score = parse_score(review_text)
        review_path.parent.mkdir(parents=True, exist_ok=True)
        review_path.write_text(review_text, encoding='utf-8')
        gt_avg_score = paper['avg_score']
        abs_error = abs(score - float(gt_avg_score)) if gt_avg_score is not None else None
        row = {
            'paper_id': paper_id,
            'title': paper['title'],
            'status': 'completed',
            'pred_score': f'{score:.4f}',
            'gt_avg_score': f'{float(gt_avg_score):.4f}' if gt_avg_score is not None else '',
            'abs_error': f'{abs_error:.4f}' if abs_error is not None else '',
            'cost_usd': f'{state.usage.openrouter.cost_usd:.8f}',
            'openrouter_calls': state.usage.openrouter.calls,
            'input_tokens': state.usage.token.input_tokens,
            'output_tokens': state.usage.token.output_tokens,
            'total_tokens': state.usage.token.total_tokens,
            'job_id': job_id,
            'review_path': str(review_path),
            'error': '',
        }
        await write_csv(csv_path, csv_lock, row)
        await write_event(
            log_path,
            log_lock,
            {
                'event': 'sample_done',
                'paper_id': paper_id,
                'job_id': job_id,
                'score': score,
                'cost_usd': state.usage.openrouter.cost_usd,
                'openrouter_calls': state.usage.openrouter.calls,
                'review_path': str(review_path),
            },
        )
        return {'status': 'completed', 'cost_usd': state.usage.openrouter.cost_usd}
    except Exception as exc:
        error = f'{type(exc).__name__}: {exc}'
        state = load_job_state(job_id) if job_id else None
        if job_id and state is not None and state.status != JobStatus.completed:
            fail_job(job_id, message='Text benchmark review pipeline failed.', error=error)
            state = load_job_state(job_id)
        cost_usd = state.usage.openrouter.cost_usd if state is not None else 0.0
        openrouter_calls = state.usage.openrouter.calls if state is not None else 0
        input_tokens = state.usage.token.input_tokens if state is not None else 0
        output_tokens = state.usage.token.output_tokens if state is not None else 0
        total_tokens = state.usage.token.total_tokens if state is not None else 0
        row = {
            'paper_id': paper_id,
            'title': paper['title'],
            'status': 'failed',
            'pred_score': '',
            'gt_avg_score': f"{float(paper['avg_score']):.4f}" if paper['avg_score'] is not None else '',
            'abs_error': '',
            'cost_usd': f'{cost_usd:.8f}',
            'openrouter_calls': openrouter_calls,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'total_tokens': total_tokens,
            'job_id': job_id,
            'review_path': str(review_path) if review_path.exists() else '',
            'error': error,
        }
        await write_csv(csv_path, csv_lock, row)
        await write_event(
            log_path,
            log_lock,
            {
                'event': 'sample_failed',
                'paper_id': paper_id,
                'job_id': job_id,
                'error': error,
                'cost_usd': cost_usd,
                'openrouter_calls': openrouter_calls,
            },
        )
        return {'status': 'failed', 'cost_usd': cost_usd}


async def run_benchmark(args: argparse.Namespace) -> None:
    if args.workers < 1:
        raise ValueError('--workers must be >= 1')

    dataset = Path(args.dataset).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    reviews_dir = output_dir / 'reviews'
    csv_path = output_dir / 'scores.csv'
    log_path = output_dir / 'benchmark.log.jsonl'
    papers = load_manifest(dataset)

    if args.resume:
        finished = load_finished(csv_path, reviews_dir)
        if not csv_path.exists() or csv_path.stat().st_size == 0:
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            with csv_path.open('w', encoding='utf-8', newline='') as f:
                csv.DictWriter(f, fieldnames=CSV_FIELDS).writeheader()
    else:
        finished = set()
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with csv_path.open('w', encoding='utf-8', newline='') as f:
            csv.DictWriter(f, fieldnames=CSV_FIELDS).writeheader()
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text('', encoding='utf-8')

    todo = [paper for paper in papers if paper['paper_id'] not in finished]
    csv_lock = asyncio.Lock()
    log_lock = asyncio.Lock()
    await write_event(
        log_path,
        log_lock,
        {
            'event': 'batch_start',
            'dataset': str(dataset),
            'output_dir': str(output_dir),
            'total': len(papers),
            'skipped': len(finished),
            'to_run': len(todo),
            'workers': args.workers,
        },
    )

    sem = asyncio.Semaphore(args.workers)

    async def run_guarded(paper: dict[str, Any]) -> dict[str, Any]:
        async with sem:
            return await run_one(paper, reviews_dir, csv_path, csv_lock, log_path, log_lock)

    results = await asyncio.gather(*(run_guarded(paper) for paper in todo))
    completed = sum(1 for row in results if row['status'] == 'completed')
    failed = sum(1 for row in results if row['status'] == 'failed')
    cost_usd = sum(float(row['cost_usd']) for row in results)
    await write_event(
        log_path,
        log_lock,
        {
            'event': 'batch_done',
            'total': len(papers),
            'skipped': len(finished),
            'completed': completed,
            'failed': failed,
            'cost_usd': cost_usd,
        },
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Run DeepReviewer-v2 OpenRouter benchmark on ICLR 2026 text papers.')
    parser.add_argument('--workers', type=int, default=1)
    parser.add_argument('--dataset', default='/home/wg25r/review_agent/iclr2026_new')
    parser.add_argument('--output-dir', default=str(ROOT / 'data' / 'benchmarks' / 'iclr2026_new'))
    parser.add_argument('--resume', action='store_true')
    return parser


if __name__ == '__main__':
    asyncio.run(run_benchmark(build_parser().parse_args()))
