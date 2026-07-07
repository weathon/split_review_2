Now I have all the information I need. Let me produce the final consolidated review.

---

## Summary

This paper introduces a framework for studying how neural language models learn context-free grammars (CFGs) through the lens of "subgrammars" — formal substructures of CFGs defined as inner subgrammars (subtrees of derivations) and outer subgrammars (simplified rule-sets). The authors prove several theorems relating the KL divergence of language modeling to subgrammar structure (including a recursion blow-up result, Theorem 4.6), and conduct small-scale experiments on synthetic CFGs. The empirical claims are that small transformers learn subgrammars in parallel, that pretraining on subgrammars improves performance and aligns internal representations, and that models struggle with recursive depth more than sequence length.

## Strengths

1. **Well-motivated and clean subgrammar definitions (Def. 3.3, 3.5).** The inner/outer subgrammar distinction is conceptually clear and connects naturally to the goal of studying how grammatical substructures interact with learning. These definitions provide a principled vocabulary that future work could build on, and the connection to Gruska (1971) situates them in the literature.

2. **Theorem 4.6 (KL-divergence with expected recurrence) is a genuinely non-trivial theoretical result.** The blow-up factor \(1/(1-\mathbb{E}[R])\) makes a testable prediction: as expected recursion approaches 1, per-subgrammar errors get amplified. The simple two-rule CFG illustration (S → x with probability p, S → (S and S) with probability 1-p) makes the mechanism concrete. This goes beyond the additive decomposition results.

3. **The depth vs. length generalization experiment (Section 6, Figure 3) is clean and informative.** Separating context length from recursive depth in the Nested Parentheses grammar directly addresses a known open question. The contrast between \((a)^i\) (flat context, error stays low at 0.017) and \((^i\) (deep context, error grows to 0.173) provides clear evidence that the difficulty is specifically about recursive depth, not sequence length. The GPT-5.1 anecdote is appropriately caveated with explicit footnotes.

## Weaknesses

### Major

1. **The core KL decomposition theorems (4.3, Corollaries 4.4–4.5) are largely structural/definitional, and the paper's framing overstates their depth.** The abstract claims "a suite of fundamental theorems showing that the loss of language modeling obeys recurrences with respect to subgrammars." However, if one defines restricted KL terms over a partition of the data distribution's support (as Definition 4.2 does), the total KL is additive across the parts by the definition of KL as an expectation over the data. The subgrammar structure provides a *principled* partition, which has real value as an organizational framework, but the "decomposition theorem" is primarily a consequence of how the terms are set up rather than a non-trivial structural discovery. Theorem 4.6 is the one genuinely substantive result and is not subject to this criticism; it should be foregrounded.

2. **The "parallel learning" claim lacks statistical support and relies on visual inspection alone.** The paper asserts that small transformers "learn all subgrammars in parallel" based on Figure 2(a), where all KL curves decrease together. There is no formal test comparing against a null model of sequential learning, no analysis of whether the observed co-decrease is merely an artifact of shared parameters driving overall loss reduction, and no statistical comparison of the temporal ordering of subgrammar convergence. Corollary 4.7, presented as a formal result on when parallel learning occurs, is near-tautological: it states that if gradient updates for one subgrammar do not harm others, then all are learned in parallel — this restates the definition of "not harming" as "learning in parallel" without providing a testable condition or mechanism. The paper itself acknowledges this ("simple but fundamental scenario") and suggests weakening the assumptions as future work.

3. **The child-language comparison in the abstract and introduction is unsubstantiated.** The abstract states that models learn subgrammars "in parallel, unlike children — who first master simple substructures before progressing to more complex constructions" (p. 1). No child language data is presented. The sole citation, Evanson et al. (2023), is about GPT-2 displaying developmental stages *reminiscent* of child language, not about children themselves, and does not support the specific claim about children mastering simple substructures first. The paper's empirical setting (tiny transformers on synthetic CFGs) has no demonstrated connection to child language acquisition. This claim is rhetorical and should either be supported with evidence or removed.

4. **The method for computing per-subgrammar KL divergences is not clearly specified, making the central empirical validation unverifiable.** Definition 4.2 (p. 4, line 136) is unclear: it uses notation \(D_{\text{KL}}(P_G \parallel Q \mid \neg s)\) that is not properly defined, and the term \(P_G(A \mid s)\) is ambiguous. The operational description says only "using a random (but likely) prefix" (Figure 1 caption, p. 6). Without a precise algorithm for estimating \(D_{\text{KL}}(P_G \parallel Q_\theta)_A\) from a trained model and a PCFG, the visual confirmation of the decomposition in Figures 1–2 is uninterpretable — it could simply reflect that the computation was designed to produce additivity.

5. **The CKA analysis (Section 5.2, Table 1) reports small effects without statistical testing, yet the abstract claims "definitive" evidence.** The largest absolute change is from 0.249 to 0.303 (attention layer, 2-layer, 20 epochs); many changes are near zero (−0.2% for 2-layer MLP at 10 epochs). The paper reports using 30 random seeds but provides no confidence intervals, standard errors, or p-values. The characterization "use alignment analysis to show, quite definitively, that such pre-training results in internal representations that are more aligned with the grammar's substructure" (abstract, p. 1) is unsupported by the evidence presented.

### Minor

1. **The derivation from Equation (1) to (4) in the main text is garbled.** Equation (4) shows ratios of logarithms rather than differences of log probabilities (e.g., \(\frac{\log P_G(\alpha \mid \epsilon)}{\log Q_\theta(\alpha \mid \epsilon)}\)), which is mathematically nonsensical as a KL decomposition. While this may be a formatting artifact, it undermines the main text's presentation of the paper's central theoretical contribution.

2. **Definitions 3.4 and 3.5 contain imprecise phrasing.** Definition 3.4: "A proper subgrammar is an inner subgrammar \(G'\) of a CFG \(G\) which does not contain \(G\) itself" — it is unclear whether this means \(\mathcal{N}' \subsetneq \mathcal{N}\) or something else. Definition 3.5 ends with "for each of its non-terminals" without completing the clause (must contain at least one rule? what property must those rules have?).

3. **The observation that pretraining helps 2-layer but not 4-layer transformers (Section 5.1) is reported without analysis.** The paper notes "this occurs for 2-layer transformers but not 4-layers" but does not discuss whether this is because 4-layer models are expressive enough to learn the full grammar directly, or because they overfit the subgrammar during pretraining.

4. **No statistical uncertainty is reported for the learning curves in Figures 1 and 2.** Only Figure 3 shows variance (a shaded area). Since the learning dynamics are central to the paper's empirical claims, it is unclear whether the patterns in Figures 1–2 are reliable or idiosyncratic.

### Trivial

None.

## Nice-to-Haves

- Provide a quantitative test for the parallel-learning claim, e.g., measuring the epoch at which each subgrammar's KL reaches a threshold and testing whether the ordering is distinguishable from random.
- Give a precise algorithmic description of how subgrammar KL values are computed from a trained model and a PCFG.
- Add confidence intervals or error bands to Figures 1–2 and Table 1.
- Discuss why the context-insensitivity assumption matters for the claimed decomposition and what conditions would cause it to fail.

## Removed Points

- **"Missing training details (architecture, optimizer, etc.)":** REMOVED per hard rule — these details are likely in the appendix, which was stripped by the parser. The paper explicitly references "Grammar definitions are given in the appendix" (p. 6), so the details may exist in the original submission.
- **"Section 6 feels disconnected from the paper's theoretical apparatus":** REMOVED — this is a subjective organizational opinion, not a verifiable weakness. The section tests depth sensitivity, which relates to the recursive structure central to the paper's framework.
- **"The paper never quantifies approximation error for context-insensitivity":** REMOVED — the paper acknowledges this is a strong assumption and provides empirical checks (varying prefixes gave qualitatively similar results). Quantifying the error is a reasonable extension but not a necessary condition for the paper's validity.
- **"The paper overstates the parallel-learning claim because KL curves could just reflect overall loss reduction":** MERGED into Major weakness #2 — this is the same criticism about lacking a proper baseline/statistical test.
- **"Claims about structures learned are not justified by evidence" (from the child-language comparison):** Already covered in Major weakness #3.
- **Generic "evaluation lacks rigor" / "evidence is weak" phrasing without concrete anchor:** REMOVED — the concrete anchor points (CKA confidence intervals, parallel learning statistical test, KL computation method) are already captured in the specific weaknesses above.

## Novel Insights

None beyond the paper's own contributions. The most interesting observation to emerge from the review process is that Theorem 4.6 (the recursion blow-up) is clearly the paper's strongest result and should be its centerpiece, while the additive KL decomposition — which the paper frames as its primary theoretical contribution — is largely definitional. Restructuring the paper to emphasize the non-trivial recursion result and to demote the decomposition to a useful framework observation would substantially improve the paper's impact.

## Suggestions

1. **Recalibrate the claims.** Remove or heavily qualify "fundamental theorems" and "quite definitively" from the abstract. Theorem 4.6 is genuinely interesting and can be highlighted. The child-language comparison should either be supported with evidence or removed entirely.

2. **Specify the KL computation methodology.** Provide a clear algorithm for computing \(D_{\text{KL}}(P_G \parallel Q_\theta)_A\) from a trained model and a PCFG, including how contexts are sampled and how probability mass is attributed.

3. **Add statistical testing to the parallel-learning claim.** Compare learning curves against baselines (e.g., a null model where subgrammars are learned sequentially), or at minimum provide confidence intervals and test whether the ordering of subgrammar convergence is statistically distinguishable from random.

4. **Add uncertainty quantification to the CKA analysis.** With 30 random seeds, reporting standard errors or confidence intervals is standard practice.

5. **Fix derivation issues.** The garbled Equation (4) and the ambiguous Definitions 3.4–3.5 should be corrected.

## Score and Decision

### Calibration Anchors

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| 0pLCDJVVRD (Percolation/Emergence) | 7.00 | R1 | Yes | Substantially stronger execution: well-written, clear contribution, well-supported findings. Our paper is notably weaker on empirical rigor and claim calibration. |
| fp77Ln5Hcc (Depth Extrapolation) | 4.50 | R2 | Yes | Most similar anchor. Shares same evidential gaps: insufficient statistical rigor, writing clarity issues, overclaiming. Our paper has a broader framework but similar weaknesses. |
| F0Zd3knG9j (Hierarchical filtering) | 5.00 | R2 | Yes | Somewhat stronger experiments. Our paper has comparable novelty of framework but weaker empirical support. |
| q5lJxCXjiY (Compositionality signatures) | 5.40 | R1 | Yes | More extensive experiments but similar speculative claims. Our paper has cleaner definitions but weaker empirical foundation. |
| hNkXTqDrfb (Syntax/semantics learning) | 3.75 | R1 | Yes | Had a significant proof error not present in our paper. Our paper is stronger than this anchor. |
| uOnElfFuey (Hardening LMs to DFAs) | 3.00 | R1 | Yes | Very limited empirical basis. Our paper has a stronger theoretical framework and better experiments. |
| ILStlRb1Sp (Memorisation dynamics) | 5.00 | R2 | No | Different topic but similar level of empirical rigor. Our paper has more overclaiming issues. |

**Bracket (Round 1):** The paper sits between 3.75 and 5.40. Narrowed to 4.0–5.0 via weighted-item comparison against the closest anchors. The most informative comparison is with **fp77Ln5Hcc (4.50)**, which studies nested-structure depth generalization in transformers and shares similar evidential gaps (insufficient statistical rigor, overclaiming, unclear methodology). Our paper adds an unsubstantiated child-language claim absent from that anchor but has a more novel theoretical framework. The weighted-item comparison places our paper slightly below F0Zd3knG9j (5.00) because our empirical support is thinner, and above hNkXTqDrfb (3.75) because we do not have a proof error. Final score: **4.5**.

### Final Score

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>