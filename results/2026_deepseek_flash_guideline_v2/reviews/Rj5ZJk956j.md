## Summary

This paper introduces a weight-based cosine-similarity method for analyzing the "read-write" (RW) functionality of gated neurons (SwiGLU/GEGLU) in transformer LLMs. Applying this method across 12 models (0.5B–9B parameters), the authors discover a systematic pattern: early-middle layers are dominated by "strengthening" and "conditional strengthening" neurons, while late layers contain more "weakening" neurons — a small class (~243 in OLMo-7B) with negative cos(w_in, w_out). Ablation experiments on OLMo-7B show that removing these few weakening neurons measurably affects attribute rate and entropy. A conditional ablation technique further reveals that negative Swish gate values — conventionally considered unimportant for model mechanisms — contribute to this effect. The paper also establishes a strong negative correlation between cos(w_in, w_out) and activation frequency, connecting RW class to how often neurons fire.

## Strengths

1. **Robust cross-model validation across 12 LLMs.** Section 5 and Figure 1(a) show the same strengthening-then-weakening pattern of median cos(w_in, w_out) across layers for all 12 tested models (OLMo, Llama-2/-3.1/-3.2, Mistral, Qwen 2.5, Yi, Gemma), spanning 0.5B to 9B parameters and covering both SwiGLU and GeGLU gating variants. This breadth substantially exceeds typical neuron analyses that focus on one or two models. The pattern is non-trivial and emerges cleanly from a simple weight-based method.

2. **Conditional ablation method and discovery that negative gate values have functional importance.** The conditional ablation technique (Section 6.2) isolates which activation regimes of a neuron drive a given behavior. Applying it reveals that the regime x_gate < 0, x_in < 0 (gate-negative, post-positive) accounts for a substantial portion of the entropy-sharpening effect of weakening neurons (Figure 3b, bottom-left subplot closely matching the full weakening histogram). This is a genuinely novel finding that challenges the common assumption that negative Swish gate values are only relevant for training dynamics, not model mechanisms. The paper explicitly notes concurrent work (Kong et al., 2025) studying a different phenomenon.

3. **Layer-controlled ablation baseline.** The ablation design (Section 6.1) compares weakening neurons against the same number of random neurons drawn from the *same layers*. The random baseline shows negligible effect while the weakening ablation produces a clear divergence from layer ~10 onward (Figure 3a). This rules out the confound that the observed effect is simply due to which layers the weakening neurons reside in. The appendix further shows that other RW classes from the same layers also show no effect.

4. **Quantitative link between RW class and activation frequency.** Section 7 establishes a strong negative correlation between cos(w_in, w_out) and activation frequency (r ≈ −0.97, p < 0.01 in layer 15 of OLMo-7B), with correlations of at least −0.71 across most layers. This extends Gurnee et al. (2024)'s finding from GELU models to gated architectures and provides a principled explanation for why weakening neurons are disproportionately impactful.

## Weaknesses

### Fatal
None.

### Major

1. **The ablation experiments do not control for activation frequency, confounding the "outsize influence" claim.** Section 7 independently shows that weakening neurons activate *very often* while (conditional) strengthening neurons activate *very rarely*. However, the ablation experiments (Section 6) compare weakening neurons against random neurons from the same layers — the vast majority of which are strengthening/conditional-strengthening neurons that rarely fire. Knocking out neurons that rarely fire would trivially produce little effect. The other RW classes tested in the appendix suffer from the same confound. 

   The paper interprets the ablation results as evidence that weakening neurons as an RW class have "outsize influence" (abstract, conclusion), but the evidence cannot distinguish whether the effect is due to the RW class or simply due to these neurons activating far more often. To establish class-specific influence, the experiment needs a control of frequently-activating non-weakening neurons matched on activation count or frequency. 

   **This does not invalidate the paper.** Both findings — (a) weakening neurons are impactful when ablated and (b) weakening neurons activate frequently — are independently valid and the paper connects them. But the "outsize influence" framing overstates what the current evidence supports. The negative-gate finding (Section 6.2) is not affected by this confound and stands as a separate contribution. The paper should either add the proper control or explicitly reframe the claim.

### Minor

1. **Ablation experiments performed on a single model (OLMo-7B).** The weight-based analysis in Section 5 covers 12 models, which is the paper's strongest part. However, the functional ablation experiments that underpin the central claims about weakening neurons' influence and the negative-gate mechanism are run on OLMo-7B only, with 20M tokens from Dolma (OLMo's training data). The paper acknowledges this resource constraint (Section 6, "to save resources"), but the consequence is that the functional claims may not generalize beyond this specific model. Replication on at least one other model family would significantly strengthen the paper's claims.

2. **No threshold sensitivity analysis for ablation results.** The neuron classification uses a threshold of |0.5| on cosine similarities (Section 4.2). While the paper partially mitigates this by offering three levels of analysis (threshold-based, marginal distributions, scatter plots), the ablation experiments (Section 6) rely on the threshold-based classification to select which neurons to ablate. The paper does not report whether the ablation results are stable under different thresholds (e.g., |0.4| or |0.6|), leaving the results' threshold-dependence unexamined.

3. **No confidence intervals or statistical tests for ablation effects.** The ablation results (Figure 3) are shown as line plots and histograms without error bars, confidence intervals, or significance tests. Given that the ablation is on a single model with a single dataset, this makes it difficult to assess the reliability and variability of the reported effects.

4. **The sign-convention dependence of the full taxonomy is under-discussed in the main text.** The preprocessing (Section 3.2) multiplies w_in and w_out by sign(cos(w_gate, w_in)). While this is an exact invariance and the paper correctly notes it, the transformation changes cos(w_gate, w_out) — the quantity that determines whether a neuron is "strengthening" vs. "conditional strengthening" (and "weakening" vs. "conditional weakening") in Table 1. The main qualitative findings (strengthening in early layers, weakening in late) rely on cos(w_in, w_out), which IS invariant, and are therefore robust. But the fine-grained taxonomy counts (e.g., how many "conditional strengthening" vs. "strengthening" neurons exist) are convention-dependent. The paper acknowledges "atypical" categories but could be more upfront about this in the main text.

### Trivial
None.

## Nice-to-Haves
- Replicating the ablation experiments on at least one additional model from a different family.
- Adding a matched control of frequently-activating non-weakening neurons to disentangle RW class from activation frequency.
- Reporting threshold sensitivity analysis for ablation results (|0.4|, |0.6|).
- Adding confidence intervals or statistical tests for the ablation effects.

## Removed Points
- **"The ablation claim is fatal because it doesn't control for activation frequency"** → Demoted from Fatal to Major. The confound is real but does not invalidate the paper: the weight-based findings (Section 5), activation frequency correlation (Section 7), and negative-gate finding (Section 6.2) stand independently. The paper needs to either add controls or reframe claims, not withdraw the paper.
- **"Related work is somewhat defensive about SAEs"** → Removed (subjective opinion, not a concrete weakness).
- **"The introduction should caveat concurrent work by Kong et al."** → Removed (paper already acknowledges this in Section 6.2: "concurrently with Kong et al. (2025) who focus on a different phenomenon").
- **"The case study is cherry-picked"** → Removed (the paper explicitly notes this is the "most extreme" example; case studies in interpretability are inherently illustrative by design).
- **"Missing confidence intervals"** → Kept but as Minor (valid point but standard for exploratory mechanistic interpretability).
- **"Ablation dataset is in-distribution"** → Removed (standard practice; using training data for ablation is common and appropriate).
- **"Activation frequency confound should be treated as fatal"** → As noted above, demoted to Major.

## Novel Insights

The harsh critic's observation about the activation frequency confound is the most valuable insight to emerge from the reviews. The paper presents the activation frequency finding (Section 7) as *supporting* evidence for weakening neurons' importance, but it simultaneously undermines the specificity of the ablation claim — a tension the paper does not acknowledge. This is a genuinely useful observation: the paper could resolve it by either (a) running a matched-frequency control or (b) reframing the claim from "weakening neurons have outsized influence *because of their RW class*" to "weakening neurons are the only RW class that activates frequently, and their high activation frequency mediates their large functional impact." Either move would make the paper internally consistent and more honest about what the evidence supports. Additionally, the reviewer's suggestion to use conditional ablation on other RW classes (beyond weakening neurons) is a potentially fruitful direction not explored in the paper.

## Suggestions

1. **Address the activation frequency confound directly.** Either add a control experiment ablatening frequently-activating non-weakening neurons matched on activation count, or explicitly reframe the "outsize influence" claim to acknowledge that the observed effect is mediated by activation frequency. The negative-gate finding (Section 6.2) is not affected by this and should be highlighted as the stronger functional claim.

2. **Replicate ablation findings on at least one other model** (e.g., Llama-3.2-3B or Gemma-2-2B). The weight-based universality across 12 models is the paper's strongest result; adding even one more ablation replication would substantially strengthen the functional claims.

3. **Report threshold sensitivity** for the ablation results to show they are not artifacts of the |0.5| cosine threshold.

4. **Clarify in the main text** that the distinction between "strengthening" and "conditional strengthening" (and "weakening" vs. "conditional weakening") depends on the preprocessing sign convention, and note which findings are invariant vs. convention-dependent.

## Score and Decision

**Calibration note:** The calibration retrieval tool was unavailable due to file system errors, so I was unable to retrieve anchor papers for direct score comparison. I instead calibrated against my knowledge of ICLR reviewing standards for mechanistic interpretability papers.

This paper makes genuine empirical contributions: (1) a simple weight-based method for gated neuron analysis that reveals a strikingly consistent cross-model pattern (12 models), (2) the discovery that negative gate values have functional importance, and (3) the conditional ablation technique. The cross-model validation is unusually broad for this area. However, the paper's most prominent claim — that weakening neurons have "outsize influence" as an RW class — is partially confounded by activation frequency, and the functional experiments are limited to a single model. These are addressable weaknesses, not fatal flaws, and the weight-based findings and negative-gate discovery stand independently.

Comparable to accepted mechanistic interpretability papers at ICLR that combine a simple method with broad empirical validation; the activation frequency confound tempers the paper's strongest claim but does not outweigh its contributions.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>