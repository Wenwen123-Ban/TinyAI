"""Training data block loader for TinyAI v1.7."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class KnowledgeBlocks:
    constants: dict[str, float]
    number_map: dict[str, float]
    math_rules: list[str]


class DataBlockLoader:
    """Loads and updates text-based knowledge blocks from disk."""

    def __init__(self, training_dir: str | Path = "training_data") -> None:
        self.training_dir = Path(training_dir)
        self.constants_file = self.training_dir / "constants.txt"
        self.number_map_file = self.training_dir / "number_map.txt"
        self.math_rules_file = self.training_dir / "math_rules.txt"

    def load(self) -> KnowledgeBlocks:
        self.training_dir.mkdir(parents=True, exist_ok=True)
        constants = self._load_mapping_file(self.constants_file)
        number_map = self._load_mapping_file(self.number_map_file)
        math_rules = self._load_rules_file(self.math_rules_file)
        return KnowledgeBlocks(constants=constants, number_map=number_map, math_rules=math_rules)

    def update_block(self, block_name: str, text_blob: str) -> Path:
        target = {
            "constants": self.constants_file,
            "number_map": self.number_map_file,
            "math_rules": self.math_rules_file,
        }.get(block_name)
        if target is None:
            raise ValueError(f"Unknown block '{block_name}'.")

        target.parent.mkdir(parents=True, exist_ok=True)
        clean = text_blob.strip() + "\n"
        target.write_text(clean, encoding="utf-8")
        return target

    @staticmethod
    def _load_mapping_file(path: Path) -> dict[str, float]:
        if not path.exists():
            return {}

        mapping: dict[str, float] = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, sep, value = line.partition("=")
            if not sep:
                continue
            try:
                mapping[key.strip().lower()] = float(value.strip())
            except ValueError:
                continue
        return mapping

    @staticmethod
    def _load_rules_file(path: Path) -> list[str]:
        if not path.exists():
            return []
        return [
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
