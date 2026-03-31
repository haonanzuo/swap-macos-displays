import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock


SCRIPT_PATH = Path(__file__).with_name("swap_macos_displays.py")
SPEC = importlib.util.spec_from_file_location("swap_macos_displays", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
if SPEC.loader is None:
    raise RuntimeError("Failed to load swap_macos_displays.py")
SPEC.loader.exec_module(MODULE)


class SwapMacOSDisplaysTests(unittest.TestCase):
    def test_resolve_displayplacer_prefers_bundled_binary(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundled_binary = Path(tmpdir) / "displayplacer"
            bundled_binary.write_text("#!/bin/sh\n")

            with mock.patch.object(MODULE, "BUNDLED_DISPLAYPLACER", bundled_binary):
                with mock.patch.object(MODULE.shutil, "which", return_value="/usr/local/bin/displayplacer"):
                    resolved = MODULE.resolve_displayplacer_cmd()

            self.assertEqual(resolved, str(bundled_binary))

    def test_resolve_displayplacer_falls_back_to_path(self):
        missing_binary = Path("/tmp/definitely-missing-displayplacer")

        with mock.patch.object(MODULE, "BUNDLED_DISPLAYPLACER", missing_binary):
            with mock.patch.object(MODULE.shutil, "which", return_value="/opt/homebrew/bin/displayplacer"):
                resolved = MODULE.resolve_displayplacer_cmd()

        self.assertEqual(resolved, "/opt/homebrew/bin/displayplacer")

    def test_extract_current_command_uses_last_displayplacer_line(self):
        output = """
Intro text
Rotation example: displayplacer "id:internal degree:90"
displayplacer "id:first res:1920x1080 origin:(0,0) degree:0" "id:second res:3024x1964 origin:(1920,0) degree:0"
""".strip()

        command = MODULE.extract_current_command(output)

        self.assertEqual(
            command,
            'displayplacer "id:first res:1920x1080 origin:(0,0) degree:0" "id:second res:3024x1964 origin:(1920,0) degree:0"',
        )

    def test_swap_origins_for_two_displays(self):
        command = (
            'displayplacer '
            '"id:first res:1920x1080 hz:100 color_depth:8 scaling:off origin:(0,0) degree:0" '
            '"id:second res:3024x1964 hz:60 color_depth:8 scaling:on origin:(1920,-37) degree:0"'
        )

        swapped = MODULE.swap_origins(command)

        self.assertEqual(
            swapped,
            'displayplacer '
            '"id:first res:1920x1080 hz:100 color_depth:8 scaling:off origin:(1920,-37) degree:0" '
            '"id:second res:3024x1964 hz:60 color_depth:8 scaling:on origin:(0,0) degree:0"',
        )

    def test_swap_requires_exactly_two_displays(self):
        command = (
            'displayplacer '
            '"id:first res:1920x1080 origin:(0,0) degree:0" '
            '"id:second res:3024x1964 origin:(1920,0) degree:0" '
            '"id:third res:1920x1080 origin:(-1920,0) degree:0"'
        )

        with self.assertRaisesRegex(ValueError, "exactly two"):
            MODULE.swap_origins(command)


if __name__ == "__main__":
    unittest.main()
