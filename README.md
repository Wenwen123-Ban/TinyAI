# TinyAI v1.7

TinyAI v1.7 is a modular, offline NLP math engine designed for lightweight hardware.

## Features
- Single-pass regex tokenization with scientific notation support.
- Knowledge block loading from `training_data/` (`constants.txt`, `number_map.txt`, `math_rules.txt`).
- Entity substitution for constants/number words at token-resolution time.
- Primary operation detection for symbolic and natural-language operators.
- Comparison reasoning for prompts like: `If 2 is greater than 1, what is the answer?`.
- Simple developer admin login and data block update workflow.
- Number output formatting with comma separators and 8 significant figures.

## Run
```bash
python tinyai.py
```

## Developer account
- Username: `devadmin`
- Password: `tinyai-dev-1700`

## Example prompts
- `What is the sum of 5 and 5?`
- `If 2 is greater than 1, what is the answer?`
- `What is lightspeed plus 2?`
