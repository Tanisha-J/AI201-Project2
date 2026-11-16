# Capstone run log — after

2026-11-15 22:55, `python capstone_trials.py --label after`. 3 trials of the 24-request set defined in criteria.md. Raw logs: `results/capstone_logs/after_trial<N>.jsonl`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| C1. Every request leaves exactly one complete log record | 24 of 24 | 24/24 | 24/24 | 24/24 | MET |
| C2. Logged numbers match (±250 ms, 2 calls, tokens > 0) | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| C3. Dead key: < 5 s, says 'API key', logged model_unavailable | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| C4. Malformed requests get a 400, never a 500 | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| C5. Warm completed runs ≤ 10,000 ms | 9 of 10 | 10/10 | 9/10 | 9/10 | MET |

## Every scored request

**C1. Every request leaves exactly one complete log record — trial 1**

- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 3,942 ms · id `46359f02a12a` · 
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 3,156 ms · id `3ca4f7e73223` · 
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 5,202 ms · id `66ca18dd5b02` · 
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 7,072 ms · id `0cecc66aca2d` · 
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 2,008 ms · id `e2b73ebdd651` · 
- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 2,307 ms · id `c808ea44c073` · 
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 4,639 ms · id `f07c059c40eb` · 
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 2,153 ms · id `9aaa99f370f3` · 
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 2,732 ms · id `8a42b0f0f410` · 
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 4,479 ms · id `409f2af64782` · 
- PASS · impossible · `designer ballgown size XXS under $5` · HTTP 200 · curl 325 ms · id `02e9a4ed9874` · 
- PASS · impossible · `gold sequin gown size 2 under $3` · HTTP 200 · curl 296 ms · id `f403c240566c` · 
- PASS · no_item · `size W30` · HTTP 200 · curl 2 ms · id `ac667c8e640e` · 
- PASS · no_item · `under $30 size M` · HTTP 200 · curl 2 ms · id `146190ea1631` · 
- PASS · malformed · `no body` · HTTP 400 · curl 2 ms · id `4d52095d74b2` · 
- PASS · malformed · `{}` · HTTP 400 · curl 2 ms · id `848aa9004d82` · 
- PASS · malformed · `{"query": ""}` · HTTP 400 · curl 2 ms · id `6eb8a49929dd` · 
- PASS · malformed · `{"query": 42}` · HTTP 400 · curl 2 ms · id `a338dc4959e9` · 
- PASS · malformed · `["denim jacket"]` · HTTP 400 · curl 2 ms · id `6af1249990e4` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 906 ms · id `830f51609b8e` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 381 ms · id `a1013c5f434c` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 380 ms · id `de3dcca261e9` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 374 ms · id `91edb3c12e76` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 369 ms · id `f65b97b0605d` · 

**C1. Every request leaves exactly one complete log record — trial 2**

- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 2,956 ms · id `28b88e6af905` · 
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 2,006 ms · id `7ffaf6ccefaa` · 
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 3,846 ms · id `f9226809baef` · 
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 2,531 ms · id `773ae71ffa7f` · 
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 5,717 ms · id `82a40186ae82` · 
- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 3,196 ms · id `3990d9eb342d` · 
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 11,026 ms · id `960d718aaf67` · 
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 8,719 ms · id `b8814bfa3228` · 
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 4,261 ms · id `7a6c207dc8db` · 
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 3,204 ms · id `a9c9824ee1bd` · 
- PASS · impossible · `designer ballgown size XXS under $5` · HTTP 200 · curl 404 ms · id `393c6ba34b54` · 
- PASS · impossible · `gold sequin gown size 2 under $3` · HTTP 200 · curl 298 ms · id `7edd2768edf6` · 
- PASS · no_item · `size W30` · HTTP 200 · curl 2 ms · id `70bb3b501f46` · 
- PASS · no_item · `under $30 size M` · HTTP 200 · curl 2 ms · id `5890012f88fe` · 
- PASS · malformed · `no body` · HTTP 400 · curl 2 ms · id `7a008279f90d` · 
- PASS · malformed · `{}` · HTTP 400 · curl 2 ms · id `f762dcb7c8bd` · 
- PASS · malformed · `{"query": ""}` · HTTP 400 · curl 2 ms · id `5fc203957edd` · 
- PASS · malformed · `{"query": 42}` · HTTP 400 · curl 2 ms · id `2d86bcdbbee5` · 
- PASS · malformed · `["denim jacket"]` · HTTP 400 · curl 2 ms · id `86c8165caa08` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 1,208 ms · id `d73703f4f653` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 443 ms · id `01358b53992f` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 443 ms · id `300b5f3d82c3` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 423 ms · id `86f4fe9b5b06` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 384 ms · id `0e86ac1bd02b` · 

**C1. Every request leaves exactly one complete log record — trial 3**

- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 5,651 ms · id `ae19be0d6dc1` · 
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 4,959 ms · id `c2a2ab2f277e` · 
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 4,689 ms · id `8f1e55aedf60` · 
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 3,181 ms · id `247c78ff6595` · 
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 7,863 ms · id `5dd92a731380` · 
- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 2,058 ms · id `b0e42a17b165` · 
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 5,840 ms · id `97ff00fb41a5` · 
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 17,775 ms · id `99e989a0c110` · 
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 4,886 ms · id `d279da449364` · 
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 2,961 ms · id `13bf596f8b5b` · 
- PASS · impossible · `designer ballgown size XXS under $5` · HTTP 200 · curl 325 ms · id `1e85601ba983` · 
- PASS · impossible · `gold sequin gown size 2 under $3` · HTTP 200 · curl 298 ms · id `920926aa91bd` · 
- PASS · no_item · `size W30` · HTTP 200 · curl 2 ms · id `da0ca994ae5f` · 
- PASS · no_item · `under $30 size M` · HTTP 200 · curl 2 ms · id `c78a22f4a734` · 
- PASS · malformed · `no body` · HTTP 400 · curl 2 ms · id `0f40e4eea1ca` · 
- PASS · malformed · `{}` · HTTP 400 · curl 2 ms · id `0db580ff52d3` · 
- PASS · malformed · `{"query": ""}` · HTTP 400 · curl 2 ms · id `f4c5f29d9841` · 
- PASS · malformed · `{"query": 42}` · HTTP 400 · curl 2 ms · id `fdd2b6707fc9` · 
- PASS · malformed · `["denim jacket"]` · HTTP 400 · curl 2 ms · id `56a65e36f03a` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 905 ms · id `22a2a227932a` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 385 ms · id `0c3faaaaba7d` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 380 ms · id `4bc961d4b431` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 377 ms · id `cb8fa5da95ba` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 377 ms · id `aa6441d7b53c` · 

**C2. Logged numbers match (±250 ms, 2 calls, tokens > 0) — trial 1**

- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 3,942 ms · id `46359f02a12a` · gap 4 ms, 604 tokens
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 3,156 ms · id `3ca4f7e73223` · gap 5 ms, 691 tokens
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 5,202 ms · id `66ca18dd5b02` · gap 5 ms, 668 tokens
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 7,072 ms · id `0cecc66aca2d` · gap 4 ms, 614 tokens
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 2,008 ms · id `e2b73ebdd651` · gap 4 ms, 615 tokens
- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 2,307 ms · id `c808ea44c073` · gap 5 ms, 693 tokens
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 4,639 ms · id `f07c059c40eb` · gap 5 ms, 658 tokens
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 2,153 ms · id `9aaa99f370f3` · gap 4 ms, 593 tokens
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 2,732 ms · id `8a42b0f0f410` · gap 5 ms, 680 tokens
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 4,479 ms · id `409f2af64782` · gap 6 ms, 627 tokens

**C2. Logged numbers match (±250 ms, 2 calls, tokens > 0) — trial 2**

- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 2,956 ms · id `28b88e6af905` · gap 6 ms, 616 tokens
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 2,006 ms · id `7ffaf6ccefaa` · gap 6 ms, 654 tokens
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 3,846 ms · id `f9226809baef` · gap 5 ms, 691 tokens
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 2,531 ms · id `773ae71ffa7f` · gap 7 ms, 657 tokens
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 5,717 ms · id `82a40186ae82` · gap 4 ms, 654 tokens
- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 3,196 ms · id `3990d9eb342d` · gap 5 ms, 630 tokens
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 11,026 ms · id `960d718aaf67` · gap 5 ms, 746 tokens
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 8,719 ms · id `b8814bfa3228` · gap 7 ms, 681 tokens
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 4,261 ms · id `7a6c207dc8db` · gap 5 ms, 659 tokens
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 3,204 ms · id `a9c9824ee1bd` · gap 5 ms, 599 tokens

**C2. Logged numbers match (±250 ms, 2 calls, tokens > 0) — trial 3**

- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 5,651 ms · id `ae19be0d6dc1` · gap 5 ms, 668 tokens
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 4,959 ms · id `c2a2ab2f277e` · gap 6 ms, 639 tokens
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 4,689 ms · id `8f1e55aedf60` · gap 5 ms, 689 tokens
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 3,181 ms · id `247c78ff6595` · gap 6 ms, 623 tokens
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 7,863 ms · id `5dd92a731380` · gap 6 ms, 646 tokens
- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 2,058 ms · id `b0e42a17b165` · gap 6 ms, 618 tokens
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 5,840 ms · id `97ff00fb41a5` · gap 6 ms, 691 tokens
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 17,775 ms · id `99e989a0c110` · gap 6 ms, 682 tokens
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 4,886 ms · id `d279da449364` · gap 6 ms, 711 tokens
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 2,961 ms · id `13bf596f8b5b` · gap 4 ms, 598 tokens

**C3. Dead key: < 5 s, says 'API key', logged model_unavailable — trial 1**

- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 906 ms · id `830f51609b8e` · 906 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 381 ms · id `a1013c5f434c` · 381 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 380 ms · id `de3dcca261e9` · 380 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 374 ms · id `91edb3c12e76` · 374 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 369 ms · id `f65b97b0605d` · 369 ms

**C3. Dead key: < 5 s, says 'API key', logged model_unavailable — trial 2**

- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 1,208 ms · id `d73703f4f653` · 1,208 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 443 ms · id `01358b53992f` · 443 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 443 ms · id `300b5f3d82c3` · 443 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 423 ms · id `86f4fe9b5b06` · 423 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 384 ms · id `0e86ac1bd02b` · 384 ms

**C3. Dead key: < 5 s, says 'API key', logged model_unavailable — trial 3**

- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 905 ms · id `22a2a227932a` · 905 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 385 ms · id `0c3faaaaba7d` · 385 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 380 ms · id `4bc961d4b431` · 380 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 377 ms · id `cb8fa5da95ba` · 377 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 377 ms · id `aa6441d7b53c` · 377 ms

**C4. Malformed requests get a 400, never a 500 — trial 1**

- PASS · malformed · `no body` · HTTP 400 · curl 2 ms · id `4d52095d74b2` · HTTP 400
- PASS · malformed · `{}` · HTTP 400 · curl 2 ms · id `848aa9004d82` · HTTP 400
- PASS · malformed · `{"query": ""}` · HTTP 400 · curl 2 ms · id `6eb8a49929dd` · HTTP 400
- PASS · malformed · `{"query": 42}` · HTTP 400 · curl 2 ms · id `a338dc4959e9` · HTTP 400
- PASS · malformed · `["denim jacket"]` · HTTP 400 · curl 2 ms · id `6af1249990e4` · HTTP 400

**C4. Malformed requests get a 400, never a 500 — trial 2**

- PASS · malformed · `no body` · HTTP 400 · curl 2 ms · id `7a008279f90d` · HTTP 400
- PASS · malformed · `{}` · HTTP 400 · curl 2 ms · id `f762dcb7c8bd` · HTTP 400
- PASS · malformed · `{"query": ""}` · HTTP 400 · curl 2 ms · id `5fc203957edd` · HTTP 400
- PASS · malformed · `{"query": 42}` · HTTP 400 · curl 2 ms · id `2d86bcdbbee5` · HTTP 400
- PASS · malformed · `["denim jacket"]` · HTTP 400 · curl 2 ms · id `86c8165caa08` · HTTP 400

**C4. Malformed requests get a 400, never a 500 — trial 3**

- PASS · malformed · `no body` · HTTP 400 · curl 2 ms · id `0f40e4eea1ca` · HTTP 400
- PASS · malformed · `{}` · HTTP 400 · curl 2 ms · id `0db580ff52d3` · HTTP 400
- PASS · malformed · `{"query": ""}` · HTTP 400 · curl 2 ms · id `f4c5f29d9841` · HTTP 400
- PASS · malformed · `{"query": 42}` · HTTP 400 · curl 2 ms · id `fdd2b6707fc9` · HTTP 400
- PASS · malformed · `["denim jacket"]` · HTTP 400 · curl 2 ms · id `56a65e36f03a` · HTTP 400

**C5. Warm completed runs ≤ 10,000 ms — trial 1**

- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 3,942 ms · id `46359f02a12a` · 3,938 ms
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 3,156 ms · id `3ca4f7e73223` · 3,151 ms
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 5,202 ms · id `66ca18dd5b02` · 5,198 ms
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 7,072 ms · id `0cecc66aca2d` · 7,067 ms
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 2,008 ms · id `e2b73ebdd651` · 2,003 ms
- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 2,307 ms · id `c808ea44c073` · 2,302 ms
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 4,639 ms · id `f07c059c40eb` · 4,633 ms
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 2,153 ms · id `9aaa99f370f3` · 2,149 ms
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 2,732 ms · id `8a42b0f0f410` · 2,727 ms
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 4,479 ms · id `409f2af64782` · 4,474 ms

**C5. Warm completed runs ≤ 10,000 ms — trial 2**

- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 2,956 ms · id `28b88e6af905` · 2,950 ms
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 2,006 ms · id `7ffaf6ccefaa` · 2,000 ms
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 3,846 ms · id `f9226809baef` · 3,841 ms
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 2,531 ms · id `773ae71ffa7f` · 2,524 ms
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 5,717 ms · id `82a40186ae82` · 5,712 ms
- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 3,196 ms · id `3990d9eb342d` · 3,191 ms
- FAIL · matching · `90s track jacket in size M` · HTTP 200 · curl 11,026 ms · id `960d718aaf67` · 11,021 ms
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 8,719 ms · id `b8814bfa3228` · 8,712 ms
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 4,261 ms · id `7a6c207dc8db` · 4,257 ms
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 3,204 ms · id `a9c9824ee1bd` · 3,199 ms

**C5. Warm completed runs ≤ 10,000 ms — trial 3**

- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 5,651 ms · id `ae19be0d6dc1` · 5,646 ms
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 4,959 ms · id `c2a2ab2f277e` · 4,953 ms
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 4,689 ms · id `8f1e55aedf60` · 4,684 ms
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 3,181 ms · id `247c78ff6595` · 3,175 ms
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 7,863 ms · id `5dd92a731380` · 7,856 ms
- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 2,058 ms · id `b0e42a17b165` · 2,052 ms
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 5,840 ms · id `97ff00fb41a5` · 5,834 ms
- FAIL · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 17,775 ms · id `99e989a0c110` · 17,769 ms
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 4,886 ms · id `d279da449364` · 4,881 ms
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 2,961 ms · id `13bf596f8b5b` · 2,957 ms

## Trial 1 log, verbatim

```jsonl
{"ts": "2026-11-16T06:49:52.258+00:00", "request_id": "46359f02a12a", "route": "/ask", "query": "vintage graphic tee under $30", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_006", "fit_card_chars": 226, "queued_ms": 0.0, "agent_ms": 3937.3, "duration_ms": 3938.4, "timings": {"parse_query": 0.1, "search_listings_mcp": 546.0, "suggest_outfit": 1409.6, "create_fit_card": 1981.3, "total": 3937.3}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 459, "tokens_output": 145, "tokens_total": 604}
{"ts": "2026-11-16T06:50:02.230+00:00", "request_id": "3ca4f7e73223", "route": "/ask", "query": "90s track jacket in size M", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_004", "fit_card_chars": 261, "queued_ms": 0.0, "agent_ms": 3149.6, "duration_ms": 3150.6, "timings": {"parse_query": 0.0, "search_listings_mcp": 418.2, "suggest_outfit": 1278.0, "create_fit_card": 1453.1, "total": 3149.6}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 504, "tokens_output": 187, "tokens_total": 691}
{"ts": "2026-11-16T06:50:11.416+00:00", "request_id": "66ca18dd5b02", "route": "/ask", "query": "silk slip dress in midi length under $40", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_013", "fit_card_chars": 294, "queued_ms": 0.0, "agent_ms": 5196.9, "duration_ms": 5197.8, "timings": {"parse_query": 0.0, "search_listings_mcp": 392.9, "suggest_outfit": 3499.2, "create_fit_card": 1304.6, "total": 5196.9}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 492, "tokens_output": 176, "tokens_total": 668}
{"ts": "2026-11-16T06:50:22.635+00:00", "request_id": "0cecc66aca2d", "route": "/ask", "query": "platform sneakers size 8", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_019", "fit_card_chars": 232, "queued_ms": 0.0, "agent_ms": 7066.5, "duration_ms": 7067.4, "timings": {"parse_query": 0.0, "search_listings_mcp": 388.6, "suggest_outfit": 5993.6, "create_fit_card": 684.1, "total": 7066.5}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 465, "tokens_output": 149, "tokens_total": 614}
{"ts": "2026-11-16T06:50:35.741+00:00", "request_id": "e2b73ebdd651", "route": "/ask", "query": "denim jacket under $50", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_007", "fit_card_chars": 218, "queued_ms": 0.0, "agent_ms": 2002.4, "duration_ms": 2003.4, "timings": {"parse_query": 0.0, "search_listings_mcp": 490.1, "suggest_outfit": 762.6, "create_fit_card": 749.5, "total": 2002.4}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 468, "tokens_output": 147, "tokens_total": 615}
{"ts": "2026-11-16T06:50:43.774+00:00", "request_id": "c808ea44c073", "route": "/ask", "query": "vintage graphic tee under $30", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_006", "fit_card_chars": 272, "queued_ms": 0.0, "agent_ms": 2301.2, "duration_ms": 2302.2, "timings": {"parse_query": 0.0, "search_listings_mcp": 389.7, "suggest_outfit": 1063.5, "create_fit_card": 847.7, "total": 2301.2}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 500, "tokens_output": 193, "tokens_total": 693}
{"ts": "2026-11-16T06:50:52.108+00:00", "request_id": "f07c059c40eb", "route": "/ask", "query": "90s track jacket in size M", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_004", "fit_card_chars": 261, "queued_ms": 0.0, "agent_ms": 4631.8, "duration_ms": 4633.1, "timings": {"parse_query": 0.0, "search_listings_mcp": 385.4, "suggest_outfit": 2261.1, "create_fit_card": 1984.9, "total": 4631.8}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 486, "tokens_output": 172, "tokens_total": 658}
{"ts": "2026-11-16T06:51:02.775+00:00", "request_id": "9aaa99f370f3", "route": "/ask", "query": "silk slip dress in midi length under $40", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_013", "fit_card_chars": 306, "queued_ms": 0.0, "agent_ms": 2147.6, "duration_ms": 2148.7, "timings": {"parse_query": 0.0, "search_listings_mcp": 387.1, "suggest_outfit": 1092.3, "create_fit_card": 667.8, "total": 2147.6}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 455, "tokens_output": 138, "tokens_total": 593}
{"ts": "2026-11-16T06:51:10.958+00:00", "request_id": "8a42b0f0f410", "route": "/ask", "query": "platform sneakers size 8", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_019", "fit_card_chars": 278, "queued_ms": 0.0, "agent_ms": 2725.8, "duration_ms": 2726.6, "timings": {"parse_query": 0.0, "search_listings_mcp": 315.8, "suggest_outfit": 1484.8, "create_fit_card": 924.9, "total": 2725.8}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 494, "tokens_output": 186, "tokens_total": 680}
{"ts": "2026-11-16T06:51:19.717+00:00", "request_id": "409f2af64782", "route": "/ask", "query": "denim jacket under $50", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_007", "fit_card_chars": 293, "queued_ms": 0.0, "agent_ms": 4472.8, "duration_ms": 4473.6, "timings": {"parse_query": 0.0, "search_listings_mcp": 325.5, "suggest_outfit": 743.9, "create_fit_card": 3403.1, "total": 4472.8}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 465, "tokens_output": 162, "tokens_total": 627}
{"ts": "2026-11-16T06:51:30.225+00:00", "request_id": "02e9a4ed9874", "route": "/ask", "query": "designer ballgown size XXS under $5", "wardrobe": "example", "status": 200, "outcome": "no_results", "error": "Nothing matched 'designer ballgown' in size XXS under $5. Try: raise or drop the price limit; drop the size; use fewer or broader words (e.g. 'dress' instead of 'designer ballgown').", "selected_item": null, "fit_card_chars": null, "queued_ms": 0.0, "agent_ms": 320.9, "duration_ms": 321.4, "timings": {"parse_query": 0.0, "search_listings_mcp": 320.7, "total": 320.9}, "model_calls": 0, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:51:30.558+00:00", "request_id": "f403c240566c", "route": "/ask", "query": "gold sequin gown size 2 under $3", "wardrobe": "example", "status": 200, "outcome": "no_results", "error": "Nothing matched 'gold sequin gown' in size 2 under $3. Try: raise or drop the price limit; drop the size; use fewer or broader words (e.g. 'dress' instead of 'designer ballgown').", "selected_item": null, "fit_card_chars": null, "queued_ms": 0.0, "agent_ms": 292.9, "duration_ms": 293.2, "timings": {"parse_query": 0.0, "search_listings_mcp": 292.8, "total": 292.9}, "model_calls": 0, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:51:30.863+00:00", "request_id": "ac667c8e640e", "route": "/ask", "query": "size W30", "wardrobe": "example", "status": 200, "outcome": "no_item", "error": "Your search doesn't say what kind of item you want, so there was nothing to search for. I kept size W30. Add an item and try again — e.g. 'graphic tee', 'denim jacket' or 'platform sneakers'.", "selected_item": null, "fit_card_chars": null, "queued_ms": 0.0, "agent_ms": 0.0, "duration_ms": 0.3, "timings": {"parse_query": 0.0, "total": 0.0}, "model_calls": 0, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:51:30.875+00:00", "request_id": "146190ea1631", "route": "/ask", "query": "under $30 size M", "wardrobe": "example", "status": 200, "outcome": "no_item", "error": "Your search doesn't say what kind of item you want, so there was nothing to search for. I kept size M and under $30. Add an item and try again — e.g. 'graphic tee', 'denim jacket' or 'platform sneakers'.", "selected_item": null, "fit_card_chars": null, "queued_ms": 0.0, "agent_ms": 0.0, "duration_ms": 0.3, "timings": {"parse_query": 0.0, "total": 0.0}, "model_calls": 0, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:51:30.886+00:00", "request_id": "4d52095d74b2", "route": "/ask", "query": null, "wardrobe": null, "status": 400, "outcome": "bad_request", "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "selected_item": null, "fit_card_chars": null, "queued_ms": null, "agent_ms": null, "duration_ms": 0.0, "timings": null, "model_calls": 0, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:51:30.896+00:00", "request_id": "848aa9004d82", "route": "/ask", "query": null, "wardrobe": null, "status": 400, "outcome": "bad_request", "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "selected_item": null, "fit_card_chars": null, "queued_ms": null, "agent_ms": null, "duration_ms": 0.1, "timings": null, "model_calls": 0, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:51:30.906+00:00", "request_id": "6eb8a49929dd", "route": "/ask", "query": "", "wardrobe": null, "status": 400, "outcome": "bad_request", "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "selected_item": null, "fit_card_chars": null, "queued_ms": null, "agent_ms": null, "duration_ms": 0.1, "timings": null, "model_calls": 0, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:51:30.917+00:00", "request_id": "a338dc4959e9", "route": "/ask", "query": 42, "wardrobe": null, "status": 400, "outcome": "bad_request", "error": "'query' must be text, not int. Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "selected_item": null, "fit_card_chars": null, "queued_ms": null, "agent_ms": null, "duration_ms": 0.1, "timings": null, "model_calls": 0, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:51:30.927+00:00", "request_id": "6af1249990e4", "route": "/ask", "query": null, "wardrobe": null, "status": 400, "outcome": "bad_request", "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "selected_item": null, "fit_card_chars": null, "queued_ms": null, "agent_ms": null, "duration_ms": 0.1, "timings": null, "model_calls": 0, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:51:31.473+00:00", "request_id": "830f51609b8e", "route": "/ask", "query": "denim jacket under $50", "wardrobe": "example", "status": 200, "outcome": "model_unavailable", "error": "The search worked — it found Denim Jacket — Light Wash, Cropped ($42 on poshmark) — but the styling model couldn't be reached, so there's no outfit or fit card. The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com. Then run the same query again.", "selected_item": "lst_007", "fit_card_chars": null, "queued_ms": 0.0, "agent_ms": 901.0, "duration_ms": 901.7, "timings": {"parse_query": 0.1, "search_listings_mcp": 476.2, "suggest_outfit": 424.5, "total": 901.0}, "model_calls": 1, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:51:32.396+00:00", "request_id": "a1013c5f434c", "route": "/ask", "query": "denim jacket under $50", "wardrobe": "example", "status": 200, "outcome": "model_unavailable", "error": "The search worked — it found Denim Jacket — Light Wash, Cropped ($42 on poshmark) — but the styling model couldn't be reached, so there's no outfit or fit card. The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com. Then run the same query again.", "selected_item": "lst_007", "fit_card_chars": null, "queued_ms": 0.0, "agent_ms": 376.5, "duration_ms": 377.0, "timings": {"parse_query": 0.0, "search_listings_mcp": 308.9, "suggest_outfit": 67.4, "total": 376.5}, "model_calls": 1, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:51:32.790+00:00", "request_id": "de3dcca261e9", "route": "/ask", "query": "denim jacket under $50", "wardrobe": "example", "status": 200, "outcome": "model_unavailable", "error": "The search worked — it found Denim Jacket — Light Wash, Cropped ($42 on poshmark) — but the styling model couldn't be reached, so there's no outfit or fit card. The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com. Then run the same query again.", "selected_item": "lst_007", "fit_card_chars": null, "queued_ms": 0.0, "agent_ms": 376.2, "duration_ms": 376.7, "timings": {"parse_query": 0.0, "search_listings_mcp": 296.6, "suggest_outfit": 79.5, "total": 376.2}, "model_calls": 1, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:51:33.184+00:00", "request_id": "91edb3c12e76", "route": "/ask", "query": "denim jacket under $50", "wardrobe": "example", "status": 200, "outcome": "model_unavailable", "error": "The search worked — it found Denim Jacket — Light Wash, Cropped ($42 on poshmark) — but the styling model couldn't be reached, so there's no outfit or fit card. The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com. Then run the same query again.", "selected_item": "lst_007", "fit_card_chars": null, "queued_ms": 0.0, "agent_ms": 370.6, "duration_ms": 371.1, "timings": {"parse_query": 0.0, "search_listings_mcp": 296.1, "suggest_outfit": 74.4, "total": 370.6}, "model_calls": 1, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:51:33.572+00:00", "request_id": "f65b97b0605d", "route": "/ask", "query": "denim jacket under $50", "wardrobe": "example", "status": 200, "outcome": "model_unavailable", "error": "The search worked — it found Denim Jacket — Light Wash, Cropped ($42 on poshmark) — but the styling model couldn't be reached, so there's no outfit or fit card. The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com. Then run the same query again.", "selected_item": "lst_007", "fit_card_chars": null, "queued_ms": 0.0, "agent_ms": 365.6, "duration_ms": 366.0, "timings": {"parse_query": 0.0, "search_listings_mcp": 297.8, "suggest_outfit": 67.6, "total": 365.6}, "model_calls": 1, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
```
