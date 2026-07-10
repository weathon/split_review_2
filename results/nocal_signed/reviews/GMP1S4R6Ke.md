Now let me produce the final consolidated review.

## Summary

This paper introduces LoRA-Mixer, a framework that applies Mixture-of-Experts-style routing over LoRA adapters attached to the attention projection layers (Q, K, V) of LLMs, rather than to FFN blocks as in prior work. The paper also proposes Routing Specialization Loss (RSL), which adds an entropy regularization term to the standard load-balancing auxiliary loss to encourage input-aware expert selection. Experiments on 15 benchmarks across Transformers (LLaMA3, Mistral) and SSMs (Falcon-Mamba) show consistent improvement over existing LoRA-MoE methods, with a practically compelling plug-and-play demonstration using frozen, internet-sourced LoRAs (Section 4.3).

## Strengths

- **Well-motivated architectural design.** Applying MoE-style LoRA routing to attention projection layers rather than FFN blocks is a clear design choice supported by a useful taxonomy (Figure 1). The argument that projection layers are expressive and ubiquitous across both Transformers and SSMs is coherent and distinguishes LoRA-Mixer from existing methods (MixLoRA, MoLE).

- **Plug-and-play regime for frozen LoRAs is practically compelling.** Section 4.3 (Table 3) demonstrates that LoRA-Mixer can route over pre-trained, frozen LoRAs downloaded from public repositories (LoRAHub) using only 2K additional mixed data for router training. This directly addresses the stated motivation of enabling reuse of off-the-shelf LoRA modules and is the most practically valuable experiment in the paper.

- **RSL is a cleanly motivated modification.** Adding an entropy regularization term to the standard load-balancing loss (Eq. 5) is simple but principled. The gradient analysis (Eqs. 7-9) correctly illustrates why the standard auxiliary loss suppresses token-level variance and how the entropy term counteracts this, providing a clear mechanism for encouraging input-aware routing.

## Weaknesses

### Major

- **Cross-model transfer experiment contains a factual error and the evidence is thin.** The paper states (line 194) "Mistral-7B and LLaMA3-8B have the same architecture" — this is incorrect. They differ in vocabulary size (32K vs 128K), intermediate dimensions, and tokenizers. The experimental results (Table 5) are also mixed: transferring the Mistral-trained router to LLaMA3 yields marginal gains on GSM8K (59.13 vs 57.92, 0-shot) and ARC-C (79.14 vs 78.65), but degrades ARC-E (85.89 vs 88.45 baseline). The paper's claim that this "validates the design motivation" and demonstrates "extremely robust and transferable" routing is not supported by the evidence as presented.

- **No measures of uncertainty despite small improvements.** The paper states (line 136) that experiments are run three times with averages reported, but no standard deviations, confidence intervals, or any variance estimates are provided for any result. This is critical because many reported improvements over the best baseline are very small (e.g., Δ=0.11 on SST2, Δ=0.39 on GSM8K, Δ=0.72 on CoLA for LLaMA3-8B in Table 2). Without variance estimates, the reader cannot determine whether these differences are meaningful or within random fluctuation. Given that the central claim is that LoRA-Mixer "outperforms" baselines, this omission directly affects whether the empirical claims can be trusted.

### Minor

- **A headline quantitative claim lacks main-text support.** The abstract and introduction prominently state that LoRA-Mixer uses "only 48% of the trainable parameters of existing methods," but no table, calculation, or parameter comparison appears in the main text. The only reference is "For parameter, training and inference analysis, please refer to A.4 A.7" (line 134). A central numerical claim of this kind should be verifiable in the main body.

- **The RSL data efficiency advantage (Table 9) is modest and inconsistent.** The improvement over the w/o RSL baseline peaks at +1.97 (2K data), reverses at 4K (−0.37), and converges to near-zero at larger data sizes (+0.04 at 6K, +0.27 at 8K, +0.43 at 10K). The paper's claim that RSL achieves "comparable or even superior performance using only 51.62% of the training data with auxiliary loss" overstates what the data shows, especially without error bars to assess significance.

- **The abstract's percentage gains do not clearly correspond to any visible comparison.** The abstract reports gains of +3.79%, +2.90%, and +3.95% on GSM8K, CoLA, and ARC-C, but in Table 2 (LLaMA3-8B), the raw absolute gaps are +0.39, +0.72, and +0.34 over the best baseline — far smaller. The abstract does not anchor these percentages to a specific baseline or experimental condition, creating ambiguity about what is being compared.

- **The "LoRA" baseline in Tables 2-4 is not defined in the experimental setup (Section 4.1).** It appears to be standard single-task LoRA fine-tuning, but this is never clarified. Its strong performance relative to MoE baselines (e.g., LoRA at 81.09 vs MixLoRA at 79.87 on Medical with LLaMA3-8B) makes the comparison tables harder to interpret without knowing exactly what this baseline represents.

- **Several experimental configuration details are underspecified in the main text:** (1) the number of experts E used in the main experiments is not stated (Figure 3 uses 6 experts, Figure 4 uses 5); (2) it is not specified whether experts are applied to all of Q, K, V, and O projections or a subset; (3) the internal architecture of the router (linear, MLP, input features) is not described beyond α(x) ∈ ℝᴱ.

### Trivial

None.

## Nice-to-Haves

- A direct ablation comparing projection-layer vs. FFN-layer expert placement would directly validate the paper's core architectural claim, which is currently motivated but never tested.
- Report standard deviations or confidence intervals on the main comparison tables.

## Removed Points

These points from the input review are removed with justification:

- **Cross-model transfer as a standalone strength**: Removed because the strength (testing an interesting property) conflicts with the verified weakness that the experiment contains a factual error and thin evidence. The idea is interesting but the execution undermines it as a positive signal.
- **Criticism about missing appendix proofs**: The analysis of the 48% parameter claim was retained as a structural weakness (support should be in the main text), not because the appendix is missing. Purely appendix-related criticism was removed per the filtering rules.
- **Section-by-Section notes about Section 2 and Section 4 cleanroom comparison**: These were commentary/observations rather than concrete weaknesses requiring action.
- **"Strengthening the Paper on Its Own Terms" recommendations**: Moved to Suggestions.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Directly compare projection-layer vs. FFN-layer placement** in a controlled ablation — the paper motivates this distinction heavily but never tests it experimentally.
2. **Report standard deviations or confidence intervals** on the main comparison tables (Table 2) so readers can assess whether the small reported improvements are statistically meaningful.
3. **Report complete parameter counts** for all compared methods in the main text to substantiate the 48% efficiency claim.
4. **Clarify what "LoRA" means** in Tables 2-4 and discuss why it sometimes closely matches or exceeds MoE baselines.
5. **Correct the factual claim about architecture identity** (Mistral-7B and LLaMA3-8B), and either adapt the router for cross-model transfer or soften the claims made from this experiment.

---

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>