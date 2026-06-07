import os
from typing import List, Union
from dotenv import load_dotenv
from markitdown import MarkItDown
from google import genai

load_dotenv()

def research_assistant(inputs: List[Union[str, bytes]]):
    md = MarkItDown()
    combined_content = []

    for item in inputs:
        print(f"Processing: {item}")
        try:
            # MarkItDown handles URLs and local files
            result = md.convert(item)
            combined_content.append(f"--- Source: {item} ---\n{result.text_content}\n")
        except Exception as e:
            print(f"Error processing {item}: {e}")

    full_text = "\n\n".join(combined_content)
    
    if not full_text:
        return "No content could be extracted from the provided sources."

    # Initialize the modern genai client
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    
    prompt = f"""
    You are a world-class Research Assistant. Below is content extracted from various sources (webpages, YouTube transcripts, documents) in Markdown format.
    Please synthesize this information into a professional, comprehensive research summary. 
    
    Your summary should:
    1. Provide a high-level executive summary.
    2. Break down key themes and detailed findings.
    3. Identify and contrast conflicting viewpoints or data.
    4. Provide a final conclusion based on the evidence.
    
    Content:
    {full_text}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error generating synthesis: {e}"

if __name__ == "__main__":
    # Testing with a mix of a webpage and a YouTube video
    test_sources = [
        "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    ]
    
    print("Starting Deep Research synthesis...")
    summary = research_assistant(test_sources)
    print("\n--- Final Research Summary ---\n")
    print(summary)
