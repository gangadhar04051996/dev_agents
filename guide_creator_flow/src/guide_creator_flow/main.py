#!/usr/bin/env python
import json
import os
from typing import List, Dict, Optional
from pathlib import Path
from pydantic import BaseModel, Field
from crewai import LLM
from crewai.flow import Flow, listen, start
from .crews.code_writer.code_writer import CodeWriter

# Add constants for output directories
OUTPUT_DIR = "output"
CODE_DIR = os.path.join(OUTPUT_DIR, "code")
REPORTS_DIR = os.path.join(OUTPUT_DIR, "reports")

class CodeSection(BaseModel):
    name: str = Field(description="Name of the code component")
    description: str = Field(description="Description of what this component does")
    dependencies: List[str] = Field(description="List of required dependencies", default=[])

class CodeStructure(BaseModel):
    project_name: str = Field(description="Name of the project")
    description: str = Field(description="Brief description of the project")
    components: List[CodeSection] = Field(description="List of code components")
    tech_stack: Dict[str, str] = Field(description="Technology stack details")

class CodeWriterState(BaseModel):
    feature_name: str = Field(default="")
    programming_language: str = Field(default="python")
    program: str = Field(default="")
    file_name: str = Field(default="")
    code_structure: Optional[CodeStructure] = None

    def generate_file_name(self):
        """Generate standardized file name based on feature name and language"""
        # Clean the feature name to be file-system friendly
        clean_name = self.feature_name.lower().replace(" ", "_")

        # Map common language names to their extensions
        extensions = {
            "python": ".py",
            "javascript": ".js",
            "typescript": ".ts",
            "java": ".java",
            "rust": ".rs",
            "cpp": ".cpp",
            "c++": ".cpp",
            "c": ".c",
            "go": ".go",
            "ruby": ".rb",
            "php": ".php"
        }

        extension = extensions.get(self.programming_language.lower(), ".txt")
        return f"{clean_name}_{self.programming_language.lower()}{extension}"

class CodeWriterFlow(Flow[CodeWriterState]):
    """Flow for creating code implementations with proper documentation and diagrams"""

    def __init__(self):
        super().__init__()
        # Create necessary directories
        for directory in [OUTPUT_DIR, CODE_DIR, REPORTS_DIR]:
            os.makedirs(directory, exist_ok=True)

    @start()
    def get_user_input(self):
        """Get input from the user about the feature and the programming language"""
        print("\n=== Provide the details of the program you want to build ===\n")

        # Get user input
        self.state.feature_name = input("What program do you want to build? ")
        self.state.programming_language = input("What programming language do you want to use? ")

        # Generate standardized file name
        self.state.file_name = self.state.generate_file_name()
        return self.state

    @listen(get_user_input)
    def create_code_structure(self):
        """Create a structured outline for the code implementation"""
        print("Creating code structure...")

        llm = LLM(
            model="ollama/gemma3",
            base_url="http://localhost:11434"
        )

        messages = [
            {"role": "system", "content": """You are a software architect designing code structure.
            Please provide your response in a structured JSON format with the following schema:
            {
                "project_name": "string",
                "description": "string",
                "components": [
                    {
                        "name": "string",
                        "description": "string",
                        "dependencies": ["string"]
                    }
                ],
                "tech_stack": {
                    "language": "string"
                }
            }"""},
            {"role": "user", "content": f"""
            Create a detailed structure for implementing {self.state.feature_name}
            using {self.state.programming_language}.
            Include necessary components, their relationships, and required dependencies.
            Ensure your response follows the JSON schema specified above.
            """}
        ]

        response = llm.call(messages=messages)

        try:
            # Parse the response into JSON
            structure_dict = json.loads(response)
            # Create a CodeStructure instance from the parsed JSON
            self.state.code_structure = CodeStructure(
                project_name=structure_dict.get("project_name", self.state.feature_name),
                description=structure_dict.get("description", ""),
                components=[CodeSection(**comp) for comp in structure_dict.get("components", [])],
                tech_stack=structure_dict.get("tech_stack", {
                    "language": self.state.programming_language
                })
            )
        except json.JSONDecodeError as e:
            print(f"Warning: Could not parse LLM response as JSON: {e}")
            # Create a default structure
            self.state.code_structure = CodeStructure(
                project_name=self.state.feature_name,
                description="Auto-generated structure",
                components=[],
                tech_stack={
                    "language": self.state.programming_language
                }
            )

        return self.state

    @listen(create_code_structure)
    def generate_program(self):
        """Generate the actual code implementation"""
        print("Generating program...")

        if not self.state.code_structure:
            raise ValueError("Code structure not created. Cannot generate program.")

        result = (
            CodeWriter()
            .crew()
            .kickoff(inputs={
                "feature_name": self.state.feature_name,
                "programming_language": self.state.programming_language,
                "file_name": self.state.file_name,
                "code_structure": self.state.code_structure.model_dump()
            })
        )

        # Get the actual code from the first task (code_development_task)
        if result.tasks_output and len(result.tasks_output) > 0:
            self.state.program = result.tasks_output[0].raw
        else:
            raise ValueError("No code was generated by the CodeWriter crew")

        # Save the program code to the code directory
        code_file_path = os.path.join(CODE_DIR, self.state.file_name)
        with open(code_file_path, "w") as f:
            f.write(self.state.program)

        print(f"Generated code saved to {code_file_path}")
        return self.state

    @listen(generate_program)
    def flow_diagram_creator(self):
        """Create a flow diagram showing the logical flow of the generated program"""
        print("Creating flow diagram...")

        # Generate diagram filename
        diagram_filename = f"{self.state.feature_name.lower().replace(' ', '_')}_output.mmd"

        llm = LLM(
            model="ollama/gemma3",
            base_url="http://localhost:11434"
        )

        messages = [
            {"role": "system", "content": """You are a technical diagram expert.
            Create a Mermaid flowchart diagram that shows the logical flow of the given program.
            Focus on the algorithm's steps, decision points, and data flow.
            Use 'flowchart TD' syntax (not 'graph TD').
            Include appropriate styling for different node types.
            Make sure to show:
            - Input/Output operations
            - Processing steps
            - Decision points
            - Loops if any
            - Data transformations

             Remove any ``` values in the output.
            """},
            {"role": "user", "content": f"""
            Create a detailed Mermaid flowchart for this program:

            {self.state.program}

            Show how the program flows from start to end, including all major operations and decision points.
            Start the diagram with 'flowchart TD' (not 'graph TD').
            Use only valid Mermaid flowchart syntax.
            """}
        ]

        # Get the Mermaid diagram code from LLM
        mermaid_code = llm.call(messages=messages)

        # Ensure the code starts with flowchart TD
        if not mermaid_code.strip().startswith("flowchart TD"):
            mermaid_code = "flowchart TD\n" + mermaid_code.replace("graph TD", "")

        # Save the Mermaid diagram code to the reports directory
        diagram_file_path = os.path.join(REPORTS_DIR, diagram_filename)
        with open(diagram_file_path, "w") as f:
            f.write(mermaid_code)

        # Generate and save a markdown report
        report_filename = f"{self.state.feature_name.lower().replace(' ', '_')}_report.md"
        report_content = f"""# {self.state.feature_name} Implementation Report

## Code Implementation
The implementation has been saved to: `{os.path.join('code', self.state.file_name)}`

## Flow Diagram
The flow diagram has been saved to: `{os.path.join('reports', diagram_filename)}`

### Program Flow Description
{self._generate_flow_description(self.state.program)}
"""

        report_file_path = os.path.join(REPORTS_DIR, report_filename)
        with open(report_file_path, "w") as f:
            f.write(report_content)

        print(f"Flow diagram saved to {diagram_file_path}")
        print(f"Report saved to {report_file_path}")
        return self.state

    def _generate_flow_description(self, program: str) -> str:
        """Generate a textual description of the program flow"""
        llm = LLM(
            model="ollama/gemma3",
            base_url="http://localhost:11434"
        )

        description = llm.call([{
            "role": "system",
            "content": "Provide a clear, concise description of how the given program works, focusing on its logical flow and main operations."
        }, {
            "role": "user",
            "content": f"Describe the flow of this program:\n\n{program}"
        }])

        return description

def kickoff():
    """Run the code writer flow"""
    CodeWriterFlow().kickoff()
    print("\n=== Flow Complete ===")
    print(f"Your implementation files are ready in the following locations:")
    print(f"- Code: {CODE_DIR}")
    print(f"- Reports: {REPORTS_DIR}")

def plot():
    """Generate a visualization of the flow"""
    flow = CodeWriterFlow()
    flow.plot("code_writer_flow")
    print("Flow visualization saved to code_writer_flow.html")

if __name__ == "__main__":
    kickoff()
