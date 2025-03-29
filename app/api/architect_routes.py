from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any

from app.models.architect import Agent, Workflow, Project, AgentTask, PerformanceMetrics
from app.utils.agent_manager import AgentManager
from app.utils.workflow_manager import WorkflowManager

# Create instances of managers
agent_manager = AgentManager()
workflow_manager = WorkflowManager(agent_manager)

router = APIRouter(prefix="/architect", tags=["architect"])

# ------ Agent Routes ------

@router.post("/agents", response_model=Agent)
async def create_agent(
    name: str,
    description: str,
    domain: str,
    capabilities: List[str] = None,
    personality: Dict[str, Any] = None,
    knowledge_base: List[str] = None
):
    """Create a new agent"""
    agent = agent_manager.create_agent(
        name=name, 
        description=description, 
        domain=domain,
        capabilities=capabilities,
        personality=personality,
        knowledge_base=knowledge_base
    )
    return agent

@router.get("/agents", response_model=List[Agent])
async def list_agents():
    """List all available agents"""
    return agent_manager.list_agents()

@router.get("/agents/{agent_id}", response_model=Agent)
async def get_agent(agent_id: str):
    """Get a specific agent by ID"""
    agent = agent_manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent with ID {agent_id} not found")
    return agent

@router.put("/agents/{agent_id}", response_model=Agent)
async def update_agent(agent_id: str, update_data: Dict[str, Any]):
    """Update an agent's attributes"""
    agent = agent_manager.update_agent(agent_id, **update_data)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent with ID {agent_id} not found")
    return agent

@router.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str):
    """Delete an agent by ID"""
    success = agent_manager.delete_agent(agent_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Agent with ID {agent_id} not found")
    return {"message": f"Agent with ID {agent_id} has been deleted"}

# ------ Task Routes ------

@router.post("/agents/{agent_id}/tasks", response_model=AgentTask)
async def create_task(agent_id: str, description: str, input_data: Dict[str, Any]):
    """Create a new task for an agent"""
    task = agent_manager.create_task(agent_id, description, input_data)
    if not task:
        raise HTTPException(status_code=404, detail=f"Agent with ID {agent_id} not found")
    return task

@router.get("/tasks/{task_id}", response_model=AgentTask)
async def get_task(task_id: str):
    """Get a specific task by ID"""
    task = agent_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    return task

@router.put("/tasks/{task_id}", response_model=AgentTask)
async def update_task(task_id: str, status: str, result: Dict[str, Any] = None):
    """Update a task's status and result"""
    task = agent_manager.update_task_status(task_id, status, result)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    return task

@router.get("/agents/{agent_id}/tasks", response_model=List[AgentTask])
async def get_agent_tasks(agent_id: str):
    """Get all tasks for a specific agent"""
    agent = agent_manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent with ID {agent_id} not found")
    return agent_manager.get_agent_tasks(agent_id)

# ------ Workflow Routes ------

@router.post("/workflows", response_model=Workflow)
async def create_workflow(
    name: str,
    description: str,
    steps: List[Dict[str, Any]],
    input_schema: Dict[str, Any],
    output_schema: Dict[str, Any]
):
    """Create a new workflow"""
    workflow = workflow_manager.create_workflow(
        name=name,
        description=description,
        steps=steps,
        input_schema=input_schema,
        output_schema=output_schema
    )
    return workflow

@router.get("/workflows", response_model=List[Workflow])
async def list_workflows():
    """List all available workflows"""
    return workflow_manager.list_workflows()

@router.get("/workflows/{workflow_id}", response_model=Workflow)
async def get_workflow(workflow_id: str):
    """Get a specific workflow by ID"""
    workflow = workflow_manager.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail=f"Workflow with ID {workflow_id} not found")
    return workflow

@router.put("/workflows/{workflow_id}", response_model=Workflow)
async def update_workflow(workflow_id: str, update_data: Dict[str, Any]):
    """Update a workflow's attributes"""
    workflow = workflow_manager.update_workflow(workflow_id, **update_data)
    if not workflow:
        raise HTTPException(status_code=404, detail=f"Workflow with ID {workflow_id} not found")
    return workflow

@router.delete("/workflows/{workflow_id}")
async def delete_workflow(workflow_id: str):
    """Delete a workflow by ID"""
    success = workflow_manager.delete_workflow(workflow_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Workflow with ID {workflow_id} not found")
    return {"message": f"Workflow with ID {workflow_id} has been deleted"}

@router.post("/workflows/{workflow_id}/execute", response_model=Dict[str, Any])
async def execute_workflow(workflow_id: str, input_data: Dict[str, Any]):
    """Execute a workflow with the given input data"""
    try:
        result = workflow_manager.execute_workflow(workflow_id, input_data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing workflow: {str(e)}")

# ------ Project Routes ------

@router.post("/projects", response_model=Project)
async def create_project(name: str, description: str, metadata: Dict[str, Any] = None):
    """Create a new project"""
    project = workflow_manager.create_project(name, description, metadata)
    return project

@router.get("/projects", response_model=List[Project])
async def list_projects():
    """List all available projects"""
    return list(workflow_manager.projects.values())

@router.get("/projects/{project_id}", response_model=Project)
async def get_project(project_id: str):
    """Get a specific project by ID"""
    project = workflow_manager.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")
    return project

@router.post("/projects/{project_id}/agents/{agent_id}", response_model=Project)
async def add_agent_to_project(project_id: str, agent_id: str):
    """Add an agent to a project"""
    project = workflow_manager.add_agent_to_project(project_id, agent_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project or agent not found")
    return project

@router.post("/projects/{project_id}/workflows/{workflow_id}", response_model=Project)
async def add_workflow_to_project(project_id: str, workflow_id: str):
    """Add a workflow to a project"""
    project = workflow_manager.add_workflow_to_project(project_id, workflow_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project or workflow not found")
    return project