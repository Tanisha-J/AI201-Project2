# Capstone run log — before

2026-11-15 22:49, `python capstone_trials.py --label before`. 3 trials of the 24-request set defined in criteria.md. Raw logs: `results/capstone_logs/before_trial<N>.jsonl`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| C1. Every request leaves exactly one complete log record | 24 of 24 | 24/24 | 24/24 | 24/24 | MET |
| C2. Logged numbers match (±250 ms, 2 calls, tokens > 0) | 10 of 10 | 10/10 | 10/10 | 9/10 | MISSED |
| C3. Dead key: < 5 s, says 'API key', logged model_unavailable | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| C4. Malformed requests get a 400, never a 500 | 5 of 5 | 3/5 | 3/5 | 3/5 | MISSED |
| C5. Warm completed runs ≤ 10,000 ms | 9 of 10 | 10/10 | 10/10 | 9/10 | MET |

## Every scored request

**C1. Every request leaves exactly one complete log record — trial 1**

- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 2,844 ms · id `e4fedc810bbc` · 
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 2,803 ms · id `a0d8f93aa9cb` · 
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 2,341 ms · id `e8e7fd306cf6` · 
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 2,011 ms · id `584c4964c494` · 
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 3,081 ms · id `b769f2a1e0f5` · 
- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 5,639 ms · id `2e812204ac15` · 
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 2,146 ms · id `2e579234e980` · 
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 2,586 ms · id `21aa1379d7aa` · 
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 2,165 ms · id `4576f59b586e` · 
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 3,196 ms · id `587eb545c584` · 
- PASS · impossible · `designer ballgown size XXS under $5` · HTTP 200 · curl 328 ms · id `4734689de1ed` · 
- PASS · impossible · `gold sequin gown size 2 under $3` · HTTP 200 · curl 291 ms · id `675d6698b7cb` · 
- PASS · no_item · `size W30` · HTTP 200 · curl 2 ms · id `65b102b7e163` · 
- PASS · no_item · `under $30 size M` · HTTP 200 · curl 2 ms · id `94244a6e21b3` · 
- PASS · malformed · `no body` · HTTP 400 · curl 2 ms · id `338297960898` · 
- PASS · malformed · `{}` · HTTP 400 · curl 2 ms · id `c62f8ef4cf8d` · 
- PASS · malformed · `{"query": ""}` · HTTP 400 · curl 2 ms · id `7b910a99de17` · 
- PASS · malformed · `{"query": 42}` · HTTP 500 · curl 2 ms · id `2e74de670c75` · 
- PASS · malformed · `["denim jacket"]` · HTTP 500 · curl 2 ms · id `00dddf27a6d4` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 885 ms · id `d9209cc82c1f` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 387 ms · id `eafaec0e18e1` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 366 ms · id `6450ac056c42` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 363 ms · id `9b6e2d796554` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 399 ms · id `f6c004664016` · 

**C1. Every request leaves exactly one complete log record — trial 2**

- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 3,122 ms · id `0029ce8ead46` · 
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 1,746 ms · id `5d13a4216f47` · 
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 2,470 ms · id `438f47ae0c20` · 
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 2,552 ms · id `ee7369254993` · 
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 2,066 ms · id `01507aef8a51` · 
- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 2,088 ms · id `ea996a873205` · 
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 1,806 ms · id `c6cbde915365` · 
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 4,216 ms · id `99dd85f3f076` · 
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 2,234 ms · id `e68ae17e393c` · 
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 3,730 ms · id `b0c3ad0ce458` · 
- PASS · impossible · `designer ballgown size XXS under $5` · HTTP 200 · curl 404 ms · id `bc02073dca59` · 
- PASS · impossible · `gold sequin gown size 2 under $3` · HTTP 200 · curl 295 ms · id `43421b161767` · 
- PASS · no_item · `size W30` · HTTP 200 · curl 2 ms · id `b70bd334b04b` · 
- PASS · no_item · `under $30 size M` · HTTP 200 · curl 2 ms · id `82fa9e55027d` · 
- PASS · malformed · `no body` · HTTP 400 · curl 2 ms · id `a950a0ec28ca` · 
- PASS · malformed · `{}` · HTTP 400 · curl 2 ms · id `49784381c81d` · 
- PASS · malformed · `{"query": ""}` · HTTP 400 · curl 2 ms · id `734be8d58bad` · 
- PASS · malformed · `{"query": 42}` · HTTP 500 · curl 2 ms · id `51ebefe703c2` · 
- PASS · malformed · `["denim jacket"]` · HTTP 500 · curl 2 ms · id `21a662d7cca0` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 915 ms · id `2766452424e3` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 390 ms · id `15c173de2d65` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 379 ms · id `30dcde9538d6` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 374 ms · id `5b7681a75e43` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 368 ms · id `366483b693f6` · 

**C1. Every request leaves exactly one complete log record — trial 3**

- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 5,520 ms · id `54a367f16e6c` · 
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 2,486 ms · id `46078b21d3e0` · 
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 2,693 ms · id `172b100f0bd2` · 
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 1,919 ms · id `37e07b8a4a76` · 
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 2,536 ms · id `046c7bfcf12a` · 
- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 2,144 ms · id `6f103ff9d6a8` · 
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 4,419 ms · id `c9f01740b18f` · 
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 1,837 ms · id `8c5175d85051` · 
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 2,862 ms · id `c115bf00bcd0` · 
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 3,507 ms · id `777d6c1f8f30` · 
- PASS · impossible · `designer ballgown size XXS under $5` · HTTP 200 · curl 348 ms · id `09f77dab2cba` · 
- PASS · impossible · `gold sequin gown size 2 under $3` · HTTP 200 · curl 296 ms · id `739741e269b1` · 
- PASS · no_item · `size W30` · HTTP 200 · curl 2 ms · id `4fe658a2dab1` · 
- PASS · no_item · `under $30 size M` · HTTP 200 · curl 2 ms · id `9397c7b44ae3` · 
- PASS · malformed · `no body` · HTTP 400 · curl 2 ms · id `ecedc1d5fe4f` · 
- PASS · malformed · `{}` · HTTP 400 · curl 2 ms · id `e47e562d1794` · 
- PASS · malformed · `{"query": ""}` · HTTP 400 · curl 2 ms · id `48f989b9c56d` · 
- PASS · malformed · `{"query": 42}` · HTTP 500 · curl 2 ms · id `e0370fa80be5` · 
- PASS · malformed · `["denim jacket"]` · HTTP 500 · curl 2 ms · id `6c8b8b08af39` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 902 ms · id `5b2ff16fd167` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 389 ms · id `8fc5dc894860` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 368 ms · id `d1208b90c57a` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 379 ms · id `e37aeb58e079` · 
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 365 ms · id `7b91af755f31` · 

**C2. Logged numbers match (±250 ms, 2 calls, tokens > 0) — trial 1**

- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 2,844 ms · id `e4fedc810bbc` · gap 5 ms, 675 tokens
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 2,803 ms · id `a0d8f93aa9cb` · gap 7 ms, 688 tokens
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 2,341 ms · id `e8e7fd306cf6` · gap 6 ms, 671 tokens
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 2,011 ms · id `584c4964c494` · gap 6 ms, 638 tokens
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 3,081 ms · id `b769f2a1e0f5` · gap 5 ms, 709 tokens
- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 5,639 ms · id `2e812204ac15` · gap 5 ms, 614 tokens
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 2,146 ms · id `2e579234e980` · gap 6 ms, 664 tokens
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 2,586 ms · id `21aa1379d7aa` · gap 6 ms, 719 tokens
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 2,165 ms · id `4576f59b586e` · gap 6 ms, 629 tokens
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 3,196 ms · id `587eb545c584` · gap 5 ms, 700 tokens

**C2. Logged numbers match (±250 ms, 2 calls, tokens > 0) — trial 2**

- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 3,122 ms · id `0029ce8ead46` · gap 5 ms, 639 tokens
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 1,746 ms · id `5d13a4216f47` · gap 5 ms, 667 tokens
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 2,470 ms · id `438f47ae0c20` · gap 7 ms, 723 tokens
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 2,552 ms · id `ee7369254993` · gap 5 ms, 693 tokens
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 2,066 ms · id `01507aef8a51` · gap 5 ms, 608 tokens
- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 2,088 ms · id `ea996a873205` · gap 5 ms, 602 tokens
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 1,806 ms · id `c6cbde915365` · gap 5 ms, 650 tokens
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 4,216 ms · id `99dd85f3f076` · gap 6 ms, 682 tokens
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 2,234 ms · id `e68ae17e393c` · gap 5 ms, 624 tokens
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 3,730 ms · id `b0c3ad0ce458` · gap 5 ms, 670 tokens

**C2. Logged numbers match (±250 ms, 2 calls, tokens > 0) — trial 3**

- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 5,520 ms · id `54a367f16e6c` · gap 6 ms, 687 tokens
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 2,486 ms · id `46078b21d3e0` · gap 6 ms, 635 tokens
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 2,693 ms · id `172b100f0bd2` · gap 4 ms, 654 tokens
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 1,919 ms · id `37e07b8a4a76` · gap 5 ms, 637 tokens
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 2,536 ms · id `046c7bfcf12a` · gap 5 ms, 650 tokens
- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 2,144 ms · id `6f103ff9d6a8` · gap 5 ms, 627 tokens
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 4,419 ms · id `c9f01740b18f` · gap 5 ms, 649 tokens
- FAIL · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 1,837 ms · id `8c5175d85051` · outcome model_unavailable; model_calls 1; tokens_total 0
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 2,862 ms · id `c115bf00bcd0` · gap 5 ms, 636 tokens
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 3,507 ms · id `777d6c1f8f30` · gap 4 ms, 611 tokens

**C3. Dead key: < 5 s, says 'API key', logged model_unavailable — trial 1**

- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 885 ms · id `d9209cc82c1f` · 885 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 387 ms · id `eafaec0e18e1` · 387 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 366 ms · id `6450ac056c42` · 366 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 363 ms · id `9b6e2d796554` · 363 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 399 ms · id `f6c004664016` · 399 ms

**C3. Dead key: < 5 s, says 'API key', logged model_unavailable — trial 2**

- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 915 ms · id `2766452424e3` · 915 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 390 ms · id `15c173de2d65` · 390 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 379 ms · id `30dcde9538d6` · 379 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 374 ms · id `5b7681a75e43` · 374 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 368 ms · id `366483b693f6` · 368 ms

**C3. Dead key: < 5 s, says 'API key', logged model_unavailable — trial 3**

- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 902 ms · id `5b2ff16fd167` · 902 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 389 ms · id `8fc5dc894860` · 389 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 368 ms · id `d1208b90c57a` · 368 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 379 ms · id `e37aeb58e079` · 379 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 365 ms · id `7b91af755f31` · 365 ms

**C4. Malformed requests get a 400, never a 500 — trial 1**

- PASS · malformed · `no body` · HTTP 400 · curl 2 ms · id `338297960898` · HTTP 400
- PASS · malformed · `{}` · HTTP 400 · curl 2 ms · id `c62f8ef4cf8d` · HTTP 400
- PASS · malformed · `{"query": ""}` · HTTP 400 · curl 2 ms · id `7b910a99de17` · HTTP 400
- FAIL · malformed · `{"query": 42}` · HTTP 500 · curl 2 ms · id `2e74de670c75` · HTTP 500: AttributeError: 'int' object has no attribute 'strip'
- FAIL · malformed · `["denim jacket"]` · HTTP 500 · curl 2 ms · id `00dddf27a6d4` · HTTP 500: AttributeError: 'list' object has no attribute 'get'

**C4. Malformed requests get a 400, never a 500 — trial 2**

- PASS · malformed · `no body` · HTTP 400 · curl 2 ms · id `a950a0ec28ca` · HTTP 400
- PASS · malformed · `{}` · HTTP 400 · curl 2 ms · id `49784381c81d` · HTTP 400
- PASS · malformed · `{"query": ""}` · HTTP 400 · curl 2 ms · id `734be8d58bad` · HTTP 400
- FAIL · malformed · `{"query": 42}` · HTTP 500 · curl 2 ms · id `51ebefe703c2` · HTTP 500: AttributeError: 'int' object has no attribute 'strip'
- FAIL · malformed · `["denim jacket"]` · HTTP 500 · curl 2 ms · id `21a662d7cca0` · HTTP 500: AttributeError: 'list' object has no attribute 'get'

**C4. Malformed requests get a 400, never a 500 — trial 3**

- PASS · malformed · `no body` · HTTP 400 · curl 2 ms · id `ecedc1d5fe4f` · HTTP 400
- PASS · malformed · `{}` · HTTP 400 · curl 2 ms · id `e47e562d1794` · HTTP 400
- PASS · malformed · `{"query": ""}` · HTTP 400 · curl 2 ms · id `48f989b9c56d` · HTTP 400
- FAIL · malformed · `{"query": 42}` · HTTP 500 · curl 2 ms · id `e0370fa80be5` · HTTP 500: AttributeError: 'int' object has no attribute 'strip'
- FAIL · malformed · `["denim jacket"]` · HTTP 500 · curl 2 ms · id `6c8b8b08af39` · HTTP 500: AttributeError: 'list' object has no attribute 'get'

**C5. Warm completed runs ≤ 10,000 ms — trial 1**

- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 2,844 ms · id `e4fedc810bbc` · 2,839 ms
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 2,803 ms · id `a0d8f93aa9cb` · 2,796 ms
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 2,341 ms · id `e8e7fd306cf6` · 2,335 ms
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 2,011 ms · id `584c4964c494` · 2,005 ms
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 3,081 ms · id `b769f2a1e0f5` · 3,076 ms
- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 5,639 ms · id `2e812204ac15` · 5,634 ms
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 2,146 ms · id `2e579234e980` · 2,139 ms
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 2,586 ms · id `21aa1379d7aa` · 2,580 ms
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 2,165 ms · id `4576f59b586e` · 2,159 ms
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 3,196 ms · id `587eb545c584` · 3,191 ms

**C5. Warm completed runs ≤ 10,000 ms — trial 2**

- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 3,122 ms · id `0029ce8ead46` · 3,116 ms
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 1,746 ms · id `5d13a4216f47` · 1,741 ms
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 2,470 ms · id `438f47ae0c20` · 2,463 ms
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 2,552 ms · id `ee7369254993` · 2,547 ms
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 2,066 ms · id `01507aef8a51` · 2,060 ms
- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 2,088 ms · id `ea996a873205` · 2,082 ms
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 1,806 ms · id `c6cbde915365` · 1,801 ms
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 4,216 ms · id `99dd85f3f076` · 4,210 ms
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 2,234 ms · id `e68ae17e393c` · 2,229 ms
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 3,730 ms · id `b0c3ad0ce458` · 3,725 ms

**C5. Warm completed runs ≤ 10,000 ms — trial 3**

- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 5,520 ms · id `54a367f16e6c` · 5,514 ms
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 2,486 ms · id `46078b21d3e0` · 2,480 ms
- PASS · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 2,693 ms · id `172b100f0bd2` · 2,688 ms
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 1,919 ms · id `37e07b8a4a76` · 1,914 ms
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 2,536 ms · id `046c7bfcf12a` · 2,531 ms
- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 2,144 ms · id `6f103ff9d6a8` · 2,139 ms
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 4,419 ms · id `c9f01740b18f` · 4,414 ms
- FAIL · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 1,837 ms · id `8c5175d85051` · did not complete
- PASS · matching · `platform sneakers size 8` · HTTP 200 · curl 2,862 ms · id `c115bf00bcd0` · 2,857 ms
- PASS · matching · `denim jacket under $50` · HTTP 200 · curl 3,507 ms · id `777d6c1f8f30` · 3,503 ms

## Trial 1 log, verbatim

```jsonl
{"ts": "2026-11-16T06:44:33.258+00:00", "request_id": "e4fedc810bbc", "route": "/ask", "query": "vintage graphic tee under $30", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_006", "fit_card_chars": 256, "queued_ms": 0.0, "agent_ms": 2838.1, "duration_ms": 2839.3, "timings": {"parse_query": 0.1, "search_listings_mcp": 552.9, "suggest_outfit": 1473.1, "create_fit_card": 811.6, "total": 2838.0}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 492, "tokens_output": 183, "tokens_total": 675}
{"ts": "2026-11-16T06:44:42.129+00:00", "request_id": "a0d8f93aa9cb", "route": "/ask", "query": "90s track jacket in size M", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_004", "fit_card_chars": 204, "queued_ms": 0.0, "agent_ms": 2795.0, "duration_ms": 2796.1, "timings": {"parse_query": 0.0, "search_listings_mcp": 319.8, "suggest_outfit": 1639.4, "create_fit_card": 835.2, "total": 2795.0}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 507, "tokens_output": 181, "tokens_total": 688}
{"ts": "2026-11-16T06:44:50.966+00:00", "request_id": "e8e7fd306cf6", "route": "/ask", "query": "silk slip dress in midi length under $40", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_013", "fit_card_chars": 284, "queued_ms": 0.0, "agent_ms": 2334.1, "duration_ms": 2335.4, "timings": {"parse_query": 0.1, "search_listings_mcp": 338.0, "suggest_outfit": 1131.1, "create_fit_card": 864.5, "total": 2334.1}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 494, "tokens_output": 177, "tokens_total": 671}
{"ts": "2026-11-16T06:44:59.343+00:00", "request_id": "584c4964c494", "route": "/ask", "query": "platform sneakers size 8", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_019", "fit_card_chars": 194, "queued_ms": 0.0, "agent_ms": 2003.8, "duration_ms": 2004.7, "timings": {"parse_query": 0.0, "search_listings_mcp": 320.8, "suggest_outfit": 1070.6, "create_fit_card": 612.0, "total": 2003.8}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 479, "tokens_output": 159, "tokens_total": 638}
{"ts": "2026-11-16T06:45:07.385+00:00", "request_id": "b769f2a1e0f5", "route": "/ask", "query": "denim jacket under $50", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_007", "fit_card_chars": 319, "queued_ms": 0.0, "agent_ms": 3075.4, "duration_ms": 3076.3, "timings": {"parse_query": 0.0, "search_listings_mcp": 331.1, "suggest_outfit": 1828.4, "create_fit_card": 915.6, "total": 3075.4}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 504, "tokens_output": 205, "tokens_total": 709}
{"ts": "2026-11-16T06:45:16.499+00:00", "request_id": "2e812204ac15", "route": "/ask", "query": "vintage graphic tee under $30", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_006", "fit_card_chars": 248, "queued_ms": 0.0, "agent_ms": 5633.5, "duration_ms": 5634.3, "timings": {"parse_query": 0.0, "search_listings_mcp": 320.9, "suggest_outfit": 4590.2, "create_fit_card": 722.2, "total": 5633.5}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 463, "tokens_output": 151, "tokens_total": 614}
{"ts": "2026-11-16T06:45:28.166+00:00", "request_id": "2e579234e980", "route": "/ask", "query": "90s track jacket in size M", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_004", "fit_card_chars": 252, "queued_ms": 0.0, "agent_ms": 2138.4, "duration_ms": 2139.4, "timings": {"parse_query": 0.0, "search_listings_mcp": 399.0, "suggest_outfit": 968.4, "create_fit_card": 770.6, "total": 2138.4}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 489, "tokens_output": 175, "tokens_total": 664}
{"ts": "2026-11-16T06:45:36.346+00:00", "request_id": "21aa1379d7aa", "route": "/ask", "query": "silk slip dress in midi length under $40", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_013", "fit_card_chars": 344, "queued_ms": 0.0, "agent_ms": 2578.8, "duration_ms": 2579.8, "timings": {"parse_query": 0.0, "search_listings_mcp": 354.7, "suggest_outfit": 1271.4, "create_fit_card": 952.4, "total": 2578.8}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 512, "tokens_output": 207, "tokens_total": 719}
{"ts": "2026-11-16T06:45:44.961+00:00", "request_id": "4576f59b586e", "route": "/ask", "query": "platform sneakers size 8", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_019", "fit_card_chars": 209, "queued_ms": 0.0, "agent_ms": 2157.8, "duration_ms": 2158.8, "timings": {"parse_query": 0.0, "search_listings_mcp": 315.2, "suggest_outfit": 867.8, "create_fit_card": 974.4, "total": 2157.8}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 474, "tokens_output": 155, "tokens_total": 629}
{"ts": "2026-11-16T06:45:53.155+00:00", "request_id": "587eb545c584", "route": "/ask", "query": "denim jacket under $50", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_007", "fit_card_chars": 285, "queued_ms": 0.0, "agent_ms": 3189.9, "duration_ms": 3190.9, "timings": {"parse_query": 0.0, "search_listings_mcp": 323.9, "suggest_outfit": 1052.0, "create_fit_card": 1813.7, "total": 3189.9}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 504, "tokens_output": 196, "tokens_total": 700}
{"ts": "2026-11-16T06:46:02.386+00:00", "request_id": "4734689de1ed", "route": "/ask", "query": "designer ballgown size XXS under $5", "wardrobe": "example", "status": 200, "outcome": "no_results", "error": "Nothing matched 'designer ballgown' in size XXS under $5. Try: raise or drop the price limit; drop the size; use fewer or broader words (e.g. 'dress' instead of 'designer ballgown').", "selected_item": null, "fit_card_chars": null, "queued_ms": 0.0, "agent_ms": 324.9, "duration_ms": 325.3, "timings": {"parse_query": 0.0, "search_listings_mcp": 324.8, "total": 324.9}, "model_calls": 0, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:46:02.723+00:00", "request_id": "675d6698b7cb", "route": "/ask", "query": "gold sequin gown size 2 under $3", "wardrobe": "example", "status": 200, "outcome": "no_results", "error": "Nothing matched 'gold sequin gown' in size 2 under $3. Try: raise or drop the price limit; drop the size; use fewer or broader words (e.g. 'dress' instead of 'designer ballgown').", "selected_item": null, "fit_card_chars": null, "queued_ms": 0.0, "agent_ms": 288.3, "duration_ms": 288.7, "timings": {"parse_query": 0.0, "search_listings_mcp": 288.3, "total": 288.3}, "model_calls": 0, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:46:03.023+00:00", "request_id": "65b102b7e163", "route": "/ask", "query": "size W30", "wardrobe": "example", "status": 200, "outcome": "no_item", "error": "Your search doesn't say what kind of item you want, so there was nothing to search for. I kept size W30. Add an item and try again — e.g. 'graphic tee', 'denim jacket' or 'platform sneakers'.", "selected_item": null, "fit_card_chars": null, "queued_ms": 0.0, "agent_ms": 0.0, "duration_ms": 0.3, "timings": {"parse_query": 0.0, "total": 0.0}, "model_calls": 0, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:46:03.033+00:00", "request_id": "94244a6e21b3", "route": "/ask", "query": "under $30 size M", "wardrobe": "example", "status": 200, "outcome": "no_item", "error": "Your search doesn't say what kind of item you want, so there was nothing to search for. I kept size M and under $30. Add an item and try again — e.g. 'graphic tee', 'denim jacket' or 'platform sneakers'.", "selected_item": null, "fit_card_chars": null, "queued_ms": 0.0, "agent_ms": 0.0, "duration_ms": 0.2, "timings": {"parse_query": 0.0, "total": 0.0}, "model_calls": 0, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:46:03.044+00:00", "request_id": "338297960898", "route": "/ask", "query": null, "wardrobe": null, "status": 400, "outcome": "bad_request", "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "selected_item": null, "fit_card_chars": null, "queued_ms": null, "agent_ms": null, "duration_ms": 0.0, "timings": null, "model_calls": 0, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:46:03.054+00:00", "request_id": "c62f8ef4cf8d", "route": "/ask", "query": null, "wardrobe": null, "status": 400, "outcome": "bad_request", "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "selected_item": null, "fit_card_chars": null, "queued_ms": null, "agent_ms": null, "duration_ms": 0.1, "timings": null, "model_calls": 0, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:46:03.065+00:00", "request_id": "7b910a99de17", "route": "/ask", "query": "", "wardrobe": null, "status": 400, "outcome": "bad_request", "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "selected_item": null, "fit_card_chars": null, "queued_ms": null, "agent_ms": null, "duration_ms": 0.1, "timings": null, "model_calls": 0, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:46:03.075+00:00", "request_id": "2e74de670c75", "route": "/ask", "query": 42, "wardrobe": null, "status": 500, "outcome": "server_error", "error": "AttributeError: 'int' object has no attribute 'strip'", "selected_item": null, "fit_card_chars": null, "queued_ms": null, "agent_ms": null, "duration_ms": 0.1, "timings": null, "model_calls": 0, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:46:03.086+00:00", "request_id": "00dddf27a6d4", "route": "/ask", "query": null, "wardrobe": null, "status": 500, "outcome": "server_error", "error": "AttributeError: 'list' object has no attribute 'get'", "selected_item": null, "fit_card_chars": null, "queued_ms": null, "agent_ms": null, "duration_ms": 0.1, "timings": null, "model_calls": 0, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:46:03.636+00:00", "request_id": "d9209cc82c1f", "route": "/ask", "query": "denim jacket under $50", "wardrobe": "example", "status": 200, "outcome": "model_unavailable", "error": "The search worked — it found Denim Jacket — Light Wash, Cropped ($42 on poshmark) — but the styling model couldn't be reached, so there's no outfit or fit card. The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com. Then run the same query again.", "selected_item": "lst_007", "fit_card_chars": null, "queued_ms": 0.0, "agent_ms": 881.6, "duration_ms": 882.2, "timings": {"parse_query": 0.1, "search_listings_mcp": 472.6, "suggest_outfit": 408.7, "total": 881.6}, "model_calls": 1, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:46:04.534+00:00", "request_id": "eafaec0e18e1", "route": "/ask", "query": "denim jacket under $50", "wardrobe": "example", "status": 200, "outcome": "model_unavailable", "error": "The search worked — it found Denim Jacket — Light Wash, Cropped ($42 on poshmark) — but the styling model couldn't be reached, so there's no outfit or fit card. The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com. Then run the same query again.", "selected_item": "lst_007", "fit_card_chars": null, "queued_ms": 0.0, "agent_ms": 383.5, "duration_ms": 384.0, "timings": {"parse_query": 0.0, "search_listings_mcp": 308.9, "suggest_outfit": 74.5, "total": 383.5}, "model_calls": 1, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:46:04.935+00:00", "request_id": "6450ac056c42", "route": "/ask", "query": "denim jacket under $50", "wardrobe": "example", "status": 200, "outcome": "model_unavailable", "error": "The search worked — it found Denim Jacket — Light Wash, Cropped ($42 on poshmark) — but the styling model couldn't be reached, so there's no outfit or fit card. The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com. Then run the same query again.", "selected_item": "lst_007", "fit_card_chars": null, "queued_ms": 0.0, "agent_ms": 362.5, "duration_ms": 363.0, "timings": {"parse_query": 0.0, "search_listings_mcp": 294.2, "suggest_outfit": 68.1, "total": 362.5}, "model_calls": 1, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:46:05.314+00:00", "request_id": "9b6e2d796554", "route": "/ask", "query": "denim jacket under $50", "wardrobe": "example", "status": 200, "outcome": "model_unavailable", "error": "The search worked — it found Denim Jacket — Light Wash, Cropped ($42 on poshmark) — but the styling model couldn't be reached, so there's no outfit or fit card. The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com. Then run the same query again.", "selected_item": "lst_007", "fit_card_chars": null, "queued_ms": 0.0, "agent_ms": 359.4, "duration_ms": 359.8, "timings": {"parse_query": 0.0, "search_listings_mcp": 295.9, "suggest_outfit": 63.4, "total": 359.4}, "model_calls": 1, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:46:05.689+00:00", "request_id": "f6c004664016", "route": "/ask", "query": "denim jacket under $50", "wardrobe": "example", "status": 200, "outcome": "model_unavailable", "error": "The search worked — it found Denim Jacket — Light Wash, Cropped ($42 on poshmark) — but the styling model couldn't be reached, so there's no outfit or fit card. The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com. Then run the same query again.", "selected_item": "lst_007", "fit_card_chars": null, "queued_ms": 0.0, "agent_ms": 395.4, "duration_ms": 395.8, "timings": {"parse_query": 0.0, "search_listings_mcp": 324.0, "suggest_outfit": 71.2, "total": 395.4}, "model_calls": 1, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
```
