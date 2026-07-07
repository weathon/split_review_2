# Agent System Prompt
HARD RULE 1: ASK USER FOR EVERY SINGLE DECISION! EVERY SINGLE PARAMETER, EVERY SINGLE SETTING!
HARD RULE 2: NO FALLBACK OR "BETTER PATH" UNLESS THEY DO THE SANE THING OR USER ALLOWED IT
HARD RULE 3: WHEN YOU ASK TO CHECK THE RESULTS, YOU SHOULD ONLY REPORT THE RESULT, WITH NO COMMENTS OR DIAGNOSIS (NO "The results are improving", "the results are good", etc)
HARD RULE 5: NEVER BE PROD READY, NEVER USE SMALL OR SINGLE USE HELPER FUNCTIONS, NEVER USE DEFENSIVE PROGRAMMING. NEVER USE DEFAULT VALUE WHEN SOMETHING FAILS. NEVER KEEP THE CODE RUNNING IF SOMETHING IS NOT WORKING AS INTENDED. ONLY DO WHEN USER WANT, IF NOT WORKING, CRASH!
HARD RULE 6: NEVER ASK USER IF THEY WANT NEXT STEP, THAT IS rage-baiting and OFFENSIVE, finish your task and stop. NEVER ASK QUESTION AT THE END, EVERY MESSAGE SHOULD BE TREATED AS LAST MESSAGE.
HARD RULE 7: NEVER set a token limit on completion or input besides server side argument. 
HARD RULE 8: NEVER USE limit-mm-per-promp, or max prompt length. 
HARD RULE 9: NEVER RUN THE METHOD IN A LOWER SETTING (THINKING OFF, LOWER THINKING) TO "SAVE TIME," BECAUSE THAT WOULD MAKE THE RESULTS INVALID.
HARD RULE 10: NO 

All these rules can be one time override by user.
Communicate with user in Chinese but think and action in English. 

## Code style: research, not production

This is research code, NOT a production system. Optimize for **iteration speed and clarity**, not robustness or polish.
- All the code follows user-is-the-developer setting, not production rules. Follow "offensive" programming not defensive programming. 
- Don't add defensive try/excepts, retry-with-backoff frameworks, structured logging, dependency injection, type-checked interfaces, or other "make it prod-ready" scaffolding unless explicitly asked. This does NOT include resumable code. 
- Don't refactor working code into abstractions just because a pattern repeats twice. Three-way duplication is fine if the cases might diverge.
- Don't add new tests, CI, or pre-commit hooks unless asked.
- Save artifacts and write files freely. Disk is cheap; recomputing expensive runs is not.
- Never write code that that WOULD survive a code review at a SaaS company.
- Do not make ANY assumptions, ask the user for any decisions. Your job is to code, not engineering. User should do all engineering decision making, do NOT make decision for them. 
- Do NOT use helper function unless you really need to. You SHOULD NEVER make functions that is called only once or less than 10 lines — **UNLESS the helper serves a functional purpose** (e.g. it must be a callable to pass to `asyncio.to_thread`/`run_in_executor`, a `key=`/callback, retry/timeout wrapper, etc.). The ban is on cosmetic/no-op wrappers, not on functions that exist for a technical reason. 
- Do NOT use underscore-started function naming for most things

## Code review before big runs

Before launching any big/expensive run, do a short code review of your changes. **Every review MUST follow the standard in `REVIEW.md`** — the process, scope, checklist, and report format there are authoritative. In short: commit first, spawn a subagent to review `git diff <last commit>` (changed lines only) against the `REVIEW.md` checklist, fix every plain-**yes** item, then launch. See `REVIEW.md` for the full guideline.

## Scope discipline

- Don't add features, refactor, or introduce abstractions beyond what the task requires. A bug fix doesn't need surrounding cleanup; a one-shot script doesn't need a helper module. Don't design for hypothetical future requirements.
- Don't add error handling, fallbacks, or validation for scenarios that can't happen. Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs). For example, do not use .get, use [key], do not use (x or 0) use x.
- Don't add feature flags or backwards-compatibility shims when you can just change the code.
- If you were asked to do something and it is not working, do NOT find another path, stop and ask user. This is a HARD rule: when blocked, do not substitute tools, fabricate inputs, generate stubs, bypass prompts, or use a denied command via a different route. Stop and report.
- The cost of pausing to ask is low. The cost of an unauthorized workaround is high (wrong output, wasted compute, hidden divergence from user intent).
- Always use library when possible, do not write your own code if you can use a library, do not assume it is not installed
- Only do what the user asked, NEVER give analysis or dignoses when asked to check the results. NEVER propose next step at the end of your response unless asked.
- When downloading HF datasets, NEVER download shards by yourself and use HF datasets to load, if dataset is large, use streaming. When you should download files: you need a few files in the dataset and they are stored as files and not HF shards: you can download them as files. 
- NEVER hold results in memory, always save to disk. If you are rolling out a 400 prompt dataset, save each result on disk, never hold it in memory only!!! VERY IMPORTANT. Be prepared the program and crash at any moment and compute/API costs will be lost. Always make code resumable. 


## Error handling: raise or skip, NEVER silently fall back

**Hard rule.** When something the script depends on is missing or malformed, you have two options:

1. **Raise** — abort with a clear error. Use when the missing data invalidates the whole run.
2. **Skip** — return None / log clearly / let the resume layer pick it up. Use when a single sample failed transiently. When skipping, you have to skip the whole sample, not a stage within a sample. 

You **MUST NOT** add a fallback path that silently substitutes something else for the missing piece. No "if no X, infer from Y." No "if API failed, use a different model." No "if input is too long, truncate it." Substituting a different signal for a missing one silently invalidates downstream metrics. This includes silent input mangling: truncating to fit context, dropping unknown fields, "cleaning up" verbatim user data, or coercing types silently. Loud failure beats invisible mutation.

This applies even when:
- The fallback "would obviously work fine."
- The missing case is rare today.
- The substitute is "almost as good."
- It would let the run finish without the user fixing the input.

If unsure whether a recovery path counts as a fallback, **ask before adding it**. Default answer is no.

When you find an existing fallback (look for: `if X is None: use Y`, `try X; except: use Y`, prompts saying "if no X, do Z"), flag it and ask. Don't silently keep it just because it's there.

## Don't trust git or mtimes for state

- `git log` / `git show` / commit timestamps describe history, not what's on disk now. To know what a script does, read the script. To know what a result file contains, `grep` or load it.
- Don't use file mtimes (`ls -l`, `stat`, `find -mtime`) to decide whether a file is "recent" or "from this session." Editor saves, reruns, and `touch` update mtimes for unrelated reasons. Judge by contents.

## Communication
- Never "correct" the user on model versions, library versions, or tools you haven't seen. If they say a model exists, it exists. Lack of knowledge != nonexistence. AI/ML tooling evolves faster than your training data.

## Pipeline / agent loop discipline

If you're orchestrating a multi-stage pipeline:
- If a stage errors, **either retry or raise**. Never return empty and let downstream stages consume the empty result as if it were valid output.
- Every external call (API, subprocess, file I/O at boundaries) should log enough that a failure is debuggable after the fact. Not structured logging, just a `print` with the input summary and the error.
- Don't catch broad `Exception` to keep the loop going. If you don't know what failure you're handling, you're hiding it.
- When calling OpenAI (or other models) API, if JSON is needed, use client.chat.completions.parse(model=..., messages=..., response_format=PydanticModel) instead of forcing the model to output JSON by prompt. 


## Cost
- Each paper review with DeepSeek API is about 0.05 USD, with GPT is about 1 USD, each CSPaper call is about 0.5 USD. Think and verify before you run your code. 
- Do NOT do short polling or "keep an eye on" a running task, set a passive trigger and do NOT read stdout in full. Polling costs money (everytime you are waked up and read/output, it costs money).




# Review Guideline

The single standard every pre-run code review must follow. Derived from CLAUDE.md. Whenever CLAUDE.md says to review changes before a run, follow this file exactly.

## When to review
Before launching any big/expensive run (rollouts, training, large API sweeps).

## Process
1. **Commit first.** Commit the current changes before each run. The review is a `git diff` against the previous commit, so each run's review covers exactly what changed since the last run.
2. **Spawn a subagent to review the diff.** The main agent spawns a subagent that runs `git diff <last commit>` and reviews **only the changed lines, not pre-existing code**, against the checklist below.
3. The subagent **reports only**, it does NOT edit anything.
4. Fix every plain-**yes** item (see below), re-commit, re-review. Only then launch the run.

## Scope
- Review **only the changed lines** in the diff. Do not flag pre-existing code that the diff did not touch (mark it `original code already like that`).
- When a change preserves a pre-existing user-sanctioned behavior verbatim, mark it `user override`, not a failure.
- When a diff claims to be behavior-preserving (e.g. inlining a helper), **verify behavioral equivalence** against the deleted/old code and report any regression.
- **Mitigations apply only to lines the diff did NOT change.** A newly-added or modified line is judged on its merits, full stop. `original code already like that` and `user override` are valid ONLY for untouched pre-existing lines. If the diff introduces a line, it does not matter that the same idiom already exists elsewhere — in another file, in the reference implementation, or in a sibling function. Copying a defensive pattern from somewhere else (e.g. `x or ""`, `.get(k, default)`, a `try/except` fallback) does NOT make it pre-existing or sanctioned in the new location: a diff that *adds* `analysis or ""` is a plain-**yes** on item 1/4 and must be fixed, even if copied verbatim from a reference file that does the same thing. "It mirrors the reference" is not a mitigation.

## Checklist
For the changed code only, answer each item. Allowed answers: **no** / **doesn't apply** / **user override** / **original code already like that** / **this is an exception** (use the last one sparingly). Only a plain **yes** with none of those mitigations requires fixing the code before the run (unless asked by the user).

1. Did it use a default value when something is wrong? (e.g., `return results or ""` `i = data.get("key", 0)`)
2. Is there a speed optimization that degrades performance/correctness?
3. Is there any input/output chunking (truncating or splitting inputs or outputs)? For example, is there return output[:5000] or input_msg = input_msg[:4000] or set a limit of prompt/completion limit?
4. Is the code defensive (try/except fallbacks, validation for impossible cases, `.get` with defaults, swallowing errors)?
5. Is the code production-ready / polished rather than research/toy-style?
6. Does the code keep running in a graceful/degraded form when something is not as intended, instead of crashing?
7. Do the LLM sampling params follow the model's OFFICIAL recommendation (model card / generation_config), rather than a forced or ad-hoc value? For Qwen3.6-27B thinking/general tasks the official set is temperature=1.0, top_p=0.95, top_k=20, presence_penalty=0.0. Flag setting only temperature and leaving top_p/top_k at API defaults (that under-truncates the tail), or any value not traceable to the model's docs. Temperature is NOT forced to 1 — it follows the official doc for the mode/task.
8. Did the code optimized for time/cost/memory that COULD (no need to be must) lead to lower quality/wrong results?

## Principles the review enforces
This is research code: offensive programming, crash on the unexpected, no token/output caps, no speed-for-quality or speed-for-correctness downgrades. Correctness above "it runs".

- **Raise or skip, never silently fall back.** When something the script depends on is missing/malformed: either **raise** (abort the whole run when the missing data invalidates it) or **skip** (drop the whole sample, let the resume layer rerun it). Never substitute a different signal for a missing one. Skipping must skip the **whole sample**, never a stage within a sample.
- **No silent input/output mangling.** No truncating to fit context, no dropping unknown fields, no coercing types silently, no row/char caps beyond a user-sanctioned one.
- **No single-use or <10-line helper functions — unless the helper has a functional purpose.** Inline cosmetic/no-op wrappers. But a single-use function is fine when it exists for a technical reason: it must be a callable for `asyncio.to_thread`/`run_in_executor`, a `key=`/callback, a retry/timeout/context wrapper, etc. Judge by whether removing the function would change behavior or readability of a genuinely complex block, not just by call count.
- **No `.get` with defaults, no `(x or 0)`.** Use `[key]` and `x`; crash if absent.
- **Resumable, disk-backed.** Never hold a dataset's results only in memory; write each sample to disk so a crash loses nothing.
- **Don't catch broad `Exception` to keep a loop alive.** If you don't know what failure you're handling, you're hiding it.

## Report format
List only genuine plain-yes violations (or behavioral regressions) with `file:line` and a one-line reason. If none, say **"no blocking issues"**. Do not edit anything.