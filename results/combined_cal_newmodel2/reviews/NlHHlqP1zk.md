## Summary

This paper proposes the Fast and Slow Effect (FSE) framework and Class Representation Index (CRI) metric to evaluate whether LLM/VLM-generated concept annotations are semantically sufficient for class discrimination — without requiring human supervision. The framework compares a "fast mode" (image-based classification) to a "slow mode" (classification from the model's own progressively refined text concepts). Experiments across 6 models (GPT, Qwen, Llama families) and 5 datasets show that on fine-grained datasets, slow mode underperforms fast mode by 25%+ on average, suggesting current automated annotations provide insufficient semantic coverage.

## Strengths

- **The problem is well-motivated and timely.** Automated concept annotation is increasingly used in XAI to replace costly human annotations, but no established method exists to verify whether generated concepts truly capture class-discriminating information. The motivating example (Figure 1) — where a model correctly classifies an image but fails when forced to reason from its own concepts — effectively illustrates the practical risk. This is a genuine gap that the paper identifies and addresses.

- **The evaluation scope is thorough.** Six models spanning three families (GPT-4o, GPT-4o-mini, QwenVL2-72b/7b, Llama-3.2-vision-90b/11b) are tested across five datasets covering both fine-grained (CUB-200, Cars-196, Flowers-102) and general recognition (CIFAR-100, Caltech-101), under two annotation paradigms (post-hoc class-level and visual-grounded image-level). This breadth strengthens the generality of the findings.

- **The five-stage hierarchical concept gathering procedure** (Background → Superclass → Salient Features → Detailed Features → Auxiliary Features) is a reasonable operationalization of coarse-to-fine concept refinement, with clear acknowledgment of prior extraction methods it extends (Yuksekgönül et al., Oikarinen et al., Sun et al.).

## Weaknesses

### Fatal
None.

### Major

- **The evaluation design partially conflates annotation quality with the model's text-only classification capability.** Definition 3.1 defines annotation sufficiency as "generated concepts alone are expressive, clear, and precise enough to enable accurate inference of the corresponding class." The CRI then measures whether the *same model* that generated the concepts can classify from them in text-only mode. Low CRI could mean either (a) the concepts are genuinely insufficient, or (b) the model is poor at text-only classification even from sufficient concepts — and the framework cannot fully distinguish these. The paper partially addresses this by showing high CRI (>90%) on coarse datasets (CIFAR-100, Caltech-101), demonstrating that models *can* succeed at text-only classification in some settings. However, this is confounded: coarse classes are inherently more visually distinct and likely yield more distinctive textual descriptions, so the CRI difference across dataset types could partly reflect class similarity rather than annotation sufficiency per se. Without a human-concept baseline (e.g., expert-written concepts for the same fine-grained classes), the central claim of annotation insufficiency remains circumstantial. This is the most significant limitation of the paper.

### Minor

- **The CRI formula (Eq. 2) contains a mathematical error in its published definition.** The equation reads $CRI = 100\% \times \frac{1}{t} \sum_{i=1}^t \mathbb{1}[y_i^t = y_i]$, where $t$ is the annotation step index (1–5) and $i$ indexes test instances (of which there are $l$ total). The sum should be over all $l$ test instances with denominator $l$, not over $i=1$ to $t$ with denominator $t$. The empirical results were computed correctly (they are inconsistent with the erroneous formula), so this is a presentation error, but it should be corrected to avoid confusion.

- **The "Slow Mode Superiority" hypothesis is asserted with weak theoretical justification.** The paper appeals to dual-process theory (Kahneman, 2011) to argue that slow (concept-based) classification should outperform fast (image-based) classification. This theory describes human cognition and does not straightforwardly imply that stripping away a VLM's native visual modality and replacing it with generated text descriptions should improve accuracy. The empirical finding that slow mode underperforms fast mode by 25%+ is interesting regardless, but the framing overstates the theoretical basis for the expected superiority, and the negative result is more naturally interpreted as "VLMs are better at classifying images than at classifying from their own generated text" than as direct and unambiguous evidence of annotation insufficiency.

- **The utility-as-proxy fusion experiment (Section 6, Table 4) is an imperfect simulation.** The paper gives the model both the image AND text concepts jointly and reports that the fused CRI (~90%) matches the fast mode rather than the slow mode (~50%). The conclusion that "strong performance in downstream tasks may not correlate with adequate conceptual supervision" is reasonable. However, the paper claims this "rigorously simulat[es] the end-to-end inference pipeline commonly employed by standard concept-based multimodal models" — but in actual concept bottleneck models, concept representations mediate between the visual encoder and the prediction head, rather than the image and concepts being jointly fed to the classifier. The simulation demonstrates a weaker point than claimed.

- **Several experimental details are underspecified:** (a) the test set size $l$ is never reported for the main experiments (only the preliminary contradiction test specifies "100 images per dataset"); (b) "three runs with different seeds" is mentioned (Figure 3 caption) but what is seeded (decoding temperature? data subsampling?) is not specified; (c) the five-stage process is described but its superiority over fewer stages is not validated.

### Trivial
None.

## Nice-to-Haves

- A human-concept baseline would substantially strengthen the paper: annotate a subset of images with human-generated concepts and compute CRI. If human concepts yield significantly higher CRI than automated concepts on fine-grained data, the annotation-insufficiency claim becomes much more compelling.
- Control for text-only classification capability by testing whether models can classify from *expert-written* concept descriptions for fine-grained classes.
- Explicitly acknowledge that the CRI confound (annotation quality vs. model capability) is a limitation that future work should address.

## Removed Points

These points are flagged for removal — treat them with caution:

- **"The contradiction test conflates distinct outcomes"** (Harsh Critic weakness 5): Removed because the contradiction test is solely a preliminary experiment for selecting distractor strategies (semantically related vs. random). Whether a contradiction goes correct→wrong or wrong→correct is irrelevant for this distractor-selection purpose. The main CRI evaluation uses accuracy directly, so this criticism does not affect the paper's central claims.

- **Pure presentation criticisms** (abstract overclaiming "self-evaluation", Definition 3.1 being "too vague"): These are either framing disagreements or style preferences rather than verifiable flaws.

## Novel Insights

None beyond the paper's own contributions. The reviews identify the same core issues the paper discusses without offering fundamentally new perspectives.

## Suggestions

1. **Correct the CRI formula** (Eq. 2) to sum over all $l$ test instances with denominator $l$.
2. **Add a human-concept baseline** on a subset of fine-grained data to disentangle annotation quality from model text-only classification capability.
3. **Temper the theoretical framing** of "Slow Mode Superiority" — the empirical finding is valuable independently of the dual-process theory analogy.
4. **Report test set sizes** and clarify what "three runs with different seeds" seeds (decoding temperature, prompt ordering, or data subsampling).
5. **Acknowledge the simulation limitations** in the utility-as-proxy experiment more explicitly.

## Score and Decision

**Calibration summary.** All anchors retrieved across rounds:

| Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| `/home/.../5kMwiMnUip.md` | 1.40 | R1 | No | Irrelevant (jailbreaking paper) |
| `/home/.../kTjEPEy96Q.md` | 3.00 | R1 | Yes | Evaluation framework for unsupervised CBMs — had weak connection between metrics and actual prediction task; submitted paper is stronger empirically but shares the "metric doesn't fully measure what it claims" concern |
| `/home/.../KLUDshUx2V.md` | 3.40 | R1 | Yes | LLM concept bank generation + evaluation — criticized for novelty and weak experiments; submitted paper has broader evaluation so it is stronger |
| `/home/.../dZsjj4vQjl.md` | 4.50 | R1/R2 | Yes | Multi-grained concept annotation dataset paper; different contribution type |
| `/home/.../apPItJe0wO.md` | 5.50 | R2 | Yes | Uses explanation self-consistency for LLM uncertainty — similar self-check paradigm but different domain; criticized for unclear framing |
| `/home/.../wk77w7DG1N.md` | 4.67 | R2 | No | LLM generation consistency evaluation; tangential |
| `/home/.../RC5FPYVQaH.md` | 5.75 | R1 | Yes | Concept bottleneck for LLMs — similar topic area; praised for novelty but criticized for limited model testing |
| `/home/.../rp0EdI8X4e.md` | 6.25 | R1 | Yes | Faithful VLC model — stronger formalization and experiments than submitted paper |

**Round-1 bracket:** The submitted paper clearly exceeds the 3.0–3.4 band (weak evaluation papers) due to its broader evaluation scope and clearly defined framework. It does not reach the 6.25 level (faithful VLC paper with stronger formalization and fewer methodological gaps). Initial bracket: 4.5–6.0.

**Round-2 narrowing:** Comparing item favorability ratings, the submitted paper's Major weakness (circularity confound, favorability 2.24) has lower favorability than any weakness in the 5.75 anchor paper (RC5FPYVQaH, lowest weakness ~0.21), indicating this is a more significant drag. The submitted paper's strengths (9.5–12.3) are comparable to the 5.75 and 6.25 anchors' strengths. However, the 5.50 anchor paper (apPItJe0wO) had a similar pattern of meaningful methodological caveats and was scored 5.50 with a Reject decision.

**Final score: 5.0.** The paper addresses a real problem, the empirical work is broad, and the core observation is valid. However, the major confound (annotation quality vs. model text-only capability) is not adequately resolved, and several presentation issues (formula error, underspecified experimental details, overstated framing) keep the contribution from being fully established. A revision with a human-concept baseline and tempered claims would merit reconsideration at a higher score.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>