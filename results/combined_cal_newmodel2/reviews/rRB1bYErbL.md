## Summary

This paper proposes R-HORIZON, a method for constructing multi-step reasoning benchmarks by composing existing single-step problems with arithmetic dependencies, where the answer to one problem becomes a key variable in the next. The paper evaluates 26 LRMs across math, code, and agent domains, finding dramatic degradation as the reasoning horizon increases (e.g., DeepSeek-R1 drops from 87.3% to 24.6% on AIME25 at n=5). Mechanistic analyses reveal limited effective reasoning length, localized reflection, and poor thinking budget allocation. Finally, RL training on R1-Qwen-7B with composed data shows improvements on both composed and single-problem tasks.

## Strengths

- **Clear identification of a genuine blind spot (favorability=8.04).** The paper identifies that existing reasoning benchmarks evaluate models on isolated, single-horizon problems while real-world reasoning frequently requires chaining across multiple interdependent steps. The gap between what benchmarks measure and what deployed systems need is real and underexplored. The framing is precise and well-motivated.

- **Broad and informative evaluation across 26 models (favorability=16.37).** The evaluation spans three domains (math, code, agent) and 26 models from families including R1-series, Qwen, DeepSeek, Gemini, Claude, o4-mini, and Nemotron. Figure 3 shows consistent and dramatic degradation across model families, sizes, and task types. The finding that even o4-mini and DeepSeek-R1 drop from ~80-90% to ~20-30% on AIME25 at n=5 is striking and constitutes the paper's strongest empirical contribution.

- **Mechanistic analysis beyond raw scores (favorability=14.93).** The error-type breakdown (Figure 5), effective reasoning length analysis (Figure 6), reflection analysis (Figure 7), and token budget allocation (Figure 8) go beyond "models get worse" to diagnose *why* — premature termination, localized reflection, and front-loaded token allocation. These analyses are genuinely informative and useful to the community.

- **Clear RL training benefit as a proof-of-concept (favorability=12.11).** The RL experiments on R1-Qwen-7B show that training with composed data (+17.4 on AIME24 n=2) not only improves multi-step performance but also transfers to single-problem tasks (+7.5 on AIME24). The n=4 data yielding +50.6 on MATH500 n=8 vs. +8.4 for n=1 training is a large and meaningful difference.

## Weaknesses

### Major

- **Expected accuracy metric conflates dependency-propagation effects with reasoning-length effects.** The paper defines expected accuracy as the product of per-problem pass rates (Eq. 4), which assumes independence across sub-problems. However, the composed problems have explicit arithmetic dependencies (Algorithm 1): an error on problem i propagates a wrong value forward, making problem i+1 harder than its atomic version. The gap between actual and expected accuracy therefore simultaneously reflects dependency propagation, cognitive load from longer chains, and budget allocation effects. The paper's analysis in Section 5.1 largely attributes the gap to "limited effective reasoning length" but does not cleanly separate these factors. A control experiment composing problems without dependencies (independent concatenation) would isolate the length effect. The paper references NEST (Pan et al., 2025) which does independent concatenation, but does not directly compare against it. This weakens the specific mechanistic claims about "effective reasoning length" while not undermining the broader finding that composed problems are much harder for LRMs.

- **RL experiments are conducted on a single small model only.** All RL results (Table 1, Figures 4, 9, 10) are obtained from training R1-Qwen-7B, a 7B distilled model. The conclusion claims R-HORIZON is a "scalable, controllable, and low-cost paradigm for enhancing and evaluating the long-horizon reasoning capabilities of LRMs," but the training evidence only supports this claim for one small model. Whether benefits extend to 32B, 70B, or larger models is unknown — larger models already show less degradation in the evaluation (Figure 3), so the marginal benefit may shrink with scale. The paper lacks a limitations section acknowledging this.

### Minor

- **Seed problem filtering statistics are unreported.** The filtering criteria (Eq. 1) require that each problem's answer is an integer AND the question text contains at least one integer. The paper does not report what fraction of problems from MATH500, AIME, and AMC survive this filter, or whether surviving problems differ systematically from the original distribution. Without these statistics, it is difficult to assess how representative the R-HORIZON benchmark is of the broader reasoning challenges in the original datasets.

- **RL training comparison may not control for problem exposure.** When n=2 composed problems are used, each training example contains 2 atomic problems. The paper does not report total training steps, number of training examples, or whether total problem exposure per epoch was controlled between the n=1 and n=2 conditions. If the n=2 condition provides more engagement per atomic problem, the improvement could partly reflect more intensive practice rather than the compositional structure per se.

- **No variance or significance measures reported.** All evaluation results (Figure 3) and RL results (Table 1) are point estimates without error bars, confidence intervals, or multiple-seed training runs. Given the inherent stochasticity of GRPO sampling, single-run results should be interpreted cautiously.

### Trivial

- **Minor inconsistency in model count:** The abstract states "26 LRMs" while Section 4.1 says "25 advanced LRMs."
- **Table formatting issue:** Qwen3-32B appears twice with different values (rows corresponding to lines 157 vs. 162 in the extracted text), and one entry (127.6 on MATH500 n=4) exceeds 100, which is impossible for an accuracy metric. This suggests a data presentation error.

## Nice-to-Haves

- A controlled comparison between sequentially composed problems (with dependencies) and simply concatenated independent problems (without dependencies) would strengthen the mechanistic claims about "effective reasoning length" vs. dependency-propagation effects.
- Reporting seed-filtering retention rates per dataset would address the representativeness concern.
- Training at least one larger model (e.g., R1-Qwen-32B) with a subset of RL conditions would substantially strengthen the generalizability of the training claims.

## Removed Points

These points were removed from the input review after cross-checking against the paper:

- **Error-position confounding with difficulty:** The critic argued that the error position analysis (Figure 6) is confounded with problem difficulty. This was removed because the analysis uses the same seed problems across different composition lengths, holding individual problem difficulty constant. The stabilization of error positions as query num increases actually supports the reasoning-length-limit interpretation.
- **Pure formatting/style notes** that are parser artifacts (e.g., minor figure caption duplication).
- **Section-by-section observations** that were rhetorical or stylistic rather than substantive (e.g., the framing mismatch between "thousands or millions of steps" in the introduction and the actual n=20 maximum).
- **Criticism of the dependency function being "wholly mechanical":** This is a design choice, not a flaw, and is a reasonable starting point for constructing a benchmark.

## Novel Insights

None beyond the paper's own contributions. The reviews primarily converge on the same strengths and weaknesses that the paper itself presents.

## Suggestions

1. Add a control experiment with independent (non-dependent) concatenation of the same seed problems to isolate dependency-propagation from length effects, and report how much of the accuracy gap remains.
2. Report seed-filtering retention rates per dataset (MATH500, AIME, AMC) and compare the difficulty distribution of surviving vs. excluded problems.
3. Add a limitations section acknowledging the single-model RL experiments and the scope of the benchmark.
4. Consider training at least one larger model (e.g., 32B) with a subset of RL conditions to strengthen claims about scalability.

## Score and Decision

### Calibration Summary

**Round 1 — Bracketing anchors (broad search across score bands):**

| Anchor | Avg Score | Round | Itemized? | Comparison |
|--------|-----------|-------|-----------|------------|
| NEMESIS (jailbreaking) | 1.40 | R1 | No | Unrelated topic, very weak paper. Our paper is far stronger. |
| Planning in Strawberry Fields (LRM o1 evaluation) | 3.00 | R1 | Yes | Evaluates 2 models on existing benchmarks with no new method/dataset — our paper introduces a new method, benchmark, and RL training, making it substantially stronger. |
| Supervised CoT | 2.50 | R1 | No | Different focus, much weaker. |
| Efficiently Deploying LLMs | 3.00 | R1 | No | Different topic. |
| Alice in Wonderland (reasoning deficits in SOTA) | 5.20 | R1 | Yes | Shares the "models fail at simple variants" finding but is narrower (one problem type, no training intervention). Our paper has broader scope (3 domains, 26 models, RL training) and stronger strengths (favorability 16.37 vs. 11.49 max). |
| Putnam-AXIOM (math reasoning benchmark) | 5.80 | R1 | Yes | Similar as a benchmark showing degradation, but smaller scale (236 problems, fewer models). Our paper covers more domains and includes RL training. |
| ProcBench (multi-step reasoning) | 3.75 | R1 | No | Narrower focus, lower quality. |
| FACTOR (long-context evaluation) | 5.00 | R1 | No | Different focus (context length, not reasoning horizon). |
| Smaller, Weaker, Yet Better (training reasoners) | 7.00 | R1 | Yes | Stronger paper with more rigorous RL experiments across model sizes. Our paper's RL evidence is weaker (single model) but our evaluation is broader. |

**Round 2 — Narrowing anchors (targeted search inside 5.5–7.5):**

| Anchor | Avg Score | Round | Itemized? | Comparison |
|--------|-----------|-------|-----------|------------|
| Are Transformers Able to Reason... (FTCT) | 6.00 | R2 | Yes | Purely synthetic study. Our paper's real-world benchmarks and 26-model evaluation provide stronger empirical contribution. |
| Language Models, Grade-School Math... | 6.00 | R2 | No | Different focus (GSM8K mechanistic analysis). |
| SciBench (college-level science) | 5.60 | R2 | No | Different domain, similar tier. |
| Understanding Reasoning with Looped Models | 6.50 | R2 | No | Different methodology (synthetic looped models). |
| Step-by-Step Reasoning via TSMC | 6.60 | R2 | No | Different methodology (inference-time verification). |
| Buffer Mechanism for Multi-Step Reasoning | 6.25 | R2 | No | Synthetic study of internal mechanisms. |

**Initial bracket (Round 1):** Between 5.5 and 6.5.

**Narrowing (Round 2):** The paper is clearly stronger than Putnam-AXIOM (5.80) and Alice in Wonderland (5.20) in breadth and contribution, but weaker than Smaller, Weaker, Yet Better (7.00) in experimental rigor for the training component. The FTCT paper (6.00) is a fair comparison — both have a clear novel finding with complementary strengths (FTCT is more mechanistic/theoretical; this paper is more empirical and broad).

**Final placement:** The paper's core empirical finding (dramatic degradation on composed tasks across 26 models) is robust and important. The mechanistic analyses add diagnostic value. The RL training results are a promising proof-of-concept. The main weakness (expected accuracy conflation and single-model RL) does not invalidate the core findings but limits the strength of specific mechanistic claims and the generality of training claims. Comparing itemized favorability: the paper's strongest strengths (16.37, 14.93) exceed those of the 5.20 and 5.80 anchors, while its most negative weakness (-1.21) is less severe than the most negative items in the 5.20 anchor (-5.19, -4.73). The paper sits comfortably above papers scoring 5–6 but below the 7.00 anchor whose RL experiments are more comprehensive. I therefore place it at **6.0**.

**Score and Decision:**

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>