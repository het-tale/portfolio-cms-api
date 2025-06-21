from enum import Enum


class ProjectStatus(Enum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Category(Enum):
    PROGRAMMING_LANGUAGES = "programming_languages"
    FRONTEND = "frontend"
    BACKEND = "backend"
    DATABASE = "database"
    DEVOPS = "devops"
    TOOLS = "tools"
