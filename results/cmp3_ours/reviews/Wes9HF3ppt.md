Now I have a clear calibration picture. Let me write the final review.

## Summary
This paper introduces Insertion Language Models (ILMs), which generate sequences by inserting one token at a time at arbitrary positions, addressing limitations of both autoregressive models (fixed left-to-right order) and masked diffusion models (fixed-length masks and simultaneous unmasking). The authors propose a denoising training objective with a transformer parameterization, and evaluate on planning tasks (star graphs, zebra puzzles) and text generation/infilling (LM1B, TinyStories). ILMs substantially outperform ARMs and MDMs on planning tasks with variable-length outputs, while being competitive on text tasks and offering greater flexibility for arbitrary-length infilling.

## Strengths
- **Genuinely novel approach targeting a real MDM limitation.** The paper identifies that MDMs cannot handle arbitrary-length infilling because masks are fixed-count placeholders, and designs a token-dropping + insertion mechanism that directly addresses this. The motivating example ("The conference, <mask> was postponed" cannot produce "originally planned for March" with a single mask) is clean and the design follows naturally from the identified gap.
- **Decisive results on planning tasks.** ILM achieves 100%/100%/99.1% accuracy on star graph easy/medium/hard variants, while MDM drops to 36.5%/21.0% and ARM (left-to-right) scores 32.3%/75.0%/23.0%. On zebra puzzles, ILM achieves 90.0% vs ARM 81.2% and MDM 82.6%. These are categorical differences, not incremental improvements, and they cleanly validate the thesis that out-of-order one-at-a-time insertion helps on problems with non-sequential dependencies and variable-length outputs.
- **Controlled comparison setup.** Model size (~85M non-embedding parameters), architecture family (RoPE transformer for ILM/ARM, DDiT for MDM), training steps, and hyperparameters are matched across all three families. The MDM uses the standard DDiT from prior work — not a strawman baseline.
- **Clean interpretable analysis of failure modes.** On star graphs, the paper shows that ARMs succeed when trained in reverse order (100%) but fail left-to-right (32.3%), and that MDMs fail on variable-length arms because they use absolute token positions. This provides strong evidence for *why* ILMs succeed on these tasks.

## Weaknesses

### Fatal
None.

### Major
- **The core training objective is acknowledged as "biased" but never analyzed.** Section 3 states that a naive denoising objective for the token-dropping process has "extremely high variance" and is replaced with a "biased training objective" that trains the model to predict normalized counts of all dropped tokens simultaneously. The paper provides no analysis of this bias — its direction, magnitude, or effect on the learned distribution — and the referenced appendix (D) is unavailable. This matters because training uses aggregate targets over all dropped tokens (Equation 2) while inference inserts tokens one at a time conditioned on its own previous insertions. If the bias systematically distorts the conditional distribution, the text generation results (which rely on the quality of this distribution) would be affected. Even a small-scale synthetic experiment where the true objective is tractable via enumeration, comparing the biased objective to the ground truth, would substantially increase confidence in the method.
- **No statistical uncertainty reported for any experimental result.** No standard deviations, confidence intervals, or number of seeds are reported. This is particularly problematic for the text results where differences are small (e.g., ARM NLL 2.11 vs ILM 2.14 on Stories — a 1.4% gap — and infilling improvements of 1–5 percentage points). Without error bars it is impossible to know whether these gaps are meaningful or would vanish across runs. While the planning results are large enough that variance is unlikely to change the qualitative conclusion, the lack of rigor on text results is a significant methodological gap.

### Minor
- **The primary text metric systematically advantages the ARM baseline.** The main metric for unconditional generation (Table 2) is per-token NLL under Llama-3.2-3B — an autoregressive model. An AR evaluator assigns lower NLL to sequences matching its own left-to-right conditional structure and could penalize semantically valid but differently-structured non-AR outputs. The paper partially addresses this with Prometheus 2 7B as an LLM judge (Figure 5), where ILM "generally outperforms ARM and MDM across most metrics." However, the Prometheus results are reported only as bar charts without numerical values, making the magnitude of ILM's advantage unverifiable.
- **ILM's average generated length on Stories (119 tokens) differs notably from the training data (205 tokens) but is not discussed.** The paper discusses MDM's length deviation (985 vs 205) but does not address whether ILM's shorter outputs systematically affect NLL comparison. Under an AR evaluator, shorter sequences tend to have lower NLL because there are fewer tokens to deviate from the evaluator's expectations, which could partially explain ILM's competitive NLL despite other apparent quality differences.

### Trivial
None.

## Nice-to-Haves
- An ablation comparing the stopping classifier (ILM's approach) against EOS-based stopping (Insertion Transformer's approach) on text data would isolate how much of ILM's advantage comes from the stopping mechanism versus the insertion training itself.
- Qualitative examples of text infilling showing concrete cases where ILM handles multi-segment or variable-length infilling that MDM cannot would ground the claims (e.g., the "conference...postponed" example from the Introduction).

## Removed Points
[These points are flagged to be removed — treat them with caution]
- **Section-by-section presentation suggestions** (e.g., "the description would benefit from a worked example", "the paper should clarify whether this limitation generalizes to text") — these are subjective presentation preferences or scope-creep, not substantive weaknesses. Removed per soft rules.
- **Concerns about missing appendix content** (e.g., missing analysis from Appendix D) — removed per rule that appendix was stripped by the parser and exists in the original submission.
- **Missing related works / citations** — removed because I cannot independently verify whether specific papers were cited or not.
- **Criticism about unreleased code/data/models** — removed per hard rule that all cited references are assumed to exist.
- **"The paper should note that the greedy sequential unmasking variant of MDMs is a known workaround"** — the paper already addresses this in the Related Work section (lines 125-127), so this criticism misreads the paper. Removed.

## Novel Insights
None beyond the paper's own contributions. One observation that emerges from the review is that the key strength (decisive planning results) and key weakness (unanalyzed biased objective) are somewhat decoupled: the planning tasks are sufficiently structured and deterministic that even a biased objective would likely converge to the correct solution, while the text tasks depend much more critically on the fidelity of the learned distribution. This suggests the paper's core contribution is strongest on structured/constrained generation problems, and the text claims should be viewed with appropriate caution.

## Suggestions
1. **Analyze the biased objective.** Provide either a theoretical characterization of the bias (direction, magnitude, dependence on sequence length/vocabulary) or an empirical validation on small sequences where the true objective is tractable via enumeration.
2. **Add statistical rigor.** Report standard deviations / confidence intervals for all quantitative results, especially text NLL, entropy, and infilling metrics. Report number of random seeds for all experiments (at minimum for zebra puzzles and text results).
3. **Report numerical values for Prometheus evaluation** alongside the bar charts in Figure 5, so the magnitude of ILM's claimed advantage can be independently assessed.
4. **Discuss the length distribution of generated text.** ILM's average length on Stories is 119 vs training data 205 — comment on whether this affects the NLL comparison and whether the stopping classifier is undershooting.

## Score and Decision

**Calibration anchor papers used (retrieved across all rounds):**

| Path | Avg Score | Round | Comparison to this paper |
|------|-----------|-------|------------------------|
| COrAL (0JjsZC0w8x.md) | 5.75 | R1, R2 | Order-agnostic language modeling with modest gains on reasoning; this paper has more novel approach and stronger planning results |
| FiLM (UbOzNf6hGq.md) | 4.25 | R1 | Any-order generation via beta-distribution masking; this paper's planning results are far stronger and the method is more distinctive |
| SAR Diffusion (tyEyYT267x.md) | 8.00 | R1 | Strong theory + SOTA text results; this paper has less thorough theoretical grounding but a cleaner novel contribution |
| PlaSma (dFcXJgnrGB.md) | 6.50 | R2 | Procedural planning with small LMs; comparable quality but different domain |
| LLMs Can Plan (K3KrOsR6y9.md) | 6.40 | R2 | LLM planning in constrained settings; comparable contribution level |

**Round 1 bracket (initial):** [5.5, 7.5] — based on comparison to COrAL (5.75), FiLM (4.25), and SAR Diffusion (8.00).

**Narrowing:** The paper is clearly stronger than COrAL (5.75) and FiLM (4.25) due to (a) a more novel and cleanly-motivated method and (b) unequivocally stronger planning results. It falls short of the SAR Diffusion paper (8.00) which provides thorough theoretical grounding for its training objective, has SOTA text results, and reports extensive ablations. The PlaSma and "LLMs Can Plan" papers at 6.40–6.50 provide a reasonable comparator for contribution level and empirical quality.

**Final score:** 6.5 — a genuinely novel method with strong validation on planning tasks and promising (if not yet decisive) text results. The unanalyzed biased objective and missing statistical rigor prevent a higher score, but the core contribution is substantial and well-supported on the paper's strongest terms.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>