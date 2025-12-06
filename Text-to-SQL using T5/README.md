# Text-to-SQL CLI (Fine-tuned T5) + SQL Explanation + Suggestions

This project provides a simple **command-line interface (CLI)** that:
1. Translates **natural language (English)** into **SQL** using a **fine-tuned T5 Seq2Seq model**
2. Explains SQL queries in **plain English**
3. Suggests helpful follow-up actions (filters, grouping, sorting, joins, etc.)

---

## Features

- **English → SQL translation** using Hugging Face Transformers (`AutoModelForSeq2SeqLM`)
- Runs on **GPU (CUDA)** if available, otherwise CPU
- **SQL explanation** using `sqlparse` tokenization + keyword mapping
- **Query suggestions** for better analytics-style exploration
- Interactive CLI loop with menu options



