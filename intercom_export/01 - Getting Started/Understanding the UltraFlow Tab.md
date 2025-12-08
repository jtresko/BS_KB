---
title: "Understanding the UltraFlow Tab"
source: "https://help.bigshort.com/en/articles/10442189-understanding-the-ultraflow-tab"
collection: "Getting StartedEverything you need to get going.By Matt and 1 other2 authors16 articles"
---

# Overview

The UltraFlow tab in BigShort is a powerful tool designed to provide traders with a holistic view of market activity within different indexes. By aggregating data from all constituent tickers, UltraFlow offers insights into the collective flow of dollars, trading volume, and momentum across the index. This unique perspective allows traders to identify trends, manipulations, and anomalies that may not be apparent when analyzing a single stock or ETF.

🔍 **To Clarify:** For example, when you look at Net Option Flow for SPY in UltraFlow, you are not seeing the puts and calls being traded for the SPY ticker, you are actually seeing the sum of all puts and calls of all 500 companies that comprise the S&P 500! _(Yes, this is a crazy amount of data, but we still bring it to you in real time.)_

# UltraFlow Indexes

[![](https://downloads.intercomcdn.com/i/o/u9e1zc58/1346519280/2beec111d1ce679ab5a8d8968df6/Screenshot+2025-01-22+at+8_46_49+AM.png?expires=1765215000&signature=3cbbc48f9b7330382d3dd9a414a10fc2e4e99ce681305dfa68e3216c051181d2&req=dSMjEMx%2FlINXWfMW1HO4zYTE0XE14gPTSwyS6uJW091o2a2QVSirVMuPpJmI%0AuxWxTXt%2FlP%2FE3wsPL1M%3D%0A)](https://downloads.intercomcdn.com/i/o/u9e1zc58/1346519280/2beec111d1ce679ab5a8d8968df6/Screenshot+2025-01-22+at+8_46_49+AM.png?expires=1765215000&signature=3cbbc48f9b7330382d3dd9a414a10fc2e4e99ce681305dfa68e3216c051181d2&req=dSMjEMx%2FlINXWfMW1HO4zYTE0XE14gPTSwyS6uJW091o2a2QVSirVMuPpJmI%0AuxWxTXt%2FlP%2FE3wsPL1M%3D%0A)

There are five indexes that can be analyzed with UltraFlow. All are available by accessing the dropdown above the chart. 

# Important Notes

  * **Ticker Inclusion:** UltraFlow data does not include the index itself. For example, UF QQQ shows the cumulative data for all 100 tickers tracked by the Invesco QQQ Trust but does not include data from the QQQ ticker.

  * **Cumulative Indicators:** SmartFlow, MomoFlow, Manipulation, and Net Option Flow all show the aggregate of the index's constituent tickers

  * **Index Indicators:** Price, Dark Pools, and MM Price Discovery all show activity on the Index itself.




🔍 **Looking Deeper:** SmartFlow and MomoFlow are calculated based on dollar-weighted values. This means flows are multiplied by share prices before aggregation, ensuring accurate representation of market activity.

# Why was UltraFlow created?

UltraFlow was developed to bridge the gap between ETF-level and individual stock-level insights. While SPY and other ETFs are derivatives of their underlying stocks, trading activity in the constituents doesn't always align perfectly with the ETF's movements. UltraFlow helps traders:

  * Spot divergences between constituent flows and ETF performance.

  * Identify institutional activity, such as simultaneous trades in major S&P 500 stocks.

  * Gain a deeper understanding of how collective stock movements influence overall market behavior.




# Navigating UltraFlow

[![](https://downloads.intercomcdn.com/i/o/u9e1zc58/1346575197/c7f4aaaa2d6921f716003304eeb8/BigShort-01-22-2025_09_18_AM.png?expires=1765215000&signature=ae031532ee8a30be97ceb4755ac1d51be5a86313278a779cebc6f81509a08f38&req=dSMjEMx5mIBWXvMW1HO4zTb3RqBDfDSyWNRVbPBeMvjfsdm39PEhPtvTRkm1%0AqokBtZYFSaxuzUnQd0w%3D%0A)](https://downloads.intercomcdn.com/i/o/u9e1zc58/1346575197/c7f4aaaa2d6921f716003304eeb8/BigShort-01-22-2025_09_18_AM.png?expires=1765215000&signature=ae031532ee8a30be97ceb4755ac1d51be5a86313278a779cebc6f81509a08f38&req=dSMjEMx5mIBWXvMW1HO4zTb3RqBDfDSyWNRVbPBeMvjfsdm39PEhPtvTRkm1%0AqokBtZYFSaxuzUnQd0w%3D%0A)

## 1\. Date & Ticker

In the upper left you can select one of our five UltraFlows and the date you want to view. It will default to today's date.

This area also shows the current price information for the ticker of the UltraFlow you selected.

## 2\. SmartFlow, MomoFlow, and Manipulation Highlights

If you are looking at today, these three gears show the current SF, MF, and Manipulation accumulation tallies. This gives a quick-glance readout of the action of the day.

## 3\. Chart Timeframes

These buttons allow you to switch between a 5min candle chart (default) and other times based on your needs. You can also turn a one week historical view for broader context.

This is also where you can find the button to activate SimSearch, [a feature so cool it needs it's own artcile!](https://intercom.help/bigshort/en/articles/10279839-similarity-search-simsearch)

## 4\. Chart Controls

These buttons provide various additional info and chart tools.

  1. **Zoom** : hides everything other than the charts

  2. **Line Tool:** add a draggable, resizable line to the chart

  3. **Chart Settings:** an assortment of settings and customizations to tailor the chart to your needs




💡 **Tip:** On days where a massive NOF spike has skewed the scale of the Net Option Flow chart so much that it's impossible to read the chart well, you can experiment with turning on NOF Zoom in the chart settings. This rescales the NOF chart area and makes things easier to see. But be careful and make sure to mouse over and read the true values of the hills and bars in the tooltip when you have NOF Zoom turned on, or else you might confuse small spikes for large ones.

## 5\. Candlestick Chart

The largest and most important pane in the chart area. Here you can see the price candlesticks and [dark pools](https://intercom.help/bigshort/en/articles/10280483-understanding-dark-pools-and-darkflow-in-bigshort), along with other indicators like SMA and Bollinger Bands if you have enabled them in your chart settings.

💡 **Tip:** Remember that price and dark pools are for the ETF ticker (eg: SPY), not an aggregation of the constituent tickers.

## 6\. SmartFlow (SF) & **MomoFlow (MF)**

This displays the cumulative SF and MF data for all constituent tickers of the index you selected. For more information on this chart, [click here](https://intercom.help/bigshort/en/articles/10361455-understanding-smartflow-and-momoflow-indicators).

## 7\. Manipulation

This chart shows the [Manipulation and MM Price Discovery](https://intercom.help/bigshort/en/articles/10444514-manipulation-and-market-maker-price-discovery) data. MM Price Discovery is reported for the index ticker and Manipulation is showing the sum of the constituent tickers.

## 8\. Net Option Flow

The Net Option Flow (NOF) chart visualizes real-time sentiment in the options market by tracking net call and put premiums, unusual activity, and daily cumulative flow for all constituent tickers of the index selected. So it's not just buys and sells of calls and puts on SPY for example, but the sum of all buys and sells of calls and puts of MMM, AOS, ABT, ABBV, ACN, and the other 495 companies in the S&P 500.

For more information on this indicator, [click here](https://intercom.help/bigshort/en/articles/10354751-net-option-flow-a-complete-guide).

## 9\. Time Scaling

This slider allows you to adjust the start and/or end time of the current chart, effectively zooming in or out.

# Tips for Using UltraFlow Effectively

  1. **Compare with ETF Data:** Use UltraFlow alongside SPY or QQQ data to identify divergences and potential opportunities.  
​

  2. **Monitor Smart and Momo Flows:** These flows, calculated in dollars, can highlight where money is moving within the index, potentially signaling shifts in market sentiment.  
​

  3. **Engage with the Community:** Share observations and strategies in the BigShort community. Crowd-sourced insights can provide new ways to interpret UltraFlow data.




# Future Developments

While UltraFlow is already a powerful tool, its full potential lies in how traders use and interpret the data. BigShort is actively exploring ways to enhance its functionality and provide more definitive guidance on how to incorporate UltraFlow into trading strategies. Stay tuned for updates and new features!

* * *

**_Disclaimer:_**  
​ _The information provided in this article is for educational and informational purposes only and should not be considered as financial advice. BigShort does not provide personalized investment recommendations or advice, and you should not make any trading or investment decisions based solely on the content of this article. Trading in the stock market involves significant risk, including the potential loss of your entire investment. Past performance of our tools, indicators, or any referenced strategies does not guarantee future results. Always do your own research and consult with a qualified financial advisor before making investment decisions. Use of our platform and its features is at your own risk._
