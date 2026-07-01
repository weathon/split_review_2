## Summary

This paper proposes LoLoRA, a method that combines local (forward-pass) updates of LoRA's A matrix (via Hebbian PCA or autoencoder loss) with backpropagation-based training of the B matrix. The paper derives a theoretical result (Theorem 4.4) characterizing optimal A initialization as spanning the PCA subspace of input activations, formalizing and extending earlier empirical findings from EVA (Paischer et al., 2024). Experiments are conducted across RoBERTa-large, LLaMA-3.1-8B, LLaVA-v1.5-7B, and TinyLlama-1.1B on NLU, math reasoning, multimodal, and instruction-following tasks.

## Strengths

1. **Theorem 4.4 provides a clean theoretical characterization of optimal A initialization.** Under a random regression model for the target, the optimal A matrix spans the top-r principal subspace of the input covariance matrix. This formalizes and generalizes the EVA empirical observation and is correctly proved. The asymmetry between A and B (Theorems 4.4 vs 4.5) is a useful finding that complements the existing literature on adapter asymmetry.

2. **Thorough experimental evaluation across multiple dimensions.** The paper evaluates across model scales (RoBERTa-large, LLaMA-3.1-8B, LLaVA-v1.5-7B, TinyLlama-1.1B), task types (NLU, math reasoning, multimodal, instruction-following), and reports results with 3-seed error bars. This is more comprehensive than many LoRA modification papers.

3. **The ablation study on initialization and local rules is informative and independently useful.** Tables 5–6 provide a clean comparison showing that (a) EVA initialization beats other initializations (uniform, orthogonal, PiSSA) for frozen A, (b) HPCA updates and EVA initialization achieve essentially identical perplexity, and (c) Full LoRA consistently outperforms all low-memory variants by a clear margin.

## Weaknesses

### Fatal
None.

### Major

1. **The paper's central claim — that LoLoRA improves upon LoRA-FA — is not supported by the experimental evidence.** Across all three main experiments, LoLoRA performs at best statistically tied with, and often worse than, LoRA-FA with the stronger baseline:
   - **GLUE (Tables 1–2):** LoLoRA is worse than LoRA-FA (uniform) on 6/8 tasks (CoLA 66.3 vs 67.9, RTE 84.6 vs 86.4, MNLI 90.3 vs 90.6, QQP 90.6 vs 90.8, SST-2 96.4 vs 96.7) and comparable on the remaining two. The paper compares against the weaker EVA-initialized variant, which LoLoRA only marginally beats.
   - **MathQA (Table 3):** LoLoRA (82.9%) ties LoRA-FA (EVA) at 82.9% and is only 0.3% above LoRA-FA (uniform) at 82.6% — well within the ±0.5% error bars.
   - **LLaVA (Table 4):** LoLoRA (perplexity 2.93) sits between LoRA-FA (uniform) at 2.97 and LoRA-FA (EVA) at 2.92, while using *more* memory (24.1 GB) than LoRA-FA (23.9 GB) and taking longer (2h52m vs 2h46m).
   The conclusion's claim (line 332) that "HPCA consistently outperforms standard LoRA-FA in two out of three experimental setups" is contradicted by the data in the paper's own tables.

2. **The online HPCA updates provide no measurable benefit over a one-shot EVA initialization.** The theoretical analysis (Theorem 4.4) establishes that optimal A should span the PCA subspace — this equally supports EVA initialization (compute PCA once before training) as it does online HPCA updates. The ablations (Tables 5 vs 6) confirm this directly: LoRA-FA (EVA) at r=8 achieves 2.536 perplexity vs LoLoRA HPCA at 2.535 — statistically identical. The paper never demonstrates a scenario where iterative local updates outperform a single good initialization. The acknowledged non-stationarity limitation (line 334) further undermines the theoretical motivation for online updates over one-shot EVA.

3. **Memory savings are attributable to freezing A, not to the local update mechanism.** The advertised memory reduction ("up to 20% less GPU memory," "approximately 13% extra memory reduction") is shared with LoRA-FA, which achieves it without any local updates. In the LLaVA experiment (Table 4), LoLoRA actually uses *more* memory (24.1 GB) than LoRA-FA (23.9 GB). This weakens the practical motivation for the additional complexity of local optimizer steps.

### Minor

4. **Inconsistent comparison framing.** The paper claims "freezing A matrix during fine-tuning does not influence much the overall LoRA's performance" (lines 89–91), but the ablations show a consistent gap: Full LoRA achieves 2.521 perplexity vs 2.536 for the best LoRA-FA variant at r=8 — a gap of 0.015 that persists across all ranks. This gap should be acknowledged rather than dismissed.

5. **Compute cost of local updates is not adequately measured.** Algorithm 1 runs a local optimizer step per forward pass (lines 112–115), but wall-clock time is reported only for the LLaVA experiment (Table 4), where LoLoRA is slower than LoRA-FA (uniform) (2h52m vs 2h46m). All experiments should report runtime to quantify this overhead.

### Trivial
None.

## Nice-to-Haves

- Explore settings where the input distribution shifts significantly during training (longer fine-tuning, domain shift) to test whether online HPCA can ever provide an advantage over one-shot EVA initialization.
- Provide wall-clock time for all experiments, not just LLaVA.
- Reframe the paper around the theoretical result (optimal A = PCA subspace) and the empirical comparison of ways to achieve it, rather than presenting LoLoRA as an improvement over LoRA-FA. The data supports the theory and the ablation study, not the claim of superiority.

## Removed Points

The following points from the input review are removed per filtering rules:

- **"Memory measurements relegated to Appendix D cannot be verified from the main text"** — Removed because the appendix is stripped by the parser and exists in the original submission.
- **"'Best checkpoint' reporting inflates all numbers equally"** — Removed because this is common practice in the field and does not affect relative comparisons.
- **"LoRA (EVA) outperforms everything in Table 4 but is not discussed"** — Removed because this is an observation about an interesting data point, not a weakness of the paper.
- **"The ablation results are more informative than the main results"** — Removed as a subjective opinion rather than a verifiable weakness.

## Novel Insights

The harsh critic makes a compelling observation that the paper's own experimental data tells a different story from the one the authors tell. The ablations (Tables 5 vs 6) cleanly demonstrate that the online aspect of LoLoRA is unnecessary: one-shot EVA initialization achieves identical results. This suggests the paper's actual contribution is the theoretical result (Theorem 4.4) and the empirical validation that EVA initialization is optimal for the frozen-A setting — not the claim that local updates improve upon LoRA-FA. The paper's data therefore undercuts its own framing, and a reframed version centered on the theory and the initialization comparison would better reflect what was actually demonstrated.

## Suggestions

1. **Reframe the paper around the theoretical contribution (Theorem 4.4) and the empirical comparison of A-initialization strategies.** The data shows that EVA initialization and HPCA online updates achieve equivalent results. Acknowledge this directly and position LoLoRA as an alternative for cases where a separate PCA pre-pass is inconvenient, not as an improvement.

2. **Be transparent about which baseline comparisons support which claims.** The current framing creates the impression that LoLoRA improves upon LoRA-FA, but the data shows at best statistical parity. This discrepancy should be addressed explicitly.

3. **Add runtime measurements for all experiments.** The computational cost of the local optimizer step (Algorithm 1, lines 112–115) should be quantified across all settings, not just LLaVA.

## Score and Decision

**Round 1 — Bracketing.** I ran calibration searches across multiple score bands using LoRA fine-tuning, local learning rules, theoretical LoRA analysis, and related topics. The retrieved anchors show a clear pattern: pure theoretical contributions score 6.0–6.7 (e.g., "Expressive Power of LoRA" at 6.50, dEBORA at 6.67), while LoRA modifications whose empirical evidence does not match their claims cluster around 3.0–4.75 (HoLoRA at 3.00, ALLoRA at 3.33, LoRA Unleashed at 4.00, EVA at 4.75). **Initial bracket: 3–5.**

**Round 2 — Narrowing.** I examined the EVA paper (4.75) and "Activations Aren't Cheap" (4.25) in detail. LoLoRA has a stronger theoretical foundation than EVA (which reviewers criticized for lacking theoretical justification) but its central empirical claim is weaker than EVA's (which at least showed faster convergence). The LoLoRA paper therefore occupies a position between 3 (where papers have no redeeming evidence) and 5 (where papers have solid contributions despite limitations).

**Calibration anchors consulted:**

| Anchor Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| HoLoRA | 3.00 | R1 | Similar LoRA modification with unsupported performance claims; LoLoRA has more experiments and theory |
| ALLoRA | 3.33 | R1 | LoRA modification with theoretical limitations; comparable overclaiming issue |
| UnoLoRA / DLP-LoRA | 3.00 | R1 | Narrower-scope LoRA variants |
| LoRA Unleashed | 4.00 | R2 | LoRA extension with limited evidence; similar methodological ambition |
| Lottery Ticket Adaptation | 4.25 | R2 | Sparse adaptation with strong empirical results; different problem setting |
| Activations Aren't Cheap | 4.25 | R2 | LoRA memory analysis; clear contribution but narrow scope |
| EVA (One Init to Rule Them All) | 4.75 | R2 | Direct precursor; had faster convergence evidence but lacked theory; LoLoRA supplies the theory but lacks the empirical support |
| Expressive Power of LoRA | 6.50 | R1/R2 | Pure theoretical contribution with solid proofs; different paper type |
| dEBORA | 6.67 | R1/R2 | Novel optimization with theory and demonstrated improvements |

**Final score: 4.** This paper has genuine value — a correct theoretical result and a thorough ablation study — but the central claim of methodological improvement is not supported, and the experimental evidence consistently shows that the simpler baseline matches or exceeds the proposed method. A score of 4 (borderline reject) reflects that the paper has identifiable merit but that the framing is sufficiently misaligned with the evidence to prevent acceptance in its current form.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>