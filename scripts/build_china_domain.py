from parser import parse_rules
from classifier import DomainClassifier
from exporter import export_rules

INPUT_FILE = 'release/direct.txt'
OUTPUT_FILE = 'release/china-domain.list'


def main():
    rules = parse_rules(INPUT_FILE)
    classifier = DomainClassifier()

    total_input_rules = len(rules)
    matched_china = 0
    excluded_international = 0
    duplicate_removed = 0

    seen = set()
    output_rules = []

    for rule in rules:
        key = (rule.rule_type, rule.value)

        if key in seen:
            duplicate_removed += 1
            continue

        seen.add(key)

        if classifier.is_international(rule.value):
            excluded_international += 1
            continue

        if classifier.is_china(rule):
            matched_china += 1
            output_rules.append(rule)

    export_rules(OUTPUT_FILE, output_rules)

    print('=' * 60)
    print('China Domain Generation Statistics')
    print('=' * 60)
    print(f'Total input rules:         {total_input_rules}')
    print(f'Matched China rules:       {matched_china}')
    print(f'Excluded international:    {excluded_international}')
    print(f'Duplicate rules removed:   {duplicate_removed}')
    print(f'Final output rules:        {len(output_rules)}')
    print('=' * 60)


if __name__ == '__main__':
    main()
