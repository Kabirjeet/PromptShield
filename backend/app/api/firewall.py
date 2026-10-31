
from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.core.detection.signature_engine import analyze_prompt
from app.core.policy_engine import apply_policy
from app.schemas.firewall_schema import (
    AnalyzePromptRequest,
    AnalyzePromptResponse,
)
from app.services.log_service import record_audit_event

router = APIRouter(prefix="/firewall", tags=["Firewall"])


@router.get("/ping")
async def ping():
    return {"message": "Firewall Module Ready"}


@router.get("/protected")
async def protected_route(
    current_user: dict = Depends(get_current_user),
):
    return {
        "message": "You have accessed a protected endpoint",
        "user": current_user,
    }


@router.post("/analyze", response_model=AnalyzePromptResponse)
async def analyze_prompt_endpoint(
    request: AnalyzePromptRequest,
    current_user: dict = Depends(get_current_user),
):
    """Analyze a prompt, apply policy, and record an audit event."""
    analysis = analyze_prompt(request.prompt)
    result = apply_policy(analysis)

    user_id = current_user.get("sub") or current_user.get("id")
    if user_id is not None:
        await record_audit_event(result, str(user_id))

    return result
