---
title: "Getting Started with BigShort - New Users"
layout: default
parent: Getting Started
nav_order: 4
---

First, before the trading day starts, or even on the previous day, we recommend taking a look at the [Seasonality Tab](/docs/getting-started/Understanding the Seasonality Tab/). This shows the historic performance of the last 30 years of SPY per calendar date. While Seasonality is a weaker force in the market, it’s good to give a general directional bias for the day.  


**If you’re just getting started, we recommend looking at the[SF Segregated chart.](/docs/getting-started/SF Segregated Tab/)**

![](/assets/images/help/getting-started/Getting Started with_0-chart.png)

# Introduction

In the upper left corner, you can search by ticker and date. We have performant 5 minute charts for all tickers for the S&P500 and Nasdaq going back **six years.**  


In the upper right corner, you can see the current values for [SmartFlow and MomoFlow](/docs/indicators-and-features/Understanding SmartFlow and MomoFlow Indicators/). Under that, you can see all of our chart tools. Here, you can zoom in, draw lines, change your chart settings, use the tool tip to view all current values in a static, moveable and resizable pane, and see all option flow detail. You can see a description of all chart settings by hovering over the info icon. We offer these options because every trader has their own preference, for new users we recommend using the Recommended Settings.  
  
In my examples I’ll be going over how to trade with SPY. For other tickers, look at the historical 5 minute chart to determine whether the stock is omo or smart controlled, and what the meaningful Momo/NOF levels are.  


# Candles & Dark Pools

The first pane is the Candlestick Pane. Here we display dark pool prints directly on the chart, so you can easily see support and resistance levels. Price action is the number one indicator, that’s why it’s the biggest pane. [Dark Pools](/docs/indicators-and-features/Understanding Dark Pools and DarkFlow in BigShort/) are our number two indicator. When there are a lot of dark pools clustered around the same price range, or big dark pools, above the current price this level acts as resistance, and below the current price this level acts as support.

![](/assets/images/help/getting-started/Getting Started with_2-chart-1.png)

![](/assets/images/help/getting-started/Getting Started with_darkpool-support-4.png)

![](/assets/images/help/getting-started/Getting Started with_Darkpool-resistance-3.png)

**🔎 Looking Deeper:** Lots of Dark Pools below the current price tend to drive price up. Lots of Dark Pools above the current price tend to drive price down. Dark Pool signals are even better when supported by other indicators in BigShort.

# GEX (Gamma Exposure)

You’ll see GEX as a default on our BigShort charts, as lines directly on the candlestick pane. We offer 0DTE, 7DTE, and all DTE as chart options, which you can toggle in Chart Settings. The green line is the call wall, the red line is the put wall, and the turquoise line is the Zero Gamma Flip. We’ve made reading GEX simple for our new users, the basic rule of thumb is:

Put wall rising (red line moving up) → bearish pressure

Put wall falling (red line moving down) → bullish pressure

Call wall rising (green line moving up) → bullish pressure

Call wall falling (green line moving down) → bearish pressure

![](/assets/images/help/getting-started/Getting Started with_gex+example.png)

**NOTE:** These rules are only applicable when green line is ABOVE the red line, which it is in most cases. If red line is above green, disregard these rules.

As with all indicators, look for a **confluence** of signals from multiple indicators to help strengthen your trading decisions.

The second pane is SmartFlow. Since this is the new user guide, just disregard this pane for now.

#   
MomoFlow

The third pane is MomoFlow.

![](/assets/images/help/getting-started/Getting Started with_2-chart-2.png)

Pay attention here. Momo is a proxy for dumb money, and so MomoFlow is an inverse indicator. The shadow bar is MomoFlow for a given 5 minute bar, and the red line is the accumulation of MomoFlow throughout the day. If you see a big shadow bar pointing down, that means momo is dumping, and market makers are buying the dump. Think of it as a seesaw: the more the momo majority is on one side, the less room there is for a further move in that price direction, and the more incentive market makers have to take price in the opposite direction.

![](/assets/images/help/getting-started/Getting Started with_4-momoflow-example-2-1.png)

Scaling is important, especially in the beginning of the day, because the pane will resize to fit the bars, so be sure to check the absolute value of MomoFlow and compare it to historical norms. The larger the better.  


💡**Tip:** MomoFlow shadow bars tend to work better on non-Mondays, as SPY tends to be more momo-controlled on Mondays, especially Monday mornings.

It’s also good to see multiple shadow bars pointing in the same direction in succession, this strengthens the signal.  


# OptionFlow

The fourth pane is OptionFlow. Be sure to have our beta feature, [Net Option Flow](/docs/indicators-and-features/Net Option Flow A Complete Guide/) (NOF), turned on in your chart settings. You should see purple and blue hills, pointing both up and down.

![](/assets/images/help/getting-started/Getting Started with_3-chart-3.png)

Scaling is important, especially in the beginning of the day, because the pane will resize to fit the bars, so be sure to check the absolute value of NOF and compare it to historical norms.  
  
Traditional option volume registers 1 million contracts bought and 1 million contracts sold as the same. Net Option Flow differentiate between buys and sells, with buys pointing up and sells pointing down. This implies a directional bias. If options are being bought, they point up, if options are being sold, they point down. In general, buying calls and selling puts are bullish, selling calls and buying puts are bearish. 

![](/assets/images/help/getting-started/Getting Started with_hill-example-2.png)

Traditional option volume also doesn’t account for the amount of money going into the trades that comprise it. With options volume, 1000 contracts bought for 1 cent registers the same as 1000 contracts bought for $10. With Net Option Flow, we weigh the latter 1000x more heavily. We also deduct the buys and sells from each other, whereas traditionally, they are just all added up to create option volume. This is a novel approach for displaying options flow that reveals the net dollar-weighted reality.  
  
This green NOFA line shows the overall options sentiment for a given time period, and tracks whether there are more dollars flowing into bullish or bearish positions. If the green line is above zero on a 5min chart, this means that the net sum of past options trades throughout the day is positive. If the green line is below zero, this means that the net sum of past options trades throughout the day is negative. We can also observe the magnitude of movements in the green NOFA line to see how big the current flow is relative to what occurred prior. We can think of NOFA as an accumulation of inventory (positive or negative) throughout the day, which has longer term implications than the bar by bar NOF (net option flow for 1 candle). Read more about Net Option Flow [here](/docs/indicators-and-features/Net Option Flow A Complete Guide/).  


📝 **Note:** Selling options is not as strong of an indicator as buying options, for example call buying is more bullish than the same amount of put selling.

![](/assets/images/help/getting-started/Getting Started with_5-smartflow-1.png)

# Net Option Flow/MomoFlow Exhaustion:

One theory to keep in mind as you start trading, is that for both Net Option Flow and MomoFlow, when the indicator trends hard in one direction for a while, when things start to go in the opposite direction, that opposite direction move tends to be outsized. The theory is that if one side gets too crowded, a reversal can be triggered by a much smaller volume.  
  
Imagine there are two opponents pushing against a ball. One opponent is exerting with 100% of their strength, and eventually tires out. Once they’re tired, the other opponent can be easily overcome with much less strength than was required before the first opponent became tired.

![](/assets/images/help/getting-started/Getting Started with_7-momo-exhaustion-example.png)

![](/assets/images/help/getting-started/Getting Started with_6-nof-exhaustion-example-1.png)

#   
SimSearch

UltraFlow SimSearch shows the 5 trading days with the most similar price action to today’s, and shows how those days played out. It activates after the first 30 minutes of the day and then updates every 2 seconds. It’s good to keep the SimSearch chart open in another window to see the potential patterns of the day. Read more about SimSearch [here.](/docs/indicators-and-features/Similarity Search (SimSearch)/)

![](/assets/images/help/getting-started/Getting Started with_8-simsearch.png)

When trading, look for directional alignment in as many indicators as possible, and be cautious when the indicators conflict.  


# Indicators in order of importance:

  1. Price Action

  2. Honey Badger Days

  3. Dark Pool Prints

  4. Insider Trades

  5. Momo Shadow Bars/GEX (tied)

  6. NOF

  7. Short Exempt

  8. SimSearch

  9. Manipulation (_disregard if you’re new, only for professionals, and only for specific high-volume situations_)

  10. Golden and Bronze Sweeps

  11. Seasonality  



# Conclusion

If you’re a new trader, start by focusing just on price action, dark pool prints, NOF and shadow bars. Avoid trading power hour (the last hour of trading) as that's when a lot of dumb money and blind institutional money flood the market, so anything goes. Master these before you move on to the Advanced Guide, which is coming soon.