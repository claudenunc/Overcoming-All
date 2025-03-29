import uuid
from typing import List, Dict, Any, Optional
from app.models.architect import Agent, AgentTask, PerformanceMetrics

class AgentManager:
    """Manager class for handling AI agents in the ARCHITECT system"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, AgentTask] = {}
        self.metrics: Dict[str, PerformanceMetrics] = {}
    
    def create_agent(self, name: str, description: str, domain: str, 
                     capabilities: List[str] = None, 
                     personality: Dict[str, Any] = None,
                     knowledge_base: List[str] = None) -> Agent:
        """Create a new agent with the specified parameters"""
        agent_id = str(uuid.uuid4())
        
        agent = Agent(
            agent_id=agent_id,
            name=name,
            description=description,
            domain=domain,
            capabilities=capabilities or [],
            personality=personality or {},
            knowledge_base=knowledge_base or [],
            dependencies=[]
        )
        
        self.agents[agent_id] = agent
        self.metrics[agent_id] = PerformanceMetrics(agent_id=agent_id)
        
        return agent
    
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Retrieve an agent by ID"""
        return self.agents.get(agent_id)
    
    def update_agent(self, agent_id: str, **kwargs) -> Optional[Agent]:
        """Update an existing agent's attributes"""
        agent = self.get_agent(agent_id)
        if not agent:
            return None
        
        for key, value in kwargs.items():
            if hasattr(agent, key):
                setattr(agent, key, value)
        
        self.agents[agent_id] = agent
        return agent
    
    def delete_agent(self, agent_id: str) -> bool:
        """Delete an agent by ID"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            if agent_id in self.metrics:
                del self.metrics[agent_id]
            return True
        return False
    
    def list_agents(self) -> List[Agent]:
        """List all available agents"""
        return list(self.agents.values())
    
    def create_task(self, agent_id: str, description: str, input_data: Dict[str, Any]) -> Optional[AgentTask]:
        """Create a new task for an agent"""
        if agent_id not in self.agents:
            return None
        
        task_id = str(uuid.uuid4())
        task = AgentTask(
            task_id=task_id,
            agent_id=agent_id,
            description=description,
            input_data=input_data,
            status="pending",
            result=None
        )
        
        self.tasks[task_id] = task
        return task
    
    def get_task(self, task_id: str) -> Optional[AgentTask]:
        """Retrieve a task by ID"""
        return self.tasks.get(task_id)
    
    def update_task_status(self, task_id: str, status: str, result: Dict[str, Any] = None) -> Optional[AgentTask]:
        """Update a task's status and optionally its result"""
        task = self.get_task(task_id)
        if not task:
            return None
        
        task.status = status
        if result is not None:
            task.result = result
        
        self.tasks[task_id] = task
        return task
    
    def get_agent_tasks(self, agent_id: str) -> List[AgentTask]:
        """Get all tasks assigned to a specific agent"""
        return [task for task in self.tasks.values() if task.agent_id == agent_id]
    
    def update_metrics(self, agent_id: str, task_success: bool, response_time: float, quality_score: float) -> Optional[PerformanceMetrics]:
        """Update performance metrics for an agent"""
        if agent_id not in self.metrics:
            return None
        
        metrics = self.metrics[agent_id]
        
        # Update task count and success rate
        metrics.task_count += 1
        
        # Update success rate
        if metrics.task_count > 0:
            old_success_count = metrics.success_rate * (metrics.task_count - 1)
            new_success_count = old_success_count + (1 if task_success else 0)
            metrics.success_rate = new_success_count / metrics.task_count
        
        # Update average response time
        if metrics.task_count > 0:
            old_total_time = metrics.average_response_time * (metrics.task_count - 1)
            metrics.average_response_time = (old_total_time + response_time) / metrics.task_count
        
        # Update quality score
        if metrics.task_count > 0:
            old_total_quality = metrics.quality_score * (metrics.task_count - 1)
            metrics.quality_score = (old_total_quality + quality_score) / metrics.task_count
        
        self.metrics[agent_id] = metrics
        return metrics
    
    def get_metrics(self, agent_id: str) -> Optional[PerformanceMetrics]:
        """Get performance metrics for an agent"""
        return self.metrics.get(agent_id)
