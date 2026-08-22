"""
Module: Idiomatic Python Transformations
Demonstrating before and after Pythonic improvements using comprehensions,
pattern matching, context managers, and type hints.
"""
from typing import List, Dict, Any
from datetime import datetime


# ==========================================
# 1. Non-Idiomatic (Procedural) Python
# ==========================================
def process_active_users_procedural(user_records):
    results = []
    total_score = 0
    count = 0
    
    for i in range(len(user_records)):
        user = user_records[i]
        if user.get("is_active") == True:
            if "score" in user and user["score"] is not None:
                score = user["score"]
                total_score = total_score + score
                count = count + 1
                formatted = {
                    "id": user["id"],
                    "username": user["username"].lower().strip(),
                    "score": score,
                    "tier": "High" if score >= 80 else ("Medium" if score >= 50 else "Low")
                }
                results.append(formatted)
                
    avg = total_score / count if count > 0 else 0.0
    return {"users": results, "average_score": avg}


# ==========================================
# 2. Modern, Idiomatic (Pythonic 3.11+) Code
# ==========================================
def process_active_users_idiomatic(user_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Filter and format active user records using idiomatic list comprehensions,
    dictionary unpacking, and robust statistical calculations.
    """
    def categorize_tier(score: float) -> str:
        match score:
            case s if s >= 80:
                return "High"
            case s if s >= 50:
                return "Medium"
            case _:
                return "Low"

    active_users = [
        {
            "id": u["id"],
            "username": u["username"].strip().lower(),
            "score": u["score"],
            "tier": categorize_tier(u["score"])
        }
        for u in user_records
        if u.get("is_active") and u.get("score") is not None
    ]

    avg_score = (
        sum(u["score"] for u in active_users) / len(active_users)
        if active_users else 0.0
    )

    return {
        "users": active_users,
        "average_score": round(avg_score, 2)
    }
