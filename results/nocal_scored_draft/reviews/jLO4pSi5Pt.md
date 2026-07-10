## Summary

This paper introduces L-TTA, the first method for Test-Time Adaptation (TTA) of Vision-Language Models under long-tailed test distributions. It contains three co-designed components: Synergistic Prototypes (SyPs) that maintain two complementary prototype banks to enrich tail-class representations, Rebalancing Shortcuts (RSs) that use learnable hyper-class vectors with a class-reallocation loss, and Balanced Entropy Minimization (BEM) that adds a penalty term to standard entropy minimization to suppress head-class overconfidence. Experiments across 15 datasets, three imbalance ratios, and multiple backbones show consistent improvements in macro-F1 over existing TTA methods.

## Strengths

- **Novel problem framing and well-motivated failure-mode analysis.** The paper is the first to systematically study TTA for VLMs under long-tailed test distributions, identifying two specific failure modes (Text-induced Tail Erosion and Modality-bias Amplification) grounded in concrete observations (Figure 1(b)). This framing is timely and relevant.

- **Unusually broad experimental evaluation.** Results span 15 datasets across three benchmarks (OOD, Cross-Domain, Corruption), three imbalance ratios (10, 20, 50), 5 runs per configuration, and four backbone sizes. The macro-F1 improvements are consistent and grow as imbalance worsens (e.g., +7.33 macro-F1 over DPE on ImageNet-A at imb=50 in Table 1, +2.20% average macro-F1 on Cross-Domain in Table 2, +2.64% on Corruption in Table 3), directly supporting the paper's thesis.

- **Strong computational efficiency.** L-TTA runs in 1.45h on a single A100, dramatically faster than several strong baselines (e.g., 27.7h for WATT, 18.3h for RLCF, 6.42h for CLIPaTT) while outperforming them (Table 4). This is a meaningful practical advantage.

## Weaknesses

### Fatal
None.

### Major

- **Missing critical baseline comparison: standard LT losses applied to TTA methods.** The paper claims (line 134) that naively applying logit adjustment (Menon et al., 2020) or balanced softmax (Ren et al., 2020) to the TTA setting "may further exacerbate the model's bias toward the head classes and damage the decision boundaries," but this claim is never tested experimentally. The paper compares only against TTA methods not designed for long-tailed data, but never against e.g. TDA or DPE with their EM loss replaced by a class-rebalancing variant. Without this comparison, the claim that BEM is a "tailored optimization objective for LT-TTA" that is superior to simpler alternative losses is unsupported. (The paper references Appx. G for "further comparisons"; whether it contains this exact baseline is not verifiable from the main text.) This is the single most informative missing experiment for evaluating whether the three-component design is necessary.

### Minor

- **Circular dependency in BEM's class prior estimation.** The BEM loss (Eq. 9) uses class priors π that are "continually updated based on the current predicted pseudo-labels" (line 138). This creates a feedback loop: the model's predictions are biased toward head classes (the very problem BEM aims to fix), yet those predictions are used to estimate the prior that corrects the bias. The paper does not analyze this circularity, compare against an oracle prior (the subsampling ratios are known by construction), or test sensitivity to prior estimation error.

- **The theoretical propositions add limited weight.** Propositions 1 and 2 (lines 132-143) formalize the expected gradient behavior of EM and BEM under long-tailed distributions, but do not constitute non-obvious theoretical insights. Proposition 1 restates that EM pushes head-class gradients negative and tail-class gradients positive — a property that follows from the definition of EM under imbalance. Proposition 2 asserts BEM reduces the gradient gap — which is what BEM is designed to do. Neither proposition connects to the SyPs or RSs architecture, nor provides convergence guarantees. Downgrading these from formal propositions to intuitive motivation would better reflect their role.

- **No variance or confidence intervals despite 5 runs.** Tables 1–3 report 5-run averages without standard deviations. Some gains are modest (e.g., at imb=10 on ImageNet-A, L-TTA's 61.78% vs. DPE's 60.31% vs. SCAP's 60.54%), and in Table 6 the isolated BEM gain is only 0.36% accuracy / 0.66% macro-F1. Without variance, the statistical significance of these margins is unclear.

- **Ambiguity in the hyper-class vector count K.** The implementation states K=0.3 (line 208) and the ablation varies K from 0.1 to 1.0 (Figure 4c). These appear to be fractions of the number of classes rather than absolute counts, but this is never explicitly stated, leaving ambiguity about how K maps to actual vectors across datasets with different class counts.

- **Unclear loss choice in ablation rows.** In Table 6, it is ambiguous whether the "SyP+RS" row uses standard EM as its optimization loss or no loss at all. Clarifying the loss used in each ablation row would strengthen the interpretation, especially since the BEM-only gain (+0.36% Acc, +0.66% Mac) is modest.

### Trivial
None.

## Nice-to-Haves

- It would strengthen the paper to test whether BEM can be plugged into other TTA methods (e.g., TDA) and improve their long-tailed performance, demonstrating that BEM is a general-purpose advancement rather than a component tuned specifically to work with SyPs and RSs.
- The EP update mechanism (Eq. 5) would benefit from a concrete example or T-SNE visualization showing what the exclusionary prototypes actually capture versus the deterministic prototypes.

## Removed Points
- Weakness about the code link being empty. Removed per instructions: criticisms questioning the status of cited artifacts are not permitted.
- Weakness about missing transferability experiments (BEM pluggability). Moved to Nice-to-Haves.
- Weakness about EPs: the critic claimed a tension between the EP description and update rule. On re-examination (Eq. 5), non-predicted classes (φ≈1) receive higher relative update weight, meaning features from a dog sample contribute *more* to the cat EP update — which aligns with storing "improbable features." The critic's interpretation was incorrect.
- Various section-by-section observation notes that are not actionable weaknesses (early-stream DP initialization, CRA connection to LT-TTA, dataset construction details).

## Novel Insights
None beyond the paper's own contributions.

## Suggestions

1. **Add the missing LT-vs-TTA baseline experiment**: apply logit adjustment or balanced softmax to the top-performing open-source TTA method (e.g., TDA or DPE) and compare against L-TTA. This single experiment would substantially strengthen (or honestly bound) the claim that BEM's specific design is necessary.
2. **Report standard deviations** for the 5-run experiments in the main tables.
3. **Address the circular prior concern** by either (a) using a fixed prior from the known subsampling ratios (which the authors control), or (b) comparing estimated vs. oracle priors to bound the damage from biased estimation.
4. **Clarify that K is a fraction** of the number of classes and state how it maps to absolute vector counts per dataset.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>