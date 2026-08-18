# Tesco Order History

Use visible semantic labels and current page state. Routes are navigation hints, not permanent contracts.

## Finding an order

1. Open Tesco order history, currently `/shop/en-GB/orders`.
2. Use the `Upcoming orders`, `Past orders`, and `Returns` tabs as appropriate.
3. Match the newest plausible order by placement date, fulfilment mode, status, and visible total. Ask only when multiple entries remain ambiguous.
4. Open `View order receipt` for the matching order.

## Reading the receipt

Tesco currently groups receipt items under headings such as `Fridge`, `Freezer`, and `Cupboard`. Capture the exact product name, quantity, and shown price from each group, then capture item count, subtotal, savings, mandatory fees, and total from the payment summary.

Do not capture, repeat, or save the delivery address, account details, payment method, card digits, tracking links, or an unnecessary order identifier even when they appear on the same page.

Treat receipt values as provisional when Tesco labels them that way or the order can still change. Preserve Tesco's distinction between ordered items, substitutions, unavailable items, and refunds.
