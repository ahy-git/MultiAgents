import base64
import os
from typing import List, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr
from e2b_code_interpreter import Sandbox, Result

# Define input schema
class CodeInterpreterInput(BaseModel):
    code: str = Field(..., description="Python code to execute in the sandbox")
    # dataset_path: str = Field(..., description="Path to dataset file for analysis")

class CodeInterpreterTool(BaseTool):
    name: str = "CodeInterpreterTool"
    description: str = (
        "Executes Python code in a secure sandbox environment. "
        "Useful for data analysis, visualization, and processing. "
        "The dataset is available at {dataset_path}."
    )
    args_schema: type[BaseModel] = CodeInterpreterInput
    
    # Declare fields explicitly
    e2b_api_key: str = Field(..., description="E2B API key for sandbox access")
    output_dir: str = Field(default="output_visualizations", description="Directory for saving visualizations")
    generated_images: List[str] = Field(default_factory=list, description="Paths to generated images")
    
    # Private attributes (not part of Pydantic model)
    _sandbox: Optional[Sandbox] = PrivateAttr(default=None)

    def __init__(self, e2b_api_key: str, output_dir: str = "output_visualizations"):
        # Initialize Pydantic model
        super().__init__(
            e2b_api_key=e2b_api_key,
            output_dir=output_dir
        )
        os.makedirs(self.output_dir, exist_ok=True)

    def _run(self, code: str) -> str:
        try:
            # Initialize sandbox if not already created
            if not self._sandbox:
                self._sandbox = Sandbox(api_key=self.e2b_api_key)
            
            # Upload dataset if provided
            if self._current_dataset_path:
                with open(self._current_dataset_path, "rb") as f:
                    # Write to the sandbox with the expected filename
                    self._sandbox.files.write("/dataset.csv", f.read())
            
            # Execute code
            execution = self._sandbox.run_code(code)
            
            # Process results
            output = []
            
            # Handle stdout/stderr
            if execution.logs.stdout:
                output.append(f"STDOUT:\n{execution.logs.stdout}")
            if execution.logs.stderr:
                output.append(f"STDERR:\n{execution.logs.stderr}")
            if execution.error:
                output.append(f"ERROR:\n{execution.error}")
            
            # Save images and track paths
            for result in execution.results:
                if self._is_visualization_result(result):
                    img_path = self._save_visualization(result)
                    self.generated_images.append(img_path)
                    output.append(f"Visualization saved to: {img_path}")
            
            return "\n".join(output)
        except Exception as e:
            return f"Tool execution failed: {str(e)}"
    
    def _is_visualization_result(self, result: Result) -> bool:
        return hasattr(result, "png") and result.png
    
    def _save_visualization(self, result: Result) -> str:
        filename = f"visualization_{len(self.generated_images)}.png"
        path = os.path.join(self.output_dir, filename)
        with open(path, "wb") as f:
            f.write(base64.b64decode(result.png))
        return path
    
    def close(self):
        if self._sandbox:
            # Use the context manager's __exit__ method implicitly
            self._sandbox.__exit__(None, None, None)

if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()
    
    # Get API key from environment
    e2b_key = os.getenv("E2B_API_KEY")
    if not e2b_key:
        raise ValueError("E2B_API_KEY environment variable not set")
    
    # Create tool instance
    tool = CodeInterpreterTool(e2b_api_key=e2b_key)
    
    # Test with sample dataset and code
    sample_dataset = "sample_data.csv"
    sample_code = """
import pandas as pd
import matplotlib.pyplot as plt

# Read dataset - use the exact path we uploaded to
df = pd.read_csv('/dataset.csv')

# Create visualization
plt.figure(figsize=(10,6))
df.groupby('Category')['Sales'].sum().plot(kind='bar')
plt.title('Total Sales by Category')
plt.ylabel('Sales')
plt.tight_layout()
plt.savefig('visualization.png')  # Save to file
plt.show()  # This will generate the visualization
"""
    
    # Create sample dataset
    with open(sample_dataset, "w") as f:
        f.write("Product,Category,Sales\nA,Electronics,100\nB,Furniture,200\nC,Electronics,150")
    
    print("Starting tool test...")
    try:
        # Run the tool
        result = tool._run(code=sample_code, dataset_path=sample_dataset)
        print("\n✅ Tool Execution Result:")
        print(result)
        
        # Show generated visualizations
        print("\n🖼️ Generated Visualizations:")
        for viz in tool.generated_images:
            print(f"- {viz}")
        
        # Verify files exist
        for viz in tool.generated_images:
            if os.path.exists(viz):
                print(f"Verified: {viz} exists")
            else:
                print(f"Error: {viz} does not exist")
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
    finally:
        # Clean up
        tool.close()
        if os.path.exists(sample_dataset):
            os.remove(sample_dataset)
        print("Cleanup complete")