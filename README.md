# Introduction ![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/Loyalsoldier/surge-rules/total?logo=github) [![jsdelivr stats](https://data.jsdelivr.com/v1/package/gh/Loyalsoldier/surge-rules/stats/6m?dynamic=json)](https://www.jsdelivr.com/package/gh/Loyalsoldier/surge-rules)

This project generates rule sets (DOMAIN-SET and RULE-SET) for use with [**Surge**](https://nssurge.com). GitHub Actions are used to automatically build the rules daily at 6:30 am Beijing time to ensure accurate and timely data.

## Description

The data for the rule sets (DOMAIN-SET and RULE-SET) in this project is primarily sourced from the following projects: [@Loyalsoldier/v2ray-rules-dat](https://github.com/Loyalsoldier/v2ray-rules-dat), [@v2fly/domain-list-community](https://github.com/v2fly/domain-list-community), and [@felixonmars/dnsmasq-china-list](https://github.com/felixonmars/dnsmasq-china-list). The data is processed and compiled automatically to generate the rule sets.

## Rule File Links and Usage

### Online Links (URLs)

> If you are unable to access the domain `raw.githubusercontent.com`, you can use the alternate domain (`cdn.jsdelivr.net`). However, content updates may be delayed by approximately 12 hours.

#### DOMAIN-SET:

- **Direct Connection Domain List direct.txt**:
  - [https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/direct.txt](https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/direct.txt)
  - [https://cdn.jsdelivr.net/gh/Loyalsoldier/surge-rules@release/direct.txt](https://cdn.jsdelivr.net/gh/Loyalsoldier/surge-rules@release/direct.txt)
- **Proxy Domain List proxy.txt**:
  - [https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/proxy.txt](https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/proxy.txt)
  - [https://cdn.jsdelivr.net/gh/Loyalsoldier/surge-rules@release/proxy.txt](https://cdn.jsdelivr.net/gh/Loyalsoldier/surge-rules@release/proxy.txt)
- **CN Domain List cn.txt**:
  - [https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/cn.txt](https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/cn.txt)
  - [https://cdn.jsdelivr.net/gh/Loyalsoldier/surge-rules@release/cn.txt](https://cdn.jsdelivr.net/gh/Loyalsoldier/surge-rules@release/cn.txt)
- **GFWlist gfwlist.txt**:
  - [https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/gfwlist.txt](https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/gfwlist.txt)
  - [https://cdn.jsdelivr.net/gh/Loyalsoldier/surge-rules@release/gfwlist.txt](https://cdn.jsdelivr.net/gh/Loyalsoldier/surge-rules@release/gfwlist.txt)

#### RULE-SET:

- **Direct Connection Rules direct.list**:
  - [https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/direct.list](https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/direct.list)
  - [https://cdn.jsdelivr.net/gh/Loyalsoldier/surge-rules@release/direct.list](https://cdn.jsdelivr.net/gh/Loyalsoldier/surge-rules@release/direct.list)
- **Proxy Rules proxy.list**:
  - [https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/proxy.list](https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/proxy.list)
  - [https://cdn.jsdelivr.net/gh/Loyalsoldier/surge-rules@release/proxy.list](https://cdn.jsdelivr.net/gh/Loyalsoldier/surge-rules@release/proxy.list)

## Usage Guide

For detailed usage instructions of Surge, see the [official manual](https://manual.nssurge.com). To use the rule sets from this project, simply add the following rules into your Surge configuration file:

**Whitelist Mode (Proxy first, then direct):**

```ini
# Direct connection rules
RULE-SET,https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/direct.list,DIRECT
# Proxy rules
RULE-SET,https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/proxy.list,PROXY
# Default rule
FINAL,DIRECT
```

**Blacklist Mode (Direct first, then proxy):**

```ini
# Proxy rules
RULE-SET,https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/proxy.list,PROXY
# Direct connection rules
RULE-SET,https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/direct.list,DIRECT
# Default rule
FINAL,PROXY
```

## Acknowledgments

Thank you to the following projects for data and contributions:

- [@Loyalsoldier/geoip](https://github.com/Loyalsoldier/geoip)
- [@Loyalsoldier/v2ray-rules-dat](https://github.com/Loyalsoldier/v2ray-rules-dat)
- [@v2fly/domain-list-community](https://github.com/v2fly/domain-list-community)
- [@felixonmars/dnsmasq-china-list](https://github.com/felixonmars/dnsmasq-china-list)
- [@17mon/china_ip_list](https://github.com/17mon/china_ip_list)

## Project Star Growth Trend

[![Stargazers over time](https://starchart.cc/Loyalsoldier/surge-rules.svg)](https://starchart.cc/Loyalsoldier/surge-rules)

<!-- STATS:START -->
## 规则统计（自动生成）

### DOMAIN-SET

| 文件 | 条目数 |
| --- | ---: |
| \ | 44060 |
| \ | 163 |
| \ | 224 |
| \ | 5787 |
| \ | 26303 |
| \ | 113021 |
| \ | 33 |
| \ | 4252 |
| \ | 112 |
| \ | 10 |
| \ | 52 |
| \ | 26 |
| \ | 130 |
| \ | 26584 |
| \ | 170611 |
| \ | 12 |
| \ | 831 |

### RULE-SET

| 文件 | 条目数 |
| --- | ---: |
| \ | 44060 |
| \ | 163 |
| \ | 224 |
| \ | 5787 |
| \ | 26303 |
| \ | 113021 |
| \ | 33 |
| \ | 4252 |
| \ | 112 |
| \ | 10 |
| \ | 52 |
| \ | 26 |
| \ | 130 |
| \ | 26584 |
| \ | 170611 |
| \ | 12 |
| \ | 831 |
<!-- STATS:END -->
