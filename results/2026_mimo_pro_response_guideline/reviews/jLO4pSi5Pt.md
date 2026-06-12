Now I have enough data to calibrate. Let me finalize my assessment.

**Calibration Anchors Summary:**

| Anchor | Score | Decision | Round | Comparison |
|--------|-------|----------|-------|------------|
| 5lUdTogEL3 (Lifelong ReID) | 1.00 | Reject | R1 | Unrelated topic, much weaker paper |
| gwZ90hFSL2 (Cross-Lingual Robots) | 1.00 | Reject | R1 | Unrelated, clearly weak |
| pdzHpQbGrn (Active TTA for VLMs) | 2.50 | Reject | R1 | Related topic but weaker method, less evaluation |
| RwiUmrEHgR (Long-tail Cost-Sensitive Loss) | 3.00 | Reject | R1 | Topically related but basic approach |
| BUDxvMRkc4 (BLG: LT vision with CLIP) | 4.67 | Reject | R1 | Topically close; two-stage training, weaker eval, underperforms on many classes |
| lF9QXpfNHm (ROSITA: Open-world TTA) | 4.67 | Reject | R1 | Related TTA method; less comprehensive evaluation |
| yD2JMeKumt (DOTA: Distributional TTA) | 6.00 | Reject | R1 | Closely related TTA for VLMs; our paper is clearly stronger with more extensive eval |
| kIP0duasBb (RLCF: TTA with CLIP reward) | 6.67 | Accept | R1 | TTA for VLMs; comparable novelty, our paper has more comprehensive evaluation |
| b20VK2GnSs (Concept Drift in MLLMs) | 7.00 | Accept | R1 | Addresses long-tail+OOD in pre-training; different setting but similar scope |
| 75PhjtbBdr (Multi-Label TTA with BEM) | 6.25 | Accept | R1 | Related TTA method; our paper addresses a more important and harder problem |
| TPZRq4FALB (READ: Multi-modal TTA) | 8.00 | Accept | R1 | Strong paper: new challenge + clean methodology; our paper has more extensive eval but some clarity issues |
| uAFHCZRmXk (Modality Gap in VLMs) | 8.00 | Accept | R1 | Analysis paper on VLMs; different contribution type |

**Round 1 Bracket: 6.5–7.5**

Our paper is clearly above DOTA (6.0, reject) which is a related TTA-for-VLMs paper with much less comprehensive evaluation. It's comparable to or slightly above RLCF (6.67, accept) and the concept drift paper (7.0, accept). It's slightly below READ (8.0, accept), which has all 8s, cleaner methodology, and novel benchmarks, though our paper has more extensive evaluation across 15+ datasets. The minor formulation clarity issues (Eq. 6, Eq. 9, vague propositions) are real but fixable and don't undermine the core contribution.

**Final score: 7.0** — This paper is a solid contribution that opens a genuinely new research direction, proposes a well-motivated and co-designed method, provides extremely comprehensive evaluation, and has only minor clarity issues that are addressable. It sits above the reject line (DOTA at 6.0) and below the strongest accept papers (READ at 8.0) in this space.

---

## Summary
This paper proposes L-TTA, the first method for Long-Tailed Test-Time Adaptation of Vision-Language Models. It identifies two VLM-specific failure modes (Text-induced Tail Erosion and Modality-bias Amplification) and introduces three co-designed components—Synergistic Prototypes (with Deterministic and Exclusionary Prototypes), Rebalancing Shortcuts with Class Re-Allocation loss, and Balanced Entropy Minimization—to address them. Evaluation spans 15+ datasets across three benchmark suites (OOD, Cross-Domain, Corruption) with three imbalance ratios and multiple backbone architectures.

## Strengths
- **Novel problem formulation with concrete failure mode analysis**: The paper is the first to study TTA under long-tailed distributions for VLMs, identifying two specific failure modes—Text-induced Tail Erosion (text embeddings carry pre-training biases that intensify tail erosion, Fig. 1b.1) and Modality-bias Amplification (unimodal LT-TTA methods amplify cross-modal misalignment, Fig. 1b.2). This is a genuinely important gap since real-world test sets are rarely balanced.

- **Exclusionary Prototypes (EPs) provide a novel update mechanism**: Unlike TDA's negative cache (line 110), EPs (Eq. 5, lines 106-110) update prototypes of all classes using every view's prediction distribution, weighted by φ_c. This ensures tail-class prototypes accumulate information from every sample, directly addressing the cold-start problem ("Tail-class prototypes are more likely to be uninitialized at the beginning phase," line 98).

- **Theoretically grounded BEM**: Proposition 1 (line 132) formalizes why standard EM produces opposing gradient signs for head vs. tail classes, and Proposition 2 (lines 140-142) proves BEM shrinks this gradient gap. The penalty term (1 − P̃)^β elegantly scales class-prior adjustments by prediction confidence, avoiding the pitfall that naive logit adjustment "may further exacerbate the model's bias toward the head classes" (line 134).

- **Extensive and consistent empirical results**: At Imb=50 OOD Average, L-TTA achieves 59.78 macro-F1 vs. 54.05 for the next best (WATT), a +5.73% gap (Table 1). On the Cross-Domain benchmark, average macro-F1 gain is +2.20% (Table 2). On the Corruption benchmark, +2.64% macro-F1 improvement (Table 3). The improvements grow as imbalance worsens.

- **Clean component ablation and cross-backbone generalizability**: Table 6 shows each component contributes (DP→68.68/63.40, SyP→70.94/65.17, full→71.30/65.83 Acc/Mac on ViT-B/16). Table 5 shows consistent ~1.5% Acc / ~1.8% Mac gains across ViT-L/14, ViT-H/14, SigLIP-L/16, and MetaCLIP-BigG.

- **Good efficiency-performance trade-off**: L-TTA runs in 1.45h with 1.89G memory (Table 4), competitive with DPE (1.38h) and much faster than RLCF (18.30h) and WATT (27.70h).

## Weaknesses

### Fatal
None

### Major
None

### Minor
- **Eq. 6 underspecifies how the hyper-class vector j is selected in the RS update**: The formula `v_c ← Attn([v_c, t_c], q_j)q_j + v_c` (line 114) references a single q_j with K hyper-class vectors but does not explicitly state that j* = Argmax_j' Attn([v_c, t_c], q_{j'}) (top-1 routing). Eq. 7's CRA loss (line 118-120) defines c_{c,j}(v) = 1(j = Argmax_{j'} ...), which implies this routing, but the main update equation should be explicit. Additionally, K is introduced as a count ("assume there are K hyper-class vectors," line 112) but set to 0.3 in implementation (line 208) while Figure 4c labels the axis b with range 0.2–1.0. The paper should clarify K is a fraction of C and state the resulting integer count.

- **Undefined notation P̃ in BEM (Eq. 9)**: In z' = z − (1 − P̃)^β log(π/Σπ_i) (line 136), P̃ is used without formal definition. From context (line 44: "prediction confidence," line 138: "reduces the contribution of confident classes"), it is max_c P(y_c|x̃), but this should be stated explicitly. The notation H'(P̃) on the left side further suggests P̃ is an input argument to a function, adding confusion.

- **Vague conditions in Propositions 1 and 2**: Both propositions state "We split C into C_head and C_tail with certain measurements" (lines 132, 140). The operational definition is given later (line 206: "top-20% classes as head"), and proofs are in Appendix A. The proposition statements in the main text should include the specific split criterion rather than "with certain measurements."

### Trivial
- **Prototype initialization not discussed**: The paper does not mention how DPs and EPs are initialized (zeros, text embeddings, random), which matters for early-phase adaptation behavior and reproducibility.

## Nice-to-Haves
- An empirical comparison against naive long-tailed adaptations (e.g., adding logit adjustment to TPT or TDA) would complement the theoretical argument on line 134 that logit adjustment would worsen EM bias.
- Per-dataset head/tail accuracy breakdown in the main text (even for one representative benchmark) would directly validate that macro-F1 gains come from improved tail performance rather than head-class artifacts.

## Removed Points
These points are flagged to be removed, treat them with caution.
- **"Comparing against training-free methods is favorable"**: The paper explicitly compares against both training-free AND training-based methods (DPE, RLCF, WATT, SCAP), and L-TTA's advantage is strongest against training-based baselines in macro-F1. This is not a valid criticism.
- **"Proposition vagueness is fatal to theoretical contribution"**: The propositions serve as conceptual motivation with proofs deferred to the appendix (which exists in the original submission). The operational definition (top-20% split) is in the experimental section. This is a presentation issue, not a fundamental flaw.

## Novel Insights
The paper makes a genuinely novel observation that entropy minimization in the TTA setting creates opposing gradient effects for head vs. tail classes (Proposition 1), and that naive logit adjustment would exacerbate rather than mitigate this bias (line 134). The design insight that Exclusionary Prototypes can leverage prediction distributions of all views to update all class prototypes simultaneously—ensuring tail classes accumulate information even from samples they don't match—is a creative solution to the prototype cold-start problem unique to long-tailed TTA.

## Suggestions
- Clarify Eq. 6 to explicitly state j* = Argmax_j' Attn([v_c, t_c], q_{j'}), making the top-1 routing explicit.
- Add a formal definition: "Let P̃ = max_c P(y_c|x̃) denote the prediction confidence" before Eq. 9.
- In Propositions 1 and 2, replace "with certain measurements" with the specific condition (e.g., "where C_head contains the top-ρ fraction of classes by cardinality").
- State K as a fraction of C in implementation details: e.g., "K = ⌈0.3 × C⌉ hyper-class vectors."
- Briefly state prototype initialization strategy for reproducibility.

## Reporting

Round 1 bracket: 6.5–7.5. Our paper is clearly above DOTA (6.0, reject) which addresses a related TTA-for-VLMs problem with less comprehensive evaluation. It's comparable to or slightly above RLCF/TTA-with-CLIP-reward (6.67, accept) and the concept drift paper (7.0, accept). It sits slightly below READ (8.0, accept), which has cleaner methodology and all-8 scores from 4 reviewers, though our paper has more extensive evaluation (15+ datasets vs. 2 benchmarks). The minor formulation clarity issues prevent an 8 but the strong novelty, extensive evaluation, and well-motivated design support a 7.0.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>