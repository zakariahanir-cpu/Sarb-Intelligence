import os

def create_web_project(agent_name, project_name, files):
    """
    ينشئ مشروع موقع ويب في مجلد الوكيل باستخدام مسارات نسبية.
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    project_path = os.path.join(BASE_DIR, 'agents', agent_name, project_name)
    os.makedirs(project_path, exist_ok=True)
    
    created_files = []
    for filename, content in files.items():
        file_path = os.path.join(project_path, filename)
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(content)
        created_files.append(filename)
    
    return f"Project '{project_name}' created by {agent_name} at {project_path}"
