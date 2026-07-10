## Summary

This paper proposes HFPrune, a structured pruning method for LLMs that replaces the standard cross-entropy loss criterion in Taylor-based importance scoring with the information entropy of the model's full output distribution. The idea is that cross-entropy only considers the single next-token probability, while entropy captures the spread of all token probabilities, providing a more holistic (and label-free) signal for which neurons matter. Experiments on LLaMA-2-7B, LLaMA3.2-3.2B/1.2B, and Qwen2.5/3 models show consistent improvements over baselines (LLM-pruner, LoRAPrune, LoRAP, SDMPrune) at pruning ratios from 20% to 40%, and the method is ~3× faster and uses ~31% less peak GPU memory than SDMP-Prune.

## Strengths

- **Well-motivated, simple idea.** The paper identifies a genuine limitation of standard Taylor-pruning with cross-entropy (it scores importance based only on the single next-token probability) and proposes information entropy of the full output distribution as a clean, conceptually appealing alternative. (Section 1, Figure 1)

- **Consistent empirical wins across models and ratios.** HFPrune outperforms compared baselines on LLaMA-2-7B (Table 1), LLaMA3.2-3.2B/1.2B (Table 2), and Qwen series (Table 3) across pruning ratios from 20% to 40%. The pattern holds even at aggressive 40% pruning on Qwen2.5-7B where the gap to SDMPrune is 3.5pp (54.6 vs 51.1).

- **Clean ablation isolating the criterion.** Table 6 compares IE vs CE vs SD criteria *without any fine-tuning*, directly measuring the quality of the importance scores themselves. HFPrune wins at both 20% and 30% ratios, confirming that the entropy criterion itself drives the improvement, not the fine-tuning. (Section 5.3.1, Table 6)

- **Direct evidence of distribution preservation.** Table 7 shows that IE-pruned models have lower JS divergence and higher Top-15 Jaccard similarity to the original model's output distribution than CE-pruned models, providing evidence for the claimed mechanism. (Section 5.3.2, Table 7)

- **Practical efficiency advantage.** HFPrune is ~3× faster and uses ~31% less peak GPU memory than SDMP-Prune during the pruning process itself (Table 5), a meaningful practical benefit.

## Weaknesses

### Fatal

None.

### Major

- **The central claim — "minimizing the change of the global prediction distribution" — does not follow from the math (framing overreach).** The importance score is $I(h_i) = |\partial C_H/\partial h_i \cdot h_i|$ where $C_H(x) = -\sum p_j(x) \log_2 p_j(x)$ is the *scalar entropy*. The paper repeatedly states (lines 70, 75, 120, 173) that the method "minimizes the change of the global prediction distribution," and Figure 1(b) depicts it as minimizing changes to each individual token probability $\{\Delta p_i\}$. However, entropy is a scalar summary — two entirely different probability vectors can have identical entropy. The gradient $\partial H/\partial h_i$ tells you about changes to aggregate uncertainty, not about which specific token probabilities shift. The method is better described as using a more distributionally holistic *scalar proxy* rather than directly minimizing change to the full distribution. This is a framing overreach, not an invalidation of the method, but it should be corrected to accurately represent what the math accomplishes.

- **The claim that pruning "exceeds the original dense model" is an unfair comparison.** Line 80 states that at 20% pruning on LLaMA2-7B, the pruned model "not only recovers but even exceed[s] the performance of the original dense model" (59.0% vs 58.3% in Table 1). However, the pruned model is fine-tuned on LaMini instruction data (LoRA, 2 epochs), while the original dense model is **not fine-tuned at all**. The 0.7pp improvement could simply reflect the benefit of LoRA fine-tuning on 43K instruction examples. A proper control requires fine-tuning the original model under the same LoRA protocol and comparing against that.

### Minor

- **No statistical significance or variance reporting.** Across all tables, every result is reported as a single number without confidence intervals, multiple seeds, or any indication of variance. Many win margins are small (0.5–1.0pp on 10-way averages in Tables 1 and 6), and zero-shot benchmarks have known non-trivial variance. Without variance estimates, the reader cannot assess the reliability of claimed improvements. While single-run evaluation is common practice in this field, the small margins make this limitation more consequential here.

- **Selective baselines on Qwen models.** On LLaMA models, HFPrune is compared against four baselines (LLM-pruner, LoRAPrune, LoRAP, SDMPrune). On Qwen models (Table 3), only SDMPrune is used. The paper states "For brief, we focus on the comparative experiments with the previous best methods, SDMPrune" (line 256), but this assumes the ranking from LLaMA transfers to Qwen without verifying it. This weakens the generalizability claims about the Qwen results.

- **MLP-only vs attention&MLP comparison does not control for total compression.** In Table 8, "20% pruning ratio" means 20% of each module's parameters, so MLP-only at 20% removes ~13.6% of total parameters while attention&MLP at 20% removes ~17.6%. The paper concludes "MLP-only pruning consistently outperforms attention&MLP pruning" (line 321) without discussing this compression confound. (Note: this actually makes the MLP-only conclusion *directionally stronger* since it removes fewer total params and still outperforms, but the experiment as presented conflates *where* and *how much* is pruned.)

### Trivial

None.

## Nice-to-Haves

- The paper could provide qualitative examples showing whether the pruning decisions made by IE vs CE differ in interpretable ways (e.g., does IE keep neurons that affect low-probability tokens while CE discards them?). This would strengthen the mechanistic story.
- A brief discussion of when the entropy gradient itself might become uninformative (very peaked or very uniform output distributions) would strengthen the paper, mirroring its own critique of SDMP's zero-gradient problem.

## Removed Points

These points are flagged to be removed, treat them with caution:

- *"FLOPs reduction claim is imprecise"*: The abstract says "20% parameters and FLOPs reduction." Since only MLP modules are pruned (~68% of params), this is imprecise but is a minor presentation issue, not a substantive weakness — removed as a formatting/precision nitpick.
- *"Zero-gradient problem underexplored"*: The reviewer notes the paper criticizes SDMP's zero-gradient issue but does not analyze when the entropy gradient itself becomes uninformative. This is a nice-to-have expansion, not a core weakness.
- *"Section-by-section notes about Taylor expansion assumptions, uniform pruning"*: These describe standard practices or acknowledged limitations; none constitute genuine weaknesses.

## Novel Insights

The most penetrating observation from the review process is that the paper's central mechanistic claim (minimizing change to the "global prediction distribution") is not supported by the actual computation, which only minimizes change to the scalar entropy — a proxy, not the full distribution. This insight, captured in Weakness 1, is not present in the paper itself and represents a genuine critical finding. Beyond this, the paper's own contributions (entropy as a Taylor-pruning criterion, label-free importance scoring, empirical wins across families) are the primary novel content.

## Suggestions

1. **Reframe the contribution**: Replace "minimizing change of global prediction distribution" throughout with phrasing that accurately describes what the method does — using entropy as a scalar proxy for distributional preservation that captures more holistic information than cross-entropy. The method remains valuable under this corrected framing.
2. **Add a control experiment**: Fine-tune the original dense model on LaMini under the same LoRA protocol and report its performance alongside the pruned-and-fine-tuned model before making "exceeds original" claims.
3. **Add statistical significance indicators**: Report results with multiple seeds or bootstrapped confidence intervals, especially for the small-margin comparisons in Tables 1 and 6 and the distribution-preservation metrics in Table 7.
4. **Run at least one additional baseline on a Qwen model** to verify the ranking transfer assumption.
5. **Clarify Table 8**: Explicitly state the total parameter reduction in each condition and note that the comparison supports MLP-only under conservative assumptions.

## Score and Decision

**Calibration anchor comparison:**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| Survey paper (irrelevant) | 8QTpYC4smR.md | 1.00 | 1 | No | Much weaker; not a pruning paper |
| EfficientSkip | 7DY2DFDT0T.md | 2.50 | 1 | No | Much weaker; limited experiments |
| MoreauPruner | Y0qmwm6tgy.md | 4.80 | 1 | Yes | Less strong empirical results; unclear motivation |
| LLM Pruning & Distillation | mMmzHS28ht.md | 5.00 | 1 | Yes | Significant perf degradation at modest compression |
| LoRAPrune | 9KVT1e1qf7.md | 5.20 | 2 | Yes | Severe PPL degradation even at 20% pruning |
| What Matters in Transformers | YLTWwEjkdx.md | 5.50 | 2 | No | Similar pruning study, moderate scores |
| Reassessing Layer Pruning | EjHtQlKEzV.md | 4.50 | 2 | No | Benchmarking study, lower scores |
| OWL | pOBvr1PxFd.md | 6.00 | 1 | Yes | Strong high-sparsity results but methodological concerns (circular logic) |
| The Unreasonable Ineffectiveness | ngmEcEer8a.md | 6.50 | 1 | Yes | Clean execution, accepted — but simpler task (layer pruning) |
| Plug-and-Play | Tr0lPx9woF.md | 6.50 | 1 | Yes | Cleanly executed, accepted — stronger on execution rigor |

**Round 1 bracket**: 5.5–6.5. The paper is clearly stronger than MoreauPruner (4.8), LLM Pruning & Distillation (5.0), and LoRAPrune (5.2), all of which had significant performance degradation issues that this paper does not share. It is comparable to OWL (6.0) but without OWL's methodological confusion (circular logic in motivation). It is not as cleanly executed as Plug-and-Play (6.5, accepted) or The Unreasonable Ineffectiveness of the Deeper Layers (6.5, accepted).

**Final score placement**: At **6.0**. The shared high-magnitude items with anchors in the 5–6 range (+9+ strengths for good empirical results, -9+ weaknesses for missing controls) put this paper above LoRAPrune and MoreauPruner. Its two Major weaknesses (framing overreach, unfair comparison) are fixable and do not threaten the core claim — unlike OWL's more fundamental methodological issues. However, it lacks the executional polish of the 6.5-level accepted papers, which had stronger controls and cleaner framing. A revision addressing the two Major weaknesses could move this to the 6.5+ range.

**Decision rationale**: The paper has a genuinely novel core idea (entropy as Taylor-pruning criterion), consistent positive results across model families and pruning ratios, and a clean ablation isolating the criterion's effect. The two Major weaknesses are framing/evidential issues that can be fixed without new experiments (reframing the central claim, adding a control for the "exceeds original" comparison). The paper does not reach the 6.5+ tier only because the framing overreaches what the math supports, not because the empirical results are weak.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>