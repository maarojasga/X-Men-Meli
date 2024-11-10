from fastapi import FastAPI
from api import mutant, stats
from db.database import initialize_db

app = FastAPI(debug=True)

# Initialize the database when the app starts
initialize_db()

# Include the endpoints (routers) for mutant detection and statistics
app.include_router(mutant.router, prefix="/api")
app.include_router(stats.router, prefix="/api")