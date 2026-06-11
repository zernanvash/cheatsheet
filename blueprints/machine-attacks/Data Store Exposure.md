# Data Store Exposure

Use when Redis, Memcached, MongoDB, Elasticsearch, or other data stores are exposed.

## Signals

- Ports: Redis `6379`, Memcached `11211`, MongoDB `27017`, Elasticsearch `9200`.
- No authentication or default credentials.
- Data store contains sessions, users, password hashes, tokens, or writable paths.

## Main Path

Redis:

```bash
redis-cli -h target
INFO
KEYS *
GET key
```

Memcached:

```bash
nc target 11211
stats items
stats cachedump SLAB 0
get key
```

Elasticsearch:

```bash
curl -s http://target:9200/_cat/indices?v
curl -s http://target:9200/index/_search?pretty
```

## Options To Try

- Look for web sessions and impersonate only in lab scope.
- Crack password hashes, then test SSH/SMB/WinRM/web admin.
- If Redis can write files and path is known, consider SSH key or web-root write paths only in scoped labs.
- If DB exposes internal hostnames, add them to hosts and rescan.
- If credentials are app-only, use them to access admin panels or read source/config.

## Study Examples

- Common machine pattern: exposed data store -> credentials/session -> web admin or shell.
