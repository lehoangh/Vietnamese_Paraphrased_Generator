# Vietnamese_Paraphrased_Generator

This repo provides two tasks in one pipeline:
- First, check the plagiarism between the target passage and the source passage through a cosine similarity score. If this score is larger than a predefined threshold. The program will transfer this plagiarised passage to the paraphrase generation model.
- Secondly, the plagiarised passage is the input to the paraphrase generation model with the purpose of rewriting these plagiarised sentences to a new sentence with the same meaning to avoid the penalization of plagiarism check.

