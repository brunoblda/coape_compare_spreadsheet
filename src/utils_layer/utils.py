"""Modulo de funcoes utilitarias"""
import os.path
import pandas as pd


class Utils:
    """Classe de funcoes utilitarias"""

    def validate_file_exist(self, file_name: str) -> bool:
        """Valida se o arquivo da planilha existe"""

        if os.path.isfile(f"./{file_name}"):
            return True
        return False

    def xlsx_to_df(self, file_name: str) -> pd.DataFrame:
        """Transforma o arquivo xlsx em um dataframe do pandas"""

        planilha_df = pd.read_excel(f"./{file_name}")
        return planilha_df

    def xlsx_to_df_base_spreadsheet(self, file_name: str) -> pd.DataFrame:
        """Transforma o arquivo de planilha base xlsx em um dataframe do pandas"""

        planilha_df = pd.read_excel(
            f"./{file_name}",
            converters={
                "JAN": str,
                "FEV": str,
                "MAR": str,
                "ABR": str,
                "MAI": str,
                "JUN": str,
                "JUL": str,
                "AGO": str,
                "SET": str,
                "OUT": str,
                "NOV": str,
                "DEZ": str,
            },
        )
        return planilha_df
