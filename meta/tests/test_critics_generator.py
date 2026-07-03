"""Tests for meta/ReviewCritique/scripts/generate_subagent_workflow.py.
Deterministic units + pipeline-level generation into a temp dir (never touches the
real subagent_workflows/ outputs), then node syntax-check of the generated JS.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ReviewCritique" / "scripts"))
import generate_subagent_workflow as gen

FAILED = []

def check(name, fn):
    try:
        fn()
        print(f"PASS {name}")
    except AssertionError as e:
        print(f"FAIL {name}: {e}")
        FAILED.append(name)

IDS = json.load(open(gen.SUBSET_IDS_PATH))
DR_DIR = gen.OUT_DIR / "dr14b_reviews"  # read-only use of already-materialized reviews


# --- build_task_list ---
def t_tasks_single_md():
    tasks = gen.build_task_list("ours_cmp3_ours_v2", IDS, DR_DIR)
    assert len(tasks) > 0
    t = tasks[0]
    assert set(t) == {"paper_id", "review_path", "paper_path"}
    assert t["review_path"].endswith(f"{t['paper_id']}.md")
    assert "ours_cmp3_ours_v2/reviews" in t["review_path"]
    assert t["paper_path"].endswith(f"{t['paper_id']}.txt")
check("build_task_list single_md paths", t_tasks_single_md)

def t_tasks_cspaper():
    tasks = gen.build_task_list("cspaper", IDS, DR_DIR)
    assert len(tasks) > 0
    assert all(t["review_path"].endswith(f"{t['paper_id']}__ICLR_main_2026_2.md") for t in tasks)
check("build_task_list cspaper filename pattern", t_tasks_cspaper)

def t_tasks_skip_missing():
    tasks = gen.build_task_list("ours_cmp3_ours_v2", ["NOT_A_REAL_PAPER_ID"] + IDS[:2], DR_DIR)
    assert all(t["paper_id"] != "NOT_A_REAL_PAPER_ID" for t in tasks)
check("build_task_list skips missing review/paper", t_tasks_skip_missing)

def t_tasks_dr14b():
    tasks = gen.build_task_list("DeepReviewer_14B", IDS, DR_DIR)
    assert all("dr14b_reviews" in t["review_path"] for t in tasks)
check("build_task_list DeepReviewer_14B uses materialized dir", t_tasks_dr14b)


# --- extract_deepreviewer_reviews determinism ---
def t_dr_deterministic():
    src = gen.METHODS["DeepReviewer_14B"]["dir"]
    pid = next((p for p in IDS if (src / f"{p}.txt.json").exists()), None)
    assert pid, "no DeepReviewer_14B json found for any subset id"
    tmp1, tmp2 = Path(tempfile.mkdtemp()), Path(tempfile.mkdtemp())
    try:
        gen.extract_deepreviewer_reviews([pid], tmp1)
        gen.extract_deepreviewer_reviews([pid], tmp2)
        a = (tmp1 / f"{pid}.md").read_text()
        assert a == (tmp2 / f"{pid}.md").read_text()
        reviews = json.load(open(src / f"{pid}.txt.json"))["results"][0]["reviews"]
        assert a in [r["text"] for r in reviews]
    finally:
        shutil.rmtree(tmp1), shutil.rmtree(tmp2)
check("extract_deepreviewer_reviews deterministic seeded pick", t_dr_deterministic)


# --- template embedding (small synthetic input) ---
def t_template_embed():
    tasks = [{"paper_id": "pX", "review_path": "/r/pX.md", "paper_path": "/p/pX.txt"}]
    script = gen.TEMPLATE.format(method_json=json.dumps("m1"),
                                 guideline_json=json.dumps("GUIDE `line` with \"quotes\"\nand newline"),
                                 tasks_json=json.dumps(tasks), concurrency=gen.CONCURRENCY)
    assert 'const METHOD = "m1"' in script
    assert '"paper_id": "pX"' in script
    assert f"const CONCURRENCY = {gen.CONCURRENCY}" in script
    assert json.dumps("GUIDE `line` with \"quotes\"\nand newline") in script
    assert "Nice-to-Have" in script and "Misunderstanding" in script
    assert "${TASKS.length}" in script  # {{ }} escaping survived .format
check("TEMPLATE embeds method/guideline/tasks as JS literals", t_template_embed)


# --- node syntax check helper: workflow body has top-level await/return, so wrap ---
def node_check(script, tmpdir):
    body = script.replace("export const meta", "const meta", 1)
    wrapped = "async function workflowBody(log, agent, parallel) {\n" + body + "\n}\n"
    f = Path(tmpdir) / "wrapped.js"
    f.write_text(wrapped)
    return subprocess.run(["node", "--check", str(f)], capture_output=True, text=True)


# --- pipeline-level: run main() with OUT_DIR redirected to a temp dir ---
def t_pipeline_generate():
    tmp = Path(tempfile.mkdtemp())
    orig = gen.OUT_DIR
    gen.OUT_DIR = tmp
    try:
        gen.main()
    finally:
        gen.OUT_DIR = orig
    guideline = gen.GUIDELINE_PATH.read_text(encoding="utf-8")
    outs = sorted(tmp.glob("critics_workflow_*.js"))
    assert len(outs) == len(gen.METHODS), [o.name for o in outs]
    for out in outs:
        method = out.stem.replace("critics_workflow_", "")
        script = out.read_text()
        assert json.dumps(method) in script, out.name
        assert json.dumps(guideline) in script, f"{out.name}: guideline not embedded"
        tasks = json.loads(script.split("const TASKS = ")[1].split("\n")[0])
        assert len(tasks) > 0, out.name
        expected = gen.build_task_list(method, json.load(open(gen.SUBSET_IDS_PATH)),
                                       tmp / "dr14b_reviews")
        assert tasks == expected, f"{out.name}: TASKS != build_task_list output"
        r = node_check(script, tmp)
        assert r.returncode == 0, f"{out.name} not parseable: {r.stderr[:300]}"
        print(f"  {out.name}: {len(tasks)} tasks, node --check OK")
    shutil.rmtree(tmp)
check("pipeline: main() generates all method scripts, JS parseable, literals present", t_pipeline_generate)


print(f"\n{len(FAILED)} failed" if FAILED else "\nALL PASS")
sys.exit(1 if FAILED else 0)
