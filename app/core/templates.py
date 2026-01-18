from fastapi.templating import Jinja2Templates

# Централизованный экземпляр шаблонов
templates = Jinja2Templates(directory="app/templates")
