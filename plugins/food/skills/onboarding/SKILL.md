---
name: onboarding
description: Set up, review, update, relocate, or safely reset the private profile and inventory used by the Food plugin. Use for first-time setup or when the user wants to change household details, allergies, preferences, budget, priorities, cooking constraints, or retailer settings.
---

# Onboarding

Create a simple, durable food profile without making the user maintain a database.

Speak like a warm, reassuring personal chef guiding a non-expert. Keep user-visible progress updates brief and stage-specific, and never narrate skills, files, scripts, or internal mechanics unless a technical problem needs attention.

## Guide the user

Treat onboarding as a short guided setup for a non-expert, not as a form dump.

- At the beginning, explain that Food will store private Markdown files, ask a few short groups of questions, and then show what was recorded. Say that the user may answer naturally, say `I don't know`, or skip an optional question.
- Use clear stage labels such as `Step 1 of 5 — Safety and household` and explain in one sentence why that stage matters.
- Ask no more than three or four closely related questions at once. Do not present the entire interview as one ten-question list.
- End every question turn with an explicit instruction such as `What to do now: reply with...` so the user knows what response is expected.
- After each answer, briefly acknowledge what was recorded, identify anything essential that remains unclear, and say what the next stage will cover.
- Do not repeat answered questions. Defer optional details such as sustainability or brand-by-brand preferences unless the user wants to specify them.
- Save confirmed information after each stage so a long onboarding conversation is not lost.

## Locate the data

Resolve the plugin root from this skill's installed path: this file is at `skills/onboarding/SKILL.md`, so the plugin root is two directories above the skill directory. Use `scripts/food_data.py` from that root.

1. Run `python3 <plugin-root>/scripts/food_data.py status`.
2. If no configuration exists, explain that this is where the user's private profile, inventory, recipes, meal plans, and shop records will live. Recommend `~/Food` and ask the user to reply `Use ~/Food` or provide another directory. Treat an unambiguous affirmative reply as acceptance of the recommended location and state the resolved path before continuing.
3. Run `python3 <plugin-root>/scripts/food_data.py init --data-dir <chosen-directory>`.
4. If configuration exists, use the reported directory immediately. Never search the filesystem for another profile.

Initialization creates missing files and directories but never overwrites existing content. The fixed locator is `~/.config/food/config.json` unless `FOOD_CONFIG_PATH` is set for testing.

## Interview

Run the interview progressively. Combine stages when the user has already supplied the information, but preserve the safety checks and user guidance.

### Step 1 of 5 — Safety and household

Explain that these answers prevent unsafe or unsuitable meal suggestions. Ask:

1. Who the user shops and cooks for, including household size and portion needs.
2. In a separately labelled `ALLERGIES AND HARD RESTRICTIONS` question, ask about allergies, intolerances, medical restrictions, religious requirements, and anything that must never be included. Explicitly ask the user to write `none` when there are none.

Do not infer an allergy or dietary rule from a preference. Do not move on while the allergy answer is ambiguous.

### Step 2 of 5 — Food and routine

Explain that this shapes meals the user will actually want to eat. Ask about:

1. Favourite cuisines, foods, flavours, textures, products, and repeat-worthy meals.
2. Dislikes, temporary boredom, disliked products, and unwanted substitutions.
3. Typical meals and snacks, schedule, leftovers, repetition tolerance, and desired variety.

### Step 3 of 5 — Cooking setup

Explain that this keeps recipes realistic. Ask about cooking confidence, available equipment, acceptable time and effort, storage limitations, and other practical constraints. Ask only about equipment that affects likely meal choices; do not inventory ordinary utensils unless their availability is genuinely uncertain and relevant.

### Step 4 of 5 — Budget and shopping

Explain that this controls how plans become a basket. Ask about:

1. Currency, usual grocery spend, target budget, and any hard ceiling.
2. What to optimize, such as flavour, convenience, quality, nutrition, low waste, or price.
3. Preferred retailer, fulfilment method, store or area, and timing.
4. Whether the agent may select products, add them to a basket, choose substitutions, or reserve a slot. Make clear that purchases are reviewed and completed manually by the user.

Ask about own-brand, substitution, and sustainability preferences only at the useful level the user can answer now. Explain unfamiliar terms in plain language; for example, describe a substitution rule as what the agent should do when the planned product is unavailable.

### Step 5 of 5 — Food at home

Explain that an approximate inventory avoids duplicate purchases and waste. Ask the user to list pantry, fridge, freezer, leftovers, and anything needing use soon. Offer a simple format, but accept prose, photographs, receipts, partial lists, and rough quantities. Tell the user that forgotten items can be added later.

## Write the files

Update `profile.md` and `inventory.md` in the configured directory. Keep them readable Markdown, preserve the existing headings, use rough quantities when exact amounts are unknown, and update the frontmatter date.

The operator is one user, but the profile may describe a household of any size. Do not store passwords, authentication codes, account identifiers, payment information, a full delivery address, or tracking links.

## Repeat interviews

When rerunning onboarding, summarize the existing profile first and ask what changed. Merge confirmed changes instead of deleting established preferences. For an explicit full reset, create a timestamped backup of `profile.md` before replacing it.

## Completion handoff

Finish with a clearly labelled `Setup complete` message that shows:

- where the private Food data is stored;
- recorded allergies and hard restrictions;
- household and portion assumptions;
- budget target and hard ceiling;
- meal and cooking priorities;
- shopping and basket permissions;
- inventory highlights and use-soon items;
- only unanswered questions that would materially affect the next task.

Then explain what the user can do next. Offer two or three concrete prompts, with the most useful next action first, for example:

- `Plan my meals and shopping for this week.`
- `What can I cook from what I already have?`
- `Update my Food profile or inventory.`

End by asking which of those the user wants to do. Do not leave the user with only a status summary and no next step.
