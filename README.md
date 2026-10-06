# WikiPipe 🧠

A lightweight Python script that fetches content from Wikipedia and uses Google's Gemini LLM to parse it into a strict, predefined JSON schema. 

Built with **LangChain** and **Pydantic** to ensure predictable structured outputs.

## What It Extracts

The pipeline uses a Pydantic schema to strictly extract the following data points from any biographical or historical Wikipedia article:

* **Short Definition:** A concise summary of the subject.
* **Key People:** A list of significant individuals related to the topic.
* **Timeline Events:** Chronological milestones and their corresponding dates.
* **Fun Fact:** An interesting or lesser-known trivia piece.

*(Note: The extraction logic is completely modular. You can extract different data points by simply updating the `WikiSummary` class properties).*
## Setup

1. Install the required dependencies:
   ```bash
   pip install langchain-google-genai wikipedia pydantic python-dotenv
   ```

2. Create a `.env` file in the root directory and add your Google API key:
   ```env
   GOOGLE_API_KEY="your_api_key_here"
   ```

## Usage

Update the `wiki_page_url` constant in the script to any Wikipedia article you want to analyze, then run the script:

```bash
python wiki_pipe.py
```

## Example Output

The script outputs a beautifully formatted JSON string ready for database ingestion or API responses:

```json
{
    "short_definition": "Leonardo di ser Piero da Vinci was an Italian polymath of the High Renaissance...",
    "key_people": [
        "Leonardo da Vinci",
        "Andrea del Verrocchio",
        "Ludovico Sforza"
    ],
    "timeline_events": [
        "15 April 1452: Born in or near Vinci, Tuscany",
        "2 May 1519: Died at Clos Lucé in France"
    ],
    "fun_fact": "Leonardo da Vinci had a habit of purchasing caged birds and releasing them."
}
```

