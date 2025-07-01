# Text to JSON Processing with Title Generation

This project processes text files from a `corpus` directory and converts them to JSON format with automatically generated titles using OpenAI's GPT-3.5-turbo model.

## Features

- Converts `.txt` files to `.json` format
- Automatically generates descriptive titles using OpenAI API
- Uses both filename and content to create meaningful titles
- Includes error handling with fallback to filename-based titles
- Preserves original filename in the JSON output

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Usage

### Option 1: Use the runner script (recommended)
```bash
python run_processing.py
```

### Option 2: Run directly
```bash
python utils/text_to_json.py
```

## Output Format

Each processed file will create a JSON file in the `processed_corpus` directory with the following structure:

```json
{
  "title": "Generated descriptive title",
  "text": "Original text content",
  "filename": "original_filename.txt"
}
```

## Directory Structure

```
├── corpus/                 # Input text files
├── processed_corpus/       # Output JSON files
├── utils/
│   └── text_to_json.py    # Main processing script
├── run_processing.py       # Runner script
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## Error Handling

- If OpenAI API is unavailable or fails, the system falls back to using the filename (without extension) as the title
- All errors are logged to the console
- Processing continues even if individual files fail

## Requirements

- Python 3.6+
- OpenAI API key
- Internet connection for API calls 