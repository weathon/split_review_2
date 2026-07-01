## Summary

This paper introduces FF-Erase, the first machine unlearning framework for Forward-Forward (FF) models — a biologically plausible alternative to backpropagation that trains via layer-wise greedy optimization. The method uses a "guidance model" (trained on remaining data and ignorant of forgetting data) to provide stable target goodness distributions, then minimizes KL-divergence of the original model's goodness toward those targets. The paper also proposes G-MIA, a membership inference attack using layer-wise goodness vectors for unlearning verification. Experiments on multiple architectures (VGG13, AlexNet, TinyCNN) with FF training algorithms show FF-Erase achieves comparable effectiveness to retraining from scratch while being 1.9–3.1× faster.

## Strengths

- **First to formalize and solve the FF unlearning problem.** The paper correctly identifies two unique challenges distinguishing FF unlearning from BP unlearning: (1) heightened sensitivity to parameter tuning due to the absence of backpropagation's consistent direction signal, and (2) layer-wise independent training complicating the effectiveness-utility trade-off. This problem formulation is novel and clearly articulated — a genuine gap in the literature.

- **Method design is principled and well-motivated.** The guidance model strategy directly follows from the problem diagnosis. By training a model on remaining data (ignorant of forgetting data) and minimizing KL-divergence toward its goodness distributions, the approach provides a natural regularizer against the instability that afflicts naive gradient ascent on FF models. The ablation in Table 1 (R.G.M. row showing collapse with a random guidance model) empirically validates this core design choice.

- **G-MIA exploits a genuinely FF-specific architectural property.** Using layer-wise goodness vectors (which FF models natively produce during inference) for membership inference is a principled idea. The comparison against final-layer MIA (FL) demonstrates that multi-layer goodness information provides strictly better membership signal, and under deeper/complex settings G-MIA matches white-box methods. This contributes a useful verification tool for the FF ecosystem.

- **Quantified efficiency with explicit breakdown.** The paper provides concrete speedup numbers (1.9–3.1×) and separates time into guidance model acquisition (t₀) and goodness decrease (t₁), making the efficiency claims verifiable rather than vague.

## Weaknesses

### Fatal
None.

### Major

- **Misleading framing of G-MIA as "black-box".** The paper repeatedly describes G-MIA as a "black-box attack" (abstract: "powerful and lightweight black-box attack"; §1 contributions: "Accurate Black-Box Unlearning Verification"; §2: "under a strict black-box constraint"). However, G-MIA requires access to "the goodness vectors from all layers" (line 200–201). The paper itself defines black-box MIAs as those that "only use the model's final prediction output" (§2). Accessing per-layer activations is strictly more information than standard black-box access. The comparison with final-layer MIA (FL) in Figure 3 is consequently imbalanced: G-MIA receives richer per-layer information while FL only sees the final output. The contribution remains valid — G-MIA is more practical than white-box attacks (no parameters/gradients needed) and more accurate than final-output-only attacks — but the "black-box" label is inaccurate. This should be corrected to "intermediate-layer" or "grey-box" access throughout.

- **No variance or statistical significance reported.** All results (Figure 3, Figure 4, Table 1) are single numbers with no confidence intervals, standard deviations, or replication across random seeds. The random 20% split of training data as 𝔻_forget (line 240) is inherently stochastic. Some reported differences are very small — e.g., G-MIA ACC of RE (0.551) vs. D-(0.5,0.5) (0.556) in Table 1, or FF-Erase(D) G-MIA ACC (0.5245) vs. RE (0.532) in Figure 4(c). Without variance estimates, it is impossible to know whether these differences are meaningful or within noise. This is a significant evidential gap for a paper making quantitative claims about efficiency-effectiveness trade-offs.

### Minor

- **Limited active baselines for unlearning.** The unlearning comparison includes only one active baseline (gradient ascent, GA) plus retraining from scratch (RE). The paper argues that exact unlearning methods (SISA, influence functions) are incompatible with FF models. While this is a reasonable claim for a first paper, attempting even one adapted baseline — e.g., per-layer GA with learning rate scaling to handle the layer-wise independence issue — would strengthen the argument that the guidance model is essential, rather than FF-Erase being compared against a single strawman. (Note: the paper does evaluate GA across 6 λ values in §6.3, showing it either collapses or fails to unlearn, which is a thorough evaluation of that baseline.)

- **G-MIA sensitivity to synthetic data quality is not evaluated.** The attack assumes the attacker "can synthesize data that has a similar distribution to the training data" via model inversion (line 200). Model inversion is itself difficult for complex datasets like CIFAR-100. The paper does not evaluate how G-MIA's accuracy degrades with lower-quality synthetic data, which limits understanding of its practical robustness as a verification tool.

### Trivial

- **Minor pseudocode ambiguity in FFwd (Algorithm 1).** The FFwd function initializes z⁰ = x (input to the original model), but zₒ⁰ (the guidance model's input) is not explicitly initialized. On the first iteration (l=1), line 147 uses zₒ^{l-1}=zₒ⁰, which should also be x. This small omission should be clarified.

## Nice-to-Haves

- The efficiency analysis in Equation (9) assumes linear scaling of time with data quantity and epoch count. While reasonable as a rough estimate, the paper could acknowledge that I/O overhead and batch-size effects may cause deviations in practice.
- Testing boundary conditions — e.g., what happens when 𝔻_forget is a very large fraction of the training set (≥50%), or when forgetting and remaining data have very different distributions — would strengthen the paper's characterization of when FF-Erase works.
- The pseudo-code in Algorithm 1 uses variable names "ℓ₁" and "ℓ₂" for what appear to be loss values but then applies them as gradient updates (line 150: θₒˡ = θₒˡ − η ℓ₁[l]). This is a notational inconsistency — ℓ₁[l] is defined as ∇ D_KL(...) which is a gradient, not a loss. Clarifying this would improve reproducibility.

## Removed Points

These points were considered during review but removed or downgraded after verification against the paper:

- **"Main results for a single dataset/model combination"** — REMOVED. The paper explicitly states other results are in Appendix §C (line 242). The appendix is stripped by the PDF parser, not missing from the original submission. The paper evaluates on 4 datasets (CIFAR-10, CIFAR-100, MNIST, Fashion-MNIST) and multiple architectures. Showing one representative setting in the main text is standard practice.
- **Criticism of the efficiency analysis "conflates data quantities with time"** — DEMOTED to Nice-to-Have. The paper presents Equation (9) as an approximation ("≈"), which is appropriate for a first-order estimate.
- **Reproducibility nitpicks about undisclosed hyperparameters** — REMOVED. The paper provides sufficient detail (learning rate η, recovery step K, thresholds ε₁/ε₂, etc.) for a competent practitioner to reproduce.
- **"The GA method is a strawman"** — DEMOTED to Minor. The paper evaluates GA across 6 different λ values in §6.3, showing the method either collapses or fails to unlearn. More baselines would strengthen the paper but the GA analysis is not a strawman.

## Novel Insights

The most valuable insight from the review is that the G-MIA "black-box" framing creates an unnecessarily adversarial reading of an otherwise solid contribution. The paper's own definition of black-box (§2) is "only the model's final prediction output" — yet G-MIA requires per-layer goodness vectors. This is a self-contradiction that invites justified skepticism. However, the method itself is genuinely useful: for FF models, layer-wise goodness scores ARE the natural inference-time output (unlike hidden activations in BP models, which require modifying the model to extract). When described honestly — as an "intermediate-layer attack that is more practical than white-box (no parameters/gradients) while more accurate than black-box" — the contribution stands without overclaiming. The fix is terminological, not substantive.

## Suggestions

1. **Reframe G-MIA's access level.** Stop calling it "black-box." Describe it as an "intermediate-layer" or "grey-box" attack, noting that for FF models, per-layer goodness vectors are the natural output of inference (unlike BP hidden activations). This honestly communicates what the attacker needs without inflating the claim.
2. **Add variance reporting.** Report results over at least 3–5 random seeds with standard deviations for key metrics — G-MIA ACC, accuracy on 𝔻_forget and 𝔻_test, and wall-clock time. Without this, the fine-grained comparisons in Table 1 are uninterpretable.
3. **Add at least one adapted baseline.** Even a simple adaptation — per-layer GA with separate learning rates — would strengthen the case that the guidance model is necessary rather than merely convenient.
4. **Evaluate G-MIA's sensitivity to synthetic data quality.** Show how accuracy varies with the amount or fidelity of synthetic data used for shadow model training.
5. **Fix pseudocode ambiguity.** Explicitly initialize zₒ⁰ = x in the FFwd function, and rename ℓ₁/ℓ₂ to avoid confusion between gradients and loss values.

---

**Calibration anchors used:**

| Path | Avg Score | Decision | Comparison |
|------|-----------|----------|------------|
| `Xagys9QD3T.md` (Pseudo-Probability Unlearning) | 3.00 | Reject | Flawed optimization objective; our paper is much stronger |
| `p7mgNvOD9Q.md` (SUN) | 4.00 | Reject | Missing related work, limited applicability |
| `TLBPjECC5D.md` (Unlearning via Sparse Representations) | 5.25 | Reject | Incremental novelty, limited baselines, unreported times |
| `pUOesbrlw4.md` (Deep Unlearning) | 5.25 | Reject | Similar level but our paper has more novel problem |
| `OHOmpkGiYK.md` (Decoupling the Class Label) | 5.75 | Reject | More thorough experiments, comparable contribution |
| `pFjzF7dIgg.md` (UnCLe) | 5.75 | Reject | Similar novelty but more baselines |
| `Q1MHvGmhyT.md` (A Closer Look at MUL for LLMs) | 6.00 | Accept | More thorough analysis |
| `UstOpZCESc.md` (Privacy-Aware Lifelong Learning) | 6.25 | Accept | Comparable novelty, stronger experiments |

**Round 1 bracket:** 4.5–6.5. **Narrowing:** Paper sits above SUN (4.00) and Sparse Representations (5.25) due to genuine novelty and sound method design, but below PALL (6.25) and the LLM unlearning paper (6.00) due to the G-MIA framing issue and absence of variance reporting. Closest comparator in contribution/quality is Decoupling the Class Label (5.75) or UnCLe (5.75), but those had more thorough empirical work.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>