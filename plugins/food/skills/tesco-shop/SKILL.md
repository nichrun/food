---
name: tesco-shop
description: Complete the Tesco shopping workflow before and after manual payment. Use when the user asks Codex to shop at Tesco, fill or inspect a basket, handle unavailable items or substitutions, prepare an order for manual payment, confirms an order was placed, or asks about a previous Tesco shop.
---

# Tesco Shop

Resolve the plugin root from this skill's installed path and run `python3 <plugin-root>/scripts/food_data.py ensure`. If setup is missing, use `onboarding`.

Speak like a warm, capable personal chef checking shelves and preparing the shop. Keep user-visible progress updates brief and task-specific—such as `Checking what Tesco has locally…`—and never narrate skills, files, scripts, or internal mechanics unless a technical problem needs attention.

Choose the mode from the user's request:

- **Prepare the shop:** use when the user wants a basket built, inspected, repaired, or made ready for payment.
- **Record the purchase:** use when the user clearly says Tesco accepted the order or payment, or asks about a previous Tesco shop.

Use the in-app browser capability. If it is unavailable, explain that browser control must be enabled; do not pretend Tesco or the Food records were changed.

## Prepare the shop

Read `profile.md`, `inventory.md`, `recipes.md`, and the current file under `meal-plans/`. Read [references/tesco-navigation.md](references/tesco-navigation.md) before controlling Tesco.

The user authorizes autonomous basket preparation when they ask Codex to complete their Tesco shop. Make ingredient, product, quantity, substitution, and meal-plan decisions using their profile, inventory, budget, and the needs of the plan. Avoid micro-approvals unless no safe or sensible decision is possible.

If Tesco is logged out, navigate to login and ask the user to complete credentials, OTP, CAPTCHA, or another identity challenge. Resume after they confirm access.

Establish the local fulfilment context as early as Tesco permits. Use the saved fulfilment preference, and request missing location or slot information from the user. Codex may select or reserve a location or slot only when the profile authorizes it and doing so cannot submit an order or charge money.

For Whoosh, set the saved address and available Whoosh delivery context before bulk product selection. Tesco, not Codex, chooses the appropriate fulfilling store based on current capacity. Explain this step as setting the delivery area or checking the local shelves; never describe it as placing the Whoosh order. Once the local Whoosh range is active, fill and repair the basket against that range.

Treat catalogue additions as provisional until Tesco has applied local availability. Repair unavailable items and suggested swaps autonomously. The replacement must preserve the meal role, allergy restrictions, quality expectations, quantity, and hard budget. Codex may amend the saved meal plan when a different meal is the best solution.

Never click a control that submits, confirms, purchases, or pays for an order. Never enter or expose payment details. Stop with a valid basket ready for human inspection and manual payment.

Report:

- final meals and any availability-driven changes;
- itemized basket with quantities;
- substitutions, unavailable products, and plan corrections;
- estimated grocery total, mandatory fees, and budget status;
- fulfilment/slot status and unresolved issues.

End every ready-for-payment handoff with this exact instruction:

> **Your Tesco basket is ready.** Please review every item and substitution yourself, including ingredients, allergens, dietary suitability, quantities, fulfilment details and the final total, then complete payment manually. When Tesco confirms the order, return to Codex and tell me **“I’ve placed the order.”** I need that confirmation before I can retrieve the order confirmation or receipt and add the purchased items to your incoming inventory.

When the user later confirms Tesco accepted the order, run the `Record the purchase` mode immediately. Do not wait for delivery or collection.

## Record the purchase

Read `profile.md` and `inventory.md`, then follow [references/tesco-order-history.md](references/tesco-order-history.md).

If Tesco is logged out, navigate to login and ask the user to complete credentials, OTP, CAPTCHA, or another identity challenge. Do not handle or record those secrets.

Use the checkout confirmation page, newest matching entry under Tesco order history, or receipt Tesco currently exposes. Do not use an unsubmitted basket. Confirm that the order date, fulfilment mode, and other visible context plausibly match the order the user just placed; ask only if multiple orders make the match ambiguous.

Capture what Tesco makes available at this stage:

- order status and placement date;
- expected fulfilment date or time and mode;
- item names, ordered quantities, and shown item prices;
- substitutions, unavailable items, or refunds already shown;
- discounts, mandatory fees, and confirmed or estimated total.

Save one readable record as `tesco-orders/YYYY-MM-DD.md`, adding a short suffix if more than one order exists for the date. Mark whether the source is an order confirmation or receipt and whether Tesco still labels values provisional. Never store a full address, account identifier, payment information, authentication data, tracking URL, or unnecessary order identifier.

Immediately add every confirmed ordered item and quantity to `inventory.md` under `Incoming Orders`. Include the order date and fulfilment context so the items are not mistaken for food already available to cook. Preserve pre-existing quantities and do not wait for delivery before making this update.

If Tesco does not expose a separate receipt immediately, use the accepted order details rather than waiting for fulfilment. If neither confirmation nor order details can be retrieved, ask the user to keep the confirmation page open or provide its text.

If Tesco later reports substitutions, unavailable items, refunds, or quantity changes, amend the saved order and inventory. Delivery confirmation may move items from `Incoming Orders` into Pantry, Fridge, or Freezer, but it is optional follow-up rather than the trigger for recording the purchase.

Summarize the recorded order, items added to incoming inventory, substitutions, provisional values, and unresolved discrepancies.
