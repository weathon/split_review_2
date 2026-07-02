# Weakness Reliability Guideline

Use this guideline to judge whether a weakness raised in a paper review is RELIABLE (well-grounded, paper-specific, actionable) or UNRELIABLE (matching one of the error patterns below).

## Error type table

| Error Type | Explanation |
|---|---|
| Misunderstanding | The reviewer misinterprets claims or ideas presented in the paper, leading to inaccurate or irrelevant comments. |
| Neglect | The reviewer overlooks important details explicitly stated in the paper, resulting in unwarranted questions or critiques. |
| Vague Critique | The review lacks specificity, claiming missing components without clearly identifying what is missing. |
| Out-of-scope | The reviewer suggests additional methods, experiments, or analyses that are beyond the intended scope of the paper. |
| Invalid Criticism | The reviewer's criticism is considered invalid, especially when suggesting impractical experiments or trivializing results. |
| Superficial Review | The reviewer appears to have only skimmed the paper, providing generic or unsupported comments about the presence or absence of weaknesses. |
| Unstated statement | Statements made in the review are not supported by content in the paper. |
| Excessive demands | if the weaknesses are just asking for excessive things that are not necessary for a good paper. |
| Generic comment | weaknesses are just generic comments that can apply to any paper, without really pointing out the specific problems of the paper. |

## Unreliable weakness examples (per error type)

Each example is a real reviewer segment annotated by a human as UNRELIABLE, with the human's explanation of why. Do NOT assume a weakness is unreliable just because it is a criticism -- only mark unreliable when it matches one of these error patterns.

### Misunderstanding

*The reviewer misinterprets claims or ideas presented in the paper, leading to inaccurate or irrelevant comments.*

**Example 1**
> Reviewer wrote: But the core technical contribution is just an LM-based reweighting. Methodological nvoelty is a shortage.

Why unreliable: The method in this paper is not only about LM-based reweighting. For example, it has considered efficient generation of diverse prompts.They are the first to extract knowledge graphs of arbitrary relations from LMs.

**Example 2**
> Reviewer wrote: I gather that Transformer-XL uses a form of "top-k" sampling, that is, a generation mode more restricted than a standard (from the pure probabilistic viewpoint) "ancestral sampling". Such restricted sampling (as also beam-search) is known to improve the quality but limit the diversity of the generations. It would be interesting to see if you would obtain the same EBP conclusions with ancestral sampling.

Why unreliable: The authors do not use ancestral sampling

**Example 3**
> Reviewer wrote: This provides evidence that finetuning works more robustly than few-shot prompting, and that explicitly training to handle ambiguity helps generalization performance.

Why unreliable: The authors do not claim that finetuning works more robustly than few-shot prompting.

**Example 4**
> Reviewer wrote: The fact that this prompting fails on logical tasks (section 6) poses serious concerns on its applicability on harder problems other than simple mathematical operations and, therefore, its real-world utility.

Why unreliable: The authors never proposed anything universal. they focus on math reasoning only.

**Example 5**
> Reviewer wrote: Besides, it is well known that meta-learning methods are notoriously hard to tune and can be extremely sensitive to hyperparameter choices. It is hard to tune the framework on a large PLM with a small batch size.

Why unreliable: For hyperparameter setup, they do not perform per-task tuning but use a fixed set of hyperparameters, which works quite well for all tasks.

**Example 6**
> Reviewer wrote: It reads like the most significant contribution is using Google search as the information retriever compared with previous work using other search engines on Wikipedia, etc.

Why unreliable: The major contribution of this work is not using Google search as the retriever. The main contribution of this paper is to leverage the most up-to-date information online, instead of those traditional open-book QA methods. Since the LLM's parametric knowledge and the quick evolution of online knowledge have become more and more popular recently (2023~2024), I think this paper's contribution is also solid at 2021~2022.

**Example 7**
> Reviewer wrote: It is not clear if the external knowledge used is published or not, and if and how it is possible to obtain it.

Why unreliable: The method of acquiring external knowledge is not the focus of this paper.

**Example 8**
> Reviewer wrote: The metric called “precision@1” should be called “accuracy@1”

Why unreliable: The authors use precision as the evaluation metric for consistency of previous paper instead of accuracy.

**Example 9**
> Reviewer wrote: As far as I saw the Figure 2 and 3, the accuracy is heavily reflected by the amount data available during training and some normalization should be needed to compare these metrics each other without biases. Figure 3 also show some remarkable characteristics in translating only into C++, but the paper did not mention about this point.

Why unreliable: It is not that intuitive to compare the evaluation result to each other in Table 2 given the fact that they belong to different translation directions.

**Example 10**
> Reviewer wrote: These can happen in practice, but I'm not convinced flipping the label (essentially) is always beneficial especially in rare/infrequent classes settings.

Why unreliable: The proposed method did not "flip" the label in a hard assignment way, instead, they update the weight of soft assignment between the LF and label.

### Neglect

*The reviewer overlooks important details explicitly stated in the paper, resulting in unwarranted questions or critiques.*

**Example 1**
> Reviewer wrote: But all the tasks in your experiments are evaluated on high-level natural language understanding tasks, which typically require representations at higher layers.

Why unreliable: Figure 2 shows that the intermediate layer representation is effective on the QNLI and MRPC tasks.

**Example 2**
> Reviewer wrote: -It is not entirely clear how the shots are defined in the downstream tasks. Are they predefined in the scope of the datasets? This part can be more elaborated.

Why unreliable: The shots are already defined in Section 4. The reviwer overlooks it.

**Example 3**
> Reviewer wrote: It will be useful to see results for prompt tuning on other classification or QA tasks, for example from SuperGLUE, where the tasks require quite a different reasoning than LAMA.

Why unreliable: Similar results were indeed shown on three SuperGLUE tasks in Appendix B.

**Example 4**
> Reviewer wrote: Is it the performance for a given prompt? If so, that should be explained in the caption.

Why unreliable: Though the authors didn't mentioned the setting in caption, they did mention it in the paper.

**Example 5**
> Reviewer wrote: How could the findings benefit the community? The design principle of EncDec-based NMT is the sub-optimal performance/efficiency of LM-based NMT, and this paper just says: "yes, the intuition is true", which is not exciting at all.

Why unreliable: Authors point out that they conduted an analysis that was not done before and LMs are not always better than EncDec based NMT models

**Example 6**
> Reviewer wrote: Number of shots and classes: the numbers chosen here are a bit arbitrary and more concrete experiments could have been better.

Why unreliable: This is justified by the authors based on prior work as explanined in 4.3

**Example 7**
> Reviewer wrote: Usually, the bi-level formulations used in previous work present justifications of why such formulation is adopted, such as meta weight net, MAML, etc. However, no theoretical justification or intuitive explanation is given to explain the necessity and superiority of such a formulation in this paper.

Why unreliable: The paper provides intuitive motivation in Section 3.2 and Figure 2 for the usage of meta weight and bi-level optimization.

**Example 8**
> Reviewer wrote: It would be helpful if the author can show how much this will change the model's performance when the labels are correct.

Why unreliable: The authors show some results when the labels are correct in the third last paragraph of page 6 in the submission.

**Example 9**
> Reviewer wrote: The paper hints at the design of templates for the UniFew baseline but does not provide enough details for replication.

Why unreliable: Details about Unifew, including the exact prompt templates used for each task are already included in the appendices C and D (this is mentioned in lines 280-281 in the paper). The author also have included source code to facilitate replication. The reviewer overlooked them.

**Example 10**
> Reviewer wrote: In other words, the authors further need to whether the improvements over CB (in Table mainly come from by keeping or perfectly memorizing the corpus used for pretraining CB, or whether it comes from the use of new but well-matched corpus that is NOT seen when pretraining CB.

Why unreliable: This manuscript discusses it in section 5.5.

### Vague Critique

*The review lacks specificity, claiming missing components without clearly identifying what is missing.*

**Example 1**
> Reviewer wrote: The root cause of this is that the paper did not provide a reasonable criterion about acceptance of this experiment first.

Why unreliable: This is a vague critique and does not provide details.

**Example 2**
> Reviewer wrote: The experiment section is weak.

Why unreliable: Very subjective and vauge. The reviewer should provide explanations.

**Example 3**
> Reviewer wrote: This paper while taking a step in the right direction, seems a little premature for publication. That being said, the reported results my be of some value after all. It is hard to narrow down on the exact contributions of this paper.

Why unreliable: The reviewer seems to not provide many concrete ideas on this paper but subjectively says this paper is "premature for publication".

**Example 4**
> Reviewer wrote: _ "Our leading hypothesis here is that the LSTMs may actually relearn all weights without taking advantage of pretraining".

Why unreliable: The reviewer has forgotten to indicate the issue with this sentence from the paper

**Example 5**
> Reviewer wrote: The setting of using a shorter explanation becomes out of the general hypothesis. This might become a strength if it were presented as a limitation and not as a solution.

Why unreliable: This statement is vague and difficult to understand. The reviewer should provide reasons why to make this statement.

**Example 6**
> Reviewer wrote: some grammatical mistakes and typos.

Why unreliable: The reviewer should provide examples to illustrate the grammatical mistakes and typos.

**Example 7**
> Reviewer wrote: Individual problematic ingredients are neither being theoretically-proven nor empirically-proven.

Why unreliable: This is a vague and unreliable comment. The review does not specify what the "problematic ingredients" are. The experiments mentioned in this paper are all empirical analysis.

**Example 8**
> Reviewer wrote: The new findings are not particularly non-trivial.

Why unreliable: There is not enough justification provided by the reviewer for this claim.

**Example 9**
> Reviewer wrote: But the novelty of the proposed method is weak.

Why unreliable: It is unfair to claim weak novelty without offering much justification.

**Example 10**
> Reviewer wrote: I believe regardless of how good some of transfer learning models perform, we need to elaborate on situations those models collapse.

Why unreliable: It is not clear why the elaboration on model collapsing is needed

### Out-of-scope

*The reviewer suggests additional methods, experiments, or analyses that are beyond the intended scope of the paper.*

**Example 1**
> Reviewer wrote: Recently, the Chain-of-Thought prompting (https://arxiv.org/pdf/2201.11903.pdf) has been used by many papers using in-context learning, with reported improvements in model performance (the paper seems to have been cited already 100 times since its release earlier this year). One question this work does not address is whether model sensitivity/variance to retrieved prompts is also present when used in conjunction with chain-of-thought. And whether the vote-k scheme would be useful to limit the number of chain-of-thought annotations needed to improve in-context learning performance.

Why unreliable: This is a out-of-scope topic for this paper since the experiments are sufficient enough for general in-context learning. This could be a future work.

**Example 2**
> Reviewer wrote: Lastly, a final concern about real-world utility as the prompting does not perform well on harder problems (logical tasks).

Why unreliable: This is out of scope for the paper

**Example 3**
> Reviewer wrote: How does the pre-training (i.e., datasets, model design) of LLMs affect their multilingual abilities?

Why unreliable: The paper does not involve the pre-training of LLMs. I think this questions is out of the scope of this paper.

**Example 4**
> Reviewer wrote: The demonstrated examples are all for very basic arithmetic operations, and it is unclear whether this technique can scale to more complicated cases.

Why unreliable: out of scope for the paper

**Example 5**
> Reviewer wrote: What is the complexity (time and space) of weak supervision?

Why unreliable: The "time and space"complexity of weak supervision should not be a problem in the scope of this paper.

**Example 6**
> Reviewer wrote: It is not clear if and how the approach extends to other types of knowledge, outside of the e-commerce and products domain.

Why unreliable: This is not the focus of this paper

**Example 7**
> Reviewer wrote: (~) MTPB does not allow for "going back" (i.e., a user indicating that a generated response is wrong & clarifying their prompt).

Why unreliable: This paper focuses on factorizing a complex problem to simple subproblems, the "going back" is out of scope

**Example 8**
> Reviewer wrote: A more systematic analysis is needed to determine the optimal prompts that make the model capture a range of different patterns. This sentence seems to indicate that this will be the focus of the paper, but it isn't my understanding of the purpose of the paper.

Why unreliable: The reviewer's suggestion is off topic and is out of the scope of this paper.

**Example 9**
> Reviewer wrote: Since this is an examination work on multiple translation models and configurations, it would have been nice to provide a deeper analysis on the linguistic aspects of the experiments as well: Language pairs with different characteristics (morphologically rich languages for instance) work differently with different models. How different variations of the same model perform on different classes of languages is a significant question to investigate.

Why unreliable: Already paper has many experiments. Adding this would be out of scope

**Example 10**
> Reviewer wrote: In fact, this proposed method could be applied in sequence-to-sequence pretraining model, such as mT5. Have you explored this direction? Or leveraging synthetic parallel data generated by the GPT-3 to warm up the previous UNMT models?

Why unreliable: Out-of-scope. The main focus of this paper is decoder-only LMs.

### Invalid Criticism

*The reviewer's criticism is considered invalid, especially when suggesting impractical experiments or trivializing results.*

**Example 1**
> Reviewer wrote: 17- Section 7: the author mentions a key difference between T0 and FLAN model is that T0 is an encoder-decoder model which is pretrained and finetuned with different objectives. However, no clear comparison with FLAN model is presented in the paper

Why unreliable: Flan is a concurrent work, the author of this paper doesn't have the duty to compare T0 with the FLAN.

**Example 2**
> Reviewer wrote: While it's good to quantify the performance of models on time-stratified datasets, many conclusions are obvious, such as the synthetic experiments on question answering by shifting the end year of training data, as well as the experiments on self-containing reading comprehension.

Why unreliable: The "conclusions are obvious" shouldn't be the weakness.

**Example 3**
> Reviewer wrote: Results are not particularly surprising

Why unreliable: This is a invalid criticism. Many findings seem obvious in retrospect, but this does not mean that the community is already aware of them and can use them as building blocks for future work.

**Example 4**
> Reviewer wrote: There are models that accept more tokens, and some that claim to accept an unbound number (I expect them to deteriorate).

Why unreliable: But still token limitation is a problem with the free models available at that time.

**Example 5**
> Reviewer wrote: Another concern regarding the paper that I have is that most of the results are pretty well-known - e.g. performance of open-book models are better than parametric models, and Google search is better.

Why unreliable: "the results are well-known" should not be the reason for rejection. The experiments of this paper are simply to demonstrate the performance superiority of the internet-augmented method, instead of "demonstrating any conclusion".

**Example 6**
> Reviewer wrote: I would like to see the empirical results on stronger models, like RoBERTa related models.

Why unreliable: This is an example of a weak review provided by ACL It is not weak to have all the baselines not covered in the paper.

**Example 7**
> Reviewer wrote: More importantly, it requires highly-structured and large-scale in-domain data for pretraining, which might not be available in other domains.

Why unreliable: Perhaps there are other domains where there is a large amount of highly structured data. For example, data in the financial domain contains information about stock prices, stock reviews and other information.

**Example 8**
> Reviewer wrote: -- SentBERT → SentenceBERT or SBERT

Why unreliable: This is an overly harsh typo inspection.

**Example 9**
> Reviewer wrote: Various efficient routing functions should be compared with in this work, as intelligent routing functions achieve similar effects of improving parameter efficiency.

Why unreliable: Expert sharing and routing are orthogonal ideas

**Example 10**
> Reviewer wrote: The proposed method (objectives) is hard to transfer to other domains.

Why unreliable: Most pre-trained objectives that incorporate domain knowledge have such problems. However, it is still a meaningful research for a specific domain.

### Superficial Review

*The reviewer appears to have only skimmed the paper, providing generic or unsupported comments about the presence or absence of weaknesses.*

**Example 1**
> Reviewer wrote: The proposed continual knowledge learning problem is quite interesting and important.

Why unreliable: This statement is quite vague even though it is a strength. It does not provide enough context to other reviewers or the AC as to the paper's exact strengths.

**Example 2**
> Reviewer wrote: The FUAR metric is also technically sound.

Why unreliable: This statement is very vague and not reliable as there are no supporting evidence for the claim.

**Example 3**
> Reviewer wrote: Quality and Significance: Overall, this is a good application method and might be useful for many practical applications.

Why unreliable: Need more detail for this claim. There is very little context to the statement making it not very reliable.

**Example 4**
> Reviewer wrote: Compared to the FCM in this paper, I think the performance of causal masking methods from [2] might be better.

Why unreliable: This claim is not backed by evidence

**Example 5**
> Reviewer wrote: This paper proposes a new few-shot learning method for NLP problems by incorporating a simple,effective framework.

Why unreliable: The summary is too general and not specific to the main focus of this paper.

**Example 6**
> Reviewer wrote: Designing metrics for exposure bias is a novel task, and this paper invented appropriate approaches.

Why unreliable: This work is not demonstrated to be novel and the statement is too brief to explain the novelty of the work.

**Example 7**
> Reviewer wrote: The empirical results are solid and strong.

Why unreliable: The experiments are kind of limited in a narrow domain for the proposed general method. Thus, it is difficult to say results are solid and strong.

**Example 8**
> Reviewer wrote: The proposed continual knowledge learning problem is quite interesting and important. The benchmark is useful and the proposed FUAR metric is technically sound.

Why unreliable: Repetitive comments without any description of the comments made. The reviewer already mentions the same before and in both cases provides no supporting evidence for the claim.

**Example 9**
> Reviewer wrote: The paper doesn't have too many weaknesses.

Why unreliable: This statement is superficial and indicates that the reviewer might not spend enough time checking the details of this paper.

**Example 10**
> Reviewer wrote: The authors did mention one ablation in the supplementary that I missed, but I don’t think that is sufficient for a reader to understand how to build on this method in this future without re-running all the experiments, doing an extensive hyperparam search, etc.

Why unreliable: This comment is too general. Most papers have this limitation.

### Unstated statement

*Statements made in the review are not supported by content in the paper.*

**Example 1**
> Reviewer wrote: Ease of use, being conceivably language agnostic, training more efficiently and allowing easy reimplementation (pytorch), make this work a welcome contribution to the field.

Why unreliable: This paper did not upload the code when it was submitted, and the conclusion of this review cannot be verified.

**Example 2**
> Reviewer wrote: Like previous work, they perform multitask prompted fine-tuning on 40+ NLP tasks but while retrieving from external knowledge sources to perform the task.

Why unreliable: There is no (multitask prompted) fine-tuning on 40+ NLP tasks in this paper

### Excessive demands

*if the weaknesses are just asking for excessive things that are not necessary for a good paper.*

_No examples available in the source dataset._

### Generic comment

*weaknesses are just generic comments that can apply to any paper, without really pointing out the specific problems of the paper.*

_No examples available in the source dataset._

## Reliable (valid) weakness examples

Each example below is a real reviewer weakness segment annotated by a human as RELIABLE (a genuine, well-grounded criticism). Use these to calibrate: many critical-sounding weaknesses ARE reliable. Only mark reliable=0 when the segment clearly matches one of the error patterns above.

**Example 1**
> Reviewer wrote: Lack of detail analysis on the computational efficiency.

**Example 2**
> Reviewer wrote: In order to improve the paper, I recommend providing more insights into the workings of the method and the bias that the fixed structure like tucker decomposition can lead to.

**Example 3**
> Reviewer wrote: It is unclear why such big memories are still improving the model.

**Example 4**
> Reviewer wrote: Sec 4. --If your introduced bitext retrieval objective uses batch size, experiments comparing the effect of batch size is necessary.

**Example 5**
> Reviewer wrote: Maybe a logical tree of some sort can help improve readability here.

**Example 6**
> Reviewer wrote: Another choice made by the authors is to use only the values in FIM corresponding to the adapters.

**Example 7**
> Reviewer wrote: I don't see the point of compare different variants of LLMs with or without pre-training.

**Example 8**
> Reviewer wrote: This is not critical: this is still acceptable for the first observation.

**Example 9**
> Reviewer wrote: However, there are some concerns about experimental settings.

**Example 10**
> Reviewer wrote: Besides, the data gathering method also relies on hand-designed templates (Line 220).

**Example 11**
> Reviewer wrote: I am unclear of some of the experimental settings and how much we can conclude from them.

**Example 12**
> Reviewer wrote: I know that this can make the size of compressed model really amazing (e.g., 1.8M) and the compression ratio amazing (e.g., 86M/12.3M=7) but is not fair as the whole model including the embedding layer are used when deploying.

**Example 13**
> Reviewer wrote: There are some hints that the gains might be partly related to regularization (eg, better results on IWSLT than WMT).

**Example 14**
> Reviewer wrote: The meaning of the different-colored tokens could also be explained in the caption.

**Example 15**
> Reviewer wrote: The proposed method is novel in that it is effective and scalable.

**Example 16**
> Reviewer wrote: To explain more previous weakness, I was not clear when reading if it is enough to do prompt re-formatting or aggregation is also necessary.

**Example 17**
> Reviewer wrote: This is mentioned several times in the manuscript but it looks to just boil down to using the aforementioned prompting technique.

**Example 18**
> Reviewer wrote: I don't think the paper, overall, is particularly novel.

**Example 19**
> Reviewer wrote: (2) Unclear cost for running the proposed methods against the standard-prompting models.

**Example 20**
> Reviewer wrote: However, it would have been interesting to see tasks or domains where improvement is more significant.

**Example 21**
> Reviewer wrote: To add value, authors should have explored other text summarization datasets with different writing styles to really bring out the different style biases rather than just paraphrasing.
