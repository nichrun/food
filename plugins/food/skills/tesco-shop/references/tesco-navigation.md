# Tesco Browser Navigation

This is the initial Tesco operating playbook. Prefer visible semantic labels and current page state over brittle coordinates, assumed element order, or stale URLs. Refine this reference only after observing stable behavior in real trials.

## Safety boundary

- Control the basket, fulfilment context, quantities, and substitutions.
- Do not submit an order, purchase, or payment.
- Do not enter, reveal, or save credentials, OTPs, payment details, full addresses, account identifiers, or tracking URLs.
- Let the user complete login challenges and manual payment.

## Establish local availability early

Tesco can expose products in the general catalogue that the local fulfilling store cannot supply. Availability may become accurate only after Tesco knows the fulfilment mode, location, or slot.

1. Open Tesco Groceries or Whoosh as appropriate.
2. Inspect whether the user is signed in and whether a fulfilment mode, location, store, or slot is already active.
3. Apply the profile's preferred mode and authorized slot behavior. Ask only for missing information that cannot be obtained safely from the signed-in session.
4. Confirm the local context before doing the bulk of product selection whenever Tesco permits it.
5. If Tesco reveals local availability only later, continue provisionally and perform the mandatory repair pass before handoff.

Do not assume Whoosh is always the correct route. Test ordinary home delivery, collection, and Whoosh behavior during development and use whichever mode the profile requests.

### Whoosh sequence

Tesco's current documented flow exposes Whoosh through `Book a slot` or `Shop Whoosh`. The address can be selected there before shopping, and Tesco assigns the fulfilling store based on current capacity. Product range can vary by the assigned store.

1. Before bulk searching, open `Book a slot` or `Shop Whoosh` and select the saved delivery address without reading or recording the full address.
2. Select the available Whoosh delivery context or time frame when the profile or current request authorizes it. This establishes local shopping context; it is not checkout and does not place or pay for an order.
3. Do not attempt to force a particular store unless Tesco explicitly offers that choice. Confirm the Whoosh context Tesco assigned and note any checkout countdown.
4. Only then search and add the bulk of the products, so results reflect the locally assigned range as closely as the site permits.
5. Before handoff, inspect the basket for local unavailability, swaps, duplicates, fees, and unresolved warnings.

Describe this naturally to the user as setting the delivery area, choosing the Whoosh window, or checking the local shelves. Never say that Codex is placing the Whoosh order.

### Stable page landmarks

Live testing on the signed-in Tesco site confirmed these semantic landmarks. Prefer them over coordinates and treat URLs as navigation hints rather than permanent contracts:

- The general slot page is currently `/shop/en-GB/slots`, headed `How do you want to shop?`, with `Whoosh`, `Click+Collect`, and `Home Delivery` choices.
- The Whoosh page is currently `/shop/en-GB/slots/ondemand`, headed `Book a slot`, with fulfilment tabs, a required delivery-time choice, and a `Book Whoosh` button.
- Select a saved address without reading, repeating, or recording its full text.
- `Book Whoosh` establishes the local Whoosh context and may reserve a delivery window; use it only when the profile or current request authorizes that behavior. It is not checkout.
- After activating the context, verify the header or basket shows the intended fulfilment mode or slot before bulk shopping.
- Search results load asynchronously. After submitting a search, wait for product headings and `Add` controls rather than interpreting the first incomplete page state as no results.
- Product cards expose the product name as a heading and a nearby semantic `Add` button. After adding, verify the quantity control and basket count rather than assuming the click succeeded.

## Add products

1. Work from the agreed plan and missing-ingredients list.
2. Search by the product role and important attributes, not only one exact title.
3. Inspect size, quantity, dietary suitability, price, offer conditions, and obvious availability state.
4. Use profile preferences for brands, own-brand choices, quality, convenience, substitutions, and budget.
5. Add the intended quantity and verify the basket count changed.
6. Keep a working record of item, quantity, meal role, and acceptable alternatives.

Do not let an offer create excess waste or break a hard budget. Treat Tesco's guide price as provisional.

## Repair local unavailability

After the fulfilment context is active, inspect the basket and any `attention`, `unavailable`, `substitution`, or equivalent interface Tesco presents.

For each affected product:

1. Identify the unavailable original and its meal role.
2. Evaluate Tesco's suggested swap rather than accepting it automatically.
3. Check allergies and hard restrictions before all other considerations.
4. Prefer, in order: the same product in another size; a suitable equivalent; another ingredient preserving the meal; or a replacement meal.
5. Add or accept the replacement, then remove the unavailable original if Tesco leaves it in the basket.
6. Verify quantities, duplicates, price, and meal coverage.
7. Record any changed product or meal in the saved meal plan.

Never use a substitution when allergy suitability is uncertain. Ask the user if no safe alternative can be established.

## Final verification

Before handoff, verify:

- every planned meal still has its required ingredients;
- quantities suit the household and leftovers plan;
- inventory items were not accidentally rebought;
- unavailable originals and accidental duplicates are gone;
- substitutions follow the profile;
- the basket and mandatory fees respect any hard budget;
- Tesco shows no unresolved basket warning that can be handled safely;
- the current page is before any final submit, order, purchase, or payment action.

Leave the completed basket visible. Report exact uncertainty when Tesco does not expose reliable local availability or final pricing.
