from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Rule:
    rule_type: str
    value: str

SUPPORTED_RULES = {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD"}

def normalize_domain(domain: str) -> str:
    return domain.strip().lower().lstrip('.')

def parse_rules(file_path: str) -> list[Rule]:
    rules = []
    for line in Path(file_path).read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = [x.strip() for x in line.split(',')]
        if len(parts) < 2:
            continue
        if parts[0] not in SUPPORTED_RULES:
            continue
        rules.append(Rule(parts[0], normalize_domain(parts[1])))
    return rules
