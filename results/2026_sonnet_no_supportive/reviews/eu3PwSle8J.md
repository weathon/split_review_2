Let me read the ISE anchor paper quickly for comparison:## Summary
This paper proposes Augmented Intermediate Representations (AIR), a defense against indirect prompt injection attacks that injects instruction-hierarchy (IH) privilege signals into *every* decoder layer of an LLM, rather than exclusively at the input. Motivated by a cosine-similarity diagnostic (Figure 3) showing that input-level IH signals degrade as they propagate through layers, AIR introduces per-layer trainable embedding tables indexed by token privilege level — drawing an explicit analogy to how RoPE distributes positional information across all attention layers. Experiments across three model sizes (Llama-3.2-3B, Qwen-2.5-7B, Llama-3.1-8B), two training methods (SFT, DPO), and multiple attacks demonstrate a claimed 1.6×–9.2× ASR reduction on gradient-based attacks with negligible parameter overhead (0.005% for Llama-3.1-8B).

## Strengths

- **Consistent empirical advantage across a 3×2 experimental matrix.** Table 1 and Figure 7 document 1.6×–9.2× GCG ASR reduction over the next-best baseline across all three model sizes and both SFT and DPO training regimes. Had these results held for only one model or training method, they would be far less convincing.

- **Principled design grounded in a concrete diagnostic.** Figure 3 shows cosine similarity between representations of tokens at different privilege levels increasing with depth under Delim and ISE (from ~0.55 to ~0.90–0.92 by layer 25), while AIR maintains greater separation (~0.85 at layer 25). The analogy to RoPE is not merely rhetorical — it correctly identifies that distributing critical metadata across all layers is a general transformer design principle.

- **Negligible parameter overhead.** AIR adds only 0.4M parameters to Llama-3.1-8B (0.005%), ruling out capacity increases as an explanation for improved robustness.

## Weaknesses

### Fatal
None.

### Major

- **Gradient-based attack budgets are too short to confirm fundamental robustness.** Section 5.4 specifies only 50 GCG steps for SFT models and 200 for DPO — well below the 500–1000 steps typical in adversarial robustness research. Figure 7 shows loss curves still steeply descending at termination for ISE and Delim, indicating the attacks have *not converged*. AIR maintaining higher loss under this short budget is consistent with two hypotheses: (a) AIR creates an attack landscape with no attainable low-loss region, or (b) AIR simply slows the optimizer and sufficient budget would close the gap. The paper's data cannot distinguish these. This is significant because the headline claim — "1.6×–9.2× reduction in ASR" — rests entirely on gradient-based evaluations at these truncated step counts.

- **Inconsistency between ASR metrics for static vs. gradient-based attacks.** Section 5.4 explicitly states that static attack ASR is measured by checking for the literal string `hacked!` in model outputs, while gradient-based attack ASR is "measured using the likelihood (from model's logits) of generating the target phrase." Logit-based ASR and decoding-time string ASR are qualitatively different quantities — a defended model may assign high log-probability to `hacked!` under teacher-forcing while generating something different under greedy or sampled decoding. The paper does not specify the threshold used, nor whether logit-based ASR correlates with actual decoding outcomes. This makes the gradient-based ASR numbers in Table 1 difficult to interpret in isolation and prevents meaningful cross-comparison with the near-zero static ASRs.

### Minor

- **Figure 3's cosine similarity diagnostic conflates injection mechanism with training dynamics.** Section 3 describes Figure 3 as comparing Delim, ISE, and AIR — meaning these must be models already trained with their respective mechanisms. Consequently, Figure 3 cannot cleanly attribute the lower cosine similarity of AIR to the injection location alone, as opposed to AIR's training dynamics shaping the representations differently. A pre-adversarial-training plot would isolate the injection mechanism's direct effect on representation separability.

- **AIR's advantage on static attacks is marginal.** From Table 1, all three IH injection mechanisms achieve near-zero ASR across the four static attacks for nearly all model-training combinations. AIR's advantage over Delim/ISE on static attacks amounts to at most a few tenths of a percent. The paper's contribution rests almost entirely on gradient-based attack results; this should be stated more plainly rather than presenting AIR as uniformly superior.

- **SecAlign replication fidelity is unverified.** Section 3.2 notes that SecAlign (Chen et al., 2024b) uses Delim+DPO, but the paper trains this baseline with its own protocol and data rather than using the original checkpoint. Uncontrolled differences in training data, step count, or DPO hyperparameters could affect the Delim+DPO baseline's competitiveness.

### Trivial
None.

## Nice-to-Haves
- Run GCG/Astra to convergence (500+ steps, or until loss curves plateau) and show that AIR's loss remains elevated while baselines converge. This single experiment would decisively resolve the primary evidentiary gap.
- Report string-match ASR for gradient-based attacks alongside logit-based ASR, or clarify the logit threshold and its empirical correlation with decoding-time output strings.
- Ablation: show Figure 3's cosine similarity on models *before* adversarial robustness training to cleanly isolate the injection mechanism's direct effect.
- Report GCG/Astra ASR variance across multiple random attack seeds in Table 1 (Figure 7 shows standard deviation over instances but per-seed variance in Table 1 is uncharacterized).
- An adaptive attack targeting AIR's additive embedding structure specifically (gradient-through the embedding lookup) would further strengthen the white-box security claim.

## Removed Points
*These points are flagged to be removed, treat them with caution.*

- **GCG step asymmetry as a separate weakness:** The critic raised the SFT (50 steps) vs. DPO (200 steps) asymmetry as a distinct issue. This is absorbed into the broader attack-budget weakness above.
- **Adaptive attack absence as a weakness:** Removed from weaknesses and moved to Nice-to-Haves; standard GCG is already a white-box attack that has gradient access to the full model including AIR's embeddings. The absence of an attack specifically designed around the embedding structure is a reasonable limitation rather than a methodological gap.

## Novel Insights
The paper's sharpest conceptual contribution is the explicit and rigorous analogy between privilege-level signals and positional signals: just as positional encodings injected at the input layer are insufficient (motivating RoPE's per-layer injection), IH signals injected only at the input are insufficient for maintaining privilege-level separation deep in the network. This framing generalizes: it suggests a principle for any token-level categorical metadata (role, source trust level, modality) that needs to remain distinguishable throughout a deep transformer stack. The cosine-similarity diagnostic in Figure 3 operationalizes this claim in a way that is replicable and extensible to other architectures.

## Suggestions
1. Extend GCG evaluation to 500 steps and plot the full loss curves — if AIR's loss plateaus at a higher value than baselines, this single figure would convert the major evidentiary gap into a confirmed strength and substantially sharpen the paper's conclusions.
2. Report string-match ASR for gradient-based attacks, or explicitly state and justify the logit-probability threshold used and validate it against actual decoding outputs on a sample.
3. Include Figure 3 at an intermediate training checkpoint (after non-adversarial SFT but before adversarial robustness training) to cleanly isolate the injection mechanism's direct effect on representation separability.

---

## Score and Decision

**Calibration Anchors (Round 1):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `5kMwiMnUip.md` | 1.40 | R1 | Strong reject (jailbreak survey, no real contribution); far weaker than AIR |
| `3MDmM0rMPQ.md` | 3.00 | R1 | Reject (task-specific safety guardrails, weaker evaluation); less principled than AIR |
| `l3bUmPn6u5.md` | 4.25 | R1 | Reject (PFT, prompt-injection defense with weaker, position-based argument; similar scope but narrower evaluation) |
| `V01FPV3SNY.md` | 5.33 | R1 | Reject (RA-LLM alignment defense, similar domain, comparable evaluation rigor) |
| `sjWG7B8dvt.md` | 6.00 | R1 | **ISE paper** — the direct baseline AIR improves upon; accepted at 6.0 with similar novelty level |
| `rnJxelIZrq.md` | 6.50 | R1 | Accept (hypergraph LLM defense); less clearly motivated than AIR |
| `sULAwlAWc1.md` | 7.00 | R1 | Accept (robust jailbreak generation); stronger empirical evaluation |
| `tTPHgb0EtV.md` | 8.00 | R1 | Accept (Booster, harmful fine-tuning defense); stronger theoretical grounding and evaluation |

**Round 1 bracket:** Based on these anchors, the AIR paper sits in the range **5.0–6.5**. The ISE paper (the direct predecessor that AIR improves upon) scored 6.0. AIR has a broader experimental matrix and a more principled motivation, but the two major weaknesses (short GCG budget, inconsistent ASR metric) create real evidentiary uncertainty around the headline claim. The PFT paper (4.25), a rejected prompt-injection paper in the same domain, is clearly weaker. The 7.0 anchor (ArrAttack) has stronger evaluation methodology.

**Narrowing:** AIR is more technically mature than ISE and covers a more comprehensive experimental matrix, which would normally push it above ISE's 6.0. However, the two major weaknesses are more substantial than the issues raised in ISE's reviews (which centered mostly on novelty concerns). The gradient attack budget problem in particular undermines the primary empirical claim in a way that ISE's reviewers did not face. I settle at **5.5**: incrementally better than ISE in design and scope, but the evidentiary quality of the primary robustness claim is below ISE's level.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>