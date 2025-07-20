from langchain_community.tools import tool


@tool
async def query_semantic_tool(query: str) -> str:
    """Query relevant text chunks to find answers to user questions.

    Args:
        query (str): A query string that defines the question or topic for which relevant text chunks are to be retrieved.

    Returns:
        Any: A collection of relevant text chunks that provide the answer to the user's question."""
    try:
        return """Resetting Tasks: You can reset the planner by going to Settings > System > Reset Northgrc and start over. Then select the option to Reset Information Security Planning. This will reset the entire planner; unfortunately, it’s not possible to reset individual tasks. Another solution could be to use the Optimize option in the planner. This function will move all overdue task start dates to the current day.
                   Assets Not Displaying on Heatmap in Report: If you go to the risk analysis page and click the green "Evaluate" button next to the analyses, the asset will appear in the report. A risk evaluation is not considered "Completed" until it is sent for evaluation."""
    except Exception as e:
        print(f"[query_semantic_tool] Error: {e}")
        return "Nothing Found"