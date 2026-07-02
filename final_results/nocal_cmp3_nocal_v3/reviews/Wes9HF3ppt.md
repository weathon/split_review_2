## Summary

This paper introduces Insertion Language Models (ILMs), which generate sequences by inserting tokens one at a time at arbitrary positions, using a denoising training objective where tokens are dropped (not masked) and the model learns to predict a normalized count distribution of dropped tokens per gap. The method is motivated by two identified limitations of Masked Diffusion Models: simultaneous unmasking that can violate sequential dependencies, and fixed-length masking that prevents arbitrary infilling. On synthetic planning tasks (star-graph path generation and zebra puzzles), ILMs clearly outperform both ARMs and MDMs, demonstrating genuine advantages for structured generation where neither left-to-right nor fixed-length parallel decoding is adequate. On text generation (LM1B, TinyStories), results are more mixed — ILMs beat MDMs but trail ARMs, particularly on LM1B where the NLL gap is substantial.

## Strengths

1. **The core idea is well-motivated and clean.** Section 2 identifies two genuine limitations of MDMs — simultaneous unmasking that violates sequential dependencies (the "chef added sugar... healthier" example, lines 13–14) and fixed-length masking that prevents arbitrary infilling (the "conference \<mask\> was postponed" example, line 14). ILMs drop tokens entirely and insert them one at a time, which straightforwardly addresses both issues.

2. **The star-graph experiments are convincing and diagnostic.** Table 1 shows ILM at 100/100/99.1 across Star_easy/medium/hard, while MDM drops to 21 on Star_hard and standard ARM is at 23. The progression from easy (symmetric, fixed arm lengths) to hard (asymmetric, variable-length arms) cleanly isolates the failure mode: MDMs collapse when absolute token positions become unreliable, and ARMs fail when the optimal generation order is not left-to-right.

3. **The zebra puzzle result (90.0%) is strong** — competitive with oracle-order ARM (91.2%) and well above standard ARM (81.2%) and MDM (82.6%). This is a non-trivial constraint satisfaction task where out-of-order generation matters, and it directly supports the paper's central thesis.

4. **The paper honestly acknowledges the biased training objective** (lines 79–80), stating that the exact marginalization has high variance and a tractable approximation is used instead. This transparency is appreciated, even though the effects of the bias are not empirically analyzed.

## Weaknesses

### Fatal
None.

### Major

1. **The abstract's "on par with ARMs" claim for text generation overstates the evidence.** On LM1B (Table 2), ARM NLL = 3.94 vs. ILM NLL = 4.67 — an 18.5% relative degradation. On Stories the gap is small (2.11 vs. 2.14), but the claim is stated globally without qualification. The paper attributes the LM1B gap to "training token efficiency and scaling laws" (line 215) but provides no controlled experiment (e.g., varying total tokens processed, not just gradient steps) to substantiate this. The abstract should either qualify the text claim or the NLL gap needs a rigorous explanation.

2. **The mismatch between the training objective and the inference procedure is acknowledged as "biased" but entirely unanalyzed.** The training loss (Equation 2) trains the model to predict a normalized count distribution over *all* dropped tokens in each gap simultaneously (e.g., if 3 tokens are dropped, the target is a distribution over which token goes in which gap aggregated across all of them). During inference, the model inserts one token at a time and re-evaluates. These are different operations. The paper does not: (a) analyze how the bias manifests, (b) compare against the exact but high-variance objective on a small-scale experiment, or (c) ablate whether this mismatch hurts performance on text tasks where the gap between inference and training protocol may matter most. The strong synthetic results suggest the approximation works in those settings, but the text results are weak enough that this bias could be a contributing factor.

### Minor

3. **The Prometheus LLM-judge evaluation (Figure 5) lacks numerical reporting.** The figure is described only in prose and shown as a bar-chart image. No actual scores, confidence intervals, or standard deviations are provided. The caption asserts that ILM "generally outperforms ARM and MDM across most metrics, particularly in coherence and consistency." Without numerical values this evidence cannot be verified or compared. Scores should be reported in a table.

4. **No ablation isolates which design choices drive the improvement over the Insertion Transformer (IT).** ILM differs from IT in several ways: the stop classifier, the biased count-based training objective, RoPE position encoding, and the denoising-style training with random token dropping. Table 1 shows IT performing much worse than ILM (35.2 vs. 100 on Star_easy), but the paper attributes this solely to the stop classifier vs. EOS (line 147). Without ablations varying one factor at a time, the contribution of each component is unclear.

5. **The "arbitrary length" claim is not tested beyond the training distribution.** All training and evaluation sequences are padded to 128 (LM1B) or 1024 (Stories) tokens. There is no experiment generating sequences substantially longer than those seen in training, so the claim is supported only by the mechanism (the stop classifier), not by empirical evidence.

6. **MDM baselines use the standard tau-leaping sampler** without the improved variants (greedy or top-k unmasking, flow-based formulation) that the paper itself cites in Related Work (Gong et al. 2024, Zheng et al. 2024, Campbell et al. 2024) as addressing the very limitation the paper critiques. Including at least one such variant would separate the effect of the ILM architecture from differences in the inference strategy.

7. **No comparison with fill-in-the-middle (FIM) ARMs on infilling.** The paper dismisses FIM (Bavarian et al., 2022) as "limited" (line 129) but does not benchmark it. FIM ARMs are a natural baseline for the infilling task, and their absence weakens the claim that ILMs are uniquely suited for infilling.

### Trivial

8. **Star graph naming is confusing:** ARM scores 32.3 on Star_easy but 75.0 on Star_medium. The paper explains this correctly (the optimal order is reverse on easy, but the start node is not the junction on medium), but the labels "easy" vs. "medium" are misleading without an early clarification.

9. **Figure 6 has an inconsistency:** the running text (line 215) describes MDM as red and ILM as blue, but the figure caption lists MDM (red), ARM (blue), and ILM (green). This should be corrected.

## Nice-to-Haves

- Add a compute-controlled experiment (matching total tokens processed, not just gradient steps) to determine whether the LM1B NLL gap is a compute artifact or a genuine limitation.
- Report Prometheus scores in a table with standard errors or confidence intervals.
- Include a sensitivity analysis for sampling temperature and its interaction with top-k (position) and nucleus (token) sampling.
- Report standard deviations or confidence intervals for all main results (Tables 1, 2, 3).

## Removed Points

These points were flagged by the harsh critic but are removed under the filtering rules; they should be treated with caution:

- "Section 3 description is dense and Equation 2 not fully explained" — removed as a presentation nitpick; the description is adequate for a conference paper.
- "Section 2.1 MDM limitation lacks a citation" — removed; this is an illustrative example of the paper's own motivation, not a claim that requires a citation.
- "Figure 6 caption garbled/contradictory" — merged into Trivial point 9; the core inconsistency is kept, the formatting complaint is removed.
- "No discussion of sampling temperature effects" — removed as nice-to-have; not a core flaw given the paper's scope.
- "No statistical significance or variance reporting" — removed as nice-to-have; single-run evaluation is standard for this setting.
- "Related Work creates tension about MDM baselines" — merged into Minor point 6.
- "Section 6 understates 'slightly worse'" — merged into Major point 1.
- Strength 4 (surfaces training difficulty honestly) — demoted from a strength to a neutrality; it is standard practice to acknowledge known limitations of one's method, not a distinctive contribution.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface a genuinely novel observation that the paper itself missed.

## Suggestions

1. **Recalibrate the abstract's text-generation claim.** Replace "on par with ARMs" with "competitive with ARMs on Stories, though with a clear gap on LM1B" to match the evidence.
2. **Add a small-scale ablation of the biased training objective.** On a synthetic task, compare the exact marginalization (with many samples), the proposed count-based approximation, and a naive alternative. This would show whether the approximation matters for the method's success.
3. **Report exact Prometheus scores in a table** (mean ± std) with clear indication of which comparisons are statistically meaningful.
4. **Include a stronger MDM baseline** using greedy or top-k unmasking (as cited in Related Work) in at least one text experiment, to separate architectural advantages from inference-strategy differences.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>