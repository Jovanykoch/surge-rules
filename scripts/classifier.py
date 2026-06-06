from parser import Rule

CHINESE_COMPANY_KEYWORDS = {'baidu','qq','tencent','wechat','weixin','alibaba','aliyun','taobao','tmall','1688','alipay','antgroup','jd','jingdong','bytedance','douyin','toutiao','xiaohongshu','bilibili','youku','iqiyi','ctrip','meituan','dianping','pinduoduo','kuaishou','xiaomi','miui','huawei','oppo','vivo','netease','163','126','sina','weibo','sohu','zhihu'}
CHINESE_CLOUD_KEYWORDS = {'aliyuncs','alicloud','myqcloud','qcloud','tencentcloud','volcengine','hwcloud','huaweicloud','ucloud','ksyun','jcloud','baidubce'}
CHINESE_ISP_KEYWORDS = {'chinaunicom','10010','chinatelecom','189','chinamobile','10086'}
ALLOWLIST = {'12306.cn','people.com.cn','xinhuanet.com','cctv.com','china.com.cn'}
BLOCKLIST = {'apple.com','icloud.com','microsoft.com','office.com','live.com','google.com','gstatic.com','youtube.com','amazon.com','amazonaws.com','cloudflare.com','akamai.com','fastly.com','github.com','githubusercontent.com','openai.com','chatgpt.com','facebook.com','instagram.com','meta.com','netflix.com','spotify.com'}

class DomainClassifier:
    def is_international(self, domain: str) -> bool:
        return any(domain == d or domain.endswith('.'+d) for d in BLOCKLIST)

    def is_china(self, rule: Rule) -> bool:
        domain = rule.value
        if self.is_international(domain):
            return False
        if any(domain == d or domain.endswith('.'+d) for d in ALLOWLIST):
            return True
        if domain.endswith('.gov.cn') or domain == 'gov.cn':
            return True
        if domain.endswith('.edu.cn') or domain == 'edu.cn':
            return True
        for group in (CHINESE_COMPANY_KEYWORDS, CHINESE_CLOUD_KEYWORDS, CHINESE_ISP_KEYWORDS):
            if any(k in domain for k in group):
                return True
        return False
