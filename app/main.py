from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Загрузка .env файла
load_dotenv()

# Метрики Prometheus
requests_counter = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint"])

# Настройка шаблонов
templates = Jinja2Templates(directory="app/templates")

# Создание приложения FastAPI
app = FastAPI(
    title="FastAPI Test App",
    version="1.0.0"
)


# Pydantic модели для валидации
class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None


# Хранилище данных (в памяти)
items_db = []
counter = 1


# Middleware для метрик
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    response = await call_next(request)
    requests_counter.labels(method=request.method, endpoint=request.url.path).inc()
    return response


# Эндпоинты API
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Главная страница с шаблоном"""
    return templates.TemplateResponse("index.html", {"request": request, "title": "FastAPI Test App"})


@app.get("/health")
async def health_check():
    """Проверка здоровья приложения"""
    return {"status": "ok", "message": "FastAPI is running"}


@app.post("/items/", response_model=ItemResponse)
async def create_item(item: ItemCreate):
    """Создание нового элемента"""
    global counter
    new_item = ItemResponse(id=counter, name=item.name, description=item.description)
    items_db.append(new_item)
    counter += 1
    return new_item


@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    """Получение элемента по ID"""
    for item in items_db:
        if item.id == item_id:
            return item
    return {"error": "Item not found"}, 404


@app.get("/items/")
async def list_items():
    """Список всех элементов"""
    return {"items": items_db}


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """Удаление элемента по ID"""
    global items_db
    for i, item in enumerate(items_db):
        if item.id == item_id:
            items_db.pop(i)
            return {"message": f"Item {item_id} deleted"}
    return {"error": "Item not found"}, 404


@app.get("/metrics")
async def metrics():
    """Эндпоинт для Prometheus метрик"""
    from fastapi.responses import Response
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


# Для запуска через uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )