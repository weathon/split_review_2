Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper investigates learning dynamics differences between Transformers and modern state-space models (Mamba, Hyena) on associative recall (MQAR) and copying tasks. The central empirical finding is that SSMs are highly brittle to learning rate choice—succeeding only within an extremely narrow LR window—while Transformers maintain robust performance across orders of magnitude. Through extensive ablations (~3,000 runs), the paper also finds that contrastingly SSMs benefit from width scaling while Transformers need depth, that the 1D convolution is mechanistically critical for single-layer recall, and that DeltaNet achieves Transformer-level LR robustness. The paper argues that prior comparisons may have been confounded by optimization issues rather than pure expressivity limitations.

## Strengths

- **Clear demonstration of SSM learning-rate brittleness.** The core finding that Mamba and Hyena succeed only within an extremely narrow window of learning rates on MQAR (Figure 1), while Transformers maintain high performance across orders of magnitude, is well-supported and practically important. This finding alone justifies the study. **[weight=9.74]**

- **Convolution ablation is clean and informative.** Table 2 shows that removing the 1D convolution from a 1-layer Mamba drops its accuracy from 99% to 2%, and conversely, adding a convolution to a 1-layer Transformer raises its accuracy from 2% to 99%. This provides a crisp mechanistic link between architectural components and task performance. **[weight=10.01]**

- **DeltaNet comparison adds perspective.** Figure 7 shows that DeltaNet (Householder-based) maintains high MQAR accuracy across a wide range of learning rates, while Mamba2 only marginally improves stability over Mamba. This suggests a concrete architectural path toward more stable SSMs and is well-grounded in the discussion of off-diagonal gradient properties (Section 7). **[weight=8.90]**

- **Scale of experimentation.** The paper reports over 3,000 runs and ~20,000 GPU hours with 5 seeds per configuration, lending credibility to its empirical claims on the tasks studied. **[weight=10.07]**

## Weaknesses

### Fatal
None.

### Major

- **Central thesis is broader than the evidence supports.** The paper states its thesis (line 39) as: *"Transformers differ from SSMs not in terms of expressive power but mainly because of their optimization dynamics."* However, the paper's own Table 2 undermines the strength of this claim. A 1-layer Mamba **without convolution** achieves only 2% accuracy — the same failure point as the 1-layer Transformer — while adding a convolution to a 1-layer Transformer raises its accuracy to 99%. This shows that in single-layer models, the decisive factor is an **architectural/expressivity** component (the 1D convolution), not optimization. The paper partially acknowledges this in Section 7 (lines 202-203), noting that *"in terms of raw expressivity, a 1-layer Mamba without convolution performs approximately identically to a 1-layer Transformer,"* but the central thesis statement does not account for this tension. The paper would be stronger if it explicitly separated two distinct findings: (a) optimization instability confounds SSM performance in multi-layer settings (well-supported), and (b) architectural expressivity differences (convolution) determine single-layer capability (well-supported by Table 2 but in tension with the "mainly optimization" framing). **[weight=2.43]**

### Minor

- **Induction head claim for 1-layer Transformers lacks mechanistic evidence.** The paper lists as a contribution that single-layer Transformers exhibit dynamics *"resembling the induction head phenomenon"* (line 45, also in abstract and conclusions). The sole evidence is a loss bump in Figure 6. No attention map analysis, head-specific probing, or comparison with known induction head patterns (cf. Olsson et al., 2022) is provided. The paper uses hedged language ("resembles," "hypothesize," "attempts to form"), which is appropriate for the observation, but the absence of any mechanistic verification makes this too speculative to stand as a core contribution. Either mechanistic evidence should be added, or the claim should be explicitly demoted to an observation/hypothesis rather than a contribution bullet point. **[weight=0.21]**

- **Conclusions are drawn from synthetic tasks without downstream validation.** The paper acknowledges this limitation in one sentence (line 235), but continues to draw broad conclusions about *"fundamental learnability properties"* of these architecture classes. Without even a small-scale language modeling experiment (e.g., perplexity on a standard benchmark such as WikiText-103), it is unclear whether the LR sensitivity finding transfers to realistic setups. This is particularly relevant because practical training uses LR schedules (cosine decay, warmup) that the paper does not test. **[weight=-0.03]**

### Trivial

- **Zoology comparison could be more transparent.** The paper claims that prior work (Zoology) may have missed optimal LR windows for SSMs. While the paper shows the comparison visually (Figure 1 dashed lines, Figure 2 replication results), it would benefit from explicitly documenting Zoology's full LR grid to demonstrate conclusively that none of its values work for SSMs in the tested configurations. **[weight=3.09]**

## Nice-to-Haves

- Add LR schedule experiments (cosine decay, warmup) to verify whether the narrow LR window persists under realistic training regimes.
- A small-scale language modeling experiment (even 100M-parameter models on C4 or WikiText for a few thousand steps) would substantially strengthen the claim that the observed LR sensitivity matters in practice.
- The copying experiments (Section 5) could be expanded with more systematic depth/width sweeps, similar to the MQAR analysis in Sections 3-4.

## Removed Points

These points are flagged to be removed, treat them with caution:

- *"The central thesis is at odds with the paper's own evidence"* (Harsh Critic's Critical Issue 1) — Kept but downgraded from the harsh critic's framing. The paper does acknowledge the expressivity angle in Section 7 (lines 202-203). The issue is more about imprecise framing than contradiction.
- *"The induction head claim is not supported by the evidence"* (Critical Issue 2) — Kept but downgraded to Minor. The paper's language is appropriately hedged ("resembles," "hypothesize") but the evidence is thin for a listed contribution.
- *"Conclusions drawn from synthetic tasks alone"* (Critical Issue 3) — Kept as Minor since the paper does acknowledge this (line 235). The paper's core findings stand on their own on the tasks studied.
- *"Zoology comparison not fully transparent"* (Critical Issue 4) — Kept as Trivial. The paper shows both original results and replication with Zoology's code (Figure 2), which is reasonably transparent.
- *"Copying experiments underdeveloped"* — Removed. The comparison in Table 1 is parameter-matched (both 150M params), which is appropriate for the claim being made.
- *"No learning rate schedule experiments"* — Removed as scope-creep. The paper systematically studies constant LR and the finding stands on its own.
- Generic criticisms about missing related work, formatting, or reproducibility details — Removed per filtering rules.

## Novel Insights

None beyond the paper's own contributions. The core insight from the review process is that the paper's strongest finding (LR brittleness) and cleanest ablation (convolution) are somewhat in tension with the paper's ambitious framing — but this is a presentation issue rather than a novel discovery.

## Suggestions

1. **Reframe the central thesis to match the evidence.** The paper has two distinct findings that need not be unified under a single "optimization vs. expressivity" framing: (a) optimization instability (narrow LR window) in multi-layer settings, and (b) architectural expressivity differences (convolution) in single-layer settings. Presenting these separately would eliminate the tension between the thesis statement and Table 2.
2. **Either add mechanistic evidence for the induction head claim** (attention pattern analysis, probing experiments) or demote it from a contribution bullet point to an observation/speculation in the discussion.
3. **A small-scale language modeling experiment** (even at 100M-parameter scale) would substantially strengthen the paper's practical relevance and bridge the gap between synthetic findings and real-world applicability.

## Score and Decision

**Round 1 bracket:** The paper sits between the 4.50 anchor (Mimetic Initialization — similar topic but rejected for insufficient novelty and scope; our paper has stronger strengths and milder weaknesses) and the 8.00 anchors (Small-scale proxies for Transformer instabilities, Never Train from Scratch — well-validated papers with downstream experiments). Our paper has higher strength weights (avg ~9.68) than the 6.00 anchor (Understanding Bottlenecks, avg ~8.73) and milder weaknesses (no negative-weight items), but lower strength weights than the 8.00 anchor (Small-scale proxies, avg ~11.46).

**Round 2 narrow:** Comparing against the 6.0-7.0 bracket anchors, our paper's strengths are at the upper end and its weaknesses are at the milder end. The paper does not have the substantial methodological flaws or novelty concerns that pulled down the 4.5-5.5 anchors, but it also lacks the downstream validation and tighter framing that distinguish the 8.0 anchors.

**Calibration anchors consulted:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| iVy7aRMb0K (Mimetic Initialization) | 4.50 | R1 | Yes | Similar topic; our paper has stronger strengths and milder weaknesses |
| BwG8hwohU4 (StableSSM) | 5.33 | R1 | Yes | More theoretical; our paper is stronger empirically |
| QFgbJOYJSE (SSMs Provably Comparable) | 5.75 | R1 | Yes | Purely theoretical; our paper's empirical contribution is stronger |
| pymXpl4qvi (Understanding Bottlenecks) | 6.00 | R1 | Yes | Similar style of SSM analysis; our strengths are higher, weaknesses milder |
| d8w0pmvXbZ (Small-scale proxies) | 8.00 | R1 | Yes | Similar methodology (LR sensitivity); our paper has lower strength weights |
| PdaPky8MUn (Never Train from Scratch) | 8.00 | R1 | Yes | Very topically similar; our paper lacks downstream validation they had |

**Final placement:** The paper's strength weights (avg ~9.68) exceed those of the 6.00 anchor (avg ~8.73), and its weaknesses are uniformly mild (lowest weight -0.03 vs the 6.00 anchor's -2.16). However, the framing tension between the central thesis and Table 2, combined with the thin induction head evidence and lack of downstream validation, prevents the paper from reaching the level of the 8.00 anchors, which had either tighter framing or broader empirical validation. A score of **6.5** reflects this: the contributions are real and well-supported on their own terms, but the paper would benefit from recalibrating its claims to match its evidence more precisely.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>