Now I have enough to write the draft review. Let me compose it and call `draft_review`.Based on the calibration search, the most topically relevant anchors are:
- `s9SVlWOcLt.md` (Proto Successor Measure, zero-shot RL theoretical framework): avg **6.75**
- `9sOR0nYLtz.md` (Zero-Shot Humanoid Control via Behavioral FM, zero-shot unsupervised RL): avg **6.50**
- `X5qi6fnnw7.md` (Conservative World Models, FB-based zero-shot RL): avg **4.75**
- `YGhV8wQv3C.md` (Unsupervised-to-Online RL): avg **4.25**
- `agPpmEgf8C.md` (Predictive auxiliary objectives in deep RL, self-supervised + RL): avg **8.00**

**Round 1 bracket: 6.5 – 7.5.** TD-JEPA outperforms the 4–5 range papers (no novel theory, weak empirical scope), is comparable to or stronger than the 6.5–6.75 zero-shot RL papers (broader evaluation, stronger theory), and does not quite reach the 8.0 band (no fundamental discovery, overclaimed abstract, proprioceptive OGBench results are mixed). I'll fix the score at **7.0**.

---

## Summary
TD-JEPA introduces a temporal-difference (TD) reformulation of multi-step, policy-conditioned latent-predictive learning, enabling offline, reward-free training of zero-shot unsupervised RL agents entirely in latent space. The method trains dual state (φ) and task (ψ) encoders, a policy-conditioned predictor, and parameterized policies from single-step transitions, eliminating the on-policy data requirement of prior latent-predictive zero-shot RL methods. A "gradient matching" theoretical framework unifies several prior analyses of self-predictive representations as special cases and connects TD-JEPA to forward-backward RL methods.

## Strengths
- **Genuine off-policy TD reformulation (Section 3.1, Eq. 7/9):** The transformation from a Monte-Carlo successor-measure loss (requiring on-policy samples from all trained policies) to a TD objective computable from single-step offline transitions is the core algorithmic advance. It cleanly removes the fundamental on-policy requirement of BYOL-γ* and similar methods without approximation.
- **Unified theoretical framework (Section 4, Theorems 1–4):** The gradient matching theorems prove that, under mild assumptions, encoder gradients under latent-predictive losses are identical to those of the corresponding non-latent-predictive successor-measure losses, unifying and generalizing Tang et al. (2023), Voelcker et al. (2024), Khetarpal et al. (2025), and Lawson et al. (2025) as special cases. Theorem 4 completes the arc from loss design to bounded policy evaluation error.
- **Strong pixel-based empirical results (Table 1, Figure 2):** TD-JEPA achieves DMC_RGB avg of 628.8 vs. next-best BYOL-γ* at 582.4, and OGBench_RGB avg of 41.34 (tied with BYOL-γ* at 41.58). The probability-of-improvement analysis (Figure 2) shows TD-JEPA is consistently at the top in pixel domains, with statistically significant advantages over most baselines.
- **Asymmetric encoder ablation (Figure 3, right):** The direct empirical comparison between separate vs. shared (φ=ψ) encoders is informative and the finding—separate encoders improve more often than not—is a useful, non-obvious design validation.

## Weaknesses

### Fatal
None.

### Major
- **Overclaimed "matches or outperforms" framing in the abstract:** Table 1 reveals substantial gaps in OGBench proprioception: cube-single (TD-JEPA 34.20 vs. BYOL-γ* 79.40), cube-double (3.60 vs. HILP 20.00), scene (38.44 vs. ICVF* 65.40), antmaze-me (20.20 vs. FB 51.60). The OGBench (proprioception) suite average is 37.98—tied with HILP and clearly below FB (39.04). The headline claim in the abstract ("matches or outperforms state-of-the-art baselines … across 13 datasets") implies parity across settings that the data does not support. The paper's own probability-of-improvement analysis (Figure 2) correctly qualifies this: "TD-JEPA is only slightly preferable to FB and HILP from proprioception." This qualification must be surfaced in the abstract and conclusion rather than buried.

### Minor
- **Theoretical guarantees apply to an idealized setting not matched by Algorithm 1:** Theorem 2's non-collapse result requires a continuous-time relaxation where optimal predictors are computed at every gradient step—inconsistent with the EMA target-network + batch-update regime of Algorithm 1. Assumption A3 (symmetric transition kernels P^πz) is restrictive and does not hold in typical locomotion/manipulation environments. The paper notes these limitations in the conclusion ("formal guarantees rely on an assumption of symmetry"), but the abstract and theory section framing ("we show that TD-JEPA avoids collapse and learns encoders that capture a low-rank factorization") does not signal that these apply to an idealized variant, not the deployed algorithm. This is a presentation gap that could mislead readers.
- **No analysis of when/why TD-JEPA fails in proprioceptive manipulation (Table 1):** The paper offers no explanation for the large gaps on cube-single (34.20 vs. 79.40), scene (38.44 vs. 65.40), or antmaze-me (20.20 vs. 51.60). Understanding whether these failures are inherent to the TD-JEPA objective, the evaluation protocol, or an interaction with the data regime (low-coverage OGBench datasets) would substantially increase the paper's value to practitioners.

### Trivial
- The abstract states "zero-shot optimization of any reward function at test time" without noting the caveat (rewards must lie in the span of ψ), which does not appear until Section 3.3.

## Nice-to-Haves
- **Orthonormality regularization ablation:** Algorithm 1's L_REG is presented without isolating its contribution in the ablation study. Showing what happens empirically if it is removed would connect Theorem 2's idealized non-collapse guarantee to the practical stabilization, and is mentioned as important by Jajoo et al. (2025) for similar methods.
- **Adaptation experiments on OGBench (Figure 4):** The fine-tuning experiment covers only DMC domains. Showing adaptation on OGBench, where the largest gaps between TD-JEPA and baselines appear, would be more informative.
- **Mechanistic analysis of φ vs. ψ:** A probing or visualization analysis of what the state and task encoders actually capture would sharpen the narrative around the motivation for separate encoders (Section 3.2).
- **Contrastive vs. non-contrastive ablation:** The explanation that non-contrastive losses generalize better to pixels is plausible but informal. Ablating this choice directly (e.g., contrastive TD-JEPA) would make this claim convincing.

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **EMA coefficient sensitivity and λ hyperparameter:** The harsh critic flags these as affecting reproducibility. By the filtering rules, nitpicks about undisclosed standard hyperparameters that do not affect core claims are removed. These choices are implementation details typical of target-network-based RL papers.
- **Baseline re-instantiation as a fatal attribution problem:** The paper is transparent about BYOL*, BYOL-γ*, and ICVF* being author-adapted baselines (footnote 5, Section 6 text). The harsh critic's concern is noted but does not rise to Major, because the paper explicitly states these are designed to investigate representation impact, not to serve as standard method comparisons. Retained only as an observation in Minor that the discussion could be clearer about attribution limits.
- **Related work: contrastive vs. non-contrastive and pixel advantage:** The suggestion that the related work should formally explain FB's pixel disadvantage via batch-size sensitivity is a nice-to-have, not a weakness.
- **Missing connection between Theorem 2 and L_REG in the main text:** Valid but a nice-to-have rather than a weakness that undermines the core claim.

## Novel Insights
The "gradient matching" result (Theorems 1 and 3) is technically novel and has broader implications beyond this paper: it establishes a general equivalence between self-supervised latent-predictive losses and explicit successor-measure approximation losses at the level of encoder gradients, which implies that any improvement to the latent-predictive pipeline (architecture, training tricks) directly improves successor-measure approximation quality. The insight that TD-based latent prediction is "doubly self-predictive" (the target includes a bootstrapped version of the predictor being trained), yet still provably preserves representation covariance in the idealized continuous-time setting, is non-obvious and meaningfully advances theoretical understanding of TD-based self-supervised methods.

## Suggestions
1. Recalibrate the abstract to accurately state that TD-JEPA is strongest in pixel-based settings and competitive-but-not-dominant in proprioceptive OGBench (cite Figure 2 probability-of-improvement analysis).
2. Add a paragraph in Section 6 analyzing when and why TD-JEPA underperforms on specific proprioceptive manipulation tasks (cube-single, scene, antmaze-me).
3. Clarify in Section 4 that the theoretical guarantees (particularly Theorem 2) apply to an idealized linear setting with continuous-time relaxation and symmetric kernels, and are not direct guarantees for Algorithm 1 as deployed.
4. Add an ablation on L_REG removal (or move to appendix) to connect the practical orthonormality regularization to the theoretical non-collapse result.

## Score and Decision

**Anchor papers and comparisons:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `s9SVlWOcLt.md` | 6.75 | R1 | Proto Successor Measure — also zero-shot RL with theoretical successor-measure framework; TD-JEPA has broader empirical evaluation and more coherent theory |
| `9sOR0nYLtz.md` | 6.50 | R1 | Zero-Shot Humanoid Control (FB-CPR) — applied extension of FB; less theoretical novelty than TD-JEPA, narrower scope |
| `X5qi6fnnw7.md` | 4.75 | R1 | Conservative World Models — FB variant for low-quality data; narrower contribution, weaker theory |
| `YGhV8wQv3C.md` | 4.25 | R1 | Unsupervised-to-Online RL — related paradigm but shallower method and theory |
| `OMwD6pGYB4.md` | 5.75 | R1 | Distributional SM — theoretical framework for distributional successor representation; comparable theoretical depth but less empirical validation |
| `agPpmEgf8C.md` | 8.00 | R1 | Predictive objectives in deep RL — also self-supervised+RL, strong empirical+brain connection; broader claims and more decisive results |
| `DzGe40glxs.md` | 8.00 | R1 | Interpreting Planning in Model-Free RL — strong mechanistic contribution; different domain |
| `fnO5h1CFyh.md` | 3.00 | R1 | Learning SR with Distributed Hebbian — weaker experimental evaluation, less novelty |
| `It4KL6XnPq.md` | 3.00 | R1 | Foundation Policies with Memory — incremental extension, limited scope |
| `wYJII5BRYU.md` | 5.75 | R1 | Learning Successor Features DHTM (revised version) — accepts at 5.75, comparable scope |
| `o5Bqa4o5Mi.md` | 5.25 | R1 | π2vec Policy Representation — related successor features framework; narrower scope, limited tasks |

**Bracket (Round 1):** 6.5 – 7.5.

TD-JEPA clearly exceeds the 4–5 range papers: it has genuine algorithmic novelty (off-policy TD), a unified theoretical framework, and broad empirical coverage (65 tasks, 13 datasets). It is comparable to or stronger than the 6.5–6.75 zero-shot RL papers (Proto Successor Measure, Zero-Shot Humanoid FM) in theoretical depth and empirical breadth. It does not reach the 8.0 band because: (a) the abstract overclaims performance relative to the proprioceptive results; (b) the theoretical guarantees apply to an idealized variant not the deployed algorithm; (c) large unexplained proprioceptive failures remain.

**Final score: 7.0** (Accept). The core TD reformulation, gradient-matching theory, and pixel-based results constitute a solid, well-motivated contribution at the level expected for a top-venue acceptance. The main weaknesses (overclaimed abstract framing, idealized theory scope) are addressable in revision and do not undermine the contribution's validity.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>