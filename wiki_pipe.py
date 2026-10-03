"""
Wikipedia Knowledge Extractor Pipeline
This script fetches content from a Wikipedia URL and uses a Gemini LLM
via LangChain to extract and structure the information into a predefined JSON format.
"""

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from wikipedia import page, set_user_agent
from pydantic import BaseModel, Field

# Load environment variables (e.g., GOOGLE_API_KEY) from a local .env file
load_dotenv()

# Configuration
wiki_page_url = #insert wiki URL

# Initialize the LLM.
# API key is automatically inferred from the GOOGLE_API_KEY environment variable.
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")


class WikiSummary(BaseModel):
    """Pydantic schema defining the expected structured output from the LLM."""
    short_definition: str = Field(description="Short definition of the Wikipedia page subject")
    key_people: list[str] = Field(description="Key people mentioned in the Wikipedia page")
    timeline_events: list[str] = Field(description="List of significant dates and their corresponding events")
    fun_fact: str = Field(description="Fun fact about the subject")


# Set up the parser to enforce the Pydantic schema
parser = PydanticOutputParser(pydantic_object=WikiSummary)
format_instructions = parser.get_format_instructions()

# --- Data Ingestion ---
# Set a custom User-Agent to comply with Wikipedia's API policies and avoid server blocks
set_user_agent("WikiPipeBot/1.0")
set_user_agent("WikiPipeBot")
# Fetch the page content. auto_suggest=False prevents DisambiguationError on exact matches.
wiki_page_name = wiki_page_url.split("/")[-1]
wikipedia_text = page(wiki_page_name, auto_suggest=False).content

# --- LLM Pipeline ---
template_text = ("Read the following text: {wikipedia_text}\n"
                 "based on the text, an output according to the following output instructions:\n"
                 "{format_instructions}."
                 )


prompt = ChatPromptTemplate.from_template(template_text)

# Construct the LangChain Expression Language chain
chain = prompt | llm | parser
# Execute the chain by injecting the context and formatting rules
response = chain.invoke({"wikipedia_text": wikipedia_text,
                         "format_instructions": format_instructions
                         })

# Output the result as a JSON string
print(response.model_dump_json(indent=4))
