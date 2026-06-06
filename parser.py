"""
Parser module for Surge rule-set files.

This module handles parsing of Surge proxy configuration rules and
extracts domain information from various rule types.
"""

import re
from typing import List, Tuple, Dict


class SurgeRuleParser:
    """Parse Surge rule-set files and extract domain rules."""

    # Regular expression patterns for different rule types
    DOMAIN_PATTERN = re.compile(r'^DOMAIN,(.+)$')
    DOMAIN_SUFFIX_PATTERN = re.compile(r'^DOMAIN-SUFFIX,(.+)$')
    DOMAIN_KEYWORD_PATTERN = re.compile(r'^DOMAIN-KEYWORD,(.+)$')

    def __init__(self):
        """Initialize the parser with pattern definitions."""
        self.rules_read = 0
        self.domain_rules = []

    def parse_file(self, filepath: str) -> List[Tuple[str, str, str]]:
        """
        Parse a Surge rule-set file and extract domain rules.

        Args:
            filepath: Path to the Surge rule-set file

        Returns:
            List of tuples: (domain, rule_type, original_line)
                - domain: extracted domain name
                - rule_type: 'DOMAIN', 'DOMAIN-SUFFIX', or 'DOMAIN-KEYWORD'
                - original_line: the original rule line for reference
        """
        rules = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()

                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue

                    # Track total rules read
                    self.rules_read += 1

                    # Try to match DOMAIN rule (exact match)
                    match = self.DOMAIN_PATTERN.match(line)
                    if match:
                        domain = match.group(1).strip()
                        if self._is_valid_domain(domain):
                            rules.append((domain, 'DOMAIN', line))
                        continue

                    # Try to match DOMAIN-SUFFIX rule (domain suffix match)
                    match = self.DOMAIN_SUFFIX_PATTERN.match(line)
                    if match:
                        domain = match.group(1).strip()
                        if self._is_valid_domain(domain):
                            rules.append((domain, 'DOMAIN-SUFFIX', line))
                        continue

                    # Try to match DOMAIN-KEYWORD rule (keyword match in domain)
                    match = self.DOMAIN_KEYWORD_PATTERN.match(line)
                    if match:
                        keyword = match.group(1).strip()
                        if self._is_valid_domain(keyword):
                            rules.append((keyword, 'DOMAIN-KEYWORD', line))
                        continue

        except FileNotFoundError:
            print(f"Error: File not found - {filepath}")
            raise
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
            raise

        self.domain_rules = rules
        return rules

    @staticmethod
    def _is_valid_domain(domain: str) -> bool:
        """
        Validate if a string is a valid domain name.

        Args:
            domain: String to validate

        Returns:
            True if the string appears to be a valid domain, False otherwise
        """
        if not domain or len(domain) == 0:
            return False

        if len(domain) > 255:
            return False

        # Domain should not contain spaces or other invalid characters
        invalid_chars = [' ', '\t', '\n', '\r']
        for char in invalid_chars:
            if char in domain:
                return False

        # At least one dot for most cases (except keywords)
        # Allow keyword-only patterns for DOMAIN-KEYWORD rules
        if domain.count('.') > 0:
            return True

        # Single words allowed for DOMAIN-KEYWORD rules
        if re.match(r'^[a-zA-Z0-9-]+$', domain):
            return True

        return False

    def normalize_domain(self, domain: str) -> str:
        """
        Normalize a domain name to lowercase and remove leading dots.

        Args:
            domain: Domain name to normalize

        Returns:
            Normalized domain name
        """
        domain = domain.lower().strip()

        # Remove leading dots (from DOMAIN-SUFFIX entries)
        while domain.startswith('.'):
            domain = domain[1:]

        return domain

    def get_statistics(self) -> Dict[str, int]:
        """
        Get parsing statistics.

        Returns:
            Dictionary with parsing statistics
        """
        return {
            'total_rules_read': self.rules_read,
            'domain_rules_extracted': len(self.domain_rules)
        }


def main():
    """Test the parser with the release/direct.txt file."""
    parser = SurgeRuleParser()

    try:
        rules = parser.parse_file('release/direct.txt')
        stats = parser.get_statistics()

        print("Parser Test Results:")
        print(f"Total rules read: {stats['total_rules_read']}")
        print(f"Domain rules extracted: {stats['domain_rules_extracted']}")
        print("\nFirst 10 rules:")
        for i, (domain, rule_type, line) in enumerate(rules[:10], 1):
            print(f"{i}. [{rule_type}] {domain}")

    except Exception as e:
        print(f"Parser error: {e}")


if __name__ == '__main__':
    main()
