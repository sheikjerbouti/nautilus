import unittest
from io import StringIO
import sys
from nautilus import main

class TestNautilus(unittest.TestCase):
    def test_main_output(self):
        # Redirect stdout to capture print statements
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Call the main function
        main()
        
        # Reset redirect.
        sys.stdout = sys.__stdout__
        
        # Check if the output is as expected
        self.assertIn("Nautilus - minimal Kubernetes CLI", captured_output.getvalue())

if __name__ == "__main__":
    unittest.main()