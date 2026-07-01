Now I have all the information I need. Let me write the final review.

## Summary

This paper investigates how reasoning data (math, science, code QA pairs) injected at different training stages (pretraining vs. SFT vs. RL) affects downstream reasoning performance. It pretrains 8B models from scratch for 1T tokens with different reasoning data mixtures (small high-quality D_SHQ, large diverse D_LDQ, combined D_LMQ) and evaluates after SFT and RL. The paper claims an asymmetric principle: diversity and scale matter most during pretraining, while quality dominates during SFT, and that front-loading reasoning into pretraining creates a compounding 19% advantage.

## Strengths

1. **Large-scale, systematic experiments.** Pretraining 8B models from scratch for 1T tokens with multiple data variants across a fully crossed design (4 base models × multiple SFT recipes) represents a substantial empirical investment that is rare in the literature.

2. **The SFT data quality finding is clean and well-supported.** Table 5 shows that fine-tuning reasoning-pretrained models on small, high-quality D_SHQ (44.99 avg) massively outperforms fine-tuning on large, diverse D_LDQ (31.54) or D_LMQ (31.21). This comparison properly controls for the pretraining confound by averaging across multiple pretrained models, and the size of the gap (13+ points) makes the finding robust.

3. **The reasoning ratio ablation (Tables 6–7) provides practical guidance.** Increasing the proportion of reasoning data during pretraining from 20% to 40% improves reasoning benchmarks while preserving general-domain performance, with a modest trade-off on instruction following. This gives actionable guidance for data mixture design.

4. **Timely and practically relevant research question.** The core investigation—whether reasoning data should be front-loaded into pretraining or added later—directly addresses an active debate given the current industry trend toward reasoning-focused models and the prohibitive cost of pretraining.

## Weaknesses

### Major

1. **Repetition confound undermines the "diversity vs. quality in pretraining" comparison.** The central comparison establishing "pretraining benefits most from broad diversity" (11% gain) compares M_SHQ (54.98, trained on 1.2M unique high-quality examples) against M_LDQ (64.09, trained on 268M unique diverse examples). The paper controls for token budget (80B reasoning tokens in both cases) but the paper explicitly states: "When a reasoning dataset is small, it is repeated so that the model still observes the same total volume of reasoning tokens." To reach 80B tokens, D_SHQ must be repeated ~130× while D_LDQ has minimal repetition. The observed 9-point gap could be substantially driven by M_SHQ overfitting from heavy repetition rather than M_LDQ benefiting from diversity per se. The paper provides no validation perplexity, loss curves, or any overfitting analysis to distinguish these explanations. This confound directly affects the headline claim that "diversity drives pretraining effectiveness (11% average gain)."

2. **RL gain confounded by data overlap.** The 19% RL advantage (Table 3: M_base + SFT_SHQ + RL: 37.92 vs. M_LMQ + SFT_SHQ + RL: 56.66) compares a model that saw D_SHQ only during SFT against one that saw D_SHQ during **both** pretraining and SFT (since D_LMQ = D_LDQ + D_SHQ). The benefit cannot be cleanly attributed to "reasoning data in pretraining" in general, since M_LMQ specifically saw the exact SFT dataset twice. A cleaner comparison (e.g., M_LDQ + SFT_SHQ + RL, where D_LDQ does not include D_SHQ) is not provided.

3. **"Catch-up" experiment is too narrow to support the claim that "SFT cannot compensate."** The catch-up test (Table 4) only doubles SFT epochs on the same 1.2M-example D_SHQ dataset. This does not test whether more SFT data, more diverse SFT data, multiple rounds of SFT, or alternative SFT strategies could close the gap. The paper's conclusion—"proving that SFT cannot compensate for a weak foundation" (Section 4, repeated in Abstract)—far outstrips the evidence, which only shows that 2× epochs on the same narrow dataset is insufficient.

4. **"Latent effect" conflates data overlap with latent capability.** The finding that M_LMQ (50.95) outperforms M_LDQ (46.70) after SFT on D_SHQ is attributed to a "latent effect" of high-quality pretraining data. However, M_LMQ's pretraining corpus includes D_SHQ—the exact dataset used for SFT. The model has been exposed to the formatting, reasoning style, and distribution of D_SHQ during pretraining, making it better able to absorb similar data during SFT. This is better described as *in-distribution priming* than a latent capability. Disentangling these explanations would require SFT on a dataset not seen during pretraining.

### Minor

5. **No limitations discussion or acknowledgment of confounds.** The paper makes strong causal claims (e.g., "proving," "conclusive evidence") without ever acknowledging the repetition confound, the data overlap issue, or the narrow catch-up test. Adding a limitations section that honestly discusses these issues would substantially improve the paper's scientific rigor.

6. **No variance or statistical significance estimates.** All results are reported as point estimates without error bars, confidence intervals, or significance tests. While single-run large-scale pretraining is the norm, given the strength of the comparative claims, some variance quantification (e.g., across evaluation seeds) would strengthen the evidence.

### Trivial

7. **SFT sample count is unclear.** Section 3.1 states models are "finetuned on 4.8M reasoning samples from D_res" but D_SHQ has only 1.2M unique samples. It is unclear whether D_SHQ is repeated during SFT or mixed with other data.

## Nice-to-Haves

- Report validation perplexity or loss curves for M_SHQ vs. M_LDQ to directly assess whether the repetition-heavy condition leads to overfitting.
- Add a comparison controlling for unique example count (e.g., subsample D_LDQ to 1.2M unique examples and compare to D_SHQ at the same token budget).
- Disentangle the RL gain by comparing against a model pretrained on D_LDQ (which excludes D_SHQ) + SFT_SHQ + RL.
- Evaluate on additional non-reasoning benchmarks beyond GPR and IFEval to check for capability degradation from injecting reasoning into pretraining.

## Removed Points

- **"Missing evaluation on non-reasoning benchmarks (MMLU categorized under Science)":** The paper does evaluate GPR (ARC, HellaSwag, WinoGrande, RACE) for base models and IFEval for SFT models. The reviewer's broader concern about capability degradation is valid but the claim that these evaluations are missing is not accurate. Moved to Nice-to-Haves.
- **Reproducibility concerns about proprietary data:** The standard format issue; many large-scale industry papers face this limitation. Not unique to this paper.
- **Clarification about "4096 tokens" being unclear (tokens vs characters):** The paper clearly states "tokens." This criticism is factually incorrect.
- **Statistical significance as a structural weakness:** Single-run large-scale pretraining without significance tests is the norm in this setting. Retained as a minor note.

## Novel Insights

The most interesting structural observation from the review process is an inverse relationship between novelty and evidential support: the paper's cleanest finding (SFT quality-over-diversity, Table 5) is the least novel, largely confirming established post-training wisdom, while its most novel claims (the pretraining asymmetry principle, the latent effect, the catch-up refutation) all have confounds that make the evidence substantially weaker than the paper's language suggests. This pattern is worth noting as a common failure mode in ambitious empirical work.

## Suggestions

1. **Scale back the central claims.** Replace "diversity drives pretraining effectiveness" with a more measured claim: "large-scale diverse reasoning data in pretraining substantially outperforms small-scale repeated high-quality data (but the comparison is confounded with unique-example count)." The current language overstates what the experiment cleanly shows.

2. **Add an overfitting analysis.** Report validation perplexity or loss curves to directly address whether M_SHQ's lower performance is due to overfitting from repetition.

3. **Disentangle the RL gain.** Compare M_base + SFT_SHQ + RL against M_LDQ + SFT_SHQ + RL (where D_LDQ does not include D_SHQ) to isolate the effect of general reasoning exposure from the effect of double-dipping on the same data.

4. **Add a limitations section** that honestly discusses the repetition confound, data overlap issue, and narrow catch-up test.

## Score and Decision

**Calibration Round 1 (Bracketing):** Five query bands searched the human-review corpus.
- *Strong-reject band* (< 1.5): No topically similar papers found; returned generic low-quality papers (scores ~1.0–1.4). Our paper clearly does not belong here.
- *Lower band* (1.5–3.5): Returned papers on tangentially related topics (e.g., LogicJitter 2.50, Supervised CoT 2.50). Our paper is substantially stronger in scope and experimental scale.
- *Middle band* (3.5–6.5): Returned "Disentangling Reasoning Tokens" (4.67, Reject), "Scaling Mathematical Reasoning" (5.25, Reject), "Amuro and Char" (4.20, Reject), "Expanding the Web" (3.67, Reject), and "Advancing Mathematical Reasoning" (5.71, Accept). Our paper is most similar in topic and scale to the last two.
- *Upper band* (5.5–8.5): Returned "At Which Stage Does Code Data Help" (7.25, Accept) — the closest topical match, a paper on code data placement across training stages. That paper had a token-count confound that was addressable in rebuttal, leading to accept.
- *Strong-accept band* (> 8.5): No similar papers found.

**Round 1 bracket: 4.0–6.0.** Our paper has larger-scale experiments than the 4–5 range papers but has more serious confounds than the 7.25 anchor.

**Narrowing (Round 2):** Searched the 4.0–6.5 band, returned "Advancing Mathematical Reasoning" (5.71, Accept with mixed reviews 8,1,3,8,8,6,6). That paper accepted despite some very low scores because its strongest supporters (8,8,8) valued the empirical contribution highly. Our paper lacks that strength of conviction from even its best-case interpretation due to the structural confounds.

**Final assessment relative to anchors:**
- vs. "At Which Stage Does Code Data Help" (7.25, Accept): Our paper has comparable scale but its central confounds are more severe and harder to address. Accept for that paper but not for ours.
- vs. "Amuro and Char" (4.20, Reject): Our paper has stronger experiments (8B vs 1B, 1T tokens vs limited checkpoints) but similar issues with overclaimed conclusions relative to evidence.
- vs. "Advancing Mathematical Reasoning" (5.71, Accept): Mixed reviews but ultimately accepted. Our paper has broader scope (math + science + code) but more fundamental experimental design issues.

**Final score rationale:** The paper has genuine contributions (the SFT quality finding, the large-scale empirical investment) but the central and most novel claims are undermined by confounds that are not acknowledged. The asymmetric principle's pretraining half is not cleanly demonstrated. The SFT half is solid but less novel. The paper overclaims substantially relative to what the experiments can support.

<score>5.0</score>
<decision>Reject</decision>