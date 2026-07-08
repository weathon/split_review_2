Now I have all the information I need to write the final consolidated review. Let me compile my analysis.

**Calibration anchor summary:**

| Paper | Score | Round | Itemized | Comparison |
|-------|-------|-------|----------|------------|
| tyEyYT267x — Interpolating AR and Discrete Diffusion LMs | 8.00 | R1 | Yes | Stronger text benchmarks & theory, less novel formulation |
| riNuqYiD66 — Branching Decoder for Set Generation | 7.00 | R1 | Yes | Solid task-specific contribution, less novel paradigm |
| NRYgUzSPZz — Beyond Autoregression: Discrete Diffusion for Planning | 6.25 | R1+R2 | Yes | Similar planning focus; weaker formulation but cleaner task scope |
| WNvvwK0tut — Scaling up MDMs on Text | 6.50 | R2 | Yes | Stronger experiments, less novel contribution |
| MJNywBdSDy — Discrete Diffusion with Planned Denoising | 5.75 | R2 | Yes | Similar idea space, weaker overall |
| 0JjsZC0w8x — COrAL: Order-Agnostic LM | 5.75 | R1 | Yes | Similar scopen, limited generalization |
| FJWT0692hw — SequenceMatch | 6.00 | R1 | Yes | Different approach, similar evaluation concerns |

**Round-1 bracket:** After comparing my draft weights (strengths 9.32–11.43, weakness weights ranging from -0.39 to 5.71) against the anchors, the plausible band was 5.5–7.5.

**Narrowing to final score:** The closest anchor is the "Beyond Autoregression" paper (6.25), which has similarly strong planning results but a less novel formulation. The ILM paper's formulation is more genuinely novel, which the model weights confirm (strengths at 9.32–11.43). However, the length confound weakness has a strongly negative weight (-0.39), indicating it's a drag comparable to the "unfair comparison" weakness in the Scaling MDMs paper (6.50). The training bias concern (weight 2.36) is moderate. Overall, the ILM paper sits between the planning-focused diffusion paper (6.25) and the scaling paper (6.50) — I place it at 6.5.

---

## Summary

This paper introduces Insertion Language Models (ILMs), a novel approach to sequence generation that learns to jointly predict a token and an insertion position, allowing arbitrary-order generation. To enable tractable training, the authors propose a denoising objective where dropped tokens are removed (not masked) and the model is trained to predict normalized counts of vocabulary items per insertion slot. The paper evaluates ILMs on synthetic planning tasks (star graphs, zebra puzzles) and text generation/infilling on LM1B and TinyStories.

## Strengths

- **A genuinely novel formulation for variable-length out-of-order generation.** The core idea — learning to jointly predict a token and a position for insertion, trained via a denoising objective where dropped tokens are removed rather than masked — is a clean departure from both ARMs and MDMs. The target insertion distribution d(k,v; x,b) that aggregates normalized counts (Eq. 2) directly addresses the high-variance problem that would otherwise make training infeasible.

- **Synthetic planning results are decisive and instructive.** On Star_hard (Table 1), ILM achieves 99.1% exact-match accuracy versus 23.0% for ARM and 21.0% for MDM. The star graph experimental design (easy vs. medium vs. hard) cleanly isolates failure modes (absolute position reliance in MDM, left-to-right lookahead failure in ARM). The zebra puzzle result (90.0% vs. 82.6% for MDM, 81.2% for ARM) is similarly strong. These experiments establish that ILM can succeed on constraint-satisfaction tasks where both baselines systematically fail.

- **Honest about limitations (§6).** The paper straightforwardly acknowledges that ILMs underperform ARMs on text NLL, do not support KV caching, and are slower at inference.

## Weaknesses

### Major

- **The biased training objective is acknowledged but never analyzed.** The paper states (§3) that the true denoising objective requires marginalizing over all possible generation trajectories and replaces it with normalized counts of dropped tokens per insertion slot. However, inference is sequential — the model inserts one token at a time, and the next insertion should condition on what was just inserted. The training target is an aggregate over the entire set of dropped tokens, creating a mismatch that the paper never characterizes: the nature, direction, or magnitude of this bias, whether it is benign for planning but harmful for text, or whether the inference procedure can recover correct conditional distributions despite the mismatch. The synthetic results suggest the bias is tolerable for those tasks, but without any analysis it is unclear how far this generalizes. The paper's limitations section does not mention this issue.

- **The text generation evaluation has a massive length confound that makes some comparisons uninterpretable.** On Stories (Table 2), MDM generates 985 tokens on average vs. ILM's 119 (dataset average: 205). On LM1B, MDM averages 85 vs. ILM's 21 (dataset average: 28). Per-token NLL under Llama is not length-invariant; shorter sequences are systematically easier for an evaluator LLM because there are fewer opportunities to diverge from common patterns. Comparing NLL across models with 5× length differences makes the MDM-vs-ILM comparison uninterpretable as a quality metric. The paper does not report any length-controlled comparisons.

### Minor

- **The Prometheus judge results (Figure 5) are reported only as a bar chart with no numerical values, confidence intervals, or statistical tests.** The caption says ILM "generally outperforms ARM and MDM across most metrics," but without underlying numbers or variance information, this claim cannot be verified. Combined with the length confound (LLM judges are known to be sensitive to length), the Prometheus evidence is weak.

- **The stopping classifier creates a training/inference mismatch that likely causes the observed length undershoot.** The stopping loss (Eq. 3) trains the model to predict S=1 only when b is the all-zeros vector (i.e., when the subsequence is the *full* original sequence), and S=0 otherwise. During training, the classifier never sees a partial sequence labeled as "complete." At inference, it must decide when to stop from partial sequences, creating a mismatch. On LM1B, ILM averages 21 tokens vs. the dataset's 28 (a 25% undershoot). The paper notes this in passing but does not analyze or address it.

- **The abstract's claim that ILMs "perform on par with ARMs" in unconditional text generation is selectively supported.** On Stories the gap is small (2.14 vs 2.11 NLL, ~1.4%), but on LM1B the gap is large (4.67 vs 3.94 NLL, ~18.5%), where ILM is much closer to MDM (4.81). The paper body acknowledges ARMs are better, but the abstract's framing is stronger than the evidence supports, especially for LM1B.

### Trivial

- **Naming inconsistency:** The text (§5.1.1) refers to "Star_small" while Table 1 uses "Star_easy" for what appears to be the same condition.
- **ARMO results for Star_medium and Star_hard are marked with dashes** in Table 1 without explanation. Since ARMO (oracle-order ARM) would be an informative upper bound, the omission should be justified.
- **The entropy metric (Eq. 5) measures bag-of-token frequency, not sequential diversity** — two texts with different orderings but the same token counts have identical entropy scores. The paper uses it alongside other metrics, so this is minor.

## Nice-to-Haves

- Add a FIM-trained ARM baseline (Bavarian et al., 2022) for the single-segment infilling experiments, which the paper discusses in related work but does not compare to empirically.
- Report text generation results with length-matched or length-binned comparisons to control for the length confound.
- Provide numerical values and confidence intervals for the Prometheus judge results.
- Add a controlled experiment isolating the stopping mechanism: compare ILMs with gold-length stopping (rejection sampling) vs. learned stopping.
- Report wall-clock time to generate a complete sequence (not just per-token time).
- Include a small-scale empirical analysis of the training bias (e.g., train on a PCFG and compare learned insertion distributions to true sequential conditionals).

## Removed Points

These points from the input review were removed with justification:
1. **"Infilling comparison is not informative"** — REMOVED: The comparison demonstrates ILM's flexibility advantage over MDMs, which is a central and valid claim. The MDM limitation (needing mask counts) is a well-known design constraint, and showing ILM performs better despite not needing this information is instructive.
2. **"Missing baselines (permutation LM, span-corruption, Diffusion-LM)"** — REMOVED: Generic request for additional baselines beyond the core comparisons (ARM, MDM). Scope creep.
3. **"IT baseline may not be faithful to original architecture"** — REMOVED: Speculative without verification.
4. **"No human evaluation"** — MOVED to Nice-to-Haves; LLM judges are standard practice.
5. **"Computational cost comparison incomplete"** — MOVED to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The reviews surface two genuine concerns that the paper's own framing deemphasizes: (a) the aggregate-counts training target creates an uncharacterized training/inference mismatch that goes beyond typical "biased estimator" concerns, and (b) the text evaluation's length confound (MDM generating 5× longer sequences than ILM) fundamentally undermines the unconditional generation comparisons. Neither insight alters the paper's core contribution but both point to where the evidence needs strengthening.

## Suggestions

1. Reframe the contribution to foreground structured/constrained generation (where the evidence is strongest) and position the text results as preliminary evidence of breadth rather than a headline claim.
2. Add an analysis of the training bias — even a simple synthetic experiment on a known distribution would clarify whether the bias is benign or harmful.
3. Provide length-controlled text evaluations and numerical values for the Prometheus results.
4. Investigate and address the stopping classifier mismatch that causes the systematic length undershoot.

## Score and Decision

**Score: 6.5 — Decision: Accept**

The paper introduces a genuinely novel formulation for out-of-order sequence generation with decisive evidence on planning tasks. The text generation evaluation, however, has significant confounds (length mismatch in NLL comparisons, missing numerical rigor for Prometheus results, overclaimed abstract) that prevent the paper from being a stronger contribution. The training bias is a real but not fatal concern that deserves analysis. With revision of the text evaluation and tempering of the text generation claims, this would be a solid contribution to ICLR.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>