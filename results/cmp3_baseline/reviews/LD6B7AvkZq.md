## Summary

This paper studies how language models (LMs) learn context-free grammars (CFGs) by introducing the notion of *subgrammars* (inner and outer).  
It presents theoretical results claiming that the KL divergence (or loss) obeys a recurrence over subgrammar structure, and supports this with empirical experiments on small transformers.  
Additional experiments examine whether pretraining on a subgrammar improves performance and alignment, and whether models generalize to deep recursive structures.

## Strengths

- The idea of analyzing learning dynamics through the substructure of CFGs (subgrammars) is a reasonable conceptual direction.
- The paper attempts to connect formal language theory (PCFGs) with practical training phenomena (curriculum, representation alignment).
- The use of CKA for representational analysis is a sensible tool for probing the effect of pretraining.

## Weaknesses

### Fatal

1. **The theoretical core is not mathematically sound.** The derivation in equations (1)–(4) contains clear algebraic errors—e.g., placing logarithms in denominators, unclear handling of conditional probabilities, and non-credible manipulations of KL divergence.  Definitions such as \(D_{\text{KL}}(P_G \parallel Q)_A\) are imprecise and do not connect cleanly to standard KL divergence.  Theorems 4.2–4.6 are stated without rigorous proof; the proof sketches in the main text are insufficient to establish the claimed recurrences.  Because the paper’s central contribution is this theoretical framework, the lack of rigor renders the main claims unsubstantiated.

2. **The empirical experiments lack the detail needed to judge reproducibility or validity.**  Grammar definitions, model architectures, training hyperparameters, and evaluation protocols are either missing or only vaguely referenced (relegated to a removed appendix).  As presented, the figures and tables cannot be interpreted as solid evidence for the claimed phenomena.

### Major

1. The claim that models “learn all subgrammars in parallel” is not properly evaluated.  The observation that subgrammar KL divergences decrease together during training is an expected consequence of joint optimization on a mixture; it does not demonstrate a non-trivial property.  No comparison is made to any alternative (e.g., sequential curriculum) that would justify the claim of “parallelism.”  Corollary 4.7 essentially assumes the conclusion.

2. The alignment analysis (CKA) reports small percentage changes (e.g., +8.9%) without confidence intervals or statistical significance tests.  It is unclear whether these differences are meaningful or simply noise.  The paper’s language (“definitively”) overstates the strength of the evidence.

3. The depth‑generalization experiment (Section 6) confirms a well‑known limitation of transformers on recursive structures (documented in several of the paper’s own cited works).  The anecdotal GPT-5.1 test adds no rigorous evidence.  This section does not advance understanding beyond prior work.

### Minor

- The notation in the theoretical section is sometimes inconsistent (e.g., using \(P_G(a)\) without defining the marginal over contexts).
- The paper claims to “initiate the study” of learning dynamics with respect to subgrammar structure, but prior work (Cagnetta & Wyart, 2024; Allen-Zhu & Li, 2023) already studies CFG learning dynamics and hierarchy—the novelty is overstated.

## Nice-to-Haves

- A formal, correct derivation of the KL decomposition under explicitly stated assumptions would be essential to salvage the theoretical contribution.
- Detailed experimental specifications (grammars, model sizes, learning rates, dataset sizes) should be provided to allow reproducibility.
- Statistical significance tests and confidence intervals should be reported for all quantitative claims (CKA, loss differences).

## Novel Insights

None beyond the paper’s own contributions—the attempted theoretical decomposition is not reliably established, and the empirical findings largely echo known results.

## Suggestions

- Either provide rigorous, correct proofs of the decomposition theorems (with clear assumptions and fully worked derivations) or substantially reframe the paper as a purely empirical study.
- Document all experimental details (including grammar rules, model hyperparameters, training seeds) to meet the reproducibility standards expected at ICLR.
- When claiming parallel learning, compare explicitly to a sequential training baseline (e.g., train on one subgrammar at a time or use a curriculum).
- Report error bars / confidence intervals for all averaged results (CKA, KL values, losses).

## Score and Decision

The theoretical contribution is flawed and the empirical support is too thin to compensate.  The paper does not meet the bar for acceptance.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>