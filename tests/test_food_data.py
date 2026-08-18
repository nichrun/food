import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).parents[1] / "plugins" / "food" / "scripts" / "food_data.py"
SPECIFICATION = importlib.util.spec_from_file_location("food_data", SCRIPT_PATH)
food_data = importlib.util.module_from_spec(SPECIFICATION)
SPECIFICATION.loader.exec_module(food_data)


class FoodDataTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.config = self.root / "config" / "config.json"
        self.previous_config = os.environ.get("FOOD_CONFIG_PATH")
        os.environ["FOOD_CONFIG_PATH"] = str(self.config)

    def tearDown(self):
        if self.previous_config is None:
            os.environ.pop("FOOD_CONFIG_PATH", None)
        else:
            os.environ["FOOD_CONFIG_PATH"] = self.previous_config
        self.temporary_directory.cleanup()

    def test_initialize_creates_expected_layout(self):
        data_directory = self.root / "Food"
        result = food_data.initialize(str(data_directory), replace_location=False)

        self.assertEqual(Path(result["data_directory"]), data_directory.resolve())
        self.assertTrue((data_directory / "profile.md").is_file())
        self.assertTrue((data_directory / "inventory.md").is_file())
        self.assertIn("## Incoming Orders", (data_directory / "inventory.md").read_text())
        self.assertTrue((data_directory / "recipes.md").is_file())
        self.assertTrue((data_directory / "meal-plans").is_dir())
        self.assertTrue((data_directory / "tesco-orders").is_dir())

        configuration = json.loads(self.config.read_text())
        self.assertEqual(Path(configuration["data_directory"]), data_directory.resolve())

    def test_initialize_is_idempotent_and_preserves_content(self):
        data_directory = self.root / "Food"
        food_data.initialize(str(data_directory), replace_location=False)
        profile = data_directory / "profile.md"
        profile.write_text("personal profile\n")

        food_data.initialize(str(data_directory), replace_location=False)

        self.assertEqual(profile.read_text(), "personal profile\n")

    def test_different_location_requires_explicit_replace(self):
        first = self.root / "First"
        second = self.root / "Second"
        food_data.initialize(str(first), replace_location=False)

        with self.assertRaises(ValueError):
            food_data.initialize(str(second), replace_location=False)

        result = food_data.initialize(str(second), replace_location=True)
        self.assertEqual(Path(result["data_directory"]), second.resolve())

    def test_ensure_repairs_missing_file_without_overwriting_others(self):
        data_directory = self.root / "Food"
        food_data.initialize(str(data_directory), replace_location=False)
        profile = data_directory / "profile.md"
        inventory = data_directory / "inventory.md"
        profile.write_text("keep me\n")
        inventory.unlink()

        result = food_data.ensure()

        self.assertEqual(profile.read_text(), "keep me\n")
        self.assertTrue(inventory.is_file())
        self.assertIn(str(inventory.resolve()), result["created"])


if __name__ == "__main__":
    unittest.main()
