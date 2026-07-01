## Summary

LoRA-Mixer places mixture-of-experts (MoE) routing at the attention projection layers (Q, K, V, O) rather than the FFN blocks, and proposes Routing Specialization Loss (RSL) — an entropy-regularized auxiliary loss — to balance load balancing with input-aware specialization. Experiments across three base models (Mistral-7B, LLaMA3-8B, Falcon-Mamba-7B) and multiple benchmarks show consistent improvements over baselines, with a data efficiency analysis suggesting RSL reduces the data needed for routing training.

## Strengths

- **Architectural motivation is concretely grounded.** Placing LoRA experts at the projection layers (Eq. 4) rather than FFN blocks is a well-argued design choice: projection layers directly feed the attention mechanism, making them a more expressive integration point. The claim that this is "drop-in compatible" with SSMs (Section 3.2) is plausible because SSMs also use linear projections.

- **Cross-model transfer experiment (Table 5) is genuinely informative.** Transferring routing parameters from Mistral-7B to LLaMA3-8B and observing non-trivial performance (GSM8K 5-shot: +3.5% relative gain) provides a real data point that RSL-learned routing captures transferable patterns rather than model-specific artifacts. This is the most distinctive result in the paper.

- **Data efficiency analysis (Table 9) directly tests the central claim.** Systematically varying training data from 1K to 10K and comparing with/without RSL is well-designed. The finding that RSL achieves comparable results with roughly half the data is the strongest evidence for RSL's practical value.

- **Honest limitation paragraph (Conclusion).** The acknowledgment that "fixed top-K routing may limit adaptability to ambiguous inputs" and that "uniformly applying it across all layers can introduce redundancy" identifies the right directions for future work.

## Weaknesses

### Fatal

None.

### Major

1. **The "LoRA" baseline in Table 2 compares a multi-expert system against a single expert, failing to isolate the routing contribution.** In every block of Table 2 (Falcon-Mamba, Mistral, LLaMA-3), the row labeled "LoRA" reports a single LoRA module, while LoRA-Mixer uses multiple experts with a learned router. The comparison conflates two differences: (a) multiple experts vs. one, and (b) the specific routing mechanism. A multi-expert system will naturally outperform a single-expert one on most tasks, so this setup does not demonstrate that the *routing mechanism* is effective. The paper should compare against: a multi-LoRA setup with the same number of experts but without learned routing (e.g., averaging), or a single LoRA with a higher rank to match the capacity.

2. **The number of experts (E) and the router architecture are not specified for the main experiments.** The paper defines LoRA-Mixer as using "E low-rank experts" (Eq. 4) and a router α(x) ∈ ℝᴱ, but never states the value of E used in Table 2 or what the router is (linear layer, MLP, etc.). Figure 3 shows 6 experts in an ablation, but the main comparisons are run with an unspecified configuration. Without this, the parameter efficiency claims and the comparison against baselines are uninterpretable.

3. **RSL's novelty relative to existing routing-optimized losses is not clearly articulated.** The paper cites AESL (Guo et al., 2025b), GMoE (Bai et al., 2024), and DsMoE (Pan et al., 2024) as "strong baselines that specifically optimize auxiliary losses" (line 134) and compares against them in Table 8, but never states how RSL differs technically from these methods. Entropy regularization for routing is not new, and the paper needs to either (a) articulate a clear technical distinction (e.g., AESL regularizes a different objective), or (b) moderate the claims of novelty. The current framing leaves the reader guessing what the actual contribution is.

### Minor

4. **The "48% of parameters" headline claim is ambiguous and lacks main-text support.** The abstract and introduction prominently claim using "48% of their trainable parameters," but the paper never states against which specific baseline this is measured (MixLoRA? MoLE? The average of all baselines?). The only pointer is "For parameter, training and inference analysis, please refer to A.4 A.7" (line 135) — the appendix is stripped here, but the main text should at minimum specify the comparison baseline and give a brief parameter count.

5. **Cross-model transfer results (Table 5) are mixed and oversold.** On ARC-E (0-shot), the transferred model *underperforms* the base LLaMA3-8B by 2.56 points (85.89 vs 88.45). On ARC-C, the gain is 0.49 points. The paper claims the routing is "extremely robust and transferable" (line 214), which overstates what the data support when one of three tasks shows a clear negative transfer.

6. **Several experimental details are omitted or unclear.** (a) The "LoRA" baseline's rank is stated only indirectly (line 238 suggests r=64 for Table 2, but this isn't labeled on the table); (b) Table 8 claims "all experiments are conducted with the same training data (2k) and LoRAs parameters" but GMoE, DS-MoE, and AESL are cited as full methods — it is unclear how the LoRA architecture is held constant while using different routing methods; (c) MedicalQA evaluation uses DeepSeek-R1 (line 136), and it is not stated whether all baselines were evaluated with the same protocol, which could introduce systematic bias; (d) no standard deviations or significance tests are reported despite averaging three runs.

7. **RSL underperforms the standard auxiliary loss at 4K data in Table 9** (78.77 vs 79.14, a −0.37 gap). The paper relegates the explanation to Appendix A.16. While not fatal, this reversal weakens the consistency of the data efficiency narrative and merits a main-text explanation.

8. **"CRL" (Cross-Router Loss) appears in the Figure 2 caption but is never defined or mentioned in the main text.** This is a missing piece that creates confusion.

9. **The hard-routing strategy (Section 3.2) is described but never experimentally evaluated.** The paper mentions it as a training regime but provides no experiments where it is used against baselines.

### Trivial

None.

## Nice-to-Haves

- A direct apples-to-apples comparison fixing the number of experts, rank, and training data, varying only expert placement (projection layers vs. FFN), would directly test the paper's central architectural thesis.
- Reporting standard deviations for the three-run averages would help assess whether the 1–4% improvements are meaningful.

## Removed Points

These points were flagged by the harsh critic but are removed with justification:

- **"15 benchmarks claim is inflated"** — Removed because GLUE's subtasks can reasonably be counted separately, making 15 a valid count.
- **"Empty URL and formatting errors"** — Removed per hard rules (parser artifacts, not author errors).
- **"Gradient derivation is mathematically routine"** — Removed as an opinion about presentation, not a substantive weakness.
- **"Missing related work"** — Removed because external confirmation of missing citations is unavailable.
- **"Abstract oversimplifies prior work"** — Removed as a subjective judgment; the characterization is broadly fair.
- **General speculation about the 48% claim being "geometrically unlikely"** — Kept the core point about ambiguity, but removed speculative reasoning about architectural geometry that depends on unreported expert counts.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's most useful observation is that the paper's evaluation would be strengthened by disentangling (a) the advantage of having more capacity (multiple experts) from (b) the effectiveness of the routing mechanism — but this is a standard evaluation-design point, not a novel insight.

## Suggestions

1. Replace the "LoRA" row in Table 2 with a multi-expert baseline that uses the same total capacity but without learned routing (e.g., uniform averaging or random selection). This would isolate what the routing mechanism contributes.
2. State the number of experts E and the router architecture explicitly for every experiment table.
3. Clarify the 48% parameter claim: specify the baseline it is measured against and provide a brief parameter count in the main text.
4. Add a paragraph distinguishing RSL technically from AESL and other existing routing losses — the reader should not have to infer the difference.
5. Discuss the negative ARC-E transfer result in the body text, not just the positive results.
6. Clarify whether GMoE/DS-MoE/AESL in Table 8 are being used as loss functions within the LoRA-Mixer architecture or as full independent methods, and describe how the architecture is held constant.

## Score and Decision

This paper identifies a reasonable architectural direction and includes genuinely useful experiments (cross-model transfer, data size ablation). However, the evaluation has significant uncontrolled variables: the main comparison table (Table 2) pits a multi-expert system against a single-expert baseline (LoRA) without isolating the routing mechanism, the number of experts and router architecture are unspecified for the core experiments, and the novelty of RSL relative to existing routing-optimized losses is unclear. These issues can be addressed with targeted additions and revisions, but in the current form the evidence does not fully support the claims.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>