Now I have all the calibration data I need. Let me finalize the review.

**Bracket from Round 1:** 5.5 – 7.0. The paper sits above the "Time Transfer" anchor (5.25, rejected for overclaiming from sparse data) because its central τ experiment is clean and well-supported, but below the u-µP anchor (7.33, accepted for technical depth) because of several framing and completeness issues. The most directly comparable anchor is the Multi-Power Law paper (6.00, accepted), which has similar strengths (loss-curve prediction) and similar weaknesses (limited theoretical justification, missing baselines).

Here is the final consolidated review.

---

## Summary

This paper extends the training-loss-curve (TLC) collapse phenomenon from small-scale µP-trained models (vanilla Adam, no weight decay) to full-scale LLMs (100M–3.9B) trained with AdamW under practical scaling recipes. It identifies the normalized AdamW timescale τ = B/(ηλD) as the key shape-controlling parameter; shows that fixing TPP and τ (along with the LR schedule) makes normalized TLCs approximately scale-invariant; introduces the Celerity model family trained with deliberate collapse; and demonstrates two applications — using collapse residuals to detect training pathologies earlier than raw-loss monitoring, and fitting a small-scale surrogate to enable early stopping in hyperparameter tuning.

---

## Strengths

1. **Clean identification of τ as the TLC-shaping control (Fig. 3, Sec. 3).** The cross-sweep experiment independently varies η, λ, or B while keeping τ matched; normalized TLCs become nearly identical in each case. This is a non-obvious finding that meaningfully extends Qiu et al. (2025) from the vanilla-Adam regime to AdamW as used in practice.

2. **Compelling practical diagnostic case study (Fig. 1 right, Fig. 6 right).** In the 1.8B run, collapse residuals detected divergence at ~60% of training, while raw loss showed a visible spike only after 90%. The paper follows through by using the collapse reference to isolate the issue to a loss kernel at specific microbatch sizes, demonstrating genuine practical utility.

3. **Celerity model family lands near the compute-efficiency frontier (Fig. 2).** Among publicly documented open models, Celerity (300M–3.9B) achieves competitive accuracy for its training compute. The concrete datapoint against BTLm (75% fewer FLOPs for comparable accuracy) is informative.

4. **Directly addresses an explicit gap in prior work.** Qiu et al. (2025) called for tests at larger scales with practical scaling ladders (co-scaling width, depth, batch size, weight decay). The paper answers this call, which is a responsible and useful extension.

---

## Weaknesses

### Fatal
None.

### Major

1. **No quantitative collapse metric.** The paper's central phenomenon — collapse — is evaluated entirely by visual inspection. No numeric definition (e.g., maximum RMS deviation between normalized curves in a TPP band, compared to inter-run variation as in Qiu et al. 2025) is defined or reported. The paper acknowledges deviations at 20 TPP (warmup artifacts) and 234 TPP (late divergences for larger models, Fig. 6, line 202) but does not quantify their magnitude or specify conditions under which collapse deteriorates. The abstract's claim that curves "collapse across scales precisely" is not backed by a precision measure.

2. **Tension between "collapse as a signature of compute-efficient training" and Celerity's primary TPP=234 band.** The abstract and introduction frame collapse as "a signature of compute-efficient training." Yet Celerity's main band is TPP=234, which is ~11.7× above the compute-optimal ~20 TPP and requires 67% more FLOPs (acknowledged at line 145). The parameter-efficiency justification is reasonable on its own terms, but the contradiction between the claimed compute-efficiency signature and the deliberately compute-inefficient main demonstration band is unresolved and could mislead readers.

### Minor

1. **Normalization by division by L(T) is less principled than prior work and the diagnostic error is unquantified.** The paper uses "divide by final training loss" (line 101) rather than Qiu et al.'s affine rescaling with an irreducible-loss offset, justified only by an empirical statement that it "resulted in optimal alignment." The theoretical justification (line 131: the curvature factor h cancels after normalization) depends on an unverified assumption that residual bias at end-of-training is negligible. The diagnostic application requires estimating the unknown L(T) during training (via early-align or power-law extrapolation, lines 193–194), but the paper never quantifies how estimation error propagates into collapse residuals.

2. **Theoretical noisy-quadratic model (Eq. 3) is derived for constant LR, while all experiments use linear decay-to-zero schedules.** The connection is a verbal sketch ("η_t λ decreases and the instantaneous timescale τ_t increases," line 129) rather than a derivation or integrated treatment. This does not invalidate the empirical results — the τ intuition is robust — but it weakens the claimed theoretical grounding of the paper's framework.

3. **Early stopping evaluation lacks comparison against standard HPO baselines.** The paper compares only against "random" and "current best." Established multi-fidelity methods (ASHA, Successive Halving, Bayesian optimization with learning-curve extrapolation) are cited in related work but never compared against. While the paper's procedure is a demonstration of collapse as an enabler, not a standalone HPO contribution, the absence of any comparison makes the practical significance of the early stopping results unclear.

4. **CompleteP is referenced (line 164) but not defined.** The paper states that "Using CompleteP... was more efficient/reliable than µP (Fig. 15)" but never explains what CompleteP is. Since the theoretical framing (Sec. 2) builds on µP properties, it is unclear whether the collapse results depend on µP or generalize to any parameterization.

### Trivial
None.

---

## Nice-to-Haves

- Report a quantitative collapse metric (e.g., max/mean deviation between normalized curves within each TPP band, compared to inter-run noise) and report it for 20, 80, and 234 TPP.
- Validate the "divide by L(T)" normalization against Qiu et al.'s affine alternative (with irreducible-loss offset) to show collapse is not an artifact of the specific normalization.
- Include at least one standard multi-fidelity HPO baseline (e.g., ASHA) in the early stopping experiments.
- Briefly define CompleteP or clarify its relationship to µP in the main text.

---

## Removed Points

- **"Collapse is substantially weaker than Qiu et al.'s supercollapse"** — removed. The paper's scale (100M–3.9B, practical AdamW) is different from Qiu et al.'s (small models, vanilla Adam, no weight decay). The paper acknowledges deviations and explains them. The lack of a *quantitative metric* (captured in Major weakness 1) is the precise concern; the qualitative claim that collapse is imperfect is already in the paper.
- **"Llama-2 comparison is potentially misleading"** — removed. The Llama-2 comparison is used to show that varying TPP and τ prevents collapse, which is a fair demonstration of the importance of fixing these controls. The paper does not claim Llama-2 training was suboptimal.
- **"Missing error bars/confidence intervals"** — removed. The MAE results for the surrogate model are in the appendix (Table 11–12, stripped by parser). Given the scale of the experiments, lack of error bars on every measurement is within normal practice for this type of empirical work.
- **"Well-motivated gap"** (generic strength) — removed as superficial.

---

## Novel Insights

None beyond the paper's own contributions. The reviewer's observation about the tension between the compute-efficiency framing and the TPP=234 band is a genuine insight that the paper itself does not address.

---

## Suggestions

1. Define a quantitative collapse metric and report it for all three TPP bands. This would both strengthen the central claim and make the diagnostic application more principled (e.g., principled thresholds on collapse residuals).
2. Either reconcile the compute-efficiency signature claim with the deliberately compute-inefficient TPP=234 band, or carefully rephrase the claim to avoid implying that collapse signals proximity to the Chinchilla-optimal TPP.
3. Add at least one standard HPO baseline (ASHA is the obvious choice) to the early stopping evaluation.
4. Validate the "divide by L(T)" normalization against an affine alternative or quantify the sensitivity to the end-of-training bias assumption.
5. Briefly define CompleteP in the main text so readers can assess the generality of the collapse results across parameterizations.

---

## Score and Decision

**Calibration Anchors (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| o9YC0B6P2m (Scaling Law w/ LR Annealing) | 6.75 | 1 | Yes | More mathematically ambitious but had a fatal flaw (zero-LR non-invariance). Our paper has fewer mathematical flaws but more framing issues. Slightly below. |
| KnoS9XxIlK (Multi-Power Law) | 6.00 | 1 | Yes | Most similar: both predict TLC shapes. That paper had stronger mathematical framing but weaker practical validation. Comparable in overall merit. |
| WYL4eFLcxG (Scaling Optimal LR) | 6.00 | 1 | Yes | About LR scaling. Similar level of empirical contribution with comparable weaknesses (arbitrary functional forms, missing controls). |
| d8w0pmvXbZ (Small-scale proxies) | 8.00 | 1 | Yes | High-scoring anchor for thorough empirical work on a focused question. Our paper is broader but less rigorous in execution. |
| xGM5shdGJD (Hitchhiker's Guide) | 5.20 | 1 | Yes | About fitting scaling laws; criticized for lack of novelty. Our paper has more novel findings. |
| 79ZkWgY2FI (Small-to-Large Generalization) | 5.25 | 1 | Yes | About small-model proxies for large models. Our paper has stronger empirical evidence for its core claim. |
| P7KRIiLM8T (u-µP) | 7.33 | 2 | Yes | Technically deep parameterization paper. Our paper has a broader scope but less technical depth. |
| MLhquJb1qN (Time Transfer) | 5.25 | 2 | Yes | Overclaimed scaling laws from sparse data (rejected). Our paper's empirical evidence is more thorough. |

**Bracket (Round 1):** 5.5 – 7.0.

**Final score placed at 6.0** because: (a) compared to the Multi-Power Law anchor (6.00, accepted), our paper has similar overall merit — a real empirical contribution with a useful practical angle, but held back by incomplete quantification of its central claim and missing baselines for one of its claimed applications; (b) below the Scaling Law with LR Annealing anchor (6.75) because that paper had a more rigorous mathematical formulation even though it had a fatal flaw, whereas ours has several distinct weaknesses that individually are minor but collectively weigh on the core thesis; (c) well above the Time Transfer anchor (5.25, rejected) because our central experiment (τ cross-sweep) is clean and the diagnostic case study provides genuine evidence of practical utility.

This is a borderline accept. The paper makes a solid empirical contribution with practical value, but the overclaiming in the abstract and the lack of a quantitative collapse metric should be substantively addressed before final publication.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>