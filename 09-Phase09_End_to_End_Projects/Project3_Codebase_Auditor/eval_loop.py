import asyncio
from pydantic import BaseModel, ValidationError
from trace_logger import TraceLogger

class AuditResult(BaseModel):
    is_safe: bool
    vulnerability_description: str | None
    recommended_fix: str | None

def mock_verdict(code_snippet: str) -> tuple[bool, str | None, str | None]:
    """Decides the audit result from the code itself, so safe and unsafe files differ.

    A real auditor would call the LLM here; the demo uses a cheap heuristic
    (an f-string interpolated straight into a SQL query) so the verdict actually
    depends on the input instead of being hardcoded.
    """
    looks_like_sql_injection = "SELECT" in code_snippet and ("f'" in code_snippet or 'f"' in code_snippet)
    if looks_like_sql_injection:
        return False, "Found SQL injection", "Use parameterized queries"
    return True, None, None


async def mock_llm_call(prompt: str, code_snippet: str, attempt: int) -> str:
    """Mocks an LLM that fails on the first try but succeeds on repair."""
    await asyncio.sleep(0.5)
    is_safe, vuln, fix = mock_verdict(code_snippet)
    if attempt == 1:
        # Intentional schema error (missing quotes) — triggers the repair loop
        return f"{{is_safe: {str(is_safe).lower()}, vulnerability_description: '{vuln}', recommended_fix: '{fix}'}}"
    # Repaired output (valid JSON)
    return AuditResult(is_safe=is_safe, vulnerability_description=vuln, recommended_fix=fix).model_dump_json()

async def run_audit_loop(code_snippet: str, logger: TraceLogger, max_retries: int = 2) -> AuditResult:
    """A custom agent loop with a built-in repair mechanism."""
    
    prompt = f"Audit this code for security issues:\n{code_snippet}"
    logger.log("input", {"code_length": len(code_snippet)})
    
    for attempt in range(1, max_retries + 2):
        logger.log("think", {"attempt": attempt, "prompt": prompt[:50] + "..."})
        
        raw_output = await mock_llm_call(prompt, code_snippet, attempt)
        logger.log("raw_output", {"content": raw_output})
        
        try:
            parsed = AuditResult.model_validate_json(raw_output)
            logger.log("success", {"is_safe": parsed.is_safe})
            return parsed
            
        except ValidationError as e:
            logger.log("validation_error", {"error": str(e)})
            
            if attempt > max_retries:
                logger.log("fatal_error", {"msg": "Max retries exceeded"})
                raise
                
            # The Repair Prompt (Dialectic pattern)
            print(f"⚠️ Validation error. Injecting repair prompt (Attempt {attempt+1})...")
            prompt = f"Your previous output failed validation: {e}\nRaw output: {raw_output}\nFix the JSON format."
