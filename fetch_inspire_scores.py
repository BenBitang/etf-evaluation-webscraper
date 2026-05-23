#!/usr/bin/env python3
"""
Fetch Inspire Impact Scores for all stocks in the Catholic ETF holdings CSV.
This script uses Playwright to render JavaScript and extract scores from inspireinsight.com.
"""

import pandas as pd
import asyncio
from pathlib import Path
import json
import time
import sys
from playwright.async_api import async_playwright


async def fetch_inspire_score(page, ticker):
    """
    Fetch the Inspire Impact Score for a given stock ticker.
    Returns the score as an integer, or None if not found.
    """
    url = f"https://inspireinsight.com/{ticker}/US"
    
    try:
        # Navigate to the page with domcontentloaded (faster than networkidle)
        response = await page.goto(url, wait_until="domcontentloaded", timeout=15000)
        
        if response and response.status == 404:
            print(f"  {ticker}: Not found (404)")
            return None
        
        # Wait a bit for JavaScript to render
        await page.wait_for_timeout(1000)
        
        # Wait for the score element to appear
        try:
            await page.wait_for_selector('[data-cy="impact-score"]', timeout=5000)
        except:
            print(f"  {ticker}: Score element not found")
            return None
        
        # Extract the score
        score_element = await page.query_selector('[data-cy="impact-score"]')
        if score_element:
            score_text = await score_element.text_content()
            score_text = score_text.strip()
            if score_text:
                # The score should be a number, possibly with +/- prefix
                score = int(score_text)
                print(f"  {ticker}: {score}")
                return score
        
    except Exception as e:
        error_msg = str(e)
        if "Timeout" in error_msg:
            print(f"  {ticker}: Timeout")
        else:
            print(f"  {ticker}: Error - {error_msg[:40]}")
        return None
    
    return None


async def main():
    # Read the minimal extracted file (ticker and name only)
    csv_file = Path(__file__).parent / "tickers_to_score.csv"
    
    print(f"Reading tickers from {csv_file}...")
    
    # Read the pre-extracted tickers and names
    df = pd.read_csv(csv_file)
    
    print(f"Found {len(df)} stocks to process")
    
    # Check if there's a partial results file to resume from
    output_file = csv_file.parent / f"inspire_scores_{time.strftime('%Y%m%d')}.csv"
    start_idx = 0
    
    if output_file.exists():
        print(f"\nResuming from previous run...")
        df = pd.read_csv(output_file)
        # Find the first row with missing score
        for idx, row in df.iterrows():
            if pd.isna(row.get('Inspire Impact Score')):
                start_idx = idx
                break
        print(f"Resuming from stock {start_idx} of {len(df)}")
    else:
        # Initialize the score column
        df['Inspire Impact Score'] = None
    
    # Use Playwright to fetch scores
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 720},
            extra_http_headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
            }
        )
        page = await context.new_page()
        
        print("\nFetching Inspire Impact Scores...")
        
        for idx, row in df.iterrows():
            if idx < start_idx:
                continue
                
            ticker = row['Ticker']
            print(f"[{idx + 1}/{len(df)}] Processing {ticker}...", end="")
            sys.stdout.flush()
            
            score = await fetch_inspire_score(page, ticker)
            df.at[idx, 'Inspire Impact Score'] = score
            
            # Save progress every 10 stocks
            if (idx + 1) % 10 == 0:
                df.to_csv(output_file, index=False)
                print(f"  [saved progress]")
            
            # Be respectful to the server - add a small delay
            await asyncio.sleep(0.3)
        
        await browser.close()
    
    # Final save
    df.to_csv(output_file, index=False)
    
    print(f"\n✓ Results saved to {output_file}")
    print(f"\nSummary:")
    print(f"  Total stocks: {len(df)}")
    print(f"  Scores found: {df['Inspire Impact Score'].notna().sum()}")
    print(f"  Scores not found: {df['Inspire Impact Score'].isna().sum()}")
    
    # Show some statistics
    scores = df['Inspire Impact Score'].dropna()
    if len(scores) > 0:
        print(f"\nScore Statistics:")
        print(f"  Highest (most conservative): {int(scores.max())}")
        print(f"  Lowest (most progressive): {int(scores.min())}")
        print(f"  Average: {scores.mean():.1f}")
        print(f"  Median: {scores.median():.0f}")


if __name__ == "__main__":
    asyncio.run(main())
