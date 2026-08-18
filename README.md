# Food

Food is a personal meal-planning and grocery-shopping plugin for ChatGPT and Codex. It remembers one user's preferences, current food, useful recipes, agreed meal plans, and completed Tesco orders while leaving all purchasing and payment to the human.

## Quick start

Copy and paste this into Codex:

```text
Install the Food plugin from https://github.com/nichrun/food.

Add the repository as a Codex plugin marketplace, install the `food` plugin,
and run `$food:onboarding`.

Perform the installation and begin onboarding rather than only explaining the
steps. If the newly installed skill is unavailable in the current task,
instruct the user to open a new task and run `$food:onboarding`.
```

## Structure

```text
.agents/plugins/marketplace.json    Local/Git marketplace entry
plugins/food/
├── .codex-plugin/plugin.json       Plugin identity and UI metadata
├── scripts/food_data.py            Deterministic data setup and location
└── skills/
    ├── onboarding/                 Initial and repeat profile interviews
    ├── inventory/                  Pantry, fridge, freezer, and use-soon state
    ├── planning/                   Meal plans and shopping briefs
    ├── recipes/                    Recipe creation and feedback memory
    └── tesco-shop/                 Basket preparation and purchase recording
```

## Private data

The plugin code contains no personal food data. Onboarding suggests `~/Food` and stores the chosen absolute location in `~/.config/food/config.json`. The data directory contains:

```text
profile.md
inventory.md
recipes.md
meal-plans/
tesco-orders/
```

Initialization is idempotent: missing files are created, but existing user content is never overwritten. No hooks run during installation.

## Safety boundary

Food may plan meals, choose products, control a Tesco basket, repair unavailable items, and select an authorized fulfilment context. It must never submit an order or make a payment. The user reviews the final basket, allergens, substitutions, fulfilment details, and total before paying manually.

## Development

Validate the skills and plugin, then add this repository as a local marketplace and install `food`. Test changes in a new task so the current plugin package is reloaded.

## License and disclaimer

This project is licensed under the [MIT License](LICENSE). The software is provided “as is”, without warranty of any kind.

This plugin provides instructions and supporting tools to compatible AI agents such as Codex. When used, the agent follows those instructions and performs actions—including browsing, product selection, and basket changes—through the user’s authenticated accounts and sessions.

This plugin does not provide medical, nutritional, allergy, or food-safety advice. Agent outputs and actions may be incomplete or incorrect. A human must verify products, ingredients, allergens, dietary suitability, food condition, cooking safety, prices, substitutions, basket contents, and fulfilment details.

Every purchase must be reviewed and completed manually by the user.

## AI disclosure

This plugin was developed using OpenAI's Codex.
