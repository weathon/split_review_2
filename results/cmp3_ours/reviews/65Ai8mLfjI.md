Now let me finalize my review, complete with the calibration analysis.

## Summary
This paper studies the role of pooled CLIP text embeddings in diffusion transformers. It finds that these embeddings are largely inactive in their conventional usage (attention alone suffices for text conditioning) but can be repurposed as a guidance signal for quality improvement. The proposed "modulation guidance" extrapolates between positive and negative prompt conditions in the modulation space (Eq 3: ŷ = y + w·(y(p₊,t) − y(p₋,t))), is computationally cheap, and is demonstrated across text-to-image, text-to-video, and image-editing tasks with human evaluation showing improvements.

## Strengths
1. **Empirical finding with clean evidence.** Table 1 provides clear evidence that zeroing out the pooled CLIP embedding in HiDream-Fast produces no measurable change in CLIP Score, PickScore, or ImageReward, and only affects FLUX schnell for short prompts. This is a genuine observation that justifies the paper's motivating question.

2. **Broad applicability with negligible overhead.** The method is tested across five image-generation models (FLUX schnell/dev, SD3.5 Large, HiDream, COSMOS), two video models (Hunyuan 13B, CausVid 1.3B), and one image-editing model (FLUX Kontext). Since the modulation vector is shared across all blocks, the guidance adds only a single forward pass through a small MLP per timestep.

3. **Human evaluation for core claims.** Unlike many papers that report only automatic metrics, Tables 2 and 3 report side-by-side human win rates. The 72% win rate for aesthetics on FLUX schnell and +22pp improvement for object counting are the paper's strongest evidence.

4. **Works on few-step models without CFG.** The paper correctly identifies that few-step models (e.g., FLUX schnell) do not use classifier-free guidance, making CFG-based improvement methods inapplicable. Modulation guidance fills this gap.

## Weaknesses

### Fatal
None.

### Major
1. **Modest methodological novelty.** Equation (3) — ŷ = y + w·(y(p₊,t) − y(p₋,t)) — is structurally identical to classifier-free guidance extrapolation, differing only in the representation being guided (modulation vectors rather than noise predictions). The paper builds on Garibi et al. (2025), which already demonstrated that CLIP can control the modulation space (line 96: "drawing inspiration from Garibi et al. (2025)"). The marginal technical contribution is repurposing this mechanism from *semantic editing* to *quality improvement*. This is an interesting application but not a fundamentally new form of guidance. The paper would be stronger if it acknowledged this more directly and framed its contribution as practical/empirical rather than methodological.

2. **Automatic metric gains are small without statistical significance.** In Table 2, PickScore gains are typically +0.1–0.2 (e.g., FLUX schnell: 22.9→23.1; SD3.5 Large: 23.0→23.1) and CLIP Score gains are 0–0.2, with one *decrease* (FLUX dev: 34.7→34.5, a −0.2 drop). The paper does not report variances, standard deviations, confidence intervals, or error bars for any automatic metric (confirmed via grep — no matches for "variance", "standard deviation", or "confidence interval"). These absolute gains are small enough that without statistical significance measures, it is unclear whether they are meaningful beyond measurement noise.

### Minor
1. **"Training-free" framing is imprecise.** The abstract (line 9) and introduction characterize the approach as "training-free." However, COSMOS (Table 2) requires fine-tuning for 4K iterations on 500K synthetic samples and CausVid (Table 4) requires 1K iterations to integrate the pooled embedding before the guidance can be applied. The paper *does* disclose this in the relevant sections, but the broad "training-free" claim in the abstract conflates two distinct settings: "training-free for models that already have a CLIP pooled embedding" vs. "requiring fine-tuning to add CLIP to models that lack it." Separating these cleanly would improve clarity.

2. **Dynamic modulation guidance is weakly motivated with marginal additional benefit.** The paper motivates the dynamic strategy (skipping early layers) only by analogy to dynamic CFG (line 112: "drawing inspiration from dynamic CFG"), which operates across *timesteps* (where noise levels vary significantly) rather than across *layers*. No theoretical or architectural rationale is given for why early transformer layers should not receive modulation guidance. The empirical comparison in Figure 3(a) shows a real but modest improvement — dynamic guidance achieves PickScore ~21.74 with CLIP Score ~30.8 vs. constant guidance's best of ~21.67 with CLIP Score ~30.4. The paper acknowledges "constant guidance is generally effective" (line 112) but does not justify why the added complexity of the dynamic strategy is needed.

3. **Specific-changes experiments use only FLUX schnell.** The object counting, hands correction, color, and position results (Table 3) are validated only on FLUX schnell. Since the general-changes experiments cover five models, this limited scope makes it unclear whether the specific-change benefits generalize.

4. **Sensitivity to prompt wording is not analyzed.** The method requires manual selection of positive/negative prompts for each targeted property (aesthetics, complexity, hands, etc.). The paper does not analyze how sensitive the results are to the exact phrasing of these prompts, nor does it report the success rate of interpretable directions (e.g., how often does "Long hair" vs. "Short hair" actually change hair length?).

### Trivial
None.

## Nice-to-Haves
- Include a simple prompt-engineering baseline (e.g., appending "high quality, detailed, award-winning" to prompts) to demonstrate that modulation guidance provides benefits beyond simple prompt modification.
- Add a comparison against increasing CFG scale (where applicable) to contextualize the method's benefit relative to an established knob.
- Extend specific-changes experiments to at least one additional model beyond FLUX schnell.

## Removed Points
- **Criticism about human evaluation lacking methodological detail (Critical Issue 3 from Harsh Critic):** The paper states "details in Appendix J" for annotator counts, instructions, etc. Per reviewer rules, appendix content stripped by the parser should not be penalized.
- **Criticism about "inactive CLIP" analysis conflating two claims (Critical Issue 6):** The paper clearly acknowledges the "partially inactive" nature and the prompt-length dependence. The suggestion that CLIP information could route through T5 is speculative and not required for the paper's analysis, which is an ablation study testing a necessary condition.
- **Claim that baseline comparison numbers (34%, 16%) are only in the appendix:** The main text at line 223 explicitly states: "our approach outperforms Normalized Attention Guidance by 34% and Concept Sliders by 16%." These numbers are in the main text, with supporting tables in Appendix E.
- **Claim that dynamic and constant guidance curves "nearly overlap":** The numerical description of Figure 3(a) shows dynamic guidance reaches PickScore ~21.74 with CLIP Score ~30.8, while constant guidance peaks at ~21.67 with CLIP Score ~30.4. The curves are clearly different, with dynamic maintaining higher CLIP score throughout.
- **Criticism about the frame overselling:** Subjective; the paper largely delivers on its core claims.
- **Request for analysis of interaction between attention guidance and modulation guidance:** Beyond the paper's stated scope.
- **Criticism about CausVid gains potentially reflecting fine-tuning rather than guidance:** Table 4 includes a "+CLIP" baseline row showing fine-tuning alone gives +0.10 total score, while modulation guidance adds +2.61 on top, demonstrating the guidance provides additional benefit.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Separately frame the two settings in the abstract: "training-free guidance for models with CLIP" vs. "fine-tuning to add CLIP + guidance for models without CLIP."
2. Report confidence intervals or error bars for automatic metrics, especially PickScore and CLIP Score where gains are small.
3. Include a prompt sensitivity analysis for at least one category to demonstrate robustness.
4. Extend specific-changes experiments beyond FLUX schnell to establish generality.

## Score and Decision

**Calibration details.**

*Round 1 (bracketing):* Searched "diffusion transformer text conditioning modulation guidance" across score bands:

| Anchor | Avg Score | Decision | Relevance | Comparison |
|--------|-----------|----------|-----------|-----------|
| Dreamguider (training-free guidance) | 4.00 | Reject | High | Training-free guidance method with limited novelty over prior work (MGD); the current paper has broader validation and human evaluation |
| AutoLoRA (guidance + LoRA) | 3.00 | Reject | Moderate | Straightforward extension with questionable improvements; current paper is clearly stronger |
| Universal Guidance for Diffusion Models | 5.25 | Accept | Moderate | Practical guidance method for multiple modalities; similar contribution level |
| Blending Concepts (Black-Scholes) | 4.75 | Reject | Low-Moderate | Prompt mixing with weak theory; current paper has stronger empirical validation |
| Dynamic Negative Guidance | 6.25 | Accept | Moderate | Principled dynamic theory but limited to MNIST/CIFAR10; current paper has broader experimentation but less theory |
| Feature-guided score diffusion | 5.50 | Reject | Moderate | Novel method but limited experiments; comparable overall quality |
| RB-Modulation | 8.00 | Accept | Low | Strong theoretical framework (stochastic optimal control); substantially stronger than current paper |

*Round 1 bracket:* 4.0–6.0.

*Round 2 (narrowing):* Searched "training free guidance diffusion models modulation" restricted to 4.0–6.0, confirming the same set of anchors and reinforcing the bracket.

*Final determination:* The paper sits between Dreamguider (4.00) and Dynamic Negative Guidance (6.25). It has genuine empirical contributions (inactive CLIP finding, broad validation, human evaluation) that elevate it above Dreamguider. However, the core guidance mechanism lacks methodological novelty (it is CFG-like extrapolation in modulation space, building on Garibi et al.), the automatic metric gains are small without error bars, and the framing is imprecise. These factors prevent it from reaching the level of Dynamic Negative Guidance (6.25). The most appropriate anchor is Feature-guided score diffusion (5.50, Reject) — both have moderately novel ideas but limitations in depth or validation.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>