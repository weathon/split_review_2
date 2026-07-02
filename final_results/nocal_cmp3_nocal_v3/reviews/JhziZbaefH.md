Now I have thoroughly verified every claim against the paper. Let me write the consolidated review.

---

## Summary

The paper proposes OML, a brain-inspired neural network for online multimodal learning with hierarchical modular architecture (feature neurons, unimodal association neurons, multimodal association neurons) connected via ascending, descending, and lateral pathways. The system dynamically grows new neurons for unseen concepts, uses a coefficient-of-variation-based mechanism to extract which features a word refers to, and performs rule-based conflict detection that triggers human-in-the-loop interaction. Experiments on small fruit-image/Chinese-word datasets demonstrate cross-modal retrieval in close and open (sequential class) environments.

## Strengths

- **Reference extraction via coefficient of variation (Section 3.4).** The idea of using the stability of feature dimensions across samples to determine which features a word refers to (e.g., "red" → color, not shape) is conceptually novel and well-motivated. The mechanism exploits a simple statistical observation that relevant dimensions will have lower relative variance after sufficient samples.

- **Modal extension experiment (Table 3, VAT/VAT-HomeF).** Testing the addition of a taste modality after the network has already been trained on vision and audition is an underexplored and practically relevant capability. OML outperforms AEN across all retrieval directions (T→V, T→A, V→A, V→T, A→V, A→T), with margins of 2–4 percentage points.

- **Open environment results against other online methods (Table 1).** In the open environment setting (disjoint classes introduced sequentially), OML achieves 89.0–89.8% on Fruits and 83.6–85.5% on HomeF, outperforming ART (83.0–84.2% and 78.6–80.8%) and AEN (84.9–86.2% and 80.4–82.3%). This provides genuine evidence that OML's growing-network architecture handles sequential learning better than existing online alternatives.

## Weaknesses

### Fatal
None.

### Major

1. **Conflict detection claim is unsubstantiated (Section 4.1, line 250).** The paper states: *"when we randomly add 10% of word-image or word-taste data pairs with incorrect matches, OML is able to detect all conflicts and raise appropriate questions."* This single sentence is the entire support for one of the paper's two flagship claims (the human-in-the-loop interaction capability). There is no table, no figure, no experimental setup (number of trials, types of mismatches, detection threshold, false positive rate), and no quantitative result beyond "all." A claim of 100% detection on any task requires rigorous characterization. Without precision, recall, false positive rate, and failure case analysis, this claim cannot be evaluated.

2. **No ablation studies.** The method combines many hand-designed components: frequency-encoded cosine activation (Eq. 1), Gaussian-probability descending activations (Eq. 2), Fourier transforms in MANs (Eq. 6), coefficient-of-variation reference extraction (Eq. 7), lateral connections between similar feature neurons with threshold 2θ, and the entire conflict-detection/question-asking machinery. None of these components are ablated. It is impossible to determine which drive performance. For example, the entire performance difference in the open environment could plausibly be explained by the simple growing-neuron mechanism (add neurons for unrecognized inputs), with the frequency encoding and Fourier transforms being inert complexity or even detrimental.

3. **No statistical analysis.** Every number in Tables 1–3 is a point estimate. No error bars, standard deviations, or repeated runs with different random seeds are reported. Given the online and threshold-dependent nature of the learning process (sampling order, distance thresholds θ, probability thresholds ϑ, coefficient-of-variation thresholds r), the variance across runs could be substantial.

4. **Ambiguous comparison protocol for the open environment (Section 4, lines 223–224).** The paper states that in the open environment the dataset is split into 4 parts with disjoint classes and fed sequentially. Offline methods are described as being "iteratively optimized multiple times on the dataset" and "frozen after training." It is unclear whether offline methods in the open environment are (a) trained on all 4 parts together (as their paradigm would normally allow) and then tested, or (b) trained only on a subset and then tested on unseen parts. If (b), the comparison reveals only that frozen models fail on unseen-class data — a known property — not anything informative about OML's representational quality. The paper should clarify this protocol and, more importantly, compare against other online methods (which it does, and OML wins — but the ambiguity about offline methods undermines the presentation of results).

### Minor

5. **Evaluation limited to small, specialized datasets with hand-crafted features (Section 4, lines 187–188, 223).** Experiments use only fruit and home-object images (~tens of classes) paired with spoken Chinese names. Visual features are hand-crafted (Fourier descriptors of object boundaries + mean color), and auditory features are MFCCs. No experiments on standard multimodal benchmarks (e.g., MSCOCO, Flickr30K) or with modern learned features. This limits confidence in generalization.

6. **Human-in-the-loop simulation is trivial (Section 4, line 240).** The "interaction" is simulated by always answering "yes" if no response arrives within a certain period. This means the experiment tests only the case where all questions receive affirmative answers. The paper's claims about learning from user interaction are therefore based on a simulation that bypasses the interesting cases (conflict resolution, learning from negative answers, question appropriateness).

7. **Several design choices lack justification (Section 3).** (a) The frequency parameters λᵢ in Eq. (1) are assigned as unique natural numbers, but the paper does not explain why natural numbers or what happens when dimensions share a λ. (b) The Fourier transform in Eq. (6) converts signals to amplitude-frequency representation, but the paper never explains why the frequency domain is necessary or what physical interpretation it has — or why a simpler mechanism (e.g., direct vector matching) would not suffice. (c) The lateral connection threshold d(wᵢ, wⱼ) ≤ 2θ (line 85) and the coefficient-of-variation threshold r in Eq. (7) (lines 153–159) are asserted without justification or sensitivity analysis.

8. **Reference extraction evaluation is generous to baselines but not quantified on its own terms (Section 4.1, line 248).** The paper states that when baselines are queried with a color word, "they return all features (shape and color) ... we count this as a correct result for them." This is transparent and arguably conservative (biases against OML). However, there is no standalone evaluation of the reference extraction mechanism itself — e.g., how often does it correctly identify the referring feature dimensions, and under what conditions does it fail?

### Trivial
None.

## Nice-to-Haves

- Formalize the problem statement (input sequence, evaluation metric, task ordering assumptions) beyond the narrative introduction.
- Analyze network scalability: the system grows neurons for each new concept; discuss how it handles hundreds or thousands of concepts.
- Include failure case analysis for all claimed capabilities.

## Removed Points
- **"Evaluation is stacked by design" (reviewer's Critical Issue 1) — partially removed.** The reviewer's framing that the comparison is a "tautology" is too strong. OML also outperforms other online methods (ART, AEN), which are not frozen. The ambiguity is about offline methods, which is kept as a MAJOR weakness (#4 above) in weakened form.
- **"Precise referencing evaluation masks baseline performance" (reviewer's Critical Issue 2) — REMOVED as factually wrong.** The paper explicitly states it counts the baselines' imprecise retrieval as correct (line 248). This is generous to baselines, not biased toward OML. The transparency makes this a valid (if unusual) evaluation choice that, if anything, disfavors OML.
- **"Weak baselines and outdated comparisons" (reviewer's Critical Issue 5) — REMOVED.** The comparison set includes NRCH (2024), FUME (2025), ART (2025), and AEN (2021), which are recent. Only DAE (2011) and DBM (2014) are old, but they are standard baselines for multimodal representation learning. The suggestion of CLIP-based continual learning methods is scope creep for a paper using hand-crafted features and a completely different architectural paradigm.
- **"Abstract uses 'learning like humans'" — REMOVED as style nitpick.** This is a soft motivational claim, not a technical assertion the paper needs to prove.
- **"Related work is a flat list" — REMOVED.** Not a substantive weakness about the paper's contribution.
- **"Section 3.5 is rule-based, not learning" — REMOVED.** The rule-based approach is a design choice the paper explicitly describes; criticizing it as "not learning" mischaracterizes the contribution (growing networks with rule-based wiring are a valid approach to online learning).
- **"No formal problem statement" — MOVED to Nice-to-Haves.**

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Rigorously evaluate conflict detection.** Define the task, report precision/recall/false positive rate across multiple mismatch types, and characterize failure modes. This is essential for a paper claiming this as a core capability.

2. **Add ablation studies.** At minimum: remove frequency encoding (replace with standard distance-based activation), remove the Fourier transform in MANs (use direct matching), remove reference extraction (treat all features equally), and remove lateral connections. Report open-environment accuracy for each variant.

3. **Report statistics over multiple runs.** Provide means and standard deviations across at least 5 random seeds for all main results.

4. **Clarify the open-environment protocol for offline methods** and, if they are disadvantaged by the protocol, state this explicitly and focus the main claims on the comparison among online methods.

---

## Score and Decision

The paper identifies a genuinely interesting capability gap in multimodal learning — online learning with reference extraction and conflict-driven interaction — and proposes a novel architecture to address it. The reference extraction mechanism (coefficient-of-variation) is the paper's most creative contribution, and OML's performance against other online methods in the open environment provides real evidence of its effectiveness for sequential multimodal learning.

However, the evaluation has significant gaps that prevent the paper from standing as published. The flagship conflict detection claim (100% detection) rests on a single unsupported sentence. There are no ablation studies, no statistical rigor, and the human-in-the-loop simulation tests only affirmative responses. The paper's scope is also limited by very small datasets with hand-crafted features, leaving open questions about scalability and generalization. These weaknesses are addressable but serious: the paper needs a thorough reworking of its evaluation before its contributions can be reliably assessed.

<score>4</score>
<decision>Reject</decision>