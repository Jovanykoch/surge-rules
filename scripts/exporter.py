from pathlib import Path
from parser import Rule

def export_rules(output_path: str, rules: list[Rule]) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(f'{r.rule_type},{r.value}' for r in rules) + '\n', encoding='utf-8')
