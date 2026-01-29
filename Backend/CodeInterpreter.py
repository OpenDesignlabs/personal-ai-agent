import subprocess
import os
import sys
from Backend.Chatbot import client

def run_script(code):
    """Saves and executes a generated Python script safely."""
    temp_file = "Data/temp_script.py"
    os.makedirs("Data", exist_ok=True)
    
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(code)
    
    try:
        # Run the script and capture output
        result = subprocess.run([sys.executable, temp_file], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return f"✅ Script executed successfully. Output:\n{result.stdout}"
        else:
            return f"❌ Script failed. Error:\n{result.stderr}"
    except Exception as e:
        return f"❌ Execution error: {str(e)}"
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

def dynamic_agent(task_description, max_retries=3):
    """Ask the LLM to write a script, and self-heal if it fails."""
    system_prompt = """You are a Python Automation Engineer. Write a standalone Python script to perform the task.
- ONLY the code, no markdown, no explanation.
- Print results clearly.
- If you are fixing a previous error, analyze the error message and avoid the mistake."""
    
    current_prompt = task_description
    last_error = ""

    for attempt in range(max_retries):
        try:
            full_prompt = current_prompt
            if last_error:
                full_prompt = f"Previous script failed with error: {last_error}. Please provide a fixed version.\nOriginal Task: {task_description}"

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": full_prompt}],
                max_tokens=2000,
                temperature=0.1
            )
            code = response.choices[0].message.content.strip()
            # Clean markdown code blocks if present
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0].strip()
            elif "```" in code:
                code = code.split("```")[1].split("```")[0].strip()
            
            print(f"Executing attempt {attempt + 1}...")
            result = run_script(code)
            
            if "❌" not in result: # Success
                return result
            else:
                last_error = result # Store error for next attempt
                print(f"Attempt {attempt + 1} failed, retrying...")
                
        except Exception as e:
            last_error = str(e)
            
    return f"Agent failed after {max_retries} attempts. Last error: {last_error}"
