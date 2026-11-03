---
name: firecrawl
description: Firecrawl CLI：整站 URL 清单（`map`）、整站抓取（`crawl`）、关键词搜索带正文（`search`）、需要点击 / 登录才拿得到内容的页面（`interact`）。触发词："爬整站"、"整站抓"、"列出这站所有页面"、"搜一下带正文"、"抓这个文档站"、"要登录才能看的页面"。不用于：英文站单页（WebFetch 够用）、微信 / 小红书 / X / B 站 / YouTube（归 analyzer，云端抓这些站会吃风控页）、本地文件 / git / 部署 / 改代码。
allowed-tools:
  - Bash(firecrawl *)
  - Bash(npx firecrawl-cli *)
---

# Firecrawl CLI

Search, scrape, and interact with the web. Returns clean markdown optimized for LLM context windows. Every call costs credits.

Run `firecrawl --help` or `firecrawl <command> --help` for full option details.

<!-- 本机只保留这一个 firecrawl skill：官方装的子 skill（search/scrape/crawl/map/interact/monitor/
     build-*/workflows 等）已删，原因是 description 常驻上下文且与本机 analyzer / deep-research 抢活。
     各子命令要点已并进本文件；本文件不引用任何 firecrawl-* 子 skill。 -->

## Prerequisites

Check with `firecrawl --status` (version, auth state, concurrency limit, remaining credits).

- `crawl`, `map`, `x download`, `agent`, `monitor`, `credit-usage` and the feedback commands need an account; without credentials they prompt an interactive login. `search`, `scrape`, `interact` also work keyless (rate-limited).
- **Auth and credit errors are terminal.** On `Unauthorized: Invalid token` or insufficient credits, check `firecrawl --status` once, report the blocking reason, and stop. Retrying yields the same error.
- Install / login problems → [rules/install.md](rules/install.md). Output handling → [rules/security.md](rules/security.md).
- **Never run `firecrawl init`, `firecrawl setup`, `firecrawl make`, or `firecrawl launch`** — they reinstall the deleted sub-skills or rewrite agent/MCP defaults on this machine. Login is `firecrawl login --browser`.

## Workflow

Follow this escalation pattern:

1. **Search** - No specific URL yet. Find pages, answer questions, discover sources.
2. **Scrape** - Have a URL. Extract its content directly.
3. **Map + Scrape** - Large site or need a specific subpage. Use `map --search` to find the right URL, then scrape it.
4. **Crawl** - Need bulk content from an entire site section (e.g., all /docs/).
5. **Monitor** - Need recurring checks or ongoing alerts. Prefer setting a monitor with `--page` plus `--goal` instead of doing repeated one-off scrapes.
6. **Interact** - Scrape first, then interact with the page (pagination, modals, form submissions, multi-step navigation, login).

| Need                        | Command               | When                                                            |
| --------------------------- | --------------------- | --------------------------------------------------------------- |
| Find pages on a topic       | `search`              | No specific URL yet                                             |
| Get a page's content        | `scrape`              | Have a URL, page is static or JS-rendered                       |
| Scrape a list of known URLs | `batch-scrape`        | Many URLs, non-markdown formats, JSON extraction, or a webhook   |
| Find URLs within a site     | `map`                 | Need to locate a specific subpage                               |
| Bulk extract a site section | `crawl`               | Need many pages (e.g., all /docs/)                              |
| AI-powered data extraction  | `agent`               | Need structured data from complex sites                         |
| Interact with a page        | `scrape` + `interact` | Content requires clicks, form fills, pagination, or login       |
| Download a site to files    | `x download`          | Save an entire site as local files                              |
| Watch pages for changes     | `monitor`             | Schedule recurring scrapes/crawls/searches, diff against snapshots |

Also available, rarely needed here: `developer` (index of GitHub issues, merged PRs, READMEs, docs), `research` (paper index), `gov` (US law and regulation), `parse` (local file — usually not this skill's job).

**Done when:** the narrowest suitable command has completed the request, its output was inspected, and the answer cites the saved source files.

**Avoid redundant fetches:**

- `search --scrape` already fetches full page content. Don't re-scrape those URLs.
- Check `.firecrawl/` for existing data before fetching again.
- A client-side context/output error does not mean the job failed. Keep the job ID and inspect the saved output before repeating a paid request.

## search

```bash
firecrawl search "your query" -o .firecrawl/search-q.json --json
firecrawl search "your query" --scrape -o .firecrawl/search-q-scraped.json --json   # with full page content
firecrawl search "your query" --sources news --tbs qdr:d -o .firecrawl/news.json --json   # news, past day
```

- Search with the user's actual question; don't rewrite it into an artificial keyword string.
- Results are query-relevant highlights by default; `--no-highlights` returns the original snippets.
- With an API key, results also include matched data tools (`data.tools`, "Alexandria"). A tool match is not data — ignore it unless the task needs structured records the web results lack; then inspect it with `firecrawl list <provider> <capability> --pretty` before running `firecrawl scrape <provider>/<capability> --options '<JSON>'`. Don't browse the whole catalogue or pay for adjacent tools to probe coverage. `--no-domain-tools` turns off domain-matched tools.
- Zero-result searches write no output file — check the file exists and has results before using it.

## scrape / batch-scrape

```bash
firecrawl scrape "<url>" --only-main-content -o .firecrawl/page.md
firecrawl scrape "<url-1>" "<url-2>" "<url-3>"            # a few pages, markdown only, saved to .firecrawl/
firecrawl batch-scrape --urls-file urls.txt --format markdown,links --wait -o .firecrawl/batch.json
firecrawl batch-scrape --urls-file urls.txt --wait \
  --schema '{"type":"object","properties":{"title":{"type":"string"}}}' -o .firecrawl/batch.json
```

- Multi-URL `scrape` saves markdown only and ignores `-o`; use `batch-scrape` for other formats, JSON extraction (`--schema` / `--prompt`), a webhook, or a job you check later (`batch-scrape <job-id>`).
- `batch-scrape` results are in `.data[]`, one document per URL with `metadata.sourceURL`. `--ignore-invalid-urls` skips bad entries; `--cancel <job-id>` stops a job.

## map

```bash
firecrawl map "<url>" --search "authentication" -o .firecrawl/filtered.txt   # find one page on a big site
firecrawl map "<url>" --limit 500 --json -o .firecrawl/urls.json              # all URLs
```

Map + scrape is the common pattern: `map --search` finds the right URL, then `scrape` it. Done when the URL list is saved and you've chosen what to scrape or crawl next.

## crawl

```bash
firecrawl crawl "<url>" --include-paths /docs --limit 50 --wait --timeout 600 -o .firecrawl/crawl.json
firecrawl crawl "<url>" --max-depth 3 --wait --progress --timeout 600 -o .firecrawl/crawl.json
firecrawl crawl <job-id>                                                         # status of a running crawl
```

- **Scope with `--include-paths`** whenever the request names a section; crawl only the pages you need.
- `--wait` has **no default timeout** — always pair it with `--timeout <seconds>`. Without `--wait`, crawl returns a job ID to poll.
- Crawl costs credits per page. Check `firecrawl credit-usage` before large crawls.

## interact

```bash
firecrawl scrape "<url>"                                   # 1. scrape first; scrape ID is saved automatically
firecrawl interact "Click the login button"                # 2. natural-language action on the last scrape
firecrawl interact "<scrape-id>" "Extract the pricing table"
firecrawl interact --code "agent-browser snapshot -i" --bash   # precise control
firecrawl interact stop                                    # 3. always stop the session when done
```

- Use `scrape` first; it already handles JS-rendered SPAs. Escalate to `interact` only for clicks, forms, infinite scroll, login, or when scrape misses content. Never use interact for web searches.
- Saved sessions expire after about 10 minutes; re-scrape if the CLI warns the session is stale.
- Persist login state across scrapes with a profile: `firecrawl scrape "<url>" --profile my-app`, then `interact`. Reconnect read-only with `--no-save-changes`.
- For parallel work, scrape several pages and interact with each via `--scrape-id`.

## monitor

Schedule recurring scrapes, crawls, or searches and diff each result against the last retained snapshot. Bias toward `monitor` when the goal is ongoing change detection, alerting, or repeated checks over time. Each check labels pages `same`, `new`, `changed`, `removed`, or `error`, with webhook and email notification options.

| Mode        | Flags                          | Watches                                                |
| ----------- | ------------------------------ | ------------------------------------------------------ |
| Single page | `--page <url>`                 | one URL, for changes                                   |
| URL batch   | `--scrape-urls <url,url,...>`  | several URLs, for changes                              |
| Whole site  | `--crawl-url <root-url>`       | every page a crawl discovers, for changes              |
| Web search  | `--queries <q,...>` + `--goal` | the whole web, for **new** results matching the goal   |

When writing `--goal`, convert the user's monitoring intent into a concise 2-3 sentence monitor goal:

- Start with `Alert when ...` and state what should trigger an alert using the user's stated intent.
- Restate scope the user mentioned, such as top N, price, role type, company, region, topic, status, or a specific entity.
- Include an `Ignore ...` sentence only for intent-specific exclusions that are obvious from the request, such as points/comments for rankings, unrelated marketing copy for pricing, or general company-page updates for jobs.
- Do not repeat generic noise exclusions in every goal; the judge already handles whitespace, casing, punctuation, encoding, formatting-only changes, request/session IDs, cache busters, tracking params, generic metadata noise, and unrelated page chrome.
- Do not invent page-specific sections, entities, thresholds, exclusions, or business rules unless the user mentioned them.
- If the user is vague, keep the goal broad rather than guessing exclusions.
- If the user asks for "any change", preserve that and do not add exclusions.
- If the user mentions noise they do not care about, include that explicitly.

Good goal examples:

- User intent: `top 10 hackernews stories`
  Goal: `Alert when stories enter, leave, or change rank within the Hacker News top 10. Ignore points, comments, and timestamps. Do not alert on changes outside the top 10.`
- User intent: `pricing changes`
  Goal: `Alert when pricing information changes, including prices, plan names, billing periods, tiers, limits, or included features. Ignore unrelated marketing copy, testimonials, and regional currency display changes unless the underlying offer changes.`
- User intent: `new engineering roles`
  Goal: `Alert when a new engineering role is posted. Ignore general company-page updates unless they add, remove, or change an engineering role.`
- User intent: `track this page`
  Goal: `Alert when substantive visible content on this page changes.`
- User intent: `any change`
  Goal: `Alert when any visible page content changes, including copy, numbers, timestamps, counters, links, and layout text.`

```bash
# single page, email alert
firecrawl monitor create --name "Blog" --schedule "every 30 minutes" \
  --goal "Alert when a new blog post is published." \
  --page https://example.com/blog --email alerts@example.com

# multiple pages
firecrawl monitor create --name "Product pages" --schedule "every 30 minutes" \
  --goal "Alert when pricing, docs, or changelog content changes." \
  --scrape-urls https://example.com/pricing,https://example.com/docs,https://example.com/changelog

# web search: alert on NEW results anywhere on the web (--goal required)
firecrawl monitor create --name "Competitor launches" --schedule "daily at 9:00" \
  --queries "competitor product launch,competitor funding round" \
  --goal "Alert when a competitor announces a new product or raises funding." \
  --search-window 7d --max-results 20 --email alerts@example.com

# webhook notifications
firecrawl monitor create --name "Docs webhook" --schedule "every 30 minutes" \
  --goal "Alert when docs content changes." \
  --page https://example.com/docs \
  --webhook-url https://example.com/hook \
  --webhook-events monitor.page,monitor.check.completed

# or from JSON (positional file, or piped stdin)
firecrawl monitor create monitor.json

firecrawl monitor list --limit 20
firecrawl monitor run <monitorId>             # trigger a check now (smoke test right after create)
firecrawl monitor checks <monitorId>          # list checks
firecrawl monitor check <monitorId> <checkId> --page-status changed
firecrawl monitor update <monitorId> --state paused
firecrawl monitor delete <monitorId>
```

Subcommands: `create | list | get | update | delete | run | checks | check`. **Done when** `create` returns a monitor ID and a `run` + `check` confirms the target, state, and notification config.

- Schedules accept cron (`--cron "*/30 * * * *"`) or natural language (`--schedule "every 30 minutes"`, `--timezone` defaults to UTC). Minimum interval is 5 minutes. Not available for zero-data-retention teams.
- Each check costs credits for its scrape / crawl / search plus judging. Prefer one monitor over repeated one-off scrapes of the same URL.
- `--state` (not `--status`) pauses / resumes; `--page-status` (not `--status`) filters `check` results — `--status` is the global CLI flag. Pause with `update --state paused`; reserve `delete` for monitors that are permanently done.
- `--retention-days` controls how long snapshots are kept; lower it for high-frequency monitors.
- External email recipients must confirm an opt-in email before they get alerts; team addresses are auto-confirmed.
- **On HTTP 429, back off once** (~30s, one retry). If it persists, stop, report the rate limit, and delete any monitors created for this task. Never retry in a loop.
- Monitor scrapes default `maxAge` to `0` (always fresh) unless `scrapeOptions.maxAge` is set in a JSON payload.

**JSON-mode change tracking:** By default monitors diff each page's markdown and you get a unified text diff back. When you care about **specific structured fields** (price, headline, in-stock flag, items in a list) instead of the whole page, add a `changeTracking` format with `modes: ["json"]` and a JSON schema to the target's `scrapeOptions.formats`. The flag-based form doesn't cover this — pass a JSON body via file or stdin:

```bash
cat > pricing-monitor.json <<'EOF'
{
  "name": "Pricing watch",
  "goal": "Alert when plan prices or headline features change",
  "schedule": { "text": "hourly", "timezone": "UTC" },
  "targets": [{
    "type": "scrape",
    "urls": ["https://example.com/pricing"],
    "scrapeOptions": {
      "formats": [{
        "type": "changeTracking",
        "modes": ["json"],
        "prompt": "Extract pricing tiers and headline features for each plan.",
        "schema": {
          "type": "object",
          "properties": {
            "plans": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "name":     { "type": "string" },
                  "price":    { "type": "string" },
                  "features": { "type": "array", "items": { "type": "string" } }
                }
              }
            }
          }
        }
      }]
    }
  }]
}
EOF
firecrawl monitor create pricing-monitor.json
```

The `check` response then carries a per-field diff (paths like `plans[0].price`) and the full extraction at this run. Each changed page in `pages[]` looks like:

```json
{
  "url": "https://example.com/pricing",
  "status": "changed",
  "diff": {
    "json": {
      "plans[0].price": { "previous": "$19/mo", "current": "$24/mo" }
    }
  },
  "snapshot": { "json": { "plans": [ /* current full extraction */ ] } }
}
```

Use `modes: ["json", "git-diff"]` for **mixed mode**: you get both `diff.json` (per-field) and `diff.text` (markdown sidecar), and the page is marked `changed` whenever either surface changed. For markdown-only monitors, `diff.text` holds the unified diff and `diff.json` is a `parse-diff` AST (`{ files: [...] }`); there is no `snapshot`.

## 中文平台

- **抓中文平台链接** -> 不用本 skill，走 `analyzer` skill / sf-reader-all（云端 IP 抓 mp.weixin 会吃风控页）

## Output & Organization

Unless the user specifies to return in context, write results to `.firecrawl/` with `-o`. Add `.firecrawl/` to `.gitignore`. Always quote URLs - shell interprets `?` and `&` as special characters.

Naming conventions:

```
.firecrawl/search-{query}.json
.firecrawl/search-{query}-scraped.json
.firecrawl/{site}-{path}.md
```

Never read entire output files at once. Use `grep`, `head`, or incremental reads:

```bash
wc -l .firecrawl/file.md && head -50 .firecrawl/file.md
grep -n "keyword" .firecrawl/file.md
```

Single format outputs raw content. Multiple formats (e.g., `--format markdown,links`) output JSON. Use `jq` on JSON output:

```bash
# URLs with source and 1-indexed position (needed for search feedback)
jq -r '.data | to_entries[] | select(.key as $k | ["web","images","news"] | index($k)) | .key as $s | .value | to_entries[] | "\($s):\(.key + 1)\t\(.value.url // "-")"' .firecrawl/search.json

# titles and URLs
jq -r '.data.web[] | "\(.title): \(.url)"' .firecrawl/search.json
```

## After search: send feedback (refunds 1 credit)

Search costs 2 credits. After you've used the results (or decided they were useless), send feedback **once per search, in the background**. The first feedback per search id refunds 1 credit.

- **Time window:** within ~2 minutes of the search; late feedback is rejected.
- **`--valuable-results`**: every result you actually used, as `source:position` (`web:1`, `news:2` — each group is numbered from 1 independently). Be exhaustive; unlisted results count as not useful. Use `--valuable-sources` only for useful URLs that were NOT in the returned results.
- **`--missing-content`** (most important): specific pieces of content you expected but didn't find, one topic per entry.
- Zero-effort feedback is rejected: `good` needs `--valuable-results` or `--valuable-sources`; `partial` needs one of those or `--missing-content`; `bad` needs `--missing-content` or `--query-suggestions`.
- Daily refund cap is 100 credits per team per UTC day. When the response says `dailyCapReached: true`, stop sending search feedback for the rest of the day.

```bash
# Replace both placeholders with what actually happened; never send them as-is.
if SEARCH_ID=$(jq -er 'select(any(.data[]; length > 0)) | .id' .firecrawl/search-react-hooks.json); then
  firecrawl search-feedback "$SEARCH_ID" \
    --rating "<good|partial|bad>" \
    --valuable-results "<source:position,... - every result you actually used>" \
    --missing-content '[{"topic":"useDeferredValue","description":"No example of useDeferredValue with Suspense"}]' \
    --silent &
fi
```

**Opt out:** if `FIRECRAWL_NO_SEARCH_FEEDBACK=1` (or `FIRECRAWL_DISABLE_SEARCH_FEEDBACK=1`) is set, the CLI skips the call silently. Respect that — do not try to work around it.

## Endpoint job feedback

For non-search endpoint jobs, use `firecrawl feedback <endpoint> <jobId>`. Supported endpoints are `search`, `scrape`, `parse`, and `map`.

```bash
firecrawl feedback scrape "$SCRAPE_ID" \
  --rating partial \
  --issues missing_markdown \
  --tags docs \
  --note "The pricing table was missing from the markdown output." \
  --url "https://example.com/pricing" \
  --page-numbers 1 \
  --silent &
```

Keep generic feedback small: issue codes, tags, short notes, URLs, page numbers, and small metadata objects. Never send raw scrape/parse outputs or full page contents.

**Opt out:** `export FIRECRAWL_NO_ENDPOINT_FEEDBACK=1` makes the CLI skip every endpoint feedback call silently. Respect that flag — do not try to work around it.

## Parallelization

Run independent operations in parallel. Check `firecrawl --status` for concurrency limit:

```bash
firecrawl scrape "<url-1>" -o .firecrawl/1.md &
firecrawl scrape "<url-2>" -o .firecrawl/2.md &
firecrawl scrape "<url-3>" -o .firecrawl/3.md &
wait
```

## Credit Usage

```bash
firecrawl credit-usage
firecrawl credit-usage --json --pretty -o .firecrawl/credits.json
```

## Codex compatibility

Preserve this workflow's intent and evidence rules. Translate Claude-specific tool names to the available Codex tools.
