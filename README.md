# LLMOracle4py

## LLM‑Based Test Oracle Generation for Python Programs

### Abstract
Semantic bugs or logic errors, which lead to incorrect outputs while allowing systems to remain operational, are widespread and costly to detect. Manual creation of test oracles is labour-intensive and domain‑specific, hindering scalable testing. We introduce LLMOracle4py, a language‑agnostic framework that automatically leverages large language models to generate derived test oracles. The framework extracts function signatures, docstrings, inputs, outputs, and execution traces, then uses structured prompt engineering, including chain‑of‑thought reasoning, contextual prompting, and self‑consistency checks to guide the model in inferring expected behaviour and validating program outputs. In evaluations on the QuixBugs benchmark, LLMOracle4py attained an accuracy of eighty‑five per cent and a recall of ninety per cent, outperforming prior methods that depend on formal specifications or manual assertions. These results demonstrate the potential of LLM‑driven oracles to reduce human effort and improve the scalability of semantic bug detection. Future work will extend support to additional programming languages, incorporate dynamic feedback loops for prompt refinement, and integrate the framework into continuous integration pipelines for seamless industrial deployment.

### Keywords
Test oracle automation, Semantic bugs, Large language models, Prompt engineering, Python
