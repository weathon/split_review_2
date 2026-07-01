Now let me verify a few more specific details from the paper, particularly around Figure 7 and the optimization budget claims.Now I have all the information I need. Let me draft the review first.Now let me run calibration search — Round 1 bracketing.Let me read the most relevant anchor papers in detail, especially the ISE paper which is directly related.Now I have sufficient information for calibration. Let me form my bracket.

**Round 1 Bracket Assessment:**
- Strong reject band (< 1.5): Papers like NEMESIS (1.40) — completely different quality; AIR is far above these.
- Reject band (1.5–3.5): Papers like IPE (3.00), MRCJ (3.00) — narrow scope, limited evaluation. AIR is substantially stronger.
- Borderline reject band (3.5–5.5): Papers like PFT (4.25) — similar topic but PFT was rejected for narrow evaluation (no GCG), unclear threat model. AIR has much more thorough evaluation.
- Borderline accept band (5.5–7.5): **ISE paper (6.00)** — this is the direct predecessor to AIR, accepted with unanimous 6s. AIR improves on ISE both methodologically and empirically.
- Accept band (7.5–8.5): Booster (8.00) — very strong evaluation with no major gaps. AIR's evaluation gaps prevent it from reaching this level.
- Strong accept band (> 8.5): No relevant hits.

**My initial bracket: 5.5 to 7.0.** AIR is clearly better than PFT (4.25) and at least as good as the ISE paper (6.00) it improves upon, but the evaluation gaps (GCG budget, no adaptive attacks) prevent it from reaching the accept range (8.0).

Now let me write the final consolidated review.

---

## Summary
This paper proposes Augmented Intermediate Representations (AIR), a method for defending LLMs against indirect prompt injection attacks by injecting instruction hierarchy (IH) signals at every decoder layer rather than only at the input layer. Drawing an analogy to the evolution of positional embeddings (sinusoidal → RoPE), AIR adds layer-specific trainable embeddings encoding privilege-level information to intermediate token representations. Evaluations across three models (3B, 7B, 8B) and two training methods (SFT, DPO) show 1.6×–9.2× ASR reductions on gradient-based attacks versus prior methods, with negligible parameter overhead (0.005%) and minimal utility loss.

## Strengths
- **Empirically grounded motivating hypothesis (Figure 3, Section 3.2)**: Cosine similarity analysis across decoder layers concretely demonstrates that input-level IH signals (ISE) degrade from ~0.55 to ~0.92 similarity, while AIR maintains better separation (~0.55 to ~0.88). This provides direct, quantitative justification for the core design choice rather than relying on intuition alone.
- **Consistent improvements across a well-structured experimental matrix (Table 1)**: AIR achieves 1.6×–9.2× ASR reduction on GCG and up to 145× on Astra across three models and two training methods. The systematic evaluation of all {Delim, ISE, AIR} × {SFT, DPO} combinations goes beyond what any prior work evaluated individually, providing the community with a clearer picture of how injection mechanism and training method interact.
- **Negligible deployment overhead (Section 4)**: Only 0.005% additional parameters for Llama-3.1-8B with 3 privilege levels, making the approach practically costless to deploy.
- **Utility preservation across two complementary benchmarks (Figures 6, 8)**: AIR maintains utility within ~2% of non-adversarial baselines on AlpacaFarm, and achieves the best utility-separation tradeoff on SEP when combined with DPO.

## Weaknesses

### Fatal
None

### Major
1. **Insufficient GCG optimization budget (Section 5.4, Figure 7)** — The paper uses only 50 GCG steps for SFT models and 200 steps for DPO models. The original GCG paper (Zou et al., 2023) uses 500 steps, and many subsequent works run even longer. The paper's own Figure 7 shows the attacker's loss still visibly decreasing at the final optimization step for AIR-defended models, particularly in the SFT plots. This means the headline claim of "1.6× to 9.2× ASR reduction" may partly reflect insufficient attack optimization rather than genuine robustness. Running to convergence (≥500 steps) is needed to establish whether AIR's advantage holds at equilibrium or merely reflects a harder-to-optimize loss landscape that a patient attacker could eventually overcome.

2. **No adaptive attack evaluation** — The paper evaluates only off-the-shelf GCG and Astra attacks. While these are white-box (gradients flow through AIR's mechanism), they are not specifically designed to defeat AIR. For instance, an adaptive attacker might optimize adversarial tokens to produce representations that, after the per-layer P1 embedding addition, mimic the effect of P0 tokens. The adversarial ML defense literature has established that evaluation against adaptive adversaries is standard practice (Carlini et al., "On Evaluating Adversarial Robustness"). The absence of any such evaluation is a methodological gap that leaves the true robustness ceiling uncharacterized.

### Minor
1. **Single adversarial target for gradient-based attacks (Section 5.4)** — All gradient-based evaluations use "print exactly 'hacked!'" as the adversarial instruction, with ASR measured by likelihood of generating this specific target. While the SEP benchmark provides diversity for static-style attacks, the gradient-based evaluation — where AIR's main advantages manifest — tests only one simple, short target string. It is plausible that AIR's advantage is partly specific to this target. Testing diverse adversarial objectives would strengthen generalizability.

2. **ASR metric inconsistency between attack types (Section 5.4)** — Static attack ASR uses string match on generated outputs, while gradient-based ASR uses "the likelihood (from model's logits) of generating the target phrase 'hacked!'" No threshold for the likelihood-based metric is specified. The two metrics are measuring different things, making cross-attack comparisons less interpretable and leaving unclear what likelihood level constitutes a "successful" attack.

3. **AIR-SFT utility degradation underexplored (Section 6.2)** — The paper acknowledges that AIR-SFT sometimes reduces utility below baseline on SEP (e.g., Qwen-2.5-7B, Llama-3.1-8B in Figure 8b) but does not investigate why. This hints at an over-separation failure mode where AIR causes the model to become overly conservative about following instructions in the data segment, even when those instructions are benign.

4. **Figure 3 lacks specification of training state** — The cosine similarity analysis on Llama-3.2-3B does not state whether measurements are taken before or after adversarial training. This distinction matters: if before training, it demonstrates initial signal degradation but not whether training compensates; if after, it's more meaningful but should be specified.

### Trivial
None

## Nice-to-Haves
- Layer-wise ablation studying where in the layer stack the IH signal matters most (first half, second half, every-other layer) — this would deepen the contribution from "add embeddings everywhere" to "here is where and why the signal matters"
- Probing classifiers at each layer to measure whether the model causally uses the preserved IH signal, complementing the geometric (cosine similarity) analysis
- Ablation on injection point placement (before vs. after layer norm, after attention/FFN sub-layers)
- Explicit limitations section discussing failure modes, particularly the non-negligible ASR cases (e.g., Llama-3.2-3B + DPO + Astra = 23.8% in Table 1)

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **"Training dataset details deferred to appendix"** — Removed per policy: appendix-related concerns are excluded since the parser strips appendix content from all papers; these details exist in the original submission.
- **"Cosine similarity is only one proxy for signal preservation"** — Removed: Figure 3 serves as motivation for the design, not as proof of mechanism. The actual proof is in the ASR results themselves. The reviewer's concern that the model might encode privilege in directions not captured by cosine similarity is speculative and not anchored to a concrete problem.
- **"Missing related work"** — Removed per policy: cannot confirm existence of external references.

## Novel Insights
The analogy between instruction hierarchy signal injection and positional embedding evolution (sinusoidal/learned input-only → per-layer RoPE) is a genuinely novel framing that suggests a broader design principle: critical metadata signals beyond token content (position, privilege level, etc.) may benefit from per-layer injection rather than input-only injection. This connects security-focused architectural modifications to well-established findings in the positional embedding literature and could inspire similar approaches for other metadata signals.

## Suggestions
- Run GCG and Astra for ≥500 steps across all models and plot ASR as a function of optimization budget. If AIR's advantage persists at convergence, the robustness claim becomes much stronger; if it narrows, honestly report the converged advantage.
- Design at least one adaptive attack specifically targeting AIR (e.g., optimizing adversarial tokens to minimize the effective separation created by per-layer IH embeddings) and report results.
- Expand adversarial targets beyond "hacked!" to include diverse objectives (data exfiltration, multi-token targets, semantically-defined goals) for gradient-based evaluations.
- Investigate the AIR-SFT utility degradation on SEP to characterize when over-separation occurs and whether it can be mitigated.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to AIR |
|-------|------|-----------|-------|--------------------|
| NEMESIS (jailbreaking LLMs) | 5kMwiMnUip | 1.40 | R1 | Far weaker — no real methodology; AIR is vastly superior |
| Systematic Review of LLMs | 8QTpYC4smR | 1.00 | R1 | Survey paper, not relevant; AIR is a genuine research contribution |
| Cross-Lingual Humanoid Robots | gwZ90hFSL2 | 1.00 | R1 | Irrelevant topic; returned as nearest in score band only |
| Inverse Prompt Engineering | 3MDmM0rMPQ | 3.00 | R1 | Narrower scope, weaker evaluation than AIR |
| Code-of-thought prompting | lUyYX9VFgA | 3.00 | R1 | Attack paper, not defense; AIR has more systematic evaluation |
| Incremental Exploits MRCJ | KyKTjRtyNG | 3.00 | R1 | Attack paper with limited scope; AIR is stronger |
| Safety Alignment Depth | 6Mxhg9PtDE | 9.50 | R1 | Much broader contribution with deeper analysis; AIR is narrower |
| **PFT (position-enhanced finetuning)** | l3bUmPn6u5 | **4.25** | R1 | Similar topic but rejected for narrow evaluation (no GCG), unclear threat model; AIR has much broader evaluation |
| Defending via Robustly Aligned LLM | V01FPV3SNY | 5.33 | R1 | Different approach (RA-LLM, no fine-tuning); AIR has stronger results |
| Nested Gloss jailbreak | Q3oAX9HoH2 | 4.00 | R1 | Attack paper; not comparable |
| AutoHijacker | 2VmB01D9Ef | 4.25 | R1 | Black-box attack paper; AIR is a defense with more thorough evaluation |
| **ISE (Instructional Segment Embedding)** | sjWG7B8dvt | **6.00** | R1 | **Direct predecessor to AIR.** AIR improves on ISE with per-layer injection, more models, GCG evaluation, and consistent improvements. ISE was criticized for limited novelty and evaluation scope; AIR addresses both. |
| Hypergraph defense | rnJxelIZrq | 6.50 | R1 | Different approach; roughly comparable quality |
| ArrAttack | sULAwlAWc1 | 7.00 | R1 | Attack paper with strong evaluation; AIR's defense contribution is solid but has evaluation gaps |
| Deciphering Chaos | iKgQOAtvsD | 5.75 | R1 | Attack paper; not directly comparable |
| **Booster** | tTPHgb0EtV | **8.00** | R1 | Stronger defense paper with cleaner evaluation and no major methodological gaps; AIR's evaluation gaps prevent it from reaching this level |
| Context-Parametric Inversion | SPS6HzVzyt | 8.00 | R1 | Strong analytical contribution; AIR is narrower and less rigorous |
| DP Few-Shot Generation | oZtt0pRnOl | 8.00 | R1 | Different area; strong evaluation rigor |
| Self-Alignment Backtranslation | 1oijHJBRsT | 8.00 | R1 | Different area; strong methodology |

### Scoring Rationale

**Round 1 bracket: 5.5 to 7.0**

The key comparison is with the ISE paper (6.00), which is AIR's direct predecessor. AIR improves upon ISE both methodologically (per-layer injection with principled RoPE analogy, negligible overhead) and empirically (three models instead of fewer, GCG/Astra evaluation, systematic mechanism × training method matrix). The ISE paper was criticized for limited novelty ("merely adds an embedding layer") and evaluation clarity — AIR addresses both with a more principled design rationale and a clearer experimental structure.

However, AIR introduces its own evaluation gaps that prevent it from reaching the accept band (7.5+): the GCG optimization budget is demonstrably too low with loss curves still decreasing (Figure 7), there is no adaptive attack evaluation (expected for defense papers), and gradient-based attacks test only a single target string. These are addressable in a rebuttal but currently leave uncertainty about the magnitude of improvement.

Compared to PFT (4.25, rejected), AIR is substantially stronger — PFT was rejected for not testing against GCG at all, which AIR does. Compared to Booster (8.00, accepted), AIR lacks the evaluation rigor needed for confident acceptance at that level.

**Final score: 6.0** — The paper presents a genuine insight (per-layer IH injection) with consistent, promising results, but the evaluation gaps in its central robustness claim — particularly the insufficient GCG budget where Figure 7 shows non-converged attacks — prevent full confidence. This is a borderline accept: the contribution is real and the direction is promising, but the robustness claims need stronger evidential support to be taken at face value.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>