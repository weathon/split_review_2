Now let me read the paper in chunks to verify the reviewer's claims.Now let me read the remaining sections to make sure I have the full picture:Now I have the full paper content. Let me submit my draft review before calibration.Now let me run Round 1 calibration — bracketing across score bands:Let me read a few key anchor papers to calibrate. I'll focus on the most topically relevant ones.Let me also read the brain-inspired continual learning paper at score 4.00 and a strong reject anchor:Now I have sufficient calibration data. Let me establish my bracket and finalize.

**Round 1 Bracket:**
- Score 1.0 (strong reject): Papers with no real contribution or pseudoscience. OML is not this bad — it has a clearly specified method with novel mechanisms.
- Score 2-3 band: MIMOSA (2.60), Optimal HDC (3.00) — rejected for weak experiments on limited datasets, overclaimed contributions. OML shares the toy-scale evaluation problem.
- Score 3.5-5 band: FlyOrien (4.33), Brain-inspired CL (4.00), Beyond Unimodal (4.33) — rejected with merits, bio-inspired with limited evaluation and weak baselines. Very similar profile to OML.
- Score 5.5+: Accepted or borderline papers with stronger evaluation.

**Initial bracket: 3.0–4.0.** The paper sits between the 3.0 band (overclaimed but underevaluated contributions) and the 4.0 band (interesting bio-inspired ideas with insufficient evaluation). Key differentiators: (1) unlike the 4.0 papers, OML has an entirely unevaluated headline contribution (HITL); (2) it has genuinely novel reference extraction unlike the ~3.0 papers; (3) no dataset statistics, ablations, or error bars puts it on the weaker side.

Now let me write the final consolidated review.

---

## Summary
The paper proposes OML, a hierarchical modular neural network for online multimodal learning. It introduces feature neurons, unimodal association neurons, and multimodal association neurons connected by ascending, descending, and lateral pathways. The key technical contributions are: (1) a reference extraction algorithm using coefficient of variation to determine which features a word refers to (e.g., color vs. shape), (2) frequency-based signal routing via λ parameters for cross-modal communication, and (3) a conflict detection mechanism enabling human-in-the-loop interaction. Experiments are conducted on small fruit and household object datasets with visual and auditory modalities.

## Strengths
- **Novel reference extraction mechanism (Section 3.4)**: The coefficient-of-variation approach for determining which features a word refers to is mechanistically clear and genuinely novel. The paper demonstrates (Figure 3a, Section 4.1(2)) that "hóng sè" (red) selectively binds to color features rather than shape features — a capability explicitly absent from ART and AEN, which "treat the name words and color words without difference" (Section 4.1(2)). This is the paper's most distinctive contribution.
- **Systematic treatment of learning scenarios (Section 3.5)**: The four cases exhaustively enumerate all combinations of modality recognition states (both recognized, neither recognized, each recognized alone), with precise update rules for each. This provides a complete, mechanistically specified online learning algorithm.
- **Frequency-based signal routing with λ parameters**: The mechanism for routing signals to correct modality channels is architecturally distinctive. Table 3 provides concrete evidence that it works: "tián" (sweet) routes to the taste channel and "hóng sè" (red) routes to the visual channel, whereas AEN "cannot distinguish whether a word refers to a taste or visual concept" (Section 4.1(3)).

## Weaknesses

### Fatal
None

### Major
- **Toy-scale evaluation with unreported dataset statistics** — The entire evaluation uses two small fruit/object datasets (Fruits from Xing et al. 2019, HomeF from Lai et al. 2011) and their augmented variants. The paper never reports dataset sizes, number of classes, number of samples, feature dimensionalities, or train/test split details. Section 4 states "we divide the dataset into four equal parts, each containing different classes" for the open environment but gives no further characterization. The method's core mechanisms (pairwise distance computation against all existing neurons, dynamically growing architecture) raise obvious scalability questions that are never addressed. For a venue like ICLR, the absence of even basic dataset statistics is a significant omission, and the restriction to toy-scale datasets leaves the generality of the approach undemonstrated.

- **Human-in-the-loop contribution is prominently claimed but essentially unevaluated** — Section 1 lists conflict detection and user interaction as one of two defining attributes. Section 3.5 devotes substantial space to the mechanism (four scenarios with conflict checking, question formulation, and update rules based on user answers). Yet Section 4 states: "if the question posed to the user by OML remains unanswered for a certain period of time, we set the answer to be positive." In practice, no human is ever in the loop. The only evaluation mention is a single qualitative sentence: "when we randomly add 10% of word-image or word-taste data pairs with incorrect matches, OML is able to detect all conflicts" (Section 4.1(3)) — with no quantification, no systematic analysis of conflict rates or false alarms, no comparison of learning with vs. without the mechanism, and no user study. A contribution prominently claimed must be properly evaluated.

- **No ablation studies** — The paper presents a multi-component system (lateral connections, frequency-based routing, reference extraction, conflict detection) but never isolates any component's contribution. It is impossible to determine which design choices drive performance and which are inert.

### Minor
- **Handcrafted feature pipeline** — The backbone uses SAM for segmentation, then computes Fourier descriptors (shape), mean color values, and MFCCs (audio) as features. While the paper's contribution is the learning mechanism rather than representation learning, the reliance on hand-engineered features makes it unclear how the system would function with learned representations at larger scale.

- **Reference extraction generalizability uncharacterized** — The CV-based approach (Section 3.4) assumes that the feature dimensions a word refers to will show low variance while non-referred dimensions show high variance. This holds for the color/shape dichotomy in fruits, but the paper does not discuss when this assumption breaks — e.g., words like "fruit" that refer to concepts with high variance across all low-level features.

- **No error bars or variance across runs** — All tables report single numbers with no indication of variability across random orderings or seeds.

- **Brain-inspiration framing is superficial** — Figure 1 labels brain regions (V1–V4, IT, IPS, PF, PM, IFC, IPL, AC) and the paper claims the method does "learning like the way humans do" (Abstract). However, the actual mechanisms (threshold-based matching, coefficient-of-variation statistics, Fourier-based routing) have no demonstrated correspondence to neuroscience. No neuroscience literature is cited to support specific mechanism choices. The hierarchical modular structure is shared by many computational architectures that make no neuroscience claims.

### Trivial
None

## Nice-to-Haves
- Scalability analysis: neuron count, computation per sample, and memory as a function of concepts learned — essential for a dynamically growing architecture.
- Comparison against continual learning methods (EWC, PackNet, etc.) in the multimodal retrieval setting.
- Even a simulated user study: inject varying rates of conflicting data, vary the simulated user's answer accuracy, and measure how learning quality degrades.
- Forgetting curves or per-class accuracy over time in the open environment, rather than just aggregate final numbers.
- Targeted experiments for reference extraction beyond color/shape: vary the number of feature types, degree of feature correlation, and test with words that refer to multiple feature types simultaneously.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Evaluation protocol uses different correctness criteria for baselines (Tables 2, 3)**: The reviewer notes that imprecise retrieval by ART/AEN is "counted as correct" in Tables 2 and 3. However, the paper explicitly states this, and the asymmetry *favors the baselines* — OML is held to a stricter standard. This makes OML's advantage appear smaller, not larger. Removed per hard rule: unfair comparison that favors the baseline, not the author's method.
- **T parameter existence**: The reviewer questions why the parameter T in Eq. (1) exists if "its value does not affect the algorithm" (Section 3.1). This is a minor notational/presentation point, not a substantive weakness.
- **"Extensive experiments" phrasing in conclusion**: Section 5 states "we designed extensive experiments" — this is a style concern, not a technical weakness.

## Novel Insights
The reference extraction algorithm — using coefficient of variation across accumulated cross-modal signals to determine which feature subspace a word refers to — is a genuinely novel mechanism for grounded language learning. The insight that referential stability (low CV in referred dimensions vs. high CV in non-referred dimensions) can be computed incrementally during online learning, without supervision on the word-to-feature mapping, could inspire future work in symbol grounding and multimodal concept acquisition. The frequency-based routing via λ parameters for maintaining modality separation in cross-modal signal propagation is also architecturally distinctive, though its advantages over simpler routing mechanisms remain uncharacterized.

## Suggestions
1. Report complete dataset statistics (sample counts, class counts, feature dimensionalities, train/test splits) — this is a minimum baseline for reproducibility.
2. Evaluate the human-in-the-loop mechanism properly: at minimum, a simulated study with varying conflict injection rates (5%, 10%, 20%, 50%) and varying user accuracy (perfect, 90%, 80%) to characterize when the mechanism helps and when it fails.
3. Add ablation studies: remove lateral connections, remove frequency routing (use a simpler routing), remove conflict detection, and measure performance impact of each.
4. Characterize the reference extraction algorithm's limits: test with words referring to multiple feature types, abstract concepts, and relational properties.
5. Report scalability metrics: number of neurons created, inference time, and memory as a function of training samples processed.

## Score and Decision

**Anchor comparison table:**

| Paper | Path | Avg Score | Round | Comparison to OML |
|-------|------|-----------|-------|-------------------|
| Financial Markets NN | nSDOkm0SKo | 1.00 | R1 | Far worse — no real methodology; OML has a complete system |
| Cross-Lingual Humanoid Robots | gwZ90hFSL2 | 1.00 | R1 | Far worse — speculative with no experiments; OML has quantitative results |
| Clothing-Irrelevant L-ReID | 5lUdTogEL3 | 1.00 | R1 | Far worse — fundamental methodological issues; OML is technically coherent |
| IC-Light | u1cQYxRI1H | 10.00 | R1 | Far better — strong method, large-scale experiments, clear contribution |
| MIMOSA | uffmkDtlR2 | 2.60 | R1 | Similar toy-scale issue but MIMOSA lacks novelty; OML has more novel mechanisms |
| Explainable Multi-Modality | ky2JYPKkml | 3.00 | R1 | Similar profile — concept-based multimodal with limited datasets |
| Projected Subnetworks | WM5G2NWSYC | 2.00 | R1 | Weaker method; OML has more complete system |
| Optimal HDC | NYPJz0CL5X | 3.00 | R1 | Similar — neurally-inspired with only small-scale validation, overclaimed |
| Brain-inspired CL | 0CtIt485ew | 4.00 | R1 | Similar bio-inspired profile but Artsy has better experimental rigor; OML's unevaluated HITL claim is worse |
| FlyOrien | jYyste2HLP | 4.33 | R1 | Very similar — bio-inspired incremental learning, limited evaluation; FlyOrien has slightly better characterization |
| SNN Online Training | JAnyCnK5In | 4.75 | R1 | Better evaluation rigor; OML's novelty is comparable but evidence is weaker |
| Beyond Unimodal Learning | Pa6SiS66p0 | 4.33 | R1 | Similar — multimodal CL with weak baselines; both lack rigorous evaluation |
| Cognitive Dissonance LLMs | cHyQT6Y1jY | 5.75 | R1 | Thematically related (conflict detection in learning) but much stronger evaluation |
| Shared Decodable Concepts | L07zWidgdW | 6.75 | R1 | Much stronger — rigorous neuroscience + ML with proper evaluation |
| Concept Representations | vogtAV1GGL | 5.75 | R1 | More rigorous theoretical grounding; OML is weaker |
| Epitopological Learning | iayEcORsGd | 7.33 | R1 | Much stronger — deep theoretical contribution with extensive validation |
| Visual Cortex Invariance | kbjJ9ZOakb | 8.00 | R1 | Far stronger — rigorous method with proper evaluation |
| Multi-modal TTA (READ) | TPZRq4FALB | 8.00 | R1 | Far stronger — proper baselines, ablations, multiple datasets |
| Brain Bandit | RWJX5F5I9g | 8.00 | R1 | Far stronger — theoretical grounding + strong experiments |
| Compositional Entailment | 3i13Gev2hV | 8.00 | R1 | Far stronger — proper scale, rigorous evaluation |

**Round 1 bracket: 3.0–4.0**

**Narrowing rationale:** OML has more novel mechanisms than the ~3.0 papers (MIMOSA, Optimal HDC), which tips it slightly higher. However, compared to the ~4.0 papers (Brain-inspired CL, FlyOrien, Beyond Unimodal), OML has a critical additional problem: one of its two headline contributions (HITL) is entirely unevaluated, and it lacks even basic dataset statistics that the 4.0 papers typically provide. The combination of (1) unevaluated headline contribution, (2) missing dataset statistics, (3) no ablations, and (4) no error bars — despite having genuinely interesting ideas — places OML at the lower end of this bracket.

**Final score: 3.0** — The paper proposes interesting mechanisms (especially reference extraction) but its evaluation falls significantly short of ICLR standards. The human-in-the-loop contribution, one of two headline claims, is essentially unevaluated. The experiments are at toy scale without basic dataset statistics, ablations, or error bars. While the ideas have potential, the evidence base is insufficient to support the claims.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>