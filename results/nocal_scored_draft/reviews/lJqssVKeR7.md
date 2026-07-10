Based on the scoring model's favorabilities, the paper's strengths are all very strong (0.93–1.00) and the weaknesses are all minor (favorabilities 0.26–0.60, none approaching the near-zero that would indicate a fatal flaw). No weakness undermines the core empirical contribution. This is a solid paper with fixable issues.

---

## Summary

This paper proposes **HiSo**, a Hessian-informed zeroth-order (ZO) federated optimization method that accelerates convergence while preserving scalar-only (dimension-free) communication. The core technical contributions are: (1) a generalized scalar-only communication FL framework (Section 3.3/Algorithm 1) that decouples the dimension-free property from vanilla ZO-SGD; (2) the HiSo algorithm, which uses a running diagonal Hessian approximation built from squared ZO updates to precondition the search direction without transmitting any Hessian information; (3) a convergence analysis that generalizes the prior DeComFL framework and extends to τ>1 local updates; and (4) consistent empirical acceleration (1.4–5.4× speedup in communication rounds) on LLM fine-tuning across SST-2, QQP, and SQuAD.

## Strengths

- **Well-motivated problem.** The paper clearly articulates the tension between ZO methods' dimension-free communication advantage and their slow convergence due to ignoring curvature, and the risk that transmitting second-order information would reintroduce dimension-dependent costs. This research question (line 21) is directly and successfully addressed.

- **Generalized scalar-only communication framework (Section 3.3, Algorithm 1).** The observation that the key enabler of dimension-free communication is scalar representation, not ZO-SGD specifically, is a genuine insight. Algorithm 1 formalizes this decoupling, making it a reusable contribution that future work could plug other optimizers into.

- **Theoretical analysis that generalizes DeComFL.** Theorem 1 provides convergence bounds in the H⁻¹-norm. Corollaries 1–3 recover DeComFL as a special case (H=I) and extend to τ>1 local updates — something DeComFL's original analysis did not support. The whitening rank ζ provides a technically non-trivial extension of the low-effective-rank analysis from prior ZO work.

- **Consistent empirical improvement over DeComFL.** Across 3 tasks (SST-2, QQP, SQuAD) and 3 model sizes (OPT-350M, 1.3B, 2.7B), HiSo consistently achieves 1.4–5.4× speedup in communication rounds and higher final accuracy than DeComFL (Tables 2, 3), all while preserving scalar-only communication. The TB→KB communication savings over first-order methods are dramatic.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **"Hessian-informed" framing is slightly overstated.** The Hessian approximation H in Eq. (12) is a running average of squared preconditioned ZO updates — conceptually similar to RMSProp, as the paper's own footnote 2 acknowledges. The derivation (Eqs. 5–10) does show the expected update is Newton-like (H⁻¹∇f), and the paper is transparent in footnotes. However, the title and abstract emphasize "Hessian-informed" without signaling this caveat, which could mislead readers expecting genuine second-order estimates. The paper would benefit from making the adaptive-preconditioner nature clearer at the title/abstract level.

2. **Headline theoretical speedup depends on an unverified condition.** The d-independent convergence rate (Corollary 1) depends on the well-approximated condition (Eq. 17), which the paper itself acknowledges "it is hard to determine if this approximation holds in the context of LLMs" (line 285). No empirical validation is provided that HiSo's actual H satisfies this condition for real models — the synthetic experiment (Fig. 4) uses 200 eigenvalues from a log-normal distribution with no connection to actual LLM Hessians. This limits the practical informativeness of the theoretical rate. However, Theorem 1 does not require this condition, and the paper notes performance degenerates to DeComFL in the worst case (line 286), partially mitigating the concern.

3. **Misleading definition of "well-approximate."** The condition in Eq. (17) requires H to *whiten* Σ (making Tr(H⁻¹/²ΣH⁻¹/²) small), which is the opposite of approximating Σ. As the paper itself notes (line 224), if H perfectly approximated Σ then ζ = d, which would remove the d-independence. The term "well-preconditioning" or "well-whitening" would be more accurate and less confusing.

4. **Missing experimental details in the main text.** (a) The parameter P (line 301: "We set P = 5 for all ZO methods") is used but never defined — in the ZO literature this typically refers to the number of perturbation directions, which affects both variance and computation cost. (b) The number of local update steps τ is not reported for the LLM fine-tuning experiments, despite the theory claiming τ > 1 as an advantage over DeComFL and the model-reset mechanism making τ particularly important.

### Trivial
None.

## Nice-to-Haves

- Include a wall-clock time or FLOPs comparison between HiSo and DeComFL to contextualize the communication-round speedup with computation cost.
- Provide direct measurement (even approximate) of the whitening rank ζ for a small real model (e.g., OPT-125M on a data subset) to strengthen the theoretical claims.
- Study sensitivity to the number of clients and participation rate.

## Removed Points
*(These points were flagged by the harsh critic but removed per the filtering discipline described in the instructions.)*

- "Missing comparison to LoRA-based FL or compression-based methods": scope creep — the paper focuses on ZO methods with dimension-free communication and consistently compares against relevant ZO-FL baselines (DeComFL, FedZO) as well as first-order methods.
- "Sensitivity to number of clients and participation rate": not a core flaw — the paper uses a standard 6-client, 2-sampled setup.
- "Computation cost analysis missing from main text": partially addressed in Appendix E; a nice-to-have but not a core weakness.
- "90 million communication savings claim is misleading": this claim is technically correct (TB vs KB comparison with FO methods) and not presented as a novel advantage over other ZO methods — it simply illustrates the scale of ZO communication savings.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Define P explicitly in the main text and report the τ value used in the LLM experiments.
2. Consider softening the "Hessian-informed" framing to "Hessian-inspired" or "preconditioned" in the title, or add a clarifying sentence in the abstract that the Hessian is approximated via adaptive preconditioning (as already done in footnotes).
3. Rename the "well-approximate" condition to "well-whitening" or "well-preconditioning" to avoid confusion with approximation accuracy.
4. Add even an approximate empirical measurement of the whitening rank ζ for a small real model to provide more direct evidence for the theoretical claims.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>