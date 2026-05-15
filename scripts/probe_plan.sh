#!/usr/bin/env bash
# Probe each FMP endpoint the harvester uses against the local .fmp_key.
# Prints a table: status | endpoint | (optional reason / preview).
# Throttled at 300 calls/min (200ms between calls) to match Starter limits.

set -euo pipefail
KEY=$(cat .fmp_key | tr -d '\r\n')
BASE="https://financialmodelingprep.com/stable"
SYM_US="AAPL"
SYM_NONUS="0700.HK"
GAP=0.25  # seconds between requests (~240 RPM, comfortably under 300)

probe() {
  local path="$1"
  local label="${2:-$path}"
  # Append apikey using a separator that's correct for paths that already have a query string.
  local sep="?"
  [[ "$path" == *\?* ]] && sep="&"
  local url="${BASE}/${path}${sep}apikey=${KEY}"
  # Status + first 80 chars of body.
  local out status body
  out=$(curl -sS -o /tmp/_fmp_body.txt -w "%{http_code}" "$url" || echo "ERR")
  status="$out"
  body=$(head -c 120 /tmp/_fmp_body.txt | tr -d '\r' | tr '\n' ' ')
  # Length of body (helps spot empty 200s)
  local nbytes
  nbytes=$(stat --printf="%s" /tmp/_fmp_body.txt)
  printf "%-6s  %-60s  bytes=%-5s  %s\n" "$status" "$label" "$nbytes" "$body"
  sleep "$GAP"
}

echo "=== Directory ==="
probe "company-symbols-list" "directory.company_symbols"
probe "financial-statement-symbol-list" "directory.financial_symbols"
probe "actively-trading-list" "directory.actively_trading"
probe "etf-list" "directory.etf_list"
probe "commodities-list" "commodity.commodities_list"
probe "forex-list" "forex.forex_list"
probe "index-list" "indexes.index_list"

echo ""
echo "=== Statements (annual) ==="
for ep in income-statement balance-sheet-statement cash-flow-statement \
          key-metrics ratios enterprise-values \
          income-statement-growth balance-sheet-statement-growth \
          cash-flow-statement-growth financial-growth \
          owner-earnings revenue-product-segmentation revenue-geographic-segmentation; do
  probe "${ep}?symbol=${SYM_US}&limit=2" "statements.${ep}"
done

echo ""
echo "=== Statements (quarter — known paywall on Starter) ==="
probe "income-statement?symbol=${SYM_US}&period=quarter&limit=2" "statements.income (quarter)"
probe "key-metrics?symbol=${SYM_US}&period=quarter&limit=2" "statements.key_metrics (quarter)"

echo ""
echo "=== Calendar ==="
probe "dividends-calendar?from=2026-05-01&to=2026-05-31" "calendar.dividends"
probe "earnings-calendar?from=2026-05-01&to=2026-05-31" "calendar.earnings"
probe "ipos-calendar?from=2026-01-01&to=2026-06-30" "calendar.ipos"
probe "splits-calendar?from=2026-05-01&to=2026-05-31" "calendar.splits"

echo ""
echo "=== Chart (US symbol — daily) ==="
for ep in historical-price-eod/light historical-price-eod/full \
          historical-price-eod/non-split-adjusted historical-price-eod/dividend-adjusted; do
  probe "${ep}?symbol=${SYM_US}&from=2026-04-01&to=2026-04-30" "chart.${ep}"
done

echo ""
echo "=== Chart (intraday — US symbol) ==="
for tf in 1min 5min 15min 30min 1hour 4hour; do
  probe "historical-chart/${tf}?symbol=${SYM_US}&from=2026-04-25&to=2026-04-30" "chart.intraday_${tf}"
done

echo ""
echo "=== Commodity / Forex / Indexes (sample) ==="
probe "historical-price-eod/full?symbol=GCUSD&from=2026-04-01&to=2026-04-30" "commodity.historical_price_full (GCUSD)"
probe "historical-price-eod/full?symbol=EURUSD&from=2026-04-01&to=2026-04-30" "forex.historical_price_full (EURUSD)"
probe "historical-price-eod/full?symbol=%5EGSPC&from=2026-04-01&to=2026-04-30" "indexes.historical_price_eod_full (^GSPC)"

echo ""
echo "=== Technical indicators (US symbol) ==="
for ind in sma ema rsi standarddeviation williams adx; do
  probe "technical-indicators/${ind}?symbol=${SYM_US}&periodLength=14&timeframe=1day&from=2026-04-01&to=2026-04-30" "ti.${ind}"
done

echo ""
echo "=== Analyst ==="
probe "analyst-estimates?symbol=${SYM_US}&period=annual&page=0&limit=5" "analyst.financial_estimates (annual)"
probe "analyst-estimates?symbol=${SYM_US}&period=quarter&page=0&limit=5" "analyst.financial_estimates (quarter)"
probe "ratings-snapshot?symbol=${SYM_US}" "analyst.ratings_snapshot"
probe "ratings-historical?symbol=${SYM_US}&limit=5" "analyst.historical_ratings"
probe "price-target-summary?symbol=${SYM_US}" "analyst.price_target_summary"
probe "price-target-consensus?symbol=${SYM_US}" "analyst.price_target_consensus"
probe "grades-consensus?symbol=${SYM_US}" "analyst.stock_grades_summary"

echo ""
echo "=== DCF ==="
probe "discounted-cash-flow?symbol=${SYM_US}" "dcf.dcf_valuation"
probe "levered-discounted-cash-flow?symbol=${SYM_US}" "dcf.levered_dcf"

echo ""
echo "=== News ==="
for variant in general-latest press-releases-latest stock-latest crypto-latest forex-latest; do
  probe "news/${variant}?page=0&limit=5" "news.${variant}"
done

echo ""
echo "=== Insider / 13F / Senate ==="
probe "insider-trading/latest?page=0&limit=5" "insider_trades.latest"
probe "institutional-ownership/latest?page=0&limit=5" "form13f.latest_filings"
probe "senate-latest?page=0&limit=5" "senate.latest"
probe "house-latest?page=0&limit=5" "senate.house_latest"

echo ""
echo "=== Economics ==="
probe "treasury-rates?from=2026-04-01&to=2026-04-30" "economics.treasury_rates"
for ind in GDP CPI UNRATE FEDFUNDS DFF DCOILWTICO; do
  probe "economic-indicators?name=${ind}&from=2026-01-01&to=2026-04-30" "economics.economic_indicators (${ind})"
done

echo ""
echo "=== Market Performance ==="
probe "historical-sector-performance?sector=Technology&from=2026-04-01&to=2026-04-30" "market_perf.historical_sector"
probe "biggest-gainers" "market_perf.biggest_gainers"
