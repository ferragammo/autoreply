from langchain_community.tools import tool

from auto_reply.core.config import settings


@tool
async def query_semantic_tool(query: str) -> str:
    """Query relevant text chunks to find answers to user questions.

    Args:
        query (str): A query string that defines the question or topic for which relevant text chunks are to be retrieved.

    Returns:
        Str: Response based on a relevant text chunks that provide the answer to the user's question."""
    try:
        response = await settings.OPENAI_CLIENT.responses.create(
            model="gpt-4o-mini",
            input=query,
            max_tool_calls=1,
            temperature=0.0,
            tools=[{
                "type": "file_search",
                "vector_store_ids": [settings.VS_ID]
            }]
        )
        return response.output_text
    except Exception as e:
        print(f"[query_semantic_tool] Error: {e}")
        return "Nothing Found"