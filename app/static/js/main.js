document.addEventListener('DOMContentLoaded', function() {
    // Navigation
    const navLinks = document.querySelectorAll('.nav-links a');
    const contentSections = document.querySelectorAll('.content-section');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links
            navLinks.forEach(navLink => navLink.classList.remove('active'));
            
            // Add active class to clicked link
            this.classList.add('active');
            
            // Hide all content sections
            contentSections.forEach(section => section.classList.remove('active'));
            
            // Show corresponding content section
            const targetId = this.id.replace('-link', '');
            const targetSection = document.getElementById(targetId);
            targetSection.classList.add('active');
        });
    });
    
    // Modal handling
    const modals = {
        agent: {
            modal: document.getElementById('agent-modal'),
            openBtns: [document.getElementById('create-agent-btn'), document.getElementById('new-agent-btn')],
            form: document.getElementById('agent-form')
        },
        workflow: {
            modal: document.getElementById('workflow-modal'),
            openBtns: [document.getElementById('create-workflow-btn'), document.getElementById('new-workflow-btn')],
            form: document.getElementById('workflow-form')
        },
        project: {
            modal: document.getElementById('project-modal'),
            openBtns: [document.getElementById('create-project-btn'), document.getElementById('new-project-btn')],
            form: document.getElementById('project-form')
        }
    };
    
    // Set up modal open buttons
    Object.values(modals).forEach(modalObj => {
        modalObj.openBtns.forEach(btn => {
            if (btn) {
                btn.addEventListener('click', function() {
                    modalObj.modal.style.display = 'block';
                });
            }
        });
    });
    
    // Set up modal close buttons
    document.querySelectorAll('.close, .cancel-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const modal = this.closest('.modal');
            modal.style.display = 'none';
        });
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        document.querySelectorAll('.modal').forEach(modal => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
    });
    
    // API helper functions
    const API_BASE_URL = '/api/architect';
    
    async function fetchAPI(endpoint, method = 'GET', data = null) {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        if (data && (method === 'POST' || method === 'PUT')) {
            options.body = JSON.stringify(data);
        }
        
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'API request failed');
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            alert(`Error: ${error.message}`);
            throw error;
        }
    }
    
    // CRUD operations for Agents
    const agentManager = {
        async getAll() {
            return await fetchAPI('/agents');
        },
        
        async get(id) {
            return await fetchAPI(`/agents/${id}`);
        },
        
        async create(agentData) {
            return await fetchAPI('/agents', 'POST', agentData);
        },
        
        async update(id, agentData) {
            return await fetchAPI(`/agents/${id}`, 'PUT', agentData);
        },
        
        async delete(id) {
            return await fetchAPI(`/agents/${id}`, 'DELETE');
        }
    };
    
    // CRUD operations for Workflows
    const workflowManager = {
        async getAll() {
            return await fetchAPI('/workflows');
        },
        
        async get(id) {
            return await fetchAPI(`/workflows/${id}`);
        },
        
        async create(workflowData) {
            return await fetchAPI('/workflows', 'POST', workflowData);
        },
        
        async update(id, workflowData) {
            return await fetchAPI(`/workflows/${id}`, 'PUT', workflowData);
        },
        
        async delete(id) {
            return await fetchAPI(`/workflows/${id}`, 'DELETE');
        },
        
        async execute(id, inputData) {
            return await fetchAPI(`/workflows/${id}/execute`, 'POST', inputData);
        }
    };
    
    // CRUD operations for Projects
    const projectManager = {
        async getAll() {
            return await fetchAPI('/projects');
        },
        
        async get(id) {
            return await fetchAPI(`/projects/${id}`);
        },
        
        async create(projectData) {
            return await fetchAPI('/projects', 'POST', projectData);
        },
        
        async addAgent(projectId, agentId) {
            return await fetchAPI(`/projects/${projectId}/agents/${agentId}`, 'POST');
        },
        
        async addWorkflow(projectId, workflowId) {
            return await fetchAPI(`/projects/${projectId}/workflows/${workflowId}`, 'POST');
        }
    };
    
    // Form submission handlers
    if (modals.agent.form) {
        modals.agent.form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const capabilities = formData.get('capabilities') ? 
                formData.get('capabilities').split(',').map(cap => cap.trim()) : [];
                
            const agentData = {
                name: formData.get('name'),
                description: formData.get('description'),
                domain: formData.get('domain'),
                capabilities: capabilities,
                personality: {},
                knowledge_base: []
            };
            
            try {
                console.log('Creating agent with data:', agentData);
                const newAgent = await agentManager.create(agentData);
                modals.agent.modal.style.display = 'none';
                alert('Agent created successfully!');
                this.reset();
                loadAgents();
                updateDashboardCounts();
            } catch (error) {
                console.error('Error creating agent:', error);
                alert('Error creating agent: ' + error.message);
            }
        });
    }
    
    if (modals.workflow.form) {
        modals.workflow.form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            let workflowData;
            
            try {
                workflowData = {
                    name: formData.get('name'),
                    description: formData.get('description'),
                    steps: JSON.parse(formData.get('steps')),
                    input_schema: JSON.parse(formData.get('input_schema')),
                    output_schema: JSON.parse(formData.get('output_schema'))
                };
            } catch (error) {
                alert('Error parsing JSON. Please check your input format.');
                return;
            }
            
            try {
                const newWorkflow = await workflowManager.create(workflowData);
                modals.workflow.modal.style.display = 'none';
                alert('Workflow created successfully!');
                this.reset();
                loadWorkflows();
                updateDashboardCounts();
            } catch (error) {
                console.error('Error creating workflow:', error);
            }
        });
    }
    
    if (modals.project.form) {
        modals.project.form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const projectData = {
                name: formData.get('name'),
                description: formData.get('description')
            };
            
            try {
                const newProject = await projectManager.create(projectData);
                modals.project.modal.style.display = 'none';
                alert('Project created successfully!');
                this.reset();
                loadProjects();
                updateDashboardCounts();
            } catch (error) {
                console.error('Error creating project:', error);
            }
        });
    }
    
    // Load data functions
    async function loadAgents() {
        try {
            const agents = await agentManager.getAll();
            const agentList = document.getElementById('agent-list');
            
            if (agents.length === 0) {
                agentList.innerHTML = '<p class="empty-message">No agents found. Create your first agent to get started.</p>';
                return;
            }
            
            agentList.innerHTML = '';
            
            agents.forEach(agent => {
                const agentItem = document.createElement('div');
                agentItem.className = 'list-item';
                
                agentItem.innerHTML = `
                    <div class="col" data-label="Name">${agent.name}</div>
                    <div class="col" data-label="Domain">${agent.domain}</div>
                    <div class="col" data-label="Capabilities">${agent.capabilities.join(', ') || 'None'}</div>
                    <div class="col actions" data-label="Actions">
                        <button class="btn secondary view-agent-btn" data-id="${agent.agent_id}">View</button>
                        <button class="btn danger delete-agent-btn" data-id="${agent.agent_id}">Delete</button>
                    </div>
                `;
                
                agentList.appendChild(agentItem);
            });
            
            // Add event listeners for the action buttons
            document.querySelectorAll('.delete-agent-btn').forEach(btn => {
                btn.addEventListener('click', async function() {
                    const agentId = this.getAttribute('data-id');
                    if (confirm('Are you sure you want to delete this agent?')) {
                        try {
                            await agentManager.delete(agentId);
                            loadAgents();
                            updateDashboardCounts();
                        } catch (error) {
                            console.error('Error deleting agent:', error);
                        }
                    }
                });
            });
            
            document.querySelectorAll('.view-agent-btn').forEach(btn => {
                btn.addEventListener('click', async function() {
                    const agentId = this.getAttribute('data-id');
                    try {
                        const agent = await agentManager.get(agentId);
                        alert(`Agent Details:\nName: ${agent.name}\nDomain: ${agent.domain}\nDescription: ${agent.description}\nCapabilities: ${agent.capabilities.join(', ') || 'None'}`);
                    } catch (error) {
                        console.error('Error viewing agent:', error);
                    }
                });
            });
        } catch (error) {
            console.error('Error loading agents:', error);
        }
    }
    
    async function loadWorkflows() {
        try {
            const workflows = await workflowManager.getAll();
            const workflowList = document.getElementById('workflow-list');
            
            if (workflows.length === 0) {
                workflowList.innerHTML = '<p class="empty-message">No workflows found. Create your first workflow to get started.</p>';
                return;
            }
            
            workflowList.innerHTML = '';
            
            workflows.forEach(workflow => {
                const workflowItem = document.createElement('div');
                workflowItem.className = 'list-item';
                
                workflowItem.innerHTML = `
                    <div class="col" data-label="Name">${workflow.name}</div>
                    <div class="col" data-label="Description">${workflow.description}</div>
                    <div class="col" data-label="Steps">${workflow.steps.length} steps</div>
                    <div class="col actions" data-label="Actions">
                        <button class="btn secondary execute-workflow-btn" data-id="${workflow.workflow_id}">Execute</button>
                        <button class="btn danger delete-workflow-btn" data-id="${workflow.workflow_id}">Delete</button>
                    </div>
                `;
                
                workflowList.appendChild(workflowItem);
            });
            
            // Add event listeners for the action buttons
            document.querySelectorAll('.delete-workflow-btn').forEach(btn => {
                btn.addEventListener('click', async function() {
                    const workflowId = this.getAttribute('data-id');
                    if (confirm('Are you sure you want to delete this workflow?')) {
                        try {
                            await workflowManager.delete(workflowId);
                            loadWorkflows();
                            updateDashboardCounts();
                        } catch (error) {
                            console.error('Error deleting workflow:', error);
                        }
                    }
                });
            });
            
            document.querySelectorAll('.execute-workflow-btn').forEach(btn => {
                btn.addEventListener('click', async function() {
                    const workflowId = this.getAttribute('data-id');
                    try {
                        // For simplicity, we'll use an empty input for now
                        const result = await workflowManager.execute(workflowId, {});
                        alert(`Workflow executed successfully!\nResult: ${JSON.stringify(result, null, 2)}`);
                    } catch (error) {
                        console.error('Error executing workflow:', error);
                    }
                });
            });
        } catch (error) {
            console.error('Error loading workflows:', error);
        }
    }
    
    async function loadProjects() {
        try {
            const projects = await projectManager.getAll();
            const projectList = document.getElementById('project-list');
            
            if (projects.length === 0) {
                projectList.innerHTML = '<p class="empty-message">No projects found. Create your first project to get started.</p>';
                return;
            }
            
            projectList.innerHTML = '';
            
            projects.forEach(project => {
                const projectItem = document.createElement('div');
                projectItem.className = 'list-item';
                
                projectItem.innerHTML = `
                    <div class="col" data-label="Name">${project.name}</div>
                    <div class="col" data-label="Description">${project.description}</div>
                    <div class="col" data-label="Agents">${project.agents.length} agents</div>
                    <div class="col actions" data-label="Actions">
                        <button class="btn secondary view-project-btn" data-id="${project.project_id}">View</button>
                    </div>
                `;
                
                projectList.appendChild(projectItem);
            });
            
            // Add event listeners for the action buttons
            document.querySelectorAll('.view-project-btn').forEach(btn => {
                btn.addEventListener('click', async function() {
                    const projectId = this.getAttribute('data-id');
                    try {
                        const project = await projectManager.get(projectId);
                        alert(`Project Details:\nName: ${project.name}\nDescription: ${project.description}\nAgents: ${project.agents.length}\nWorkflows: ${project.workflows.length}`);
                    } catch (error) {
                        console.error('Error viewing project:', error);
                    }
                });
            });
        } catch (error) {
            console.error('Error loading projects:', error);
        }
    }
    
    // Update dashboard counts
    async function updateDashboardCounts() {
        try {
            const agents = await agentManager.getAll();
            const workflows = await workflowManager.getAll();
            const projects = await projectManager.getAll();
            
            document.getElementById('agent-count').textContent = agents.length;
            document.getElementById('workflow-count').textContent = workflows.length;
            document.getElementById('project-count').textContent = projects.length;
        } catch (error) {
            console.error('Error updating dashboard counts:', error);
        }
    }
    
    // Initialize the page
    try {
        updateDashboardCounts();
        loadAgents();
        loadWorkflows();
        loadProjects();
    } catch (error) {
        console.error('Error initializing page:', error);
    }
    
    // Quick start guide
    document.getElementById('quick-start-btn').addEventListener('click', function() {
        const guideText = `
Quick Start Guide:

1. Create a specialized agent:
   - Click "Create Agent" in the dashboard
   - Provide a name, description, domain, and capabilities
   - Submit the form to create your agent

2. Design workflows between agents:
   - Click "Create Workflow" in the dashboard
   - Define the workflow steps, input schema, and output schema
   - Submit the form to create your workflow

3. Organize into projects:
   - Click "Create Project" in the dashboard
   - Add agents and workflows to your project

Need more help? Check the documentation for detailed guides.
        `;
        
        alert(guideText);
    });
});