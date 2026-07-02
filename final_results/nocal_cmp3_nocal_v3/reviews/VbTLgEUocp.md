## Summary

This paper presents Calgacus, a protocol that uses an LLM to hide one text (the secret message) inside another text of exactly the same length (the stegotext). The method records the rank of each token of the secret message in the LLM's probability distribution, then uses those ranks as a sampling policy to generate a different text that follows a steerable prompt. The protocol is clearly described, strikingly simple, and correct. The paper also develops a philosophical discussion about what this capability implies for LLM knowledge, hallucinations, and authorial intent.

## Strengths

- **The core protocol is genuinely clever and cleanly specified.** Encoding a text by recording token ranks and then decoding by regenerating those ranks from a different prefix is an elegant idea. The recipe in Section 3 is precise and immediately implementable. The "full capacity" property (same-length secret and stegotext) is a genuinely distinctive feature relative to prior LLM steganography work.

- **The examples in Figure 1 are concrete and compelling.** Hiding a political speech inside a roast boar recipe makes the protocol's capability vivid and does real communicative work in the paper. These examples alone demonstrate the method is functional.

- **The "low entropy token choices" analysis (Section 3) provides a correct, mechanistic explanation** of why stegotexts have systematically lower log-probability than originals. This connects the method's mechanism to its empirical behavior with genuine insight.

- **The protocol's decoding correctness is sound.** The paper correctly exploits the property that a token's rank in a sorted probability list is recoverable from the stegotext, making the scheme information-theoretically exact.

## Weaknesses

### Fatal

None.

### Major

- **The evaluation is too narrow to support the method-level claims at a top venue.** The empirical evidence rests on 3 source texts (chosen at μ, μ−2σ, μ+2σ from 1000 Reddit posts), each generating 100 stegotexts at exactly 85 tokens, evaluated primarily by log-probability under Llama 3 8b (with one additional model check in the appendix). 
  - **No baseline comparison.** The paper distinguishes itself from prior methods (Ziegler et al., 2019; Kaptchuk et al., 2021; Zamir, 2024) in the related work but never provides any quantitative comparison—bits-per-token capacity, stegotext quality (perplexity), or computational cost. This makes it impossible to assess what "full capacity" buys in practice relative to existing approaches.
  - **No human evaluation of stegotext quality.** The paper asserts that "while for a human both the original and fake texts are plausible" (line 132) but provides no human judgments. Log-probability is a useful proxy but not equivalent to human perception of coherence, naturalness, or meaningfulness—especially for a method whose core claim is that text is plausible to human readers.
  - **No length generalization evidence.** All tests use 85-token texts with no justification for this choice and no data on longer or shorter texts.
  - These gaps mean the reader cannot assess the method's reliability across diverse inputs. The protocol is demonstrably correct, but how often it produces high-quality output (versus the kind of broken output shown for the hash example) is unknown.

- **The security analysis is entirely theoretical with no empirical evaluation.** Section 3.1 discusses brute-force complexity (O(d^|k|)), attacker knowledge of the LLM, and deniability through bogus keys, but there is no empirical test of:
  - Whether a statistical classifier or simple steganalysis method can distinguish Calgacus stegotexts from real text. (Log-probability overlap is one signal; n-gram statistics, compression-based analysis, or re-tokenization are standard checks that are absent.)
  - How much information about k leaks through s (the paper acknowledges this as "an open research question" rather than addressing it).
  - A quantitative estimate of deniability strength.
  The paper frames its contribution partly as a steganographic protocol, and the absence of any detection-resistance evidence is a significant gap. That said, the paper explicitly declines to build a formal security model (line 61), and the security discussion is presented as preliminary—this weakness is large but not a fatal invalidation of the core contribution.

### Minor

- **The steerability claim is stated but not quantitatively evaluated.** The paper claims "the topic and tone and style of the fake text are steerable" (line 19) and provides examples (Figure 1) showing different keys produce different-looking stegotexts. However, the evaluation only checks whether stegotext log-probabilities fall within the real-text distribution—it never verifies whether the generated text actually matches the intended topic/style set by k. A stegotext with plausible log-probability that ignores the key's topic is a steerability failure, and this is not checked at scale.

- **Failure cases are acknowledged but not quantified.** The paper provides an example of a hash encoded as a source text producing broken output (line 122), which demonstrates that failure modes exist. However, no failure rate analysis is reported for the 3 × 100 = 300 tested stegotexts. Were all 300 coherent? What fraction was usable? This matters because the paper's core claim about producing "coherent and plausible" text hinges on typical-case success.

- **The choice of 85 tokens is not justified.** The paper truncates all texts to exactly 85 tokens but gives no rationale for this specific length.

- **No statistical tests comparing the real-text and stegotext distributions.** Figure 4 shows the distributions visually overlap, but a Kolmogorov-Smirnov test or similar would clarify whether they are significantly different in the aggregate.

### Trivial

None.

## Nice-to-Haves

- A comparison table with prior methods (Ziegler et al., Meteor/Kaptchuk et al., Zamir) quantifying bits-per-token capacity, stegotext perplexity, and generation cost would clarify the practical contribution enormously.
- A small human evaluation (e.g., 100 stegotexts rated on fluency, or an A/B test with real texts) would substantiate the claim that stegotexts are "plausible" to humans.
- Statistical classifier-based detectability analysis (real vs. Calgacus text) is a standard steganography evaluation that would strengthen the paper.

## Removed Points

- **"Approximately 60% of the body text is philosophical reflection."** This is factually incorrect: the discussion section (lines 168–246) constitutes roughly 32% of the body text (246 lines), not 60%. The underlying observation that the paper mixes method and position is valid, but the specific figure is wrong and the characterization is exaggerated.
- **"No empirical evaluation of robustness to common steganalysis techniques."** The paper explicitly frames its security analysis as preliminary and states "we will avoid building a palace on the sand, and not frame our method in a formal model of steganography" (line 61). The security gap is real but overstates the paper's stated ambitions to frame it as missing a required evaluation.
- **"Cannot assess Calgacus against human perception"** is partially addressed by the log-probability proxy and the concrete examples; the strength of the claim remains limited.

## Novel Insights

The reviews surface an important tension this paper creates but does not resolve: the "full capacity" property (same-length stegotext) is structurally elegant and practically appealing, yet the very feature that makes the method distinctive (encoding through rank-preserving token selection) is also what makes the stegotexts systematically less probable than originals—and therefore detectable by an informed adversary with LLM access. The paper honestly identifies this tradeoff and exploits it for deniability, but the reviews highlight that this tradeoff's practical consequences are not empirically characterized. This is a genuinely interesting design tension: full capacity comes at the cost of a systematic statistical signature that the paper lacks the evaluation to bound.

## Suggestions

1. **Scale the evaluation within the paper's own framework.** Increase to 30+ source texts (not 3), test at multiple lengths (e.g., 50, 100, 200 tokens), and verify steerability explicitly (e.g., do raters or an LLM judge correctly identify the intended topic of s from k?).

2. **Add baseline comparisons.** A simple table comparing Calgacus to Ziegler et al., Kaptchuk et al. (Meteor), and Zamir on capacity (bits/token), stegotext perplexity, and computational cost would dramatically clarify the contribution.

3. **Quantify failure rates.** For the tested stegotexts, report what fraction were judged coherent (by any criterion) and how ranks of the source texts predict output quality.

4. **Add one detection-resistance experiment.** A basic logistic classifier or threshold detector on n-gram statistics would provide the first empirical security data point, which is far better than none.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>