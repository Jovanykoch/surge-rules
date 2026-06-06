"""
Classifier module for identifying China-based domains.

This module classifies domains as China-based or international using multiple
strategies including known company databases, TLD analysis, and configurable rules.
"""

from typing import Set, Dict, List, Tuple


class ChinaDomainClassifier:
    """
    Classify domains as China-based or international.

    Uses multiple strategies:
    1. Known Chinese companies and services
    2. Chinese cloud providers (Alibaba, Tencent, Huawei, etc.)
    3. Chinese ISPs
    4. Government and education domains (.gov.cn, .edu.cn)
    5. Other Chinese-specific patterns
    """

    def __init__(self):
        """Initialize the classifier with known domains and patterns."""
        # Known Chinese companies and services
        self.chinese_companies = {
            'alibaba', 'aliyun', 'taobao', 'tmall', 'tencent', 'qq', 'wechat',
            'baidu', 'netease', '163', '126', 'sohu', 'sina', 'weibo', 'douban',
            'zhihu', 'bilibili', 'kuaishou', 'douyin', 'tiktok', 'bytedance',
            'meituan', 'didi', 'jd', 'jingdong', 'xunlei', 'sogou', 'iqiyi',
            'youku', 'tudou', 'letv', 'ifeng', 'phoenix', 'chinamobileltd',
            'china-mobile', 'chinatelecom', 'chinaunicom', 'cernet', 'chinanet',
            '139', '189', '155', '166', '198', 'cnnic', 'cnr', 'cri', 'xinhuanet',
            'people', 'china', 'ccn', 'eastday', 'ifeng', 'news', 'sina',
        }

        # Chinese cloud providers
        self.chinese_cloud_providers = {
            'aliyun', 'alibabacloud', 'qcloud', 'tencent', 'cloud', 'cos',
            'huawei', 'huaweicloud', 'ucloud', 'jdcloud', 'baiducloud', 'baidu',
            'apsaradb', 'oss', 'cdn', 'dcdn', 'scdn', 'waf',
        }

        # Chinese ISPs
        self.chinese_isps = {
            'chinamobile', 'china-mobile', 'cmcc', 'chinatelecom', 'telecom',
            'chinaunicom', 'cucc', 'unicom', 'cernet', 'cstnet', 'cnnic',
            'cnpppoe', '139', '189', '155', '166', '198', '188',
        }

        # Government and education domains
        self.chinese_gov_edu_domains = {
            '.gov.cn', '.edu.cn', '.ac.cn', '.org.cn', '.net.cn',
            '.pku.edu.cn', '.tsinghua.edu.cn', '.zju.edu.cn', '.fudan.edu.cn',
            '.sjtu.edu.cn', '.bjmu.edu.cn', '.whu.edu.cn', '.xjtu.edu.cn',
        }

        # Known international services to exclude
        self.international_blocklist = {
            # Apple
            'apple', 'icloud', 'itunes', 'appstore', 'mzstatic', 'aaplimg',
            # Microsoft
            'microsoft', 'windows', 'office', 'azure', 'outlook', 'onedrive',
            'edge', 'teams', 'skype', 'xbox',
            # Google
            'google', 'gmail', 'youtube', 'youtube-nocookie', 'youtubecdn',
            'googlevideo', 'googleusercontent', 'gstatic', 'googleapis',
            'googleadservices', 'googleanalytics', 'doubleclick',
            # Amazon & AWS
            'amazon', 'aws', 'amazonservices', 's3', 'cloudfront', 'amazonaws',
            # Cloudflare
            'cloudflare', 'cf', 'cdn77',
            # Akamai
            'akamai', 'akamaitech', 'akamaitechnologies',
            # Fastly
            'fastly', 'fastlycdn',
            # GitHub & Development
            'github', 'githubusercontent', 'ghcr', 'docker', 'dockerhub',
            'npm', 'npmjs', 'yarn', 'pypi', 'maven', 'nuget', 'crates',
            # OpenAI & AI
            'openai', 'anthropic', 'huggingface', 'groq',
            # Meta/Facebook
            'facebook', 'fb', 'meta', 'instagram', 'whatsapp', 'threads',
            # Media & Entertainment
            'netflix', 'spotify', 'hulu', 'disneyplus', 'primevideo',
            'twitch', 'youtube', 'vimeo', 'dailymotion',
            # Other major international services
            'linkedin', 'twitter', 'x', 'telegram', 'discord', 'slack',
            'dropbox', 'box', 'notion', 'figma', 'slack', 'adobe', 'autodesk',
            'zoomvideo', 'zoom', 'skype', 'ringcentral', 'vonage', 'twilio',
        }

        # Configurable allowlist - domains to include even if they don't match typical patterns
        self.allowlist = {
            'aliyun.com', 'qcloud.com', 'tencentcloud.com', 'jdcloud.com',
            'huaweicloud.com', 'baiducloud.com', 'oss-cn', 'cdn-cn',
            'ntp.aliyun.com', 'ntp.tencent.com', 'hospital.pku.edu.cn',
            'opencourse.pku.edu.cn', 'moocs.unipus.cn', 'study.163.com',
        }

        # Statistics
        self.total_classified = 0
        self.china_count = 0
        self.international_count = 0

    def classify_domain(self, domain: str) -> Tuple[bool, str]:
        """
        Classify a domain as China-based or international.

        Args:
            domain: Domain name to classify (should be normalized)

        Returns:
            Tuple of (is_china: bool, reason: str)
                - is_china: True if domain is China-based
                - reason: Classification reason for logging
        """
        self.total_classified += 1
        domain_lower = domain.lower()

        # Check allowlist first
        if self._check_allowlist(domain_lower):
            self.china_count += 1
            return True, "allowlist_match"

        # Check international blocklist
        if self._check_blocklist(domain_lower):
            self.international_count += 1
            return False, "international_blocklist"

        # Check .cn TLD with additional validation
        if domain_lower.endswith('.cn'):
            # Only classify as China if .cn AND matches other criteria
            # This prevents false positives
            if self._has_china_characteristics(domain_lower):
                self.china_count += 1
                return True, "cn_tld_with_characteristics"
            return False, "cn_tld_but_suspicious"

        # Check government and education domains
        if self._check_gov_edu_domain(domain_lower):
            self.china_count += 1
            return True, "gov_edu_domain"

        # Check known Chinese companies
        if self._check_company(domain_lower):
            self.china_count += 1
            return True, "chinese_company"

        # Check for Chinese cloud provider patterns
        if self._check_cloud_provider(domain_lower):
            self.china_count += 1
            return True, "chinese_cloud_provider"

        # Check for Chinese ISP patterns
        if self._check_isp(domain_lower):
            self.china_count += 1
            return True, "chinese_isp"

        # Check for mainland China server indicators
        if self._check_china_characteristics(domain_lower):
            self.china_count += 1
            return True, "china_characteristics"

        # Default to not classified as China
        self.international_count += 1
        return False, "unmatched_domain"

    def _check_allowlist(self, domain: str) -> bool:
        """
        Check if domain is in the allowlist.

        Args:
            domain: Domain to check

        Returns:
            True if domain or its parent is in allowlist
        """
        if domain in self.allowlist:
            return True

        # Check if any allowlist entry is a suffix of this domain
        for entry in self.allowlist:
            if domain.endswith(entry):
                return True

        return False

    def _check_blocklist(self, domain: str) -> bool:
        """
        Check if domain matches international services blocklist.

        Args:
            domain: Domain to check

        Returns:
            True if domain matches international blocklist
        """
        parts = domain.split('.')

        # Check each domain part
        for part in parts:
            if part in self.international_blocklist:
                return True

        # Check full domain
        if domain in self.international_blocklist:
            return True

        return False

    def _check_company(self, domain: str) -> bool:
        """
        Check if domain belongs to known Chinese company.

        Args:
            domain: Domain to check

        Returns:
            True if matches known Chinese company
        """
        parts = domain.split('.')

        for part in parts:
            if part in self.chinese_companies:
                return True

        return False

    def _check_cloud_provider(self, domain: str) -> bool:
        """
        Check if domain belongs to Chinese cloud provider.

        Args:
            domain: Domain to check

        Returns:
            True if matches Chinese cloud provider
        """
        parts = domain.split('.')

        for part in parts:
            if part in self.chinese_cloud_providers:
                return True

        return False

    def _check_isp(self, domain: str) -> bool:
        """
        Check if domain belongs to Chinese ISP.

        Args:
            domain: Domain to check

        Returns:
            True if matches Chinese ISP
        """
        parts = domain.split('.')

        for part in parts:
            if part in self.chinese_isps:
                return True

        return False

    def _check_gov_edu_domain(self, domain: str) -> bool:
        """
        Check if domain is government or education domain.

        Args:
            domain: Domain to check

        Returns:
            True if matches government or education pattern
        """
        for suffix in self.chinese_gov_edu_domains:
            if domain.endswith(suffix):
                return True

        return False

    def _has_china_characteristics(self, domain: str) -> bool:
        """
        Check for characteristics indicating a China-based domain.

        Args:
            domain: Domain to check

        Returns:
            True if domain has China characteristics
        """
        # Chinese company names or services
        if self._check_company(domain):
            return True

        # Chinese ISP indicators
        if self._check_isp(domain):
            return True

        # Cloud provider indicators
        if self._check_cloud_provider(domain):
            return True

        # Common Chinese domain patterns
        chinese_patterns = {
            'taobao', 'tmall', 'alipay', 'qq', 'wechat', 'weixin',
            'baidu', 'netease', 'sohu', 'sina', 'weibo', 'douban',
            'zhihu', 'bilibili', 'kuaishou', 'douyin', 'tiktok',
        }

        parts = domain.split('.')
        for part in parts:
            if part in chinese_patterns:
                return True

        return False

    def _check_china_characteristics(self, domain: str) -> bool:
        """
        Check for general China characteristics.

        Args:
            domain: Domain to check

        Returns:
            True if domain has China characteristics
        """
        return self._has_china_characteristics(domain)

    def get_statistics(self) -> Dict[str, int]:
        """
        Get classification statistics.

        Returns:
            Dictionary with classification statistics
        """
        return {
            'total_classified': self.total_classified,
            'china_domains': self.china_count,
            'international_domains': self.international_count,
        }

    def set_allowlist(self, domains: Set[str]):
        """
        Set custom allowlist for China domains.

        Args:
            domains: Set of domains to add to allowlist
        """
        self.allowlist.update(domains)

    def set_blocklist(self, domains: Set[str]):
        """
        Set custom blocklist for international domains.

        Args:
            domains: Set of domains to add to blocklist
        """
        self.international_blocklist.update(domains)


def main():
    """Test the classifier with sample domains."""
    classifier = ChinaDomainClassifier()

    test_domains = [
        'aliyun.com',
        'qcloud.com',
        'google.com',
        'apple.com',
        'taobao.com',
        'baidu.com',
        'aws.amazon.com',
        'pku.edu.cn',
        'github.com',
        'tencent.com',
        'microsoft.com',
        'cloudflare.com',
        'ntp.aliyun.com',
        'netflix.com',
    ]

    print("Classifier Test Results:")
    print("-" * 60)

    for domain in test_domains:
        is_china, reason = classifier.classify_domain(domain)
        classification = "CHINA" if is_china else "INTERNATIONAL"
        print(f"{domain:30} -> {classification:15} ({reason})")

    print("-" * 60)
    stats = classifier.get_statistics()
    print(f"Total classified: {stats['total_classified']}")
    print(f"China domains: {stats['china_domains']}")
    print(f"International domains: {stats['international_domains']}")


if __name__ == '__main__':
    main()
