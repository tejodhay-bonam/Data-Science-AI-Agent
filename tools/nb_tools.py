import nbformat
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell
from nbclient import NotebookClient
import os
from smolagents import tool

# Global notebook object and path, initialized by create_noteboook
NOTEBOOK_PATH = "default_notebook.ipynb" 
notebook = new_notebook()

def create_noteboook(filename: str):
    global NOTEBOOK_PATH, notebook
    NOTEBOOK_PATH = filename

    # Load or initialize notebook
    if os.path.exists(NOTEBOOK_PATH):
        try:
            with open(NOTEBOOK_PATH, "r", encoding="utf-8") as f: # Explicitly read with UTF-8
                notebook = nbformat.read(f, as_version=4)
        except Exception as e:
            # Fallback to a new notebook if reading fails
            print(f"[DEBUG] Error reading notebook {filename}: {e}. Creating a new one.")
            notebook = new_notebook()
    else:
        notebook = new_notebook()

def save_notebook():
    global NOTEBOOK_PATH, notebook
    try:
        # Ensure the directory for NOTEBOOK_PATH exists
        notebook_dir = os.path.dirname(NOTEBOOK_PATH)
        if notebook_dir and not os.path.exists(notebook_dir):
            os.makedirs(notebook_dir, exist_ok=True) # exist_ok=True to prevent error if dir already exists

        # Using a sanitized print for debug to avoid issues with console encoding
        print(f"[DEBUG] Saving notebook with {len(notebook.cells)} cells to {NOTEBOOK_PATH}".encode('ascii', 'replace').decode('ascii', 'replace'))
        with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f: # Explicitly write with UTF-8
            nbformat.write(notebook, f)
    except Exception as e:
        # Sanitize error message for printing
        error_message = f"[DEBUG] Error saving notebook {NOTEBOOK_PATH}: {str(e)}".encode('ascii', 'replace').decode('ascii', 'replace')
        print(error_message)

@tool
def run_code_cell(code: str) -> str:
    """
    Appends a code cell to the notebook, runs it, 
    and returns the sanitized output of the last executed cell.

    Args:
        code: The Python code to execute in the code cell.

    Returns:
        str: The sanitized output of the last executed code cell.
    """
    global notebook # Ensure we're using the global notebook object

    code_cell = new_code_cell(code)
    notebook.cells.append(code_cell)
    save_notebook()

    client = NotebookClient(
        notebook, 
        timeout=600, # Increased timeout for potentially long model training
        kernel_name="python3",
        allow_errors=True
    )
    
    try:
        client.execute()
    except Exception as e:
        # This might catch errors during the NotebookClient setup or pre-execution phases
        error_msg = f"Error during NotebookClient.execute() or setup: {type(e).__name__}: {str(e)}"
        # Sanitize error_msg before returning
        return error_msg.encode('ascii', 'replace').decode('ascii', 'replace').strip()
    finally:
        save_notebook() # Save the state after execution/error

    # Process outputs
    text_to_return = ""
    if notebook.cells: # Check if there are any cells
        last_cell = notebook.cells[-1]
        outputs = last_cell.get("outputs", [])

        if outputs:
            output = outputs[-1]  # Get only the last output
            raw_text = ""
            if output.output_type == "stream":
                raw_text = output.get("text", "")
            elif output.output_type == "execute_result":
                # Ensure data and text/plain exist
                data_dict = output.get("data", {})
                if data_dict:
                    raw_text = data_dict.get("text/plain", "")
            elif output.output_type == "error":
                ename = output.get("ename", "UnknownError")
                evalue = output.get("evalue", "Unknown error detail")
                # Sanitize ename and evalue as they could contain problematic chars
                ename_safe = str(ename).encode('ascii', 'replace').decode('ascii', 'replace')
                evalue_safe = str(evalue).encode('ascii', 'replace').decode('ascii', 'replace')
                raw_text = f"{ename_safe}: {evalue_safe}"
            
            # Sanitize the raw_text to remove/replace characters problematic for 'charmap'
            if isinstance(raw_text, list): # output.text can sometimes be a list of strings
                raw_text = "".join(raw_text)

            if isinstance(raw_text, str):
                text_to_return = raw_text.encode('ascii', 'replace').decode('ascii', 'replace').strip()
            else: # If it's already bytes or other type, try to convert and sanitize
                try:
                    # Attempt to decode if bytes, then sanitize
                    decoded_text = str(raw_text, 'utf-8') if isinstance(raw_text, bytes) else str(raw_text)
                    text_to_return = decoded_text.encode('ascii', 'replace').decode('ascii', 'replace').strip()
                except Exception:
                    # Fallback: Force to string and sanitize
                    text_to_return = str(raw_text).encode('ascii', 'replace').decode('ascii', 'replace').strip()
    
    return text_to_return

@tool
def add_markdown_cell(markdown: str) -> bool:
    """
    Appends a markdown cell to the notebook and saves it.

    Args:
        markdown: The markdown content to include in the cell.
    
    Returns:
        bool: Status of success or failure
    """
    global notebook # Ensure we're using the global notebook object
    
    try:
        # Normalize to UTF-8 and replace errors, then proceed. 
        # Markdown itself supports UTF-8, so this is mainly for safety if non-UTF-8 string somehow gets here.
        safe_markdown = markdown.encode('utf-8', 'replace').decode('utf-8')
    except Exception as e:
        print(f"[DEBUG] Markdown sanitization error: {e}. Using aggressive ASCII replace.")
        safe_markdown = markdown.encode('ascii', 'replace').decode('ascii', 'replace')

    md_cell = new_markdown_cell(safe_markdown)
    notebook.cells.append(md_cell)
    save_notebook()
    return True

if __name__ == "__main__":
    # Create a new notebook
    create_noteboook("pandas_example_notebook.ipynb")

    # Markdown: Intro
    add_markdown_cell("# Pandas Data Analysis\nIn this notebook, we create a DataFrame and perform basic analysis.")

    # Code Cell 1: Create a DataFrame
    code1 = """
import pandas as pd

data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
}

df = pd.DataFrame(data)
print(df)
"""
    out1 = run_code_cell(code1)
    print("Created DataFrame:\n", out1)

    # Markdown: Next step
    add_markdown_cell("## Filtering and Statistics\nWe'll now calculate the average age and filter by age > 30.")

    # Code Cell 2: Filter and analyze
    code2 = """
average_age = df['Age'].mean()
older_people = df[df['Age'] > 30]

print(f"Average Age: {average_age}")
print("\\nPeople older than 30:")
print(older_people)
"""
    out2 = run_code_cell(code2)
    print("Analysis output:\n", out2)

    # Markdown: Conclusion
    add_markdown_cell("### Summary\n- The average age is calculated.\n- People older than 30 are listed.")