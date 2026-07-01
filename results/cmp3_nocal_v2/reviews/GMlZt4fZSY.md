Now I have all the information I need. Let me write the final consolidated review.

## Summary

The paper presents MobileLLM-R1, a family of sub-1B reasoning models trained with data-centric techniques: leave-one-out analysis to quantify per-dataset utility, influence-function-based data mixing (Datamix), and iterative rejection-sampling-based mid-training compression. Trained on 4.2T total tokens resampled from ~2T unique tokens, MobileLLM-R1-950M outperforms comparable fully-open-source models (OLMo-2, SmolLM) and matches Qwen3-0.6B despite using only 11.7% of its training tokens.

## Strengths

1. **Well-designed leave-one-out analysis (Section 2.1.2).** The LOO experiments that train models with one dataset removed at a time, measuring NLL on capability-probing datasets, provide clean marginal-utility evidence without training on every subset combination. The finding that FineWeb-Edu acts as a "glue" across domains and that StarCoder boosts math more than OpenWebMath boosts code are non-obvious and empirically grounded.

2. **Controlled post-training comparison isolates pre-training contribution (Table 2).** Applying identical reasoning SFT data to all baselines is the correct way to isolate the effect of pre-training/mid-training quality. The fact that MobileLLM-R1* consistently outperforms SmolLM and OLMo-2 baselines under this controlled setup credibly supports the claim that their data curation pipeline produces better foundations for reasoning.

3. **Full openness commitment.** Releasing models, data recipes, and code enables reproducibility and follow-up work in an area where training data is often proprietary.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

1. **Mid-training "dip at 30K" description does not match the reported data (Figure 6).** The text (Section 3, page 6) states "the original data experiences a pronounced performance dip around 30K steps." But the table in Figure 6 shows the original curve at 30K is 38.0 (a *spike* from 28.5→28.5→28.5→38.0), while the actual dip occurs at 40K (38.0→31.0). This is a factual inaccuracy in the paper's own description of its result. The overall conclusion that subsampled data performs better is supported (subsampled achieves 40.5 vs. original's 31.0–33.0 in later steps), but the text should accurately describe the data.

2. **"Knowledge transfer from math to code" claim (Section 4.1 / Figure 7) is not supported by the experimental setup.** The paper states that the perplexity drop in HumanEval during mid-training "suggests that the knowledge acquired from math training is transferable to coding." However, the mid-training data is explicitly augmented with "additional mathematics and programming data" (line 193). The HumanEval improvement could simply reflect direct exposure to more programming data in mid-training, not transfer from math. The causal claim requires an ablation that isolates math-only mid-training data.

3. **"Closed-form solution" language is overclaimed (Section 2.2).** The paper states "we derive a closed-form solution for the data mixture ratio" (line 187). What is presented (Eqs. 2–5) is an influence-weighted averaging scheme that aggregates sample-level scores into dataset weights. This is a reasonable heuristic, not a closed-form solution to a well-defined optimization problem (e.g., minimizing an objective under constraints with an analytical minimizer). The language should be corrected.

4. **AIME headline number (15.5) lacks a clear, verifiable presentation in the main text.** The abstract claims "MobileLLM-R1-950M achieves an AIME score of 15.5." The main results section (Figure 9) is labeled "post-trained models" but the table entries show model variants with "-base" suffixes, and the detailed comparison is deferred to Appendix B.1 (stripped by the parser). While the appendix likely contains the full table, the main text should clearly present this headline result rather than relying on the abstract and a deferred appendix reference.

5. **The Ask-LLM model used for data filtering is not specified (Section 2.1.1).** The paper describes using the Ask-LLM paradigm for quality scoring but never states which model performs the evaluation. If it is a small model, the filtering quality is potentially weak; if it is a large proprietary model, the "fully open-source" framing is weakened. This detail should be disclosed even if it is in the appendix.

6. **Table 2 comparison does not fully control for instruction-tuning quality.** The comparison uses baseline instruct checkpoints against MobileLLM-R1* (Tulu-3-SFT checkpoint). While the final reasoning SFT stage is controlled, the initial instruction-tuning stage differs across models and may affect the results. The paper acknowledges this setup transparently, but the comparison is not a fully controlled pre-training ablation.

### Trivial

None.

## Nice-to-Haves

- Reporting variance or multiple-seed runs would increase confidence, especially for the small 140M/360M models where benchmark variance is typically higher. (This is not standard practice in large-scale pretraining papers, but the paper's claims would be strengthened by it.)
- A stronger baseline for the Datamix comparison in Figure 4 (e.g., simple heuristic upweighting of math/code data) would better demonstrate the value of the influence-based approach over simple alternatives.

## Removed Points

These points were flagged in the harsh review but are removed with justification:

1. **"2T unique tokens framing is misleading"** — The paper clearly distinguishes unique tokens (~2T) from total training tokens (4.2T). The abstract says "pre-training with 4.2T tokens on the dataset resampled from these ~2T tokens." The comparison to Qwen3's 36T is a comparison of total training tokens, which is fair. The criticism conflates clarity the paper already provides. **Removed** (not a valid weakness).

2. **"No variance or statistical significance reported"** — While technically true, single-run evaluation is the norm in large-scale LLM pretraining papers due to computational cost. This is not a standard expectation in this subfield. **Moved to Nice-to-Haves**.

3. **"Selection bias in mid-training rejection sampling"** — The reviewer speculates that discarding negative-influence samples may discard data valuable for generalization, but no evidence is presented that this occurs. This is a speculative concern, not an identified flaw. **Removed** (speculative, not verified from the paper).

4. **"Missing comparison to Phi/Gemma parameter-matched models"** — The paper compares to Gemma models in Figure 1 and elsewhere. Phi-3.5-mini is not included, but the paper scopes to "fully open-source" models, and not every comparison can be exhaustive. **Removed** (scope creep).

5. **"Model architecture details in appendix"** — The appendix was stripped by the parser; these details exist in the original submission. **Removed** (parser artifact).

6. **"Abstract overstates that second assumption 'remains largely unquestioned'"** — The word "largely" provides qualification, and while works on data pruning exist, the paper's framing is defensible. **Removed** (overstated criticism).

7. **Strengths removed as generic:** "Practical and well-motivated problem" is somewhat generic but partially grounded. However, it conflicts with weakness about framing. I'll keep it partially as it's about the problem being real. Actually, it's specific enough - the paper motivates small model sensitivity to noise and superposition interference. Let me keep it.

## Novel Insights

The reviewer's key insight is that the paper's strongest claims would benefit from tightening the evidence chain: the mid-training description has a factual imprecision (dip location), a causal claim about knowledge transfer is unsupported by the experimental design (mid-training data includes both math and code), and the headline AIME number is deferred to the appendix rather than presented in the main text. These are presentation/validation gaps, not methodology flaws - the core data pipeline is sound and the controlled Table 2 comparison is correctly designed.

## Suggestions

1. Correct the description of Figure 6: the original data spikes at 30K and dips at 40K, not the reverse.
2. Remove or qualify the "knowledge transfer from math to code" claim, or add an ablation with math-only mid-training data.
3. Replace "closed-form solution" with more precise language (e.g., "dataset weighting scheme based on influence scores").
4. Add the AIME score for the post-trained 950M model explicitly to the main results section, not just the abstract.
5. Disclose which model was used for Ask-LLM scoring.

## Score and Decision

This paper makes a real contribution: it demonstrates that careful data curation can substantially reduce the token budget for small reasoning models, and the controlled experiments (LOO analysis, uniform Datamix comparison, Table 2) provide credible evidence. The weaknesses are presentation-level and do not threaten the core claims. The methodology is sound, the results are empirically supported, and the openness commitment is valuable.

<score>7</score>
<decision>Accept</decision>