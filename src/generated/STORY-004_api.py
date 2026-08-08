from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime

app = FastAPI(title="Portfolio Rebalancing")

class Asset(BaseModel):
    symbol: str
    current_allocation: float
    target_allocation: float

class RebalanceRequest(BaseModel):
    user_id: str
    assets: List[Asset]

class RebalanceAction(BaseModel):
    symbol: str
    action: str
    quantity: float

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "rebalance"}

@app.post("/rebalance/calculate")
def calculate_rebalance(request: RebalanceRequest) -> Dict:
    actions = []
    for asset in request.assets:
        diff = asset.target_allocation - asset.current_allocation
        if abs(diff) > 1:
            actions.append({
                "symbol": asset.symbol,
                "action": "buy" if diff > 0 else "sell",
                "change_percent": diff
            })
    return {"user_id": request.user_id, "actions": actions, "timestamp": datetime.now().isoformat()}

@app.get("/rebalance/status/{user_id}")
def get_rebalance_status(user_id: str):
    return {"user_id": user_id, "status": "balanced", "last_rebalance": "2024-01-10"}
