## Summary

Quantum-RAG introduces a learnable phase-augmented similarity kernel for dense retrieval, inspired by quantum interference, and validates it on a newly constructed Punjabi NLP stack comprising a 35GB corpus, a 124M-parameter decoder-only model (PunGPT2), a dense retrieval system (Pun-RAG), an instruction-tuned variant (Pun-Instruct), and a new evaluation benchmark (PunjabiEval). The kernel extends cosine similarity by multiplying query embedding dimensions by learnable complex phases, with the hybrid system combining BM25, cosine-dense, and phase-kernel scores.

---

## Strengths

- **Substantive Punjabi NLP resource contribution**: The 35GB corpus (4.8M documents, dual-script coverage) and full model suite (PunGPT2/Pun-RAG/Pun-Instruct) represent a genuine and rare resource for an under-resourced language. PunGPT2 achieves far lower perplexity than multilingual models on Punjabi text, as expected for a dedicated in-language model.
- **Differentiable, lightweight kernel design**: The phase kernel is differentiable (gradient flows to both encoder and phase vector θ), adds only O(d) overhead per pair (~9–12% latency increase), and cleanly reduces to squared cosine when all phases collapse to zero. This is a reasonable and practical design choice.
- **Human evaluation rigor**: Ten native-speaker annotators rating 1,000 outputs each, with Fleiss' κ = 0.71 and 95% bootstrap CIs, is more careful than most comparable papers.

---

## Weaknesses

### Fatal

**The headline claim is misrepresented.** The abstract states Quantum-RAG yields "+7.4 Recall@10 over FAISS." However, Table 7 shows:
- FAISS (cosine): 62.7
- Quantum-only (K, i.e., the phase kernel alone): 64.3 → **+1.6 over FAISS**
- Hybrid (Quantum-RAG = BM25 + cosine + K): 70.1 → **+7.4 over FAISS**

The +7.4 gain is achieved by the three-component hybrid system vs. single-component FAISS retrieval, not by the phase kernel per se. There is **no BM25+FAISS hybrid baseline** in Table 7. Without knowing the Recall@10 of a BM25+FAISS (without phase) hybrid, there is no way to isolate the marginal contribution of the quantum phase kernel in the hybrid setting. The paper's central technical claim—that the phase-augmented kernel substantively improves retrieval—rests on this missing comparison. Based on the reported numbers, the phase kernel's isolated gain is only +1.6 Recall@10; the rest comes from standard hybrid fusion that is entirely independent of the proposed method.

### Major

**Inconsistency between Figure 4 and Table 6.** The bar chart in Figure 4 reports Quantum-RAG ROUGE-L ≈ 45 and Pun-RAG ≈ 48, whereas Table 6 reports 40.1 and 38.5 respectively. Furthermore, a model called "PuroBT" appears in Figure 4 but is never mentioned, defined, or described anywhere else in the paper. These inconsistencies undermine confidence in the reported numbers.

**Misleading perplexity comparisons (Table 5).** mBERT and MuRIL are encoder-only models adapted with a "lightweight decoder"—an approach that is neither standard nor a fair generation baseline. The resulting perplexity gap (42 → 2.24) is almost entirely a consequence of comparing a dedicated Punjabi decoder-only model to an encoder model with an ad-hoc decoder, not evidence of anything methodologically novel.

### Minor

**The "quantum" framing is not well-founded.** The mechanism is a learnable complex-phase rotation on real-valued embedding dimensions. While the interference analogy is intuitive, the term "quantum" is inaccurate: there is no superposition of states, no quantum amplitude, and no quantum hardware. This framing risks misleading readers about the nature of the contribution. The method is more accurately described as a learnable complex-weighted dot product.

**Cross-lingual results are thin.** Hindi and Bangla experiments use 1k-query subsets, do not report confidence intervals or significance tests, and give no details about corpus size or retrieval setup. These results cannot be verified or built upon.

### Trivial

Equation 2 uses the same symbol on both sides (x̂_i = x̂_i e^{jθ_i}) — almost certainly a notation artifact.

---

## Nice-to-Haves

- Add BM25+FAISS hybrid (α > 0, β > 0, γ = 0) as a row in Table 7 to isolate the phase kernel's marginal contribution within the hybrid setting.
- Apply Quantum-RAG on top of a well-established multilingual encoder (e.g., mE5, LaBSE) to test whether the kernel is useful outside the custom PunGPT2 embedding space.
- Provide details on training data and corpus for the Hindi/Bangla cross-lingual subsets.

---

## Novel Insights

The paper's most interesting observation (largely implicit) is that the phase kernel's O(d) overhead with a 9–12% latency cost provides a path to learning dimension-level interaction patterns that cosine similarity cannot express, without moving to late-interaction models (ColBERT-style) that require storing per-token representations. If the missing hybrid ablation were provided and the gain were confirmed, this would be a practically valuable finding for resource-constrained retrieval systems. However, as currently reported, the isolated kernel gain of +1.6 Recall@10 is modest, and whether this reflects genuine dimension-level interference learning vs. added model capacity is unclear.

---

## Suggestions

1. Add the missing BM25+FAISS (no phase kernel) hybrid row to Table 7 immediately — this is the single most important fix.
2. Reconcile Figure 4 values with Table 6 and explain or remove "PuroBT."
3. Either remove or reframe "quantum" terminology to avoid misleading claims about the physical basis of the method.

---

## Score and Decision

The Punjabi NLP stack is a genuine community resource, and the phase kernel is a technically coherent (if modest) extension of cosine similarity. However, the paper's central empirical claim is presented in a way that conflates the hybrid fusion benefit with the kernel benefit, the key ablation needed to evaluate the core contribution is absent, and the figures contain unexplained inconsistencies with the tables. These are not minor presentation issues—they directly determine whether the method's contribution is real and how large it is.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>