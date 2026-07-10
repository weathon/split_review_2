Now let me write the final consolidated review.

## Summary

This paper introduces Insertion Language Models (ILMs), which generate sequences by inserting tokens one at a time at arbitrary positions. The key innovation is a denoising objective where tokens are dropped from the input (rather than masked), and the model learns to predict normalized count distributions over vocabulary items for each gap. A stopping classifier determines when generation is complete, enabling variable-length output. The paper evaluates ILMs against ARMs and MDMs on planning tasks (star graphs, zebra puzzles) and text generation/infilling (LM1B, TinyStories).

## Strengths

- **Clear targeting of genuine MDM limitations.** The paper isolates two concrete problems with MDMs — simultaneous unmasking violating token dependencies, and fixed mask counts preventing arbitrary-length infilling — and the ILM design directly addresses both. The running example in Section 2 ("The chef added \<mask\> to the dessert to make it \<mask\>") clearly illustrates the simultaneous-unmasking problem.

- **Strong diagnostic planning experiments.** The star graph experiments (Table 1) are the paper's most compelling contribution. The progression from Star_easy (symmetric fixed-length arms) to Star_hard (asymmetric variable-length arms) cleanly exposes MDMs' reliance on absolute positions. ILM achieves 100% and 99.1% exact-match accuracy on medium and hard variants versus MDM's 36.5% and 21.0% — a striking gap. The qualitative trajectories (Appendix C.0.3) support the claim that ILMs solve the task iteratively by generating from both ends.

- **Zebra puzzle results corroborate the planning advantage.** ILM (90.0%) outperforms both MDM (82.6%) and ARM (81.2%) on a challenging constraint satisfaction task, approaching the oracle-order ARM (91.2%), demonstrating that out-of-order generation helps beyond the star graph setting.

- **Transparent about limitations.** The Discussion (Section 6) explicitly acknowledges that ILMs underperform ARMs on text, cannot cache hidden states, and that scaling remains future work — a level of honesty that makes the paper's claims trustworthy even where results are modest.

- **Complementary text quality evaluation.** The Prometheus LLM judge (Figure 5) provides evidence beyond the Llama-based NLL metric, showing ILM generally outperforming ARM and MDM on coherence, consistency, and fluency — partially mitigating concerns about NLL's ARM bias.

## Weaknesses

### Major

- **MDM baseline omits inference-time techniques that address the paper's own criticism of MDMs.** The paper identifies simultaneous unmasking as a key MDM limitation (Section 2) and the Related Work (Section 4) describes greedy unmasking (Gong et al., 2024), top-k unmasking (Zheng et al., 2024), and flow-based sequential sampling (Campbell et al., 2024) — all designed to make MDM generate sequentially. None are tested. The paper states these are slow (Section 2: "one may achieve sequential generation from MDMs by greedily unmasking the most confident position, but this leads to slow generation"), but speed is a secondary concern; the primary claim is about generation *quality* and *flexibility*. Since these techniques operate at inference time without retraining, their omission means the claimed advantage over MDMs is demonstrated only against the weakest sampling strategy (vanilla tau-leaping). Adding these baselines would clarify whether ILM's advantage is over the sampling strategy or the MDM paradigm itself. This affects the paper's most central comparative claim.

- **Training objective bias is acknowledged but uncharacterized.** The training objective (Eq. 2) trains the model to predict normalized counts of vocabulary items aggregated over all dropped tokens in each gap. During inference, however, the model inserts tokens one at a time sequentially. The paper explicitly calls this an "approximate denoising training objective" (p. 3) and defers variance analysis to Appendix D (stripped), but provides no analysis — theoretical or empirical — of how aggregate-to-sequential transfer affects generation quality, what specific bias this introduces, or under what conditions it might degrade. The strong planning results suggest the bias is not catastrophic, but for a paper whose core contribution is a training paradigm, this gap undermines understanding of what the model actually learns.

### Minor

- **Abstract overclaims text generation performance.** The abstract states ILMs "perform on par with ARMs" in unconditional text generation, but on LM1B the NLL gap is 0.73 (ARM 3.94 vs. ILM 4.67, Table 2) — a ~20% relative degradation — while on Stories the gap is only 0.03 (ARM 2.11 vs. ILM 2.14). The paper attributes the LM1B gap to "training token efficiency and scaling laws" (Section 5.3.1) without direct evidence for why the gap differs so dramatically between datasets. The Introduction and contribution list use more appropriate language ("competitive with ARMs"); the abstract should be revised to match.

- **No variance or confidence intervals on any experiment.** All results in Tables 1–3 are point estimates without standard deviations or confidence intervals. While the large margins in planning results (e.g., 100% vs 36.5%) are robust, the small text differences (ARM 2.11 vs ILM 2.14 on Stories) cannot be assessed for statistical significance without this information.

- **Contradiction in Figure 6 color labeling.** The figure caption states "MDM (red line), ARM (w/o KV cache) (blue line), and ILM (green line)" while the main text says "the MDM (red) ... the ILM (blue)." This must be resolved for the comparison to be interpretable.

- **NLL under Llama has known ARM bias.** Llama-3.2-3B is an ARM and will assign higher likelihood to text matching left-to-right patterns, disadvantaging both MDM and ILM in the ARM comparison. The Prometheus evaluation partially addresses this, but precise scores are only shown in a figure rather than a table, making the comparison less precise.

### Trivial

None.

## Nice-to-Haves

- Compare against the Insertion Transformer (Stern et al., 2019) on text tasks, not just planning. IT already underperforms on planning (35.2% on Star_easy), but a text comparison would isolate the contribution of ILM's new training objective and stopping classifier.
- For the star graph medium/hard tasks, provide variance across random seeds for the reported accuracies.
- Include a direct test of the motivating example: given a sentence with a single obvious gap, measure whether ILM can produce variable-length infills while MDMs cannot (beyond what the current infilling evaluation already demonstrates).

## Removed Points

These points were flagged for removal; treat with caution:

- **"Infilling evaluation does not test arbitrary-length claim"** — REMOVED. The evaluation does test this: single-segment and multi-segment tasks require filling missing tokens without knowing the exact count in advance, directly demonstrating the arbitrary-length advantage over MDMs.
- **"ARMO baseline incomplete for medium/hard"** — REMOVED. The optimal order is well-defined for Star_easy (reverse) but not for medium/hard; the dashes are justified.
- **"Section-by-section notes about missing related work, framing nitpicks"** — REMOVED as speculative, not specific to the paper, or scope-creeping.

## Novel Insights

The harsh critic correctly identifies that the star graph diagnostic is the paper's strongest contribution — the progression from symmetric fixed-length arms to asymmetric variable-length arms cleanly demonstrates that MDMs' reliance on *absolute positions* is a genuine limitation that ILMs overcome through iterative insertion using relative positions. This is a more informative demonstration than typical "diffusion beats AR on planning" benchmarks because it isolates the causal mechanism (position encoding) rather than just reporting aggregate accuracy differences. The critic also astutely notes that the aggregate-count training objective may not teach the model proper sequential dependencies between tokens inserted into the same gap, which is a nontrivial methodological concern that the paper does not address.

## Suggestions

1. **Add MDM baselines with sequential decoding.** Test MDMs with greedy unmasking (Gong et al., 2024) and top-k unmasking (Zheng et al., 2024) on at least the star graph and zebra puzzle tasks to isolate whether ILM's advantage is over the sampling strategy or the MDM paradigm.
2. **Characterize the training bias empirically.** Even a small-scale synthetic experiment comparing the biased objective against a proper Monte Carlo estimate (with variance reduction) would clarify whether the aggregate-to-sequential mismatch degrades generation quality.
3. **Revise the abstract.** Replace "perform on par with ARMs" with "are competitive with ARMs" to match the more careful language used in the Introduction and contribution list.
4. **Report confidence intervals.** Add standard deviations over multiple seeds for key results, especially where differences are small (e.g., ARM vs ILM on Stories).
5. **Fix the Figure 6 color description.** Resolve the contradiction between caption and text.

## Score and Decision

**Score: 5.5**

**Decision: Reject**

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>