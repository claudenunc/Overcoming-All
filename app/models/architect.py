from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class Agent(BaseModel):
    """Model representing an AI agent in the ARCHITECT system"""
    agent_id: str = Field(..., description="Unique identifier for the agent")
    name: str = Field(..., description="Human-readable name for the agent")
    description: str = Field(..., description="Description of the agent's purpose and capabilities")
    domain: str = Field(..., description="Primary domain of expertise")
    capabilities: List[str] = Field(default_factory=list, description="List of agent capabilities")
    personality: Dict[str, Any] = Field(default_factory=dict, description="Personality traits of the agent")
    knowledge_base: List[str] = Field(default_factory=list, description="Knowledge sources the agent has access to")
    dependencies: List[str] = Field(default_factory=list, description="IDs of agents this agent depends on")

class Workflow(BaseModel):
    """Model representing a workflow between agents"""
    workflow_id: str = Field(..., description="Unique identifier for the workflow")
    name: str = Field(..., description="Human-readable name for the workflow")
    description: str = Field(..., description="Description of the workflow's purpose")
    steps: List[Dict[str, Any]] = Field(..., description="Sequence of steps in the workflow")
    input_schema: Dict[str, Any] = Field(..., description="Schema for the workflow input")
    output_schema: Dict[str, Any] = Field(..., description="Schema for the workflow output")

class Project(BaseModel):
    """Model representing a project in the ARCHITECT system"""
    project_id: str = Field(..., description="Unique identifier for the project")
    name: str = Field(..., description="Human-readable name for the project")
    description: str = Field(..., description="Description of the project's purpose")
    agents: List[Agent] = Field(default_factory=list, description="Agents assigned to this project")
    workflows: List[Workflow] = Field(default_factory=list, description="Workflows defined for this project")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional project metadata")

class AgentTask(BaseModel):
    """Model representing a task assigned to an agent"""
    task_id: str = Field(..., description="Unique identifier for the task")
    agent_id: str = Field(..., description="ID of the agent assigned to this task")
    description: str = Field(..., description="Description of the task")
    input_data: Dict[str, Any] = Field(..., description="Input data for the task")
    status: str = Field(default="pending", description="Current status of the task")
    result: Optional[Dict[str, Any]] = Field(default=None, description="Result of the task execution")

class PerformanceMetrics(BaseModel):
    """Model for tracking agent performance metrics"""
    agent_id: str = Field(..., description="ID of the agent being measured")
    task_count: int = Field(default=0, description="Number of tasks completed")
    success_rate: float = Field(default=0.0, description="Percentage of successful task completions")
    average_response_time: float = Field(default=0.0, description="Average time to complete tasks in seconds")
    quality_score: float = Field(default=0.0, description="Average quality score (0-1)")
    user_satisfaction: float = Field(default=0.0, description="Average user satisfaction score (0-1)")
