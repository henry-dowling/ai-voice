# Utils

## text_to_json.py

This script converts all `.txt` files in the `corpus` directory into `.json` files in the `processed_corpus` directory. Each JSON file contains a single field, `text`, with the full content of the original text file.

### Usage

From the project root, run:

```bash
python utils/text_to_json.py
```

- The script will create the `processed_corpus` directory if it does not exist.
- No external dependencies are required (uses only the Python standard library). 