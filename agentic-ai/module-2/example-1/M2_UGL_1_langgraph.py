#!/usr/bin/env python
# coding: utf-8

"""
M2 Agentic AI - Chart Generation with LangGraph
This is a LangGraph implementation of the reflection pattern for chart generation.
"""

# Standard library imports
import re
import json
import operator
from typing import Annotated, TypedDict

# LangGraph imports
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# Local helper module
import utils


# ============================================================================
# 1. Define State Schema
# ============================================================================

class ChartGenerationState(TypedDict):
    """State schema for the chart generation workflow."""

    # Input parameters
    dataset_path: str
    user_instructions: str
    generation_model: str
    reflection_model: str
    image_basename: str

    # V1 artifacts
    code_v1: str
    chart_v1_path: str

    # Reflection artifacts
    feedback: str

    # V2 artifacts
    code_v2: str
    chart_v2_path: str

    # Iteration tracking
    current_step: str


# ============================================================================
# 2. Define Node Functions
# ============================================================================

def load_data_node(state: ChartGenerationState) -> ChartGenerationState:
    """Node 1: Load and prepare the dataset."""
    # Load data but don't store in state (to avoid serialization issues)
    # Each node will load the data as needed
    df = utils.load_and_prepare_data(state["dataset_path"])
    utils.print_html(df.sample(n=5), title="Random Sample of Dataset")

    return {
        **state,
        "current_step": "data_loaded"
    }


def generate_v1_code_node(state: ChartGenerationState) -> ChartGenerationState:
    """Node 2: Generate initial chart code (V1)."""
    utils.print_html("Step 1: Generating chart code (V1)… 📈")

    chart_v1_path = f"{state['image_basename']}_v1.png"

    prompt = f"""
    You are a data visualization expert.

    Return your answer *strictly* in this format:
    <execute_python>
    # valid python code here
    </execute_python>

    Do not add explanations, only the tags and the code.

    The code should create a visualization from a DataFrame 'df' with these columns:
    - date (M/D/YY)
    - time (HH:MM)
    - cash_type (card or cash)
    - card (string)
    - price (number)
    - coffee_name (string)
    - quarter (1-4)
    - month (1-12)
    - year (YYYY)

    User instruction: {state['user_instructions']}

    Requirements for the code:
    1. Assume the DataFrame is already loaded as 'df'.
    2. Use matplotlib for plotting.
    3. Add clear title, axis labels, and legend if needed.
    4. Save the figure as '{chart_v1_path}' with dpi=300.
    5. Do not call plt.show().
    6. Close all plots with plt.close().
    7. Add all necessary import python statements

    Return ONLY the code wrapped in <execute_python> tags.
    """

    code_v1 = utils.get_response(state["generation_model"], prompt)
    utils.print_html(code_v1, title="LLM output with first draft code (V1)")

    return {
        **state,
        "code_v1": code_v1,
        "chart_v1_path": chart_v1_path,
        "current_step": "v1_code_generated"
    }


def execute_v1_code_node(state: ChartGenerationState) -> ChartGenerationState:
    """Node 3: Execute V1 code and generate the chart."""
    utils.print_html("Step 2: Executing chart code (V1)… 💻")

    # Load data for execution
    df = utils.load_and_prepare_data(state["dataset_path"])

    # Extract and execute code
    match = re.search(r"<execute_python>([\s\S]*?)</execute_python>", state["code_v1"])
    if match:
        initial_code = match.group(1).strip()
        exec_globals = {"df": df}
        exec(initial_code, exec_globals)

    utils.print_html(state["chart_v1_path"], is_image=True, title="Generated Chart (V1)")

    return {
        **state,
        "current_step": "v1_executed"
    }


def reflect_on_v1_node(state: ChartGenerationState) -> ChartGenerationState:
    """Node 4: Reflect on V1 chart and generate improved code (V2)."""
    utils.print_html("Step 3: Reflecting on V1 (image + code) and generating improvements… 🔁")

    chart_v2_path = f"{state['image_basename']}_v2.png"
    media_type, b64 = utils.encode_image_b64(state["chart_v1_path"])

    prompt = f"""
    You are a data visualization expert.
    Your task: critique the attached chart and the original code against the given instruction,
    then return improved matplotlib code.

    Original code (for context):
    {state['code_v1']}

    OUTPUT FORMAT (STRICT!):
    1) First line: a valid JSON object with ONLY the "feedback" field.
    Example: {{"feedback": "The legend is unclear and the axis labels overlap."}}

    2) After a newline, output ONLY the refined Python code wrapped in:
    <execute_python>
    ...
    </execute_python>

    3) Import all necessary libraries in the code. Don't assume any imports from the original code.

    HARD CONSTRAINTS:
    - Do NOT include Markdown, backticks, or any extra prose outside the two parts above.
    - Use pandas/matplotlib only (no seaborn).
    - Assume df already exists; do not read from files.
    - Save to '{chart_v2_path}' with dpi=300.
    - Always call plt.close() at the end (no plt.show()).
    - Include all necessary import statements.

    Schema (columns available in df):
    - date (M/D/YY)
    - time (HH:MM)
    - cash_type (card or cash)
    - card (string)
    - price (number)
    - coffee_name (string)
    - quarter (1-4)
    - month (1-12)
    - year (YYYY)

    Instruction:
    {state['user_instructions']}
    """

    # Call appropriate API based on model name
    lower = state["reflection_model"].lower()
    if "claude" in lower or "anthropic" in lower:
        content = utils.image_anthropic_call(state["reflection_model"], prompt, media_type, b64)
    else:
        content = utils.image_openai_call(state["reflection_model"], prompt, media_type, b64)

    # Parse feedback JSON
    lines = content.strip().splitlines()
    json_line = lines[0].strip() if lines else ""

    try:
        obj = json.loads(json_line)
    except Exception as e:
        # Fallback: try to capture the first {...} in all the content
        m_json = re.search(r"\{.*?\}", content, flags=re.DOTALL)
        if m_json:
            try:
                obj = json.loads(m_json.group(0))
            except Exception as e2:
                obj = {"feedback": f"Failed to parse JSON: {e2}"}
        else:
            obj = {"feedback": f"Failed to find JSON: {e}"}

    feedback = str(obj.get("feedback", "")).strip()

    # Extract refined code
    m_code = re.search(r"<execute_python>([\s\S]*?)</execute_python>", content)
    refined_code_body = m_code.group(1).strip() if m_code else ""
    code_v2 = utils.ensure_execute_python_tags(refined_code_body)

    utils.print_html(feedback, title="Reflection feedback on V1")
    utils.print_html(code_v2, title="LLM output with revised code (V2)")

    return {
        **state,
        "feedback": feedback,
        "code_v2": code_v2,
        "chart_v2_path": chart_v2_path,
        "current_step": "reflection_completed"
    }


def execute_v2_code_node(state: ChartGenerationState) -> ChartGenerationState:
    """Node 5: Execute V2 code and generate the improved chart."""
    utils.print_html("Step 4: Executing refined chart code (V2)… 🖼️")

    # Load data for execution
    df = utils.load_and_prepare_data(state["dataset_path"])

    # Extract and execute code
    match = re.search(r"<execute_python>([\s\S]*?)</execute_python>", state["code_v2"])
    if match:
        reflected_code = match.group(1).strip()
        exec_globals = {"df": df}
        exec(reflected_code, exec_globals)

    utils.print_html(state["chart_v2_path"], is_image=True, title="Regenerated Chart (V2)")

    return {
        **state,
        "current_step": "v2_executed"
    }


# ============================================================================
# 3. Build the Graph
# ============================================================================

def create_chart_generation_graph():
    """Create and compile the LangGraph workflow for chart generation."""

    # Create the graph
    workflow = StateGraph(ChartGenerationState)

    # Add nodes
    workflow.add_node("load_data", load_data_node)
    workflow.add_node("generate_v1_code", generate_v1_code_node)
    workflow.add_node("execute_v1_code", execute_v1_code_node)
    workflow.add_node("reflect_on_v1", reflect_on_v1_node)
    workflow.add_node("execute_v2_code", execute_v2_code_node)

    # Add edges to define the flow
    workflow.add_edge(START, "load_data")
    workflow.add_edge("load_data", "generate_v1_code")
    workflow.add_edge("generate_v1_code", "execute_v1_code")
    workflow.add_edge("execute_v1_code", "reflect_on_v1")
    workflow.add_edge("reflect_on_v1", "execute_v2_code")
    workflow.add_edge("execute_v2_code", END)

    # Compile the graph with checkpointing
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)

    return app


# ============================================================================
# 4. Run Workflow Function
# ============================================================================

def run_workflow_langgraph(
    dataset_path: str,
    user_instructions: str,
    generation_model: str,
    reflection_model: str,
    image_basename: str = "chart",
):
    """
    Run the complete chart generation workflow using LangGraph.

    Args:
        dataset_path: Path to the CSV dataset
        user_instructions: User's chart generation instructions
        generation_model: Model to use for initial code generation
        reflection_model: Model to use for reflection and refinement
        image_basename: Base name for output chart files

    Returns:
        Final state containing all artifacts (codes, feedback, image paths)
    """

    # Create the graph
    app = create_chart_generation_graph()

    # Initialize state
    initial_state = {
        "dataset_path": dataset_path,
        "user_instructions": user_instructions,
        "generation_model": generation_model,
        "reflection_model": reflection_model,
        "image_basename": image_basename,
        "current_step": "initialized",
    }

    # Run the workflow
    config = {"configurable": {"thread_id": "chart_generation_1"}}
    final_state = None

    for state in app.stream(initial_state, config):
        final_state = state

    # Extract the final state from the last node
    if final_state:
        # The state from stream is a dict with node names as keys
        # Get the last value which contains the complete state
        final_state = list(final_state.values())[-1]

    return final_state


# ============================================================================
# 5. Main Execution
# ============================================================================

if __name__ == "__main__":
    # Configuration
    user_instructions = "Create a plot comparing Q1 coffee sales in 2024 and 2025 using the data in coffee_sales.csv."
    generation_model = "gpt-4.1-mini"
    reflection_model = "o4-mini"
    image_basename = "drink_sales_langgraph"

    # Run the LangGraph workflow
    final_state = run_workflow_langgraph(
        dataset_path="coffee_sales.csv",
        user_instructions=user_instructions,
        generation_model=generation_model,
        reflection_model=reflection_model,
        image_basename=image_basename
    )

    print("\n" + "="*80)
    print("Workflow completed successfully!")
    print("="*80)
    print(f"V1 Chart: {final_state.get('chart_v1_path')}")
    print(f"V2 Chart: {final_state.get('chart_v2_path')}")
    print(f"Feedback: {final_state.get('feedback')}")
