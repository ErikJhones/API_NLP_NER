import unittest
import pandas as pd

from app.engine.interface import DBInterface, QueryParser
from app.engine.shared import DB_CONFIG


class TestApp(unittest.TestCase):

    def setUp(self) -> None:
        self.db_inst = DBInterface(**DB_CONFIG)



class TestQueryParser(TestApp):

    def test_query_parsing_to_lists_goes_successful(self):
        query_result = self.db_inst.run_query("""
            SELECT * FROM tb_chrono tc WHERE id_family = 27
        """)

        query_result = QueryParser(query_result).to_list()

        for value in query_result:
            self.assertEqual(type(value), list)


    def test_query_parsing_to_tuples_goes_successful(self):
        query_result = self.db_inst.run_query("""
            SELECT * FROM tb_chrono tc WHERE id_family = 27
        """)

        query_result = QueryParser(query_result).to_tuple()

        for value in query_result:
            self.assertEqual(type(value), tuple)


    def test_query_parsing_to_dataframe_goes_successful(self):
        query_result = self.db_inst.run_query("""
            SELECT * FROM tb_chrono tc WHERE id_family = 27
        """)

        query_result = QueryParser(query_result).to_dataframe()

        self.assertEqual(type(query_result), pd.DataFrame)



class TestDBInterface(TestApp):

    def test_get_version(self):
        version = self.db_inst.get_version()
        self.assertIsNotNone(version)


    def test_run_query(self):
        query_string = "SELECT * FROM tb_chrono"
        result = self.db_inst.run_query(query_string)

        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)


    def test_list_tables(self):
        tables = self.db_inst.list_tables()

        self.assertIsNotNone(tables)
        self.assertIn('dwsfp.tb_chrono', tables)


    def test_list_tables_with_schema(self):
        tables = self.db_inst.list_tables_with_squema()

        self.assertIsNotNone(tables)

        for table in tables:
            self.assertGreater(len(table.split(".")), 1)


    def test_export_query_to_dataframe_successfully(self):
        df = self.db_inst.export_query_to_dataframe(
            """SELECT * FROM tb_chrono"""
        )

        self.assertIsNotNone(df.columns)
        self.assertEqual(type(df), pd.DataFrame)
