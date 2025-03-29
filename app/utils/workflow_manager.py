import uuid
from typing import List, Dict, Any, Optional
from app.models.architect import Workflow, Project
from app.utils.agent_manager import AgentManager

class WorkflowManager:
    """Manager class for handling workflows in the ARCHITECT system"""
    
    def __init__(self, agent_manager: AgentManager):
        self.workflows: Dict[str, Workflow] = {}
        self.projects: Dict[str, Project] = {}
        self.agent_manager = agent_manager
    
    def create_workflow(self, name: str, description: str, steps: List[Dict[str, Any]], 
                        input_schema: Dict[str, Any], output_schema: Dict[str, Any]) -> Workflow:
        """Create a new workflow with the specified parameters"""
        workflow_id = str(uuid.uuid4())
        
        workflow = Workflow(
            workflow_id=workflow_id,
            name=name,
            description=description,
            steps=steps,
            input_schema=input_schema,
            output_schema=output_schema
        )
        
        self.workflows[workflow_id] = workflow
        return workflow
    
    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """Retrieve a workflow by ID"""
        return self.workflows.get(workflow_id)
    
    def update_workflow(self, workflow_id: str, **kwargs) -> Optional[Workflow]:
        """Update an existing workflow's attributes"""
        workflow = self.get_workflow(workflow_id)
        if not workflow:
            return None
        
        for key, value in kwargs.items():
            if hasattr(workflow, key):
                setattr(workflow, key, value)
        
        self.workflows[workflow_id] = workflow
        return workflow
    
    def delete_workflow(self, workflow_id: str) -> bool:
        """Delete a workflow by ID"""
        if workflow_id in self.workflows:
            del self.workflows[workflow_id]
            return True
        return False
    
    def list_workflows(self) -> List[Workflow]:
        """List all available workflows"""
        return list(self.workflows.values())
    
    def create_project(self, name: str, description: str, metadata: Dict[str, Any] = None) -> Project:
        """Create a new project"""
        project_id = str(uuid.uuid4())
        
        project = Project(
            project_id=project_id,
            name=name,
            description=description,
            agents=[],
            workflows=[],
            metadata=metadata or {}
        )
        
        self.projects[project_id] = project
        return project
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """Retrieve a project by ID"""
        return self.projects.get(project_id)
    
    def add_agent_to_project(self, project_id: str, agent_id: str) -> Optional[Project]:
        """Add an agent to a project"""
        project = self.get_project(project_id)
        agent = self.agent_manager.get_agent(agent_id)
        
        if not project or not agent:
            return None
        
        # Check if agent is already in the project
        if any(a.agent_id == agent_id for a in project.agents):
            return project
        
        project.agents.append(agent)
        self.projects[project_id] = project
        return project
    
    def add_workflow_to_project(self, project_id: str, workflow_id: str) -> Optional[Project]:
        """Add a workflow to a project"""
        project = self.get_project(project_id)
        workflow = self.get_workflow(workflow_id)
        
        if not project or not workflow:
            return None
        
        # Check if workflow is already in the project
        if any(w.workflow_id == workflow_id for w in project.workflows):
            return project
        
        project.workflows.append(workflow)
        self.projects[project_id] = project
        return project
    
    def execute_workflow(self, workflow_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a workflow with the given input data"""
        workflow = self.get_workflow(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow with ID {workflow_id} not found")
        
        # Placeholder implementation - in a real system, this would execute the workflow steps
        # For now, we'll just return a mock result
        result = {
            "workflow_id": workflow_id,
            "status": "completed",
            "input": input_data,
            "output": {"message": f"Executed workflow: {workflow.name}"}
        }
        
        return result