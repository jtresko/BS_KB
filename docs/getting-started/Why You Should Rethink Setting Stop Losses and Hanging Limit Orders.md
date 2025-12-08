---
title: "Why You Should Rethink Setting Stop Losses and Hanging Limit Orders"
layout: default
parent: Getting Started
grand_parent: Help Center
nav_order: 15
---

Stock traders commonly use hanging [limit orders](https://www.investopedia.com/terms/l/limitorder.asp) to enter trades at lower prices or to secure profits at higher prices. Traders also use stop loss orders, stop-limit orders, or trailing stops to limit losses and protect capital. Despite their prevalence, these order types are ultimately harmful to traders.

![](/assets/images/help/getting-started/Why You Should Rethi_ChatGPT+Image+May+25,+2025,+07_49_45+PM.png)

# The Importance of Price Targets

Traders who consider these order types to be the cornerstone of their strategies have their hearts in the right place. They believe that by setting their orders in advance, they're taking a disciplined approach to risk management by inoculating themselves against the temptation to move their price targets out of emotion. But like many things in life, good intentions can lead to tragically bad results.

# The Problem with Stop Loss Orders and Hanging Limit Orders

Market makers and high-frequency trading algorithms (HFT algos) can see the [depth of the market](https://quantifiedtrader.com/understanding-different-levels-of-market-depth-information-for-traders/) in their order book, which means they can see price levels where buy and sell orders are clustered, and they can see the proportion of these orders that were placed by weak-handed retail traders. By aggregating this data, market makers have a far better view of where real support and resistance levels are, and can take advantage of this data to avoid these levels until they're sure that they have enough firepower to break through them.

Imagine you’re in a long position with a stop loss set at $22. Meanwhile, there’s a cluster of buy orders just below at $21. Market makers know that the real equilibrium price is higher, but they need to collect as many shares as possible before allowing the price to surge. So what's their strategy? Market makers push prices as close to $21 as possible without triggering those buy orders, and in doing so, collect your shares from your stop loss at $22 before taking the stock to $30. They do this in a very short time frame, so the buyers at $21 don't have time to react. As market makers drive the price up, these $21 buyers, feeling frustration and FOMO, raise their entry targets, which adds fuel to the rally. Once market makers have amassed enough shares to overpower the $21 buyer group, they unload them just beneath the next “real” resistance level. And the cycle repeats.  
  
This example demonstrates that setting hanging limit orders and stop loss orders is like playing poker with your cards face up. If your opponents can see when you have a good hand, they will fold to you and minimize your gains. Conversely, if they can see your bad hands, they'll bet into you and maximize your losses. Setting limit orders and stop loss orders allow market makers to manipulate the market price to trigger these orders only when it suits them, and to steer clear when it doesn't.

# The Problem with Market Orders

You might think then that the solution is to use a [market order](https://www.investopedia.com/terms/m/marketorder.asp), but these are also problematic. Market orders are executed immediately at the best available price, but this immediacy is exploited by market makers. They'll move the bid/ask within milliseconds of your order hitting the tape to give you the worst possible price for your market orders. This is especially true in thinly traded markets, where the bid/ask is often not liquid enough to absorb your order. This is known as price slippage, when a market order is executed at a significantly different price from the current market price.

# The Problem with “Hidden” Orders

So then, what about hidden orders? Traders use hidden orders, which are not visible on the public order book, to combat the shortcomings of other order types. On platforms like Interactive Brokers, hidden orders can be created by selecting the "Hidden" attribute. Once submitted, the order is intended to be concealed from the market.

However, the degree to which these orders are actually hidden is dubious. While not publicly visible, they can still be tracked by detecting patterns in the systematic replenishment of liquidity via level III order-level market data. The high level of market depth offered by Level III quotes is only available to, you guessed it: **market makers.**

To make matters worse, exchanges also prioritize visible orders over hidden ones, meaning a hidden order will not be filled until [all visible orders at the same price level are executed](https://www.cboe.com/insights/posts/hide-and-seek-hidden-liquidity-on-u-s-exchanges/). In some cases, Interactive Brokers may simulate hidden orders on exchanges, in essence revealing the “hidden” order [to the market](https://www.interactivebrokers.com/en/trading/orders/hidden.php).

So while hidden orders have some advantages over hanging limit orders, they're not completely invisible, and their execution is often suboptimal. 

# Protect Your Interests with Spodin

Given the significant downsides of using these order types or other alert systems embedded in brokerage accounts, the safest way to execute your trades is to wait until your desired price hits, and only then submit a limit order for either the midpoint or the bid/ask such that it executes immediately. [Spodin](https://help.bigshort.com/en/articles/10389267-what-the-hell-is-spodin) is our proprietary closed-system alert; with it, you can set personalized price alerts that are sent directly to your phone via call or text when specific price levels are reached. By using Spodin, you can rest assured that your price alerts remain confidential and secure, which eliminates the risk of your trading intentions being exploited by market makers.

# Conclusion

While hanging limit orders, market orders, hidden orders, and stop losses may seem like straightforward trading tools, they come at a significant cost due to their vulnerability to market manipulation. By leveraging our platform's unique features such as Spodin, our subscribers are able to better protect themselves from market maker shenanigans.