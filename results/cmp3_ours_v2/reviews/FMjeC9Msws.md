## Summary

This paper presents a large-scale empirical study (400,000+ GPU-hours) of RL compute scaling for LLMs on verifiable math reasoning tasks. The authors propose a sigmoidal compute-performance curve (Equation 1) that decomposes RL method quality into asymptotic performance (parameter A) and compute efficiency (parameter B). Using a three-stage ablation methodology — short screening runs, combination of best options, then leave-one-out (LOO) validation at 16K GPU-hours each — they consolidate findings into **SCALERL**, an RL recipe. The paper's core empirical claims are: (1) different RL recipes have different asymptotic performance ceilings, (2) many common design choices primarily affect compute efficiency rather than the asymptote, and (3) the sigmoidal fit enables extrapolation from partial training trajectories.

## Strengths

1. **Scale of experimentation.** Over 400,000 GPU-hours of RL experiments, including a single 100,000 GPU-hour run, is substantially larger than comparable academic studies (e.g., ProRL at ~16K GPU-hours). This scale provides genuinely useful empirical signal that is rare in academic RL-for-LLMs research.

2. **Well-designed staged ablation methodology.** The three-stage design — short ablations at 3.5–4K GPU-hours to filter unstable choices, combining best options, then leave-one-out (LOO) experiments at 16K GPU-hours each — is methodologically sound. The LOO design (Section 4, Figure 5) tests whether each component remains beneficial in the presence of all others, avoiding the common pitfall of evaluating design choices in isolation.

3. **The A/B decomposition framework.** Distinguishing between asymptotic performance (A) and compute efficiency (B) is conceptually useful. The finding that many design choices (loss aggregation, advantage normalization, curriculum) primarily modulate efficiency rather than the asymptote (Section 4, Figure 5) is practically informative and reasonably well-supported by the data.

4. **Demonstrating the "bitter lesson" pattern in RL.** Figure 2 shows that methods that appear competitive at small compute budgets can be overtaken at larger scale. This is a genuinely important observation for practitioners deciding early in development which recipes to pursue.

5. **Honest discussion of limitations.** The paper clearly acknowledges (Section 7) that its primary evidence is on in-distribution validation, that generalization to downstream tasks is a separate question, and that multi-task RL results are preliminary. This scoping is appropriate and strengthens the paper's credibility.

## Weaknesses

### Fatal
None.

### Major

1. **Cross-method comparison (Figure 2) lacks necessary experimental detail.** The paper claims SCALERL achieves state-of-the-art asymptotic performance (A=0.61) by comparing against DeepSeek (GRPO), Qwen2.5 (DAPO), Magistral, and MiniMax-M1. The caption says "We fit sigmoid curves (Equation 1) on *iid* validation dataset to commonly-used training recipes" and references Appendix A.17 for details. However, the paper does not clarify in the main text whether these methods were re-implemented under controlled conditions (same base model, same training prompt distribution, same evaluation pipeline) or whether curves were fitted to published data from different base models and training distributions. Since these baselines use different base models (DeepSeek, Qwen, etc.) and different training distributions, an uncontrolled comparison would conflate method quality with these confounding factors. **This is the single most important piece of missing information in the paper.** The headline SOTA claim depends on this comparison being controlled; without clarification, a reader cannot assess its validity.

2. **Extrapolation validation is limited to ~2× ratios.** The paper validates sigmoidal extrapolation by fitting on, e.g., the first 50K GPU-hours and checking against the next 50K (2×), and similarly 8K→16K for LOO experiments (also 2×). Pre-training scaling laws are validated over many orders of magnitude; here, the validation primarily confirms that the sigmoid functional form fits the training trajectory. The fits look clean, but the demonstrated predictive power is modest relative to the language of "predictable scaling" and the parallel drawn to pre-training scaling laws. This is a gap between the rhetorical framing and the evidence presented.

### Minor

1. **"Scaling law" framing is somewhat inflated.** The paper borrows terminology from pre-training scaling laws (Kaplan et al., Hoffmann et al.), which predict performance as a function of multiple independent variables (model size, data size) before training begins. What this paper provides is a within-method, single-variable sigmoidal curve fitted to the training trajectory of a specific method on a specific distribution, extrapolated to longer training of the same method. The abstract claims "a principled framework for analyzing and predicting RL scaling" and the introduction invokes "the well-established concept of *scaling laws*." The paper's real contributions — the systematic ablation methodology, the A/B decomposition, and the SCALERL recipe — do not need this framing to be important, and the framing misleads readers about what has been demonstrated.

2. **No confidence intervals or uncertainty estimates for fitted parameters.** The paper reports fitted parameters A, B, C_mid without any uncertainty quantification. Given that the central claim involves *predictive* extrapolation, the reader needs to know how uncertain these extrapolations are. Bootstrap or similar methods would naturally yield such estimates.

3. **Single-run trajectories without variance characterization.** The paper reports individual training runs (e.g., the 100K GPU-hour run in Figure 1). At this scale, single runs per configuration are understandable, but the paper does not explicitly state this limitation or discuss how much of the extrapolation accuracy could be due to fitting a particular trajectory's noise rather than signal.

### Trivial
None.

## Nice-to-Haves

- **Clarify compute accounting:** Whether reported GPU-hours account for idle time, generation time, and training time separately, or are wall-clock GPU-hours that mix all three. This matters because PipelineRL's efficiency gain partly comes from reducing idle time.
- **Separate algorithmic from systems efficiency in parameter B:** The B parameter conflates statistical efficiency (gradient quality per token) with systems efficiency (tokens per second). An analysis separating these would strengthen the scientific content.
- **Explore whether the LOO procedure of averaging A and re-fitting to compare B could be validated with uncertainty intervals** — the current procedure is defensible but the paper presents it as fact rather than an analytical choice.

## Removed Points

- **C3 (in-distribution evidence sidesteps practical question):** REMOVED — the paper explicitly acknowledges this limitation (Section 7: "our primary focus is on studying predictive scaling, which is characterized through in-distribution performance curves") and shows AIME-24 results (Figure 1b). The criticism is addressed by the paper's own honest scoping, which the critic acknowledges but then repeats the concern as if unaddressed.
- **"FP32 precision raises questions about other baselines":** REMOVED — this is an unfalsifiable speculation. The critic speculates that other baselines "may suffer from the same or analogous precision mismatches" without evidence. This is not a verifiable weakness.
- **Systems vs. algorithmic efficiency conflation in B:** REMOVED — the paper frames B as a practical "compute efficiency" parameter that naturally reflects both. Separating them would be an extension, not a correction.
- **Section-by-section editorial comments (introduction framing, Related Work dismissal):** REMOVED — these are editorial-level observations and stylistic preferences, not substantive weaknesses.
- **"Generations per prompt allocation as second-order effect" from soft rules:** REMOVED — the paper's own experiments show this, and it's not framed as a weakness by the critic.

## Novel Insights

The key insight from the review process is that the paper's sigmoidal curve-fitting validation primarily demonstrates **internal consistency** — the functional form fits the data — rather than strong predictive power across methods, distributions, or multiple orders of magnitude. The extrapolation validation (2×) is substantially weaker than what pre-training scaling law papers demonstrate. Additionally, the LOO procedure of fixing A to a common value across runs to extract B differences is a defensible analytical choice but should be presented as such rather than as an incontrovertible finding, since individual A estimates genuinely differ (0.590–0.610 in the table).

## Suggestions

1. **Clarify the cross-method comparison (most urgent).** State explicitly in the main text (not only in an appendix) whether the baselines in Figure 2 were re-implemented under controlled conditions (same base model, same training data, same evaluation pipeline) or fitted to published data. If re-implemented, describe the base model and training setup. If fitted to published data, explain how confounds (different base models, data distributions, evaluation protocols) were addressed or why they do not affect the comparison.

2. **Recalibrate the framing.** Replace "scaling law" references with more precise terminology such as "within-recipe compute-performance curve" or "predictive curve-fitting for RL training." The paper's contributions — the staged ablation methodology, the A/B decomposition, and the LOO-validated SCALERL recipe — are strong enough to stand without the inflated framing.

3. **Add uncertainty quantification.** Report confidence intervals for fitted A, B, C_mid parameters (e.g., via bootstrapping). This is especially important given that the central claim involves predictive extrapolation.

4. **Acknowledge the single-run limitation explicitly.** State that scaling curves are fitted to single trajectories and discuss how this affects the strength of the predictive claims.

---

## Calibration Anchors

All anchors retrieved across rounds:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `5kMwiMnUip.md` (Jailbreaking LLMs) | 1.40 | R1, Q1 | Much weaker paper; superficial contribution |
| `8QTpYC4smR.md` (Systematic Review of LLMs) | 1.00 | R1, Q1 | Much weaker paper; survey with no novel experiments |
| `Uj0h13lVrR.md` (GFlowNets) | 1.00 | R1, Q1 | Unrelated topic; much weaker |
| `u1cQYxRI1H.md` (IC-Light) | 10.00 | R1, Q1 | Unrelated topic; very strong accept |
| `BmYzoPppij.md` (Carbon Footprint LLMs) | 3.33 | R1, Q2 | Less compelling empirical study |
| `jOuHjFw71C.md` (Planning in Strawberry Fields) | 3.00 | R1, Q2 | Evaluation paper, less methodological contribution |
| `xFezgECSLa.md` (LLM-Based Algorithms) | 3.00 | R1, Q2 | Theoretical analysis, different contribution type |
| `YW79lAHBUF.md` (ICRL) | 3.75 | R1, Q3 | Less scale, more specific algorithmic contribution |
| `d4uL2MSe0z.md` (Dynamic Layer Tying) | 4.50 | R1, Q3 | Smaller-scale experiments, less comprehensive |
| `EvRZ68ObgW.md` (Controlling Over-optimization) | 3.75 | R1, Q3 | More focused on a specific issue, less scaling scope |
| `cK7yrw5g5Q.md` (Segmenting Text RLHF) | 5.25 | R1, Q3 | Algorithmic contribution, less empirical scaling focus |
| **`PXD3FAVHJT.md` (RLHF Generalisation & Diversity)** | **5.67** | **R1, Q4** | **Similar empirical methodology; our paper has larger scale but its framing overclaims more** |
| **`eENHKMTOfW.md` (Small-Sized LLM Customization)** | **6.00** | **R1, Q4** | **Similar type of systematic empirical study; similar strengths/weaknesses profile** |
| **`zfeso8ceqr.md` (Deconstructing Optimizers)** | **6.00** | **R1, Q4** | **Very analogous: thorough empirical ablation study with clear practical findings; similar issues with interpretation precision** |
| **`o9YC0B6P2m.md` (Scaling Law with LR Annealing)** | **6.75** | **R1, Q4** | **Related contribution (parametric curve for training dynamics); stronger mathematical framing but had its own significant weaknesses** |
| `wg1PCg3CUP.md` (Scaling Laws for Precision) | 8.00 | R1, Q5 | Stronger theoretical foundation and validation; clearly higher quality |
| `VNckp7JEHn.md` (Inference Scaling Laws) | 5.75 | R2 | Empirical scaling study on inference; similar methodology (parametric curves), similar weaknesses (limited domain, outdated models) |
| `3OyaXFQuDl.md` (Smaller, Weaker, Yet Better) | 7.00 | R2 | Stronger experimental design and clearer claims; higher quality empirical study |
| `GtpubstM1D.md` (Advancing Math Reasoning) | 5.71 | R2 | Analysis paper on math reasoning; less focused on scaling methodology |
| `yaqPf0KAlN.md` (Omni-MATH) | 6.75 | R2 | Benchmark paper; different contribution type |

**Round 1 bracket:** 4.0 – 7.0 (initial plausible range based on comparison with similar empirical scaling/ablation studies)

**Narrowing rationale:** The paper is clearly stronger than papers scoring below 5 (it has real experimental scale and sound methodology), and it aligns well with papers scoring 5.67–6.75 that do systematic empirical studies with clear practical findings. It does not reach the quality of 7.5+ papers (which have stronger theoretical validation, cleaner claims, or multi-order-of-magnitude validation). The Major weaknesses (unclear baseline comparison, limited 2× extrapolation) prevent a higher score but are not fatal — they are addressable in rebuttal. The paper's strengths (400K GPU-hours scale, well-designed staged ablation, LOO methodology) are genuine.

## Score and Decision

**Score: 6.0** — This is a solid empirical study with genuine contributions (the staged ablation methodology, the A/B decomposition, the SCALERL recipe, and the large-scale experiments) that make it worthy of publication. However, the paper has two significant issues that prevent a higher score: (1) the state-of-the-art claim in Figure 2 lacks sufficient experimental detail about whether the comparison was controlled, and (2) the predictive framing outruns what is actually demonstrated (2× extrapolation, within-method curve fitting). These issues require clarification from the authors but are addressable in rebuttal and do not invalidate the paper's core contributions.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>