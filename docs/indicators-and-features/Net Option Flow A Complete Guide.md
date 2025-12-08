---
title: "Net Option Flow: A Complete Guide"
layout: default
parent: Indicators & Features
grand_parent: Help Center
nav_order: 2
---

Net Option Flow (NOF) is a key feature in BigShort, providing traders with insights into market sentiment by analyzing real-time options activity. Whether you’re looking at [SmartFlow](https://intercom.help/bigshort/en/articles/10445405-smartflow-tab), [SF Segregated](/docs/getting-started/SF Segregated Tab/), or [Ultraflow](https://intercom.help/bigshort/en/articles/10442189-understanding-the-ultraflow-tab) in BigShort the Net Option Flow chart equips you with powerful tools to uncover trading opportunities.

This guide explains what Net Option Flow is, where to find it, and how to interpret the chart to integrate it into your trading strategy.

# **What is Net Option Flow?**

![](/assets/images/help/indicators-and-features/Net Option Flow A Co_Screenshot+2025-01-06+at+12_00_13+PM.png)

Net Option Flow visualizes activity in the options market. It tracks three key metrics:

  1. **Net Call/Put Flow** : The net premium of all buying and selling of calls and puts.

  2. **Net Unusual Call/Put Premium** : Net premium from large trades, such as sweeps or blocks.

  3. **Daily Running Accumulation of Net Call/Put Flow (NOFA)** : A running tally of net premium flows over the course of the trading day.


Net Option Flow (NOF) offers a unique and refined approach to analyzing options activity, addressing key limitations of traditional option volume metrics:

  1. **Differentiating Buys and Sells** :  
Traditional option volume treats buying and selling equally, counting 1 million contracts bought and 1 million contracts sold as the same. In contrast, NOF differentiates between buys and sells, with buys pointing up and sells pointing down. 

  
This differentiation helps traders clearly identify trends in buying and selling, offering a more nuanced view of market sentiment and potential turning points.  


  2. **Dollar-Weighted Reality** :  
Traditional option volume does not account for the value of trades. For example, 1,000 contracts bought for $0.01 are treated the same as 1,000 contracts bought for $10. NOF addresses this by weighting trades based on their dollar value:

     * Larger trades with higher premiums carry more weight, emphasizing their importance.

     * Small, low-dollar trades contribute proportionally less, reducing noise.  


  3. **Net Premium Flow** :  
While traditional volume simply adds up all activity (buys and sells combined), NOF takes it a step further by **deducting sells from buys**. This creates a net dollar-weighted metric that reflects the actual sentiment of the market participants, providing traders with a clearer understanding of the flow of money into calls and puts.  



🚀 **To the Moon:** BigShort is the only trading software out there with this approach to analyzing and displaying Option Flow directly in line with price charts for maximum usability by traders.

  


# **Where to Find the Net Option Flow Charts**

The Net Option Flow chart is visible in these sections of BigShort:

  * **[SmartFlow](https://intercom.help/bigshort/en/articles/10445405-smartflow-tab)**

  * **[SF Segregated](/docs/getting-started/SF Segregated Tab/)**

  * **[Ultraflow](https://intercom.help/bigshort/en/articles/10442189-understanding-the-ultraflow-tab)**


In each section, you’ll find the Net Option Flow chart, which visualizes the three key metrics.

# **Understanding the Net Option Flow Chart**

The Net Option Flow chart consists of three primary elements: **hills** , **bars** , and the **green line**. 

## **Hills: Net Call/Put Flow**

The hills represent **net premium flow** for calls and puts, color-coded and directional:

  * **Light Blue Hills** : Call flow

  * **Purple Hills** : Put flow

  * **Direction Matters** :

    * **Hills pointing up** indicate buying activity.

    * **Hills pointing down** indicate selling activity.


🔎 **Looking Closer:** In the standard BigShort 5-minute chart, each hill represents the net flow in that five minute period. That's why you will often see hills growing and shrinking during the current five minute period. Just like the price candlestick, it is a live reading of orders as they come in.

## **Bars: Unusual Call/Put Premium**

The bars that appear with the hills highlight **unusual options activity** , specifically large trades:

  * **Light Blue Bars** : Unusual call premium

  * **Purple Bars** : Unusual put premium

  * **Direction Matters** :

    * **Bars pointing up** indicate buying.

    * **Bars pointing down** indicate selling.


🔎 **Looking Closer:** Unusual activity is defined by large trades (typically over $1M in premium), including **sweeps** (urgent trades across multiple exchanges), **blocks** (large single-exchange trades), and **splits**.

## **Green Line: Daily Running Accumulation (NOFA)**

The green line represents the **cumulative net flow** of calls and puts over the course of the trading day, tracking whether there are more dollars flowing into bullish or bearish positions. It updates in real time to provide a broader view of market sentiment. If the green line is above zero on a 5min chart, this means that the net sum of past options trades throughout the day is positive. If the green line is below zero, this means that the net sum of past options trades throughout the day is negative.

## Examples

![](/assets/images/help/indicators-and-features/Net Option Flow A Co_Screenshot+2025-01-06+at+12_07_17+PM.png)

The chart above show the Option Flow for SPY for an entire trading day. Notice the very large blue hill downward during the morning. This is showing a 5 minute period with **significant** call selling. You can see the corresponding plummet in the green line (NOFA) because what was otherwise a morning of net positive signals was brought basically to zero by that huge wave of selling calls. 

![](/assets/images/help/indicators-and-features/Net Option Flow A Co_Screenshot+2025-01-06+at+12_58_33+PM.png)

Here we can see the first 45 minutes of trading on 12/18/24 for NVDA. This morning is clearly dominated by significant call buying (and some mild put selling). Both are bullish signals.

## Sweeps

![](/assets/images/help/indicators-and-features/Net Option Flow A Co_Screenshot+2025-01-06+at+1_21_31+PM.png)

From time to time you might also see colored vertical lines on the NOF chart. These indicate sweeps and are color coded.

  * **Golden** : a large, unusual option transaction that has been analyzed as "bullish”

  * **Bronze** : a large, unusual option transaction that has been analyzed as "bearish”

  * **Gray** : No Sentiment


# **How to Use Net Option Flow Effectively**

## **1\. Read Hills and Bars**

  * **Identify Buying vs. Selling** : Pay attention to the direction (up or down) of hills and bars.

  * **Watch Colors** :

    * **Light Blue** : Call activity

    * **Purple** : Put activity


![](/assets/images/help/indicators-and-features/Net Option Flow A Co_hill-example-2.png)

**💡 Tip:** While both buying and selling activity provide insights, buying is generally a stronger directional signal. For example, **buying calls** reflects a clear bullish sentiment, as it’s an outright bet on upward price movement. Conversely, **selling puts** , while also bullish, can be driven by strategies like collecting premiums or managing volatility, making it less directional. Similarly, **buying puts** is a stronger bearish signal than **selling calls** , as it represents a direct bet on downward price movement.

## **2\. Compare Spikes & Review Raw Numbers**

  * Look at the size of hills relative to previous days to gauge the significance of current activity. 

  * It is **critical** to remember that the Net Option Flow chart uses auto-scaling. This means that what looks like a huge spike might actually be quite small relative to that ticker. 


⚠️**Important:** This point cannot be stressed enough. Make sure you review historical NOF levels for the ticker you are looking at so you understand what actually constitutes big/small moves. Additionally, when you mouse over the chart you can see the raw numbers for NOF or Unusual Premium. 

## **3\. Know Your Ticker**

  * Net Option Flow patterns vary across tickers. For example, a large spike in TSLA might mean something entirely different than a similar spike in SPY or QQQ. **Context is critical.**  



## **4\. Power Hour Caution**

  * Be cautious when interpreting Net Option Flow during the last hour of trading ("[Power Hour](https://intercom.help/bigshort/en/articles/10416277-why-we-don-t-trade-power-hour)"). Large institutional trades can distort typical sentiment patterns.


## **5\. Combine with Other Indicators**

  * As always, use Option Flow alongside price action, volume, or other BigShort indicators for a comprehensive analysis.

  * Confluence is king!  



# **Why Net Option Flow Works**

Option Flow provides a transparent view into options market sentiment. Here’s why it’s effective:

  1. **Leverage Signals Confidence** : Options involve significant leverage, making large trades a sign of high conviction.

  2. **Directional Clarity** : Buying calls is unambiguously bullish, while selling calls is bearish. Similarly, buying puts is bearish, and selling puts is bullish.

  3. **Smart Money Insight** : Large trades often originate from informed institutions or insider-level confidence, providing actionable signals for retail traders.  



# NOF Exhaustion

One important theory to keep in mind when using Net Option Flow (NOF) is the concept of **NOF Exhaustion**. This occurs when the indicator trends strongly in one direction for an extended period, and then begins to reverse. The resulting move in the opposite direction often tends to be outsized.

The theory behind NOF Exhaustion is that when one side of the market (buying or selling) becomes overly crowded, it can create an imbalance. A reversal is then triggered by relatively smaller volumes as the dominant side "tires out."

Picture two opponents both pulling a rope in tug of war. Person 1 is exerting 100% of their strength...pulling with everything they can. But they eventually tire out. And when they do and their muscles finally release from the effort of exertion the other opponent is going to gain a lot of ground even if they are only pulling with the same effort they were before.

![](/assets/images/help/indicators-and-features/Net Option Flow A Co_6-nof-exhaustion-example-1.png)

  


# Martian Net Option Flow

As of April 2025, "Martian Net Option Flow" and "Martian NOFA" were added as th default to three charts - [SF Segregated](/docs/getting-started/SF Segregated Tab/), [SmartFlow](/docs/indicators-and-features/Understanding SmartFlow and MomoFlow Indicators/), [UltraFlow](https://help.bigshort.com/en/articles/10442189-understanding-the-ultraflow-tab). "Martian Net Option Flow" and "Martian NOFA" was discovered by one of our own users (@Martian) and displays Net Option Flow slightly differently by subtracting the Net Unusual Option Premium from the Net Option Flow.   
  
NOF is made of 2 components: Regular Options Flows and Unusual Options Flows.

Classic NOF shows both together.

Martian NOF only shows Regular Options Flows. Though in the chart UO bars are still shown, they are not used for the hills or NOFA.   
  
To activate the original NOF with slightly different math, simply go to Chart Settings and click on "Net Option Flow (beta)". Using both can yield additional insights to advanced users.  


![](/assets/images/help/indicators-and-features/Net Option Flow A Co_Screenshot+2025-04-24+at+3_50_13 PM.png)

  


# **Conclusion**

BigShort's novel Net Option Flow is a versatile and powerful tool for understanding market sentiment and identifying trading opportunities. By tracking net flow, unusual activity, and cumulative trends, you can uncover insights that set your trading apart.

If you haven't already, check out our [Guide for New Users](/docs/getting-started/Getting Started with BigShort - New Users/) to see who NOF can be folded into an overall strategy.