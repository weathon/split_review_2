Now let me re-read the key sections more carefully to verify specific claims.Now I have thoroughly read the paper. Let me draft the review before calibration.Now let me run the calibration search to anchor the score.Let me read a few key anchors to calibrate the score.Now I have enough information to form my bracket and finalize the review.

**Round 1 Bracket Analysis:**

- **Strong reject (1.0)**: Papers like the Chinese NLP robots paper — fundamentally not real contributions. SigMap is clearly above this.
- **Score 3 range**: NormWear (3.0), PowerGPT (3.0) — domain foundation models with fundamental issues. SigMap is somewhat better — cleaner architecture, but shares issues.
- **Score 4-5 range**: WiFi mesh (4.0), DASFormer (5.25) — domain-specific methods with comparison fairness issues, limited novelty. Very similar profile to SigMap.
- **Score 6-7 range**: Wi-GATr (7.0) — wireless domain, accepted, includes real data, stronger evaluation. SigMap is clearly weaker.
- **Score 8+**: Strong papers. SigMap not at this level.

**Initial bracket: 3.5–5.0**

SigMap has a genuine architectural insight (map-as-prompt) but multiple structural issues: factually incorrect zero-shot claim, unfair headline comparison, unexplained Eq. 11, text-table inconsistency, missing baselines. Compared to DASFormer (5.25, rejected), SigMap has more and more serious issues. Compared to NormWear (3.0), SigMap has a cleaner architectural contribution. This places it around **4.0**.

Now let me write the final review.

---

## Summary
This paper proposes SigMap, a multimodal model for wireless localization that introduces: (1) cycle-adaptive masking that dynamically adjusts masking patterns based on CSI periodicity during self-supervised pre-training, and (2) a "map-as-prompt" framework using a GNN to encode 3D geographic information into soft prompt tokens prepended to a frozen transformer for parameter-efficient cross-scenario adaptation. Experiments on ray-tracing datasets (DeepMIMO, WAIR-D) show improvements over baselines in single-BS and multi-BS localization.

## Strengths
- **Map-as-prompt is architecturally well-motivated and clean.** Encoding 3D building geometry via a GNN into soft prompt tokens prepended to the frozen transformer (Section 3.4, Algorithm 1, Figure 4) cleanly separates environment-specific information from the learned signal representation. The ablation in Table 4 showing that a 2D bird's-eye view degrades MAE by only 8% relative to the full 3D mesh is a genuinely informative result demonstrating that topological/LoS cues carry most of the geographic value.

- **Parameter efficiency is concretely documented.** Table 5 shows only 0.085M of 11.73M parameters (0.7%) are trainable during fine-tuning, with the entire fine-tuning stage completing in 30 minutes. This is a practical advantage clearly quantified.

- **Cross-scenario evaluation on a structurally different dataset.** Testing on WAIR-D Scenario-2 (100 OpenStreetMap-derived city layouts, Section 4.5) provides a more convincing generalization test than evaluating on additional DeepMIMO scenarios, since the environment generation pipeline differs.

## Weaknesses

### Fatal
None

### Major

- **The "zero-shot generalization" claim is factually incorrect.** The abstract states the model "exhibit[s] strong zero-shot generalization in unseen environments," but Section 4.5 explicitly states "only the downstream task heads are fine-tuned using limited target samples (approximately 100 instances per scenario)." This is few-shot transfer, not zero-shot. No true zero-shot experiment (no target-domain labeled data) is reported anywhere in the paper. This is a misstatement that misleads about the nature of the contribution.

- **The headline comparison is misleading; baselines lack map access.** Tables 1–2 compare SIGMAP (w/ map) against baselines with no 3D map access. The paper's own ablation reveals the reality: SIGMAP (w/o map) achieves 2.275m vs LWLM's 2.382m in Single-BS (4.5% improvement) and 0.789m vs 0.828m in Multi-BS (4.7% improvement). The 34.4% headline improvement is primarily an information advantage, not a method advantage. Critically, no experiment provides the same map information to baselines (e.g., concatenating a map embedding to LWLM's input), so the reader cannot tell whether the gain comes from the prompting architecture or simply from having access to geographic data that competitors lack.

- **Equation 11 introduces an undescribed mechanism with undefined variables.** Section 4.2 suddenly introduces an "NLoS-aware attention mechanism" (Eq. 11) with variables $\mathbf{o}_s^{(i)}$, $\mathbf{W}_{\text{NLoS}}$, and $\phi$ that never appear in the methodology (Section 3). The multi-BS attention in Section 3.5 (Eq. 9) uses entirely different notation ($\mathbf{v}^T \tanh(\mathbf{W}_{\text{att}} \mathbf{t}_{\text{cls}}^{(t)})$). Either the methodology section is incomplete (a key architectural component is missing), or the results section introduces post-hoc narrative that does not correspond to the actual architecture. This undermines the paper's verifiability.

- **Text-table inconsistency in generalization results.** Section 4.5 text claims "1.580 m on WAIR-D Scenario-2" but the corresponding table shows 1.880m for SIGMAP (w/ map). This is a factual error that undermines confidence in the reported results.

### Minor

- **Missing random masking baseline in ablation.** Table 3 compares grid-masking, strip-masking, and adaptive masking, but omits standard random masking — the default approach in masked autoencoders. Without this comparison, the claimed advantage of cycle-adaptive masking over conventional MAE is not empirically demonstrated.

- **Same scenario for pre-training and fine-tuning.** Section 4.1 confirms O1_3p5 is used for both stages. This limits interpretability of the main results (Tables 1–2) as a test of learned representations versus scenario-specific memorization. The generalization experiments in Section 4.5 partially mitigate this, but those results involve only LWLM as a baseline.

- **Positional encoding mismatch.** The input $\mathbf{T}_{\text{input}} = [\mathbf{t}_{\text{cls}}; \mathbf{T}_{\text{geo}}; \mathbf{T}_{\text{CSI}}] + \mathbf{E}_{\text{pos}}$ uses frozen positional encodings from pre-training, but the geographic prompt token was absent during pre-training, shifting all CSI token positions. This is not discussed.

- **No variance reported.** Results are averaged over 5 runs (Section 4.1), but no standard deviations are reported. Given that the SIGMAP (w/o map) vs. LWLM margins are 4–5%, statistical significance cannot be assessed.

### Trivial
None

## Nice-to-Haves
- Providing baselines with equivalent map access (e.g., concatenating map features to LWLM's input) to isolate the value of the prompting architecture
- A true zero-shot experiment (geographic prompts but no labeled target data) to validate the cold-start deployment narrative
- Standard random masking as a baseline in Table 3
- Real-world CSI validation to support practical applicability claims
- Representation-level analysis showing what cycle-adaptive masking learns differently (beyond downstream accuracy)

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"All evaluation is on ray-tracing simulated data"** — While valid in principle, ray-tracing evaluation is standard practice in the wireless ML community (e.g., Wi-GATr at ICLR also uses simulated data alongside real). Moved to nice-to-have rather than kept as a weakness.
- **"Foundation model terminology is strained"** — The term is used loosely, but this is common in recent domain-specific ML papers. Not a substantive weakness.
- **"SWiT and CNN baselines dropped in generalization experiments"** — Only LWLM is compared in Section 4.5, but the two most relevant methods (SIGMAP variants and LWLM) are present. Minor scope concern.
- **"Introduction's research gap framing lacks evidence"** — Generic concern about motivation framing, not about the method.
- **"Cycle-adaptive masking is under-specified (cross-correlation details)"** — Removed per rules against reproducibility nitpicks about undisclosed implementation details. The missing random masking baseline is retained as a separate, more substantive concern.

## Novel Insights
The finding that a 2D bird's-eye view retains most of the localization benefit of a full 3D mesh (only 8% MAE degradation, Table 4) is a genuinely useful empirical insight for practitioners: topological/LoS cues dominate over detailed 3D facade geometry for wireless localization. The paper's observation about periodic shortcut learning in CSI masked autoencoders — that models can trivially interpolate across the antenna–subcarrier grid due to OFDM periodicity — is also a valuable diagnostic contribution to the wireless self-supervised learning literature.

## Suggestions
- Replace "zero-shot" with "few-shot" throughout (abstract, contributions, conclusion)
- Either fully define Eq. 11's variables in the methodology or reconcile it with Eq. 9's notation — the current state is confusing
- Fix the 1.580 vs 1.880m text-table discrepancy in Section 4.5
- Add random masking as a baseline in Table 3 to demonstrate that cycle-adaptive masking outperforms the standard MAE approach
- Report standard deviations for all results
- Include an experiment where baselines receive equivalent geographic information (e.g., map features concatenated to their input) to isolate the prompting architecture's contribution
- Address the positional encoding shift when geographic prompt tokens are prepended to the frozen transformer

## Score and Decision

### Calibration Anchors

| Anchor | Path | Avg Score | Round | Comparison |
|--------|------|-----------|-------|------------|
| Chinese NLP Robots | gwZ90hFSL2 | 1.0 | R1 | Not a real contribution; SigMap far above |
| Scaling Illumination | u1cQYxRI1H | 10.0 | R1 | Strong accept, not comparable |
| LLM Survey | 8QTpYC4smR | 1.0 | R1 | Pure survey, not comparable |
| Financial Markets NN | nSDOkm0SKo | 1.0 | R1 | Pseudoscience; SigMap far above |
| ECG Foundation Model | 7zJDTnogdG | 3.33 | R1 | Domain foundation model with more fundamental issues; SigMap slightly better |
| Embodied Self-Improvement | I0To0G5J7g | 3.20 | R1 | Different domain; SigMap comparable |
| NormWear | XhdckVyXKg | 3.0 | R1 | Domain foundation model with unclear methodology and insufficient baselines; SigMap has cleaner architecture |
| PowerGPT | ntSP0bzr8Y | 3.0 | R1 | Domain foundation model; SigMap has more coherent framework |
| DASFormer | 7ipjMIHVJt | 5.25 | R1 | Self-supervised domain pretraining with comparison issues; very similar profile but SigMap has more issues (factual errors, Eq. 11) |
| Self-Supervised Content+Position | nf4v09zw6O | 5.25 | R1 | SSL method; cleaner evaluation than SigMap |
| WiFi Mesh | q3WzT2mrhB | 4.0 | R1 | WiFi CSI application, limited novelty; comparable issues |
| RedMotion | 72MSbSZtHv | 5.33 | R1 | Self-supervised for motion; stronger methodology |
| Wi-GATr | 9TClCDZXeh | 7.0 | R1 | Wireless domain accepted paper with real-data validation, stronger evaluation; SigMap clearly weaker |
| Error Correction FM | 7KDuQPrAF3 | 6.25 | R1 | Foundation model with stronger novelty; SigMap below |
| EM-GANSim | 29JDZxRgPZ | 6.0 | R1 | EM simulation; better evaluation than SigMap |
| RelCon | k2uUeLCrQq | 6.75 | R1 | Foundation model with large-scale data; stronger than SigMap |
| Never Train from Scratch | PdaPky8MUn | 8.0 | R1 | Strong methodological contribution; SigMap far below |

**Round 1 bracket**: 3.5–5.0

**Narrowing rationale**: SigMap has a genuine architectural contribution (map-as-prompt) that elevates it above the 3.0-range papers (NormWear, PowerGPT), which had more fundamental methodology issues. However, it falls below the 5.25-range papers (DASFormer, Self-Supervised Content+Position) due to its accumulation of problems: a factually incorrect zero-shot claim, an undefined equation in the results, a text-table inconsistency, a structurally unfair headline comparison, and modest improvements (~5%) when the information advantage is controlled. The WiFi Mesh paper at 4.0 has a very similar profile — interesting domain application with limited demonstrated novelty and experimental issues.

The paper proposes genuinely interesting ideas (map-as-prompt, cycle-adaptive masking) but the execution has multiple structural problems that collectively undermine confidence in the headline claims. The ideas merit further development, but the current manuscript does not adequately support its stated contributions.

**Final score: 4.0** (borderline reject)

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>