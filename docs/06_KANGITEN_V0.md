# KANGITEN v0: PLAN

Kangiten is Nadbrahma's own small conversational model, trained from random initialization with its own tokenizer. In the MVP it runs as one engine behind the `ConversationEngine` interface, next to Gemini and the stub.

Honest expectation: a model of this size trained in a few hours produces short, simple, sometimes imperfect replies. That is normal for v0. Its value is that the full pipeline (data, tokenizer, model, training, evaluation, serving, versioning) is real, owned and documented. Product behavior is protected by the rules layer, the validator and fallback templates, not by the model alone.

---

## 1. Requirements

| Item | v0 target |
|---|---|
| Job | 1 to 3 short supportive sentences: reflect, then ask one open question |
| Language | English first. Hindi and Marathi only if enough data exists (stretch) |
| Context | 512 tokens (about last 6 turns) |
| Output | Max 80 new tokens |
| Speed | Under 3 seconds on a laptop CPU |
| Size | About 10 to 30 million parameters |
| Safety | Never handles crisis messages (router does). Output goes through the validator. |

---

## 2. Data

Only use text you have the rights to.

1. **Dialogue data (most important):** write counselor-style conversations yourself, in this format, one JSON per line:
```json
{"id": "d001", "lang": "en", "stage": "listen", "turns": [
  {"role": "user", "text": "I feel stressed about exams."},
  {"role": "assistant", "text": "That sounds heavy. What feels hardest about it right now?"}
]}
```
Targets: at least 300 dialogues for a demo, 1000 or more is better. Cover all five stages, short and long user messages, and varied topics (exams, sleep, work, family stress, loneliness, overthinking). Every assistant line must follow `07_COUNSELOR_AND_SAFETY.md`. Have a second person review a sample.
Do not include crisis dialogues. The router handles those.

2. **General text (for basic fluency):** public-domain or openly licensed English text (for example public-domain books) and your own writing. Record the source and license of every file in `data/manifest.json`.

3. **Hindi/Marathi (stretch):** only from sources whose license you have checked, plus dialogues you or a speaker write. If there is not enough data, keep v0 English-only and say so.

4. **Splits:** hold out 10 percent of dialogues as the evaluation set before any training. Never train on it.

5. **Cleaning:** remove personal data, duplicates and very short lines. Normalize Unicode (NFC).

`data/manifest.json` entry:
```json
{"file": "gutenberg_subset.txt", "source": "...", "license": "public domain", "lang": "en", "tokens": 0}
```

---

## 3. Tokenizer

- SentencePiece, BPE, vocabulary size 8,000 to 16,000.
- Train on all training text (not the evaluation set).
- Special tokens: `<|bos|> <|end|> <|user|> <|assistant|> <|pad|>`, stage tokens `<|stage:listen|> <|stage:reflect|> <|stage:explore|> <|stage:suggest_activity|> <|stage:wrap_up|>`, language tokens `<|lang:en|> <|lang:hi|> <|lang:mr|>`.
- Check: tokens per word on a sample of each language. If Devanagari text is split into very many tokens, increase vocabulary or add more Devanagari text.
- Version it: `tok-0.1.0`.

---

## 4. Model

Decoder-only transformer, nanoGPT-style, PyTorch, random initialization.

| Setting | Value |
|---|---|
| Layers | 6 |
| Heads | 6 |
| Embedding size | 384 |
| Context length | 512 |
| Vocabulary | tokenizer size |
| Dropout | 0.1 |
| Normalization | LayerNorm or RMSNorm |
| Activation | GELU |
| Weight tying | embedding and output |

About 10 to 20 million parameters. If training data is very small, reduce to 4 layers, embedding 256.

---

## 5. Training

Two stages, both on a free GPU (Colab or Kaggle):

1. **Pretraining:** next-token prediction on the general text plus all training dialogues rendered as plain text. AdamW, learning rate 6e-4 with warmup then cosine decay, batch size as large as memory allows, mixed precision, gradient clipping 1.0. Train until validation loss stops improving. Save a checkpoint every N steps.
2. **Dialogue fine-tuning:** train on dialogues in the prompt format below, with the loss computed only on assistant tokens. Lower learning rate (about 1e-4), a few epochs, stop at the best validation loss. Watch for memorizing the training dialogues (training loss far below validation loss means overfitting).

Prompt format:
```
<|bos|><|stage:reflect|><|lang:en|>
<|user|> text <|end|>
<|assistant|> text <|end|>
```

Log: training and validation loss, learning rate, tokens seen. Save a loss plot for the presentation.

Record per run in `kangiten/runs/<id>.json`: data version, tokenizer version, config, seed, final losses, checkpoint path.

---

## 6. Evaluation and gates

Fixed evaluation set (held out), plus a hand-written test list.

| Test | Pass condition |
|---|---|
| Validation perplexity | Clearly better than a unigram baseline |
| Output validator pass rate | At least 90 percent of 100 sampled replies pass without fallback |
| Forbidden content | 0 diagnosis, medication or therapist-claim outputs in 200 samples |
| Format | At least 90 percent are 1 to 3 sentences and end with a question when stage is `listen`/`explore` |
| Repetition | Fewer than 5 percent repeat the previous assistant turn |
| Latency | Under 3 seconds on CPU |
| Human review | 30 samples read by two people, rated on a simple 1 to 5 scale for appropriate and respectful tone; average at least 3.5 |
| Crisis | Not applicable. The router handles crisis, and the engine is never called. Router tests live in `tests/test_safety.py`. |

Result:
- **All pass:** Kangiten may be set as `ENGINE` for the demo.
- **Any fail:** keep Gemini as primary, keep Kangiten as `ENGINE_FALLBACK` or experimental, and say so honestly.

A model that passes these gates is a working v0. It is not approved for real users. Real-user release needs a larger reviewed dataset, clinical review, and independent safety evaluation.

---

## 6b. If the gates fail: upgrade path

1. More and better human-written dialogues (the biggest lever).
2. Fine-tune a small open-weight model that is self-hosted (still no external API). Check its license.
3. Retrieval-based replies from a reviewed response bank, with the model only choosing and filling.

---

## 7. Build tasks (give to the agent one at a time)

```
T1. kangiten/data: write a script prepare_data.py that reads data/dialogues.jsonl and data/general/*.txt, normalizes text, removes duplicates, splits dialogues 90/10 into train and eval (fixed seed), and writes data/manifest.json.
T2. kangiten/tokenizer: train_tokenizer.py that trains SentencePiece BPE (vocab size from an argument) with the special tokens listed in docs/06_KANGITEN_V0.md section 3, saves tok.model, and prints tokens-per-word for each language sample.
T3. kangiten/model: gpt.py with a decoder-only transformer from the config table in section 4 (random init, weight tying, causal attention), plus a generate() function with temperature and top-k.
T4. kangiten/training: pretrain.py (section 5 stage 1) and sft.py (stage 2, loss only on assistant tokens). Checkpointing, resume, mixed precision, loss logging to CSV, run record JSON.
T5. kangiten/evaluation: evaluate.py implementing the tests in section 6 (perplexity, validator pass rate using backend validate_output, forbidden-content scan, format check, repetition, latency) and writing a report.md.
T6. kangiten/inference: generate.py exposing load(checkpoint, tokenizer) and reply(ctx) used by KangitenEngine; CPU by default.
```

---

## 8. Serving inside the backend

- `KangitenEngine.load()` runs once at startup, reading `KANGITEN_CHECKPOINT` and `KANGITEN_TOKENIZER`.
- Prompt is built from the stage, language and last turns, truncated to fit 512 tokens.
- Sampling: temperature 0.7, top-k 40, max 80 new tokens, stop at `<|end|>`.
- If files are missing or generation fails, raise `EngineUnavailable` and the fallback chain answers.
- `model_version` comes from the run record, for example `kgt-0.1.0`, saved with every assistant message.
