from fastapi import FastAPI
import sys
import os
# from .routes import router as api_router
# from customer.routes import router
from src.main.database.session import async_session_local, async_engine
from src.main.database.base import Base
from src.main.customer.routes import router as customer_router
from src.main.auth.routes import router as auth_router
from src.main.orders.routes import router as order_router
# from dotenv import load_dotenv

# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))
# # Verify that SECRET_KEY is loaded
# print(f"SECRET_KEY loaded from env: {os.getenv('SECRET_KEY')}")
# # sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Initialize the FastAPI application
app = FastAPI(title="FastAPI Main Service")

app.include_router(auth_router, prefix="/auth", tags=["AUTH"])
app.include_router(customer_router, prefix="/customer", tags=["CUSTOMERS"])
app.include_router(order_router, prefix="/order", tags=["ORDERS"])


@app.on_event("startup")
async def startup_event():
    # Use async engine directly to create tables
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Main Service"}


if __name__ == '__main__':
    app.run("main:app", debug=True, host='0.0.0.0')
