import unittest
import os
from data_pipeline import DataPipeline

class TestDataPipeline(unittest.TestCase):

    def setUp(self):
        # Set up a sample data file for testing
        self.test_file = "test_data.csv"
        self.output_file = "output_data.csv"
        with open(self.test_file, "w") as file:
            file.write("id,name,age,salary,department\n")
            file.write("1,Alice,30,70000,Sales\n")
            file.write("2,Bob,40,80000,Engineering\n")
            file.write("3,Charlie,,65000,Engineering\n")
            file.write("4,Diana,35,75000,Sales\n")
            file.write("5,Edward,29,,Sales\n")
            file.write("6,Frank,50,90000,Marketing\n")
            file.write("7,Bob,40,80000,Engineering\n")  # Duplicate row

        self.pipeline = DataPipeline()

    def tearDown(self):
        # Clean up the files after tests
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_load_data(self):
        self.pipeline.load_data(self.test_file)
        self.assertEqual(len(self.pipeline.data), 7, "Data loading failed.")

    def test_display_data(self):
        # Capture the display output
        self.pipeline.load_data(self.test_file)
        self.pipeline.display_data(2)
        # Check if the first two rows are displayed correctly
        self.assertIn({'id': '1', 'name': 'Alice', 'age': '30', 'salary': '70000', 'department': 'Sales'}, self.pipeline.data)
        self.assertIn({'id': '2', 'name': 'Bob', 'age': '40', 'salary': '80000', 'department': 'Engineering'}, self.pipeline.data)

    def test_clean_data(self):
        self.pipeline.load_data(self.test_file)
        self.pipeline.clean_data()
        self.assertEqual(len(self.pipeline.data), 6, "Duplicate rows not removed or missing values not handled correctly.")
        # Check missing values filled correctly
        for row in self.pipeline.data:
            self.assertNotIn("", row.values(), "Missing values not handled properly.")
            self.assertNotIn(None, row.values(), "Missing values not handled properly.")

    def test_transform_data(self):
        self.pipeline.load_data(self.test_file)
        self.pipeline.clean_data()
        self.pipeline.transform_data()
        for row in self.pipeline.data:
            salary = int(row['salary']) if row['salary'].isdigit() else 0
            if salary >= 80000:
                self.assertEqual(row['salary_category'], 'High', "Salary category not assigned correctly.")
            elif salary >= 60000:
                self.assertEqual(row['salary_category'], 'Medium', "Salary category not assigned correctly.")
            else:
                self.assertEqual(row['salary_category'], 'Low', "Salary category not assigned correctly.")

    def test_save_data(self):
        self.pipeline.load_data(self.test_file)
        self.pipeline.clean_data()
        self.pipeline.transform_data()
        self.pipeline.save_data(self.output_file)
        # Check if the output file exists
        self.assertTrue(os.path.exists(self.output_file), "Data not saved correctly.")
        # Check if the data is saved correctly by reloading it
        with open(self.output_file, 'r') as file:
            lines = file.readlines()
        # Check if headers and rows are saved as expected
        self.assertGreater(len(lines), 1, "Output file is empty.")
        self.assertIn("salary_category", lines[0], "Header missing in output file.")

if __name__ == "__main__":
    unittest.main()
