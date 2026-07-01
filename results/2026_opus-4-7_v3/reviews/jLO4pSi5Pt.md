Now I have read the full paper. Let me verify the key reviewer claims against specific sections before drafting my review.

Let me check a few more details:
- The BEM class prior estimation (Eq. 9)
- The DP counter increment (Eq. 4)
- The K inconsistency
- Table 6 ablation structure

Now let me draft the consolidated review and then calibrate.Now let me do Round 1 — Bracketing calibration:Let me read a few key anchors to calibrate:Now I have sufficient calibration data. Let me form my assessment.

**Round 1 Bracket:**

| Band | Anchor | Score | Comparison to L-TTA |
|------|--------|-------|---------------------|
| Strong reject (<1.5) | Lifelong ReID (5lUdTogEL3) | 1.00 | Not comparable — L-TTA is a genuine contribution |
| Reject (1.5–3.5) | Active TTP (pdzHpQbGrn) | 2.50 | L-TTA far stronger: novel problem, novel mechanisms, comprehensive experiments |
| Borderline reject (3.5–5.5) | BLG (BUDxvMRkc4) | 4.67 | L-TTA stronger: more novelty (EP mechanism), broader experiments, more compelling problem. BLG was criticized for limited novelty |
| Borderline reject (3.5–5.5) | LT-LVLM (9RnTw9YiXV) | 4.40 | L-TTA is a methods paper with concrete solutions, not just analysis |
| Borderline accept (5.5–7.5) | DOTA (yD2JMeKumt) | 6.00 | L-TTA has more novelty and stronger experimental coverage than DOTA; DOTA was rejected despite uniform 6s |
| Borderline accept (5.5–7.5) | RLCF (kIP0duasBb) | 6.67 | Comparable — both novel TTA contributions for VLMs, L-TTA has broader experiments but also has evaluation gaps |
| Borderline accept (5.5–7.5) | Concept Drift (b20VK2GnSs) | 7.00 | Similar: both address novel problem settings at VLM × distribution shift intersection. L-TTA has cleaner experiments but evaluation gaps |
| Accept (7.5–8.5) | READ (TPZRq4FALB) | 8.00 | READ is stronger: unanimous 8s, novel paradigm with strong benchmarks; L-TTA has more evaluation gaps |

**Initial bracket: 5.5–7.0.** L-TTA is clearly above the borderline-reject range (BLG at 4.67, ROSITA at 4.67) and sits within the borderline-accept range, comparable to DOTA-RLCF-Concept Drift papers (6.0–7.0).

Now let me write the final consolidated review.

---

## Summary
This paper introduces Long-Tailed Test-Time Adaptation (L-TTA) for Vision-Language Models, identifying two failure modes unique to VLM-based TTA under long-tailed distributions (Text-induced Tail Erosion and Modality-bias Amplification). The proposed method combines three components: Synergistic Prototypes (with novel Exclusionary Prototypes that update for all classes at every step), Rebalancing Shortcuts (learnable adapters with class re-allocation loss), and Balanced Entropy Minimization (a modified EM objective with theoretical justification). Experiments span 15 datasets, three benchmarks, three imbalance ratios, and five backbones, demonstrating consistent improvements in both accuracy and Macro-F1.

## Strengths
- **Exclusionary Prototypes are a genuinely novel mechanism (Section 3.2, Eq. 5).** The key insight that EPs can be updated for *all* classes at every step—using prediction distributions to capture inter-class exclusion information—directly addresses the cold-start problem for tail-class prototypes. The weighting coefficient φ_c (Eq. 5) elegantly down-weights ambiguous samples while maintaining universal updates. This is the paper's most distinctive contribution and differs meaningfully from TDA's "negative cache," which only updates the predicted class.

- **Comprehensive and rigorous experimental coverage (Tables 1–5).** The evaluation spans 15 datasets across three benchmarks (OOD, Cross-Domain, Corruption), three imbalance ratios (10, 20, 50), five backbones (ViT-B/16, ViT-L/14, ViT-H/14, SigLIP-L/16, MetaCLIP-BigG), and 12 baselines. Crucially, the paper reports Macro-F1 alongside accuracy—the metric that matters most for class-balance claims. L-TTA achieves the best Macro-F1 across nearly all settings, with particularly strong gains at higher imbalance ratios (e.g., OOD Average Macro-F1 at imb=50: 59.78 vs. next-best 58.08).

- **Competitive efficiency (Table 4).** L-TTA runs in 1.45h vs. 2.96h for SCAP and 27.7h for WATT, while achieving better results. The design choice to freeze prompts and instead optimize lightweight shortcuts avoids gradient propagation through the backbone.

- **Well-motivated problem formulation (Section 1, Figure 1).** The identification of two VLM-specific failure modes under long-tailed TTA is concrete and empirically supported. The observation that unimodal TTA methods (SAR) degrade when applied to VLM backbones (Figure 1, b.2) provides clear justification for a bi-modal solution.

## Weaknesses

### Fatal
None

### Major
- **BEM's online prior estimation lacks convergence analysis (Eq. 9).** The class prior π is described as "continually updated based on the current predicted pseudo-labels." Since the core problem BEM addresses is that head classes dominate predictions, the pseudo-labels used to estimate π will themselves be biased toward head classes. The paper provides no analysis of whether this estimated prior converges to the true distribution, how estimation errors propagate through BEM's rebalancing, or under what conditions the circularity is self-correcting. The ablation on β (Figure 4d) tests penalty strength but not prior estimate quality. BEM works empirically (the results are clear), but this gap weakens the theoretical narrative built around Propositions 1 and 2 — the propositions analyze BEM's gradient properties but assume a known prior structure.

- **No rebalancing-augmented baseline isolates the source of gains (Section 4).** All 12 baselines are methods designed for balanced TTA, reproduced with their original hyperparameters. None attempts any long-tailed correction. A natural ablation would combine a strong existing method (e.g., TDA or DPE) with simple post-hoc logit adjustment using estimated class frequencies. Without this, it is impossible to determine how much of L-TTA's improvement comes from its specific mechanisms (EP, RS, BEM) versus the fact that it is the only method attempting rebalancing at all. This is a methodological gap in the evaluation design, not a flaw in the method itself, but it limits confidence in calibrating the magnitude of the contribution.

### Minor
- **Synthetic long-tailed construction (Section 4).** Long-tailed test sets are created by subsampling balanced datasets to produce exponentially decayed class curves. This means only class frequency changes; within-class feature distributions are unchanged. In naturally long-tailed data, tail classes often also exhibit higher intra-class variance or domain-specific visual challenges. While this is a reasonable starting point for a new problem setting, it limits confidence that L-TTA's improvements transfer to organic long-tailed distributions.

- **DP counter increment ambiguity (Eq. 4).** The text states N_{c,s}^{DP} "increases by 1 at each step." It is unclear whether this counter increments only when class c actually receives an update, or at every step regardless. If the latter, tail-class prototypes that are rarely updated would have their subsequent updates progressively diluted by a growing denominator, which would contradict the goal of enriching tail representations. The same phrasing appears for EPs (where universal increment makes sense since EPs update all classes). This ambiguity should be resolved.

- **Hyper-class vector representation unanalyzed (Eq. 6–7).** The Rebalancing Shortcuts use K hyper-class vectors as shared prototype modifiers via cross-attention, with an MoE-inspired load-balancing loss. However, no visualization or analysis reveals what the hyper-class vectors learn to represent, whether they capture meaningful semantic clusters, or how the learned clusters relate to head/tail class structure. This would strengthen the mechanistic understanding.

### Trivial
- **K default inconsistency.** The implementation details state K = 0.3 as the default, but the ablation in Section 4.2 states "setting K = 0.2 yields the best performance." This minor inconsistency should be clarified — the experiments apparently use K = 0.3 but the ablation suggests 0.2 is better.

## Nice-to-Haves
- Plot the estimated prior π versus the true class distribution at different points in the data stream across different imbalance ratios, to validate BEM's convergence behavior. This single analysis would do more to validate BEM than additional benchmarks.
- Include at least one baseline combining TDA or DPE with simple logit adjustment using estimated class frequencies, to isolate the contribution of L-TTA's specific mechanisms vs. "any rebalancing at all."
- Provide per-class accuracy curves (head vs. tail) more prominently — the paper defers these to the appendix, but for a paper whose central thesis is head-tail rebalancing, such breakdowns deserve main-text visibility.
- Discuss failure cases or regimes where L-TTA might not help. The near-uniform improvement across all settings is impressive but a brief characterization of limitations would add credibility.
- Evaluate on at least one naturally long-tailed dataset (e.g., iNaturalist, Places-LT) to complement the synthetic construction.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Propositions 1 and 2 lack proofs in the main text"**: Proofs are deferred to Appendix A, which is standard practice. The appendix is stripped by the parser and exists in the original submission. Removed per rules.
- **"Proposition 1 assumes head classes have higher logits"**: This concern depends on inspecting the appendix proof, which is stripped. Cannot verify. Removed per rules.
- **"P̃ notation is confusing in Eq. 9"**: This is a notation/formatting nitpick. Removed per rules.
- **"Table 7 dynamic shift variation is within noise"**: The reviewer frames this as both a concern and a positive. The small variation across ε values actually supports the paper's claim of robustness to sample ordering. The observation favors the paper. Removed.
- **"No failure case discussion"**: This is a generic critique applicable to any paper. Removed as non-specific, but retained as a nice-to-have suggestion.
- **"Rich classes vs. head classes distinction not quantitatively analyzed"**: The paper introduces this distinction in Figure 1(b.1) as motivation. The concept serves its purpose — the experiments address the downstream consequence via Macro-F1 evaluation. Removed as a presentation preference, not a substantive weakness.

## Novel Insights
The Exclusionary Prototype mechanism — using prediction distributions from all samples to update prototypes for all classes at every step — is a genuinely novel contribution to prototype-based TTA. The key insight that inter-class exclusion information (what features are *least* likely for a class) can enrich tail-class representations without requiring tail-class samples to appear is distinctive and potentially applicable beyond this specific setting (e.g., few-shot learning, continual learning). The φ_c weighting that naturally down-weights uncertain samples while maintaining universal updates is an elegant design choice.

## Suggestions
1. **Directly analyze BEM's prior estimation quality** by plotting estimated π vs. true class distribution at multiple stream positions across different imbalance ratios. If it converges, the theoretical grounding is solid; if not, characterize when BEM remains effective despite misestimation.
2. **Add a rebalancing-augmented baseline**: combine TDA or DPE with logit adjustment using estimated class frequencies to isolate L-TTA's mechanism-specific gains.
3. **Clarify the DP counter semantics**: explicitly state whether N_{c*,s}^{DP} increments only on actual updates or at every step, and justify the design choice.
4. **Resolve the K = 0.3 vs. K = 0.2 inconsistency** between implementation details and ablation findings.
5. **Visualize hyper-class vector clusters** to show what the K vectors in Rebalancing Shortcuts learn to represent.

## Score and Decision

### Calibration Anchors

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| Lifelong ReID (5lUdTogEL3) | 1.00 | R1 | Not comparable — L-TTA is a genuine research contribution |
| IC-Light (u1cQYxRI1H) | 10.00 | R1 | Retrieved as low-score anchor but actually a 10; not comparable |
| Humanoid Robots NLP (gwZ90hFSL2) | 1.00 | R1 | Not comparable — fundamentally different scope and quality |
| LLM Survey (8QTpYC4smR) | 1.00 | R1 | Not comparable — survey paper |
| Active TTP (pdzHpQbGrn) | 2.50 | R1 | L-TTA far stronger: novel problem, novel mechanisms, comprehensive experiments |
| Prototypical Evaluation VLM (ZaudLwn0Hm) | 2.50 | R1 | L-TTA far stronger in novelty and experimental breadth |
| LLM2CLIP (HfJxXbXlYJ) | 3.00 | R1 | L-TTA has stronger experimental evidence and more novel problem setting |
| LVLM-CL (JIlIYIHMuv) | 2.50 | R1 | L-TTA is more comprehensive and novel |
| BLG (BUDxvMRkc4) | 4.67 | R1 | L-TTA has more novelty (EP mechanism), broader experiments; BLG criticized for limited novelty |
| ROSITA (lF9QXpfNHm) | 4.67 | R1 | L-TTA has more novel mechanisms and broader evaluation |
| InCPL (Rc3RP9OoEJ) | 5.00 | R1 | L-TTA has more distinct novelty and stronger experimental coverage |
| LT-LVLM (9RnTw9YiXV) | 4.40 | R1 | L-TTA provides concrete solutions, not just analysis |
| Concept Drift MLLM (b20VK2GnSs) | 7.00 | R1 | Comparable: both novel problem settings at VLM × distribution shift intersection; L-TTA has cleaner experiments but evaluation gaps |
| DOTA (yD2JMeKumt) | 6.00 | R1 | L-TTA has more novelty and stronger experimental coverage; DOTA rejected despite uniform 6s |
| RLCF (kIP0duasBb) | 6.67 | R1 | Comparable: both novel TTA contributions for VLMs; L-TTA has broader experiments |
| Few-shot TTA (TD3SGJfBC7) | 6.25 | R1 | Comparable quality; L-TTA has a more novel problem setting |
| READ (TPZRq4FALB) | 8.00 | R1 | READ is stronger: unanimous 8s, novel paradigm, complete benchmarks |
| VL Data-Type (WyEdX2R4er) | 8.00 | R1 | Different topic; higher quality analysis |
| Two Effects CLIP (uAFHCZRmXk) | 8.00 | R1 | Different topic; deep analysis paper |
| Hyperbolic VLM (3i13Gev2hV) | 8.00 | R1 | Different topic; strong theoretical contribution |

**Round 1 bracket: 5.5–7.0.** L-TTA is clearly above the borderline-reject papers (BLG 4.67, ROSITA 4.67, InCPL 5.00) and sits within the borderline-accept range. It is stronger than DOTA (6.00, rejected) in novelty and experimental scope, comparable to RLCF (6.67, accepted) in overall contribution quality, and slightly below the concept drift paper (7.00, accepted) which had a similar "novel problem + comprehensive method" profile but fewer evaluation concerns.

**Narrowing to final score:** L-TTA's strengths (novel problem setting, genuinely novel EP mechanism, comprehensive experiments across 15 datasets and 5 backbones, competitive efficiency) put it solidly in the accept territory. The two major weaknesses (BEM prior estimation unanalyzed, no rebalancing baseline) are real but neither threatens the core contribution — the experimental gains are consistent and the EP mechanism is independently valuable. The paper is stronger than DOTA (6.00) and comparable to RLCF (6.67). The novel problem formulation and experimental breadth push it slightly higher than RLCF. However, the evaluation gaps (no rebalancing baseline, synthetic-only LT data) prevent it from reaching the 7.0 level of the concept drift paper.

**Final score: 6.5.** This is a borderline accept — the novel problem setting, genuinely innovative EP mechanism, and comprehensive experimental coverage constitute a meaningful contribution. The evaluation gaps are addressable in a revision and do not undermine the core claims.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>