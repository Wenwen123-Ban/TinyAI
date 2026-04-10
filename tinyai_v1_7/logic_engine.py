"""Logic engine for TinyAI v1.7."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from .data_loader import KnowledgeBlocks
from .tokenizer import Token, Tokenizer


@dataclass(slots=True)
class EvalResult:
    operation: str
    value: float | bool | None
    explanation: str


class LogicEngine:
    def __init__(self, blocks: KnowledgeBlocks) -> None:
        self.blocks = blocks
        self.tokenizer = Tokenizer()

    def solve(self, text: str) -> EvalResult:
        tokens = self.tokenizer.tokenize(text)
        resolved = self._resolve_entities(tokens)
        op = self._detect_primary_op(resolved)

        if op in {"add", "subtract", "multiply", "divide"}:
            nums = [tok.value for tok in resolved if tok.kind == "number" and tok.value is not None]
            if len(nums) < 2:
                return EvalResult(op, None, "Need at least two numeric values.")
            if op == "add":
                return EvalResult(op, sum(nums), "Computed sum from all detected values.")
            if op == "subtract":
                return EvalResult(op, nums[0] - nums[1], "Computed first value minus second value.")
            if op == "multiply":
                acc = 1.0
                for number in nums:
                    acc *= number
                return EvalResult(op, acc, "Computed product from all detected values.")
            if nums[1] == 0:
                return EvalResult(op, None, "Division by zero is undefined.")
            return EvalResult(op, nums[0] / nums[1], "Computed first value divided by second value.")

        if op == "comparison":
            return self._solve_comparison(resolved)

        nums = [tok.value for tok in resolved if tok.kind == "number" and tok.value is not None]
        if nums:
            return EvalResult("identity", nums[0], "No operation found; returning first number.")
        return EvalResult("unknown", None, "Could not detect a solvable expression.")

    def _resolve_entities(self, tokens: list[Token]) -> list[Token]:
        """Entity substitution at token-resolution time."""
        resolved: list[Token] = []
        for tok in tokens:
            if tok.kind == "word":
                constant = self.blocks.constants.get(tok.raw)
                mapped_num = self.blocks.number_map.get(tok.raw)
                if constant is not None:
                    resolved.append(Token(raw=tok.raw, kind="number", value=constant, metadata={"source": "constant"}))
                    continue
                if mapped_num is not None:
                    resolved.append(Token(raw=tok.raw, kind="number", value=mapped_num, metadata={"source": "number_map"}))
                    continue
            resolved.append(tok)
        return resolved

    def _detect_primary_op(self, tokens: list[Token]) -> str:
        raw_words = {tok.raw for tok in tokens}

        explicit = {tok.raw for tok in tokens if tok.kind == "operator"}
        if "+" in explicit:
            return "add"
        if "-" in explicit:
            return "subtract"
        if "*" in explicit:
            return "multiply"
        if "/" in explicit:
            return "divide"
        if explicit.intersection({">", "<", "="}):
            return "comparison"

        if raw_words.intersection({"sum", "add", "plus", "total"}):
            return "add"
        if raw_words.intersection({"difference", "minus", "subtract", "less"}):
            return "subtract"
        if raw_words.intersection({"product", "times", "multiply"}):
            return "multiply"
        if raw_words.intersection({"divide", "quotient", "over"}):
            return "divide"
        if raw_words.intersection({"greater", "less", "equal", "equals", "than"}):
            return "comparison"
        return "unknown"

    def _solve_comparison(self, tokens: list[Token]) -> EvalResult:
        nums = [tok.value for tok in tokens if tok.kind == "number" and tok.value is not None]
        words = [tok.raw for tok in tokens if tok.kind == "word"]
        if len(nums) < 2:
            return EvalResult("comparison", None, "Need at least two numbers for comparison.")

        left, right = nums[0], nums[1]
        if "greater" in words:
            decision = left > right
            verdict = left if decision else right
            return EvalResult("comparison", verdict, f"Compared {left} > {right} == {decision}.")
        if "less" in words:
            decision = left < right
            verdict = left if decision else right
            return EvalResult("comparison", verdict, f"Compared {left} < {right} == {decision}.")

        # equality fallback
        decision = left == right
        verdict = left if decision else None
        return EvalResult("comparison", verdict, f"Compared {left} == {right} == {decision}.")


def _fmt_number(value: float | bool | None) -> str:
    """Format values with commas and ~8 significant figures."""
    if value is None:
        return "N/A"
    if isinstance(value, bool):
        return str(value)
    if not isfinite(value):
        return str(value)

    rounded = float(f"{value:.8g}")
    return f"{rounded:,.8g}"


# public alias
fmt_number = _fmt_number
