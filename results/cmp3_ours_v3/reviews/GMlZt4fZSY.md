## Summary

This paper introduces MobileLLM-R1, a family of sub-billion parameter reasoning models (140M/360M/950M) trained with a highly data-efficient pipeline. The core contribution is a principled, influence-based data curation framework: (1) cross-capability influence scores guide the pre-training data mixture, and (2) a data-model co-evolution mechanism iteratively filters mid-training data. Using only ~2T unique tokens (4.2T total with repetition) — roughly 11.7% of Qwen3's reported 36T corpus — MobileLLM-R1-950M matches or surpasses Qwen3-0.6B on several reasoning benchmarks and substantially outperforms fully-open models like OLMo-2-1.48B and SmolLM2-1.7B, despite having fewer parameters.

## Strengths

1. **Verified empirical advantage at much smaller scale.** Table 2 directly shows MobileLLM-R1-950M achieving MATH 57.8, GSM8K 68.5, and LCBv6 13.7 — outperforming OLMo-2-1.48B (53.0, 58.8, 11.4) and SmolLM2-1.7B (41.4, 50.5, 7.4) despite having ~40% fewer parameters. The 360M model similarly beats both 135M and 362M baselines. These numbers are directly verifiable in the paper's main body.

2. **Principled and interpretable data curation methodology.** The leave-one-out analysis (Section 2.1.2, Equation 1, Figure 3) provides clean, causal evidence about which data sources contribute to which capabilities. The finding that FineWeb-Edu acts as cross-domain "glue" across all three capabilities, and that StarCoder benefits math more than OpenWebMath benefits code, are empirically grounded and go beyond conventional wisdom.

3. **Genuinely novel data-model co-evolution procedure.** The iterative influence-based filtering scheme (Section 3), where the model progressively discards negative-influence samples from its own training set, is a procedural contribution. The convergence argument (influence scores concentrating near zero by phase 2, Figure 5) is plausible, and the MMLU results (Figure 6) showing subsampled data consistently outperforming the original set provide compelling validation.

4. **Full open-source release.** The paper commits to releasing all models, curated data, and training recipes — a valuable community resource that directly supports reproducibility.

## Weaknesses

### Major

1. **The headline token-efficiency claim ("4.2T vs 36T") conflates total vs. unique tokens and excludes curation costs.** The abstract and introduction repeatedly state "11.7% of Qwen's 36T" as the central efficiency claim. The paper clarifies that its 4.2T is total tokens (with ~2x repetition over ~2T unique), but it never clarifies whether Qwen's 36T represents unique tokens or total tokens seen. If Qwen's 36T is unique tokens (the standard meaning of "corpus"), the comparison is between apples (4.2T total with repetition) and oranges (36T unique). Furthermore, the claimed efficiency does not account for the compute cost of the curation method itself: training three domain-specialized models ($\theta_{\mathcal{C}}, \theta_{\mathcal{M}}, \theta_{\mathcal{K}}$) to convergence and computing influence scores at 10 checkpoints each. The FLOPs comparison in Figure 1 partially addresses compute efficiency, but the paper's verbal framing ("11.7% of tokens") throughout the abstract, introduction, and conclusion lacks this qualification. This does not invalidate the results but means the efficiency claim is overstated.

2. **The AIME 15.5 headline claim is not cleanly verifiable from the main body.** The abstract claims "MobileLLM-R1-950M achieves an AIME score of 15.5, compared to just 0.6 for OLMo-2-1.48B and 0.3 for SmolLM-2-1.7B." However, the AIME results table in the available text (Figure 9 section) is garbled and does not cleanly present this number for MobileLLM-R1-950M. The text only states that the model "achieves scores comparable to the partially open-source Qwen3 series" on AIME, with detailed comparisons deferred to Appendix B.1 (stripped by the parser). While parser artifacts affect table rendering, the paper's most striking quantitative claim deserves clear, unambiguous presentation in the main body.

3. **The "identical SFT" comparison in Table 2 does not fully isolate pre-training quality.** The paper claims this comparison "disentangles" the contribution of pre-training data quality, but the design has a confound: baselines use their existing instruct/SFT checkpoints, while MobileLLM-R1* uses an intermediate Tulu3-SFT checkpoint (2 epochs). Different models arrive at the "identical" reasoning SFT with different post-training histories, data distributions, and training durations. A cleaner isolation would start all models from their base (not instruct) checkpoints and apply identical two-stage SFT. The observed advantage may partly come from a better post-training pipeline rather than purely from pre-training data curation. The paper acknowledges the setup in the caption but the conclusion drawn from it ("models with stronger pre-training... exhibit more robustly embedded knowledge") overreaches.

### Minor

4. **"The second assumption remains largely unquestioned" framing is overstated.** Several recent works on data curation for small models (SmolLM2, DCLM, Phi-3) have explicitly argued that data quality can substitute for scale. The paper's real contribution — the *specific* influence-based method for achieving this — is impactful on its own without needing to characterize the assumption as "largely unquestioned."

5. **The Ask-LLM scoring model is not specified.** Section 2.1.1 describes scoring samples using the "Ask-LLM paradigm" (Sachdeva et al., 2024) but never states which model performs this scoring. If a large model (e.g., Qwen or DeepSeek) is used, this creates a dependency on the very class of models the paper seeks to supplant. If a small model is used, its reliability needs discussion. This matters because the entire data mixture optimization depends on the quality of these probing sets.

6. **The influence score approximation via AutoMixer is described only by citation.** Equation 2 defines the influence score requiring the Hessian inverse, acknowledged as computationally prohibitive. The paper cites AutoMixer for an efficient approximation but does not describe what approximation is used or whether its assumptions hold for this setting. The reliance on ~10K-sample representative subsets to make computation tractable introduces a sampling approximation whose quality is not empirically evaluated (e.g., stability of mixture weights under different random subsets).

### Trivial

7. **MobileLLM-R1-140M achieves near-floor performance** (MATH 4.8, GSM8K 3.7), so claims of "substantial gains" at this scale should be tempered. The gains over SmolLM2-135M (3.2, 1.6) are real but small in absolute terms.

## Nice-to-Haves

- Quantify the compute cost of curation (training domain-specialized models, computing influence scores) and include it in the efficiency comparison.
- Perform stability analysis of the influence-based mixture weights under different random subsets, checkpoint selections, or weighting schemes.
- Run the Table 2 comparison from base (not instruct) checkpoints with identical two-stage SFT to cleanly isolate pre-training quality.
- Add a data repetition analysis comparing 2T unique tokens vs. 4.2T with repetition to clarify whether the benefit comes from curation or simply from repeating high-quality data.
- Report model architecture details (layers, hidden dimensions, heads) in the main text.

## Removed Points

- *Issue about the 4.2T vs 4.4T token discrepancy* (removed: the 4.2T figure refers to pre-training only; adding 200B mid-training yields 4.4T total, but the paper's efficiency claims center on pre-training where 4.2T is consistent).
- *Criticism about missing related works* (removed per policy: cannot verify without external sources).
- *Criticism about missing appendix details* (removed per policy: parser strips appendices; original submission contains them).
- *Criticism about missing model architecture details* (downgraded from weakness to nice-to-have: these are standard details likely in the appendix; valuable but not a core flaw).
- *Formatting/style nitpicks* (removed per policy: parser artifacts, not author errors).
- *Request for more baselines* (removed: the paper already compares against OLMo, SmolLM, and Qwen — the key comparison partners).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Clarify whether Qwen3's 36T represents unique or total tokens; if the former, reframe the token-efficiency comparison to use unique-token counts on both sides and include curation FLOPs in the accounting.
2. Present the AIME 15.5 result in a clean, dedicated table in the main body with the number explicitly tied to MobileLLM-R1-950M, rather than deferring to the appendix.
3. Specify the model used for Ask-LLM scoring and discuss its reliability.
4. Provide a brief description of the AutoMixer approximation and its assumptions in this setting, or cite a specific section of the original work that addresses them.

## Score and Decision

**Calibration Anchors (all rounds):**

| Anchor | Path | Avg Score | Round | Comparison |
|--------|------|-----------|-------|------------|
| Gradient-based Optimization of Dataset Mixtures | VdURgvImVn.md | 4.20 | 1 | Similar data mixture topic, but tested only on toy problems; current paper has vastly stronger empirical validation |
| Small-to-Large Generalization | 79ZkWgY2FI.md | 5.25 | 1 | Empirically solid but weak correlation results; current paper demonstrates real deployed models beating 2×-larger baselines |
| Improving Influence-based Instruction Tuning Data Selection | dCTGFl3lN2.md | 4.25 | 1 | Influence-based selection on related topic but marginal improvements; current paper's results are more decisive |
| Demystifying CLIP Data | 5BCFlnfE1g.md | 6.75 | 1 | Reproducible data curation pipeline; current paper has more methodological novelty but some presentation issues |

**Round 1 Bracket:** 5.5–7.5 (the paper's empirical contributions and methodological novelty clearly exceed the 4–5 range, but the framing issues around token efficiency and the unverifiable AIME claim prevent it from reaching the 8+ tier)

**Final calibration reasoning:** The paper is stronger than the 4–5 range alternatives (which lack comparable empirical validation) and comparable in strength to Demystifying CLIP Data (6.75), but with more methodological novelty offset by presentation weaknesses. A score of 6.5 reflects genuine contributions held back by framing issues that are fixable.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>