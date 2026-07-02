import json
import random
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
DATA = SCRIPT_ROOT / "data/ReviewCritique.jsonl"
OUT = SCRIPT_ROOT / "outputs/weakness_reliability_guideline.md"
MAX_PER_TYPE = 10
SEED = 0
RELIABLE_FRACTION = 1 / 3  # add reliable (valid) weakness examples = this fraction of the unreliable count

CATEGORIES = [
    ("Misunderstanding", "The reviewer misinterprets claims or ideas presented in the paper, leading to inaccurate or irrelevant comments."),
    ("Neglect", "The reviewer overlooks important details explicitly stated in the paper, resulting in unwarranted questions or critiques."),
    ("Vague Critique", "The review lacks specificity, claiming missing components without clearly identifying what is missing."),
    ("Out-of-scope", "The reviewer suggests additional methods, experiments, or analyses that are beyond the intended scope of the paper."),
    ("Invalid Criticism", "The reviewer's criticism is considered invalid, especially when suggesting impractical experiments or trivializing results."),
    ("Superficial Review", "The reviewer appears to have only skimmed the paper, providing generic or unsupported comments about the presence or absence of weaknesses."),
    ("Unstated statement", "Statements made in the review are not supported by content in the paper."),
    ("Excessive demands", "if the weaknesses are just asking for excessive things that are not necessary for a good paper."),
    ("Generic comment", "weaknesses are just generic comments that can apply to any paper, without really pointing out the specific problems of the paper."),
]

by_type = {name: [] for name, _ in CATEGORIES}
reliable_weak = []
with DATA.open() as f:
    for line in f:
        rec = json.loads(line)
        for k in ['review#1', 'review#2', 'review#3', 'review#4']:
            if k not in rec:
                continue
            for seg in rec[k]['review']:
                et = str(seg.get('error_type', '')).strip()
                rel = str(seg.get('reliability', '')).strip().lower()
                tc1 = str(seg.get('topic_class_1', '')).lower()
                text = str(seg.get('segment_text', '')).strip()
                if rel == 'no':
                    if et in by_type:
                        by_type[et].append(seg)
                elif rel == 'yes' and 'weakness' in tc1 and len(text) > 40:
                    reliable_weak.append(seg)

lines = []
lines.append("# Weakness Reliability Guideline\n")
lines.append("Use this guideline to judge whether a weakness raised in a paper review is RELIABLE (well-grounded, paper-specific, actionable) or UNRELIABLE (matching one of the error patterns below).\n")
lines.append("## Error type table\n")
lines.append("| Error Type | Explanation |")
lines.append("|---|---|")
for name, defn in CATEGORIES:
    lines.append(f"| {name} | {defn} |")
lines.append("")

lines.append("## Unreliable weakness examples (per error type)\n")
lines.append("Each example is a real reviewer segment annotated by a human as UNRELIABLE, with the human's explanation of why. Do NOT assume a weakness is unreliable just because it is a criticism -- only mark unreliable when it matches one of these error patterns.\n")
n_unreliable = 0
for name, defn in CATEGORIES:
    lines.append(f"### {name}\n")
    lines.append(f"*{defn}*\n")
    examples = by_type[name]
    if len(examples) > MAX_PER_TYPE:
        rng = random.Random(SEED)
        examples = rng.sample(examples, MAX_PER_TYPE)
    if not examples:
        lines.append("_No examples available in the source dataset._\n")
        continue
    n_unreliable += len(examples)
    for i, seg in enumerate(examples, 1):
        text = seg.get('segment_text', '').strip()
        expl = str(seg.get('explanation', '')).strip()
        if expl.lower() in ('nan', ''):
            expl = '(no explanation provided)'
        lines.append(f"**Example {i}**")
        lines.append(f"> Reviewer wrote: {text}")
        lines.append(f"")
        lines.append(f"Why unreliable: {expl}")
        lines.append("")

n_reliable = round(n_unreliable * RELIABLE_FRACTION)
rng = random.Random(SEED)
seen = set()
uniq_reliable = []
for seg in reliable_weak:
    t = str(seg.get('segment_text', '')).strip()
    if t in seen:
        continue
    seen.add(t)
    uniq_reliable.append(seg)
rng.shuffle(uniq_reliable)
picked = uniq_reliable[:n_reliable]

lines.append("## Reliable (valid) weakness examples\n")
lines.append("Each example below is a real reviewer weakness segment annotated by a human as RELIABLE (a genuine, well-grounded criticism). Use these to calibrate: many critical-sounding weaknesses ARE reliable. Only mark reliable=0 when the segment clearly matches one of the error patterns above.\n")
for i, seg in enumerate(picked, 1):
    text = str(seg.get('segment_text', '')).strip()
    expl = str(seg.get('explanation', '')).strip()
    lines.append(f"**Example {i}**")
    lines.append(f"> Reviewer wrote: {text}")
    lines.append("")
    if expl.lower() not in ('nan', ''):
        lines.append(f"Why reliable: {expl}")
        lines.append("")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(lines))
print(f"wrote {OUT}")
for name, _ in CATEGORIES:
    shown = min(len(by_type[name]), MAX_PER_TYPE) if by_type[name] else 0
    print(f"  {name}: {len(by_type[name])} available, {shown} shown")
print(f"  unreliable shown total: {n_unreliable}")
print(f"  reliable weakness pool: {len(uniq_reliable)}, added: {len(picked)}")
