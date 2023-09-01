"""Comparation spreedsheet logical"""
import pandas as pd

from ..utils_layer import Utils


class Comparation:
    """Comparation spreadsheet class"""

    def __init__(
        self, name_file_planilha_base: str, name_file_planilha_nova: str, mes: str
    ) -> None:
        self.name_file_planilha_base: str = name_file_planilha_base
        self.name_file_planilha_nova: str = name_file_planilha_nova
        self.mes: str = mes
        self.utils: Utils = Utils()

    def base_spreadsheet_higienization(self) -> pd.DataFrame:
        """Realiza a higienizacao da planilha base"""
        planilha_base: pd.DataFrame = self.utils.xlsx_to_df(
            self.name_file_planilha_base
        )
        colunas: list[str] = [
            "Matrícula",
            "SITUAÇÃO FUNCIONAL",
            "UNIDADE",
            "Unnamed: 3",
            "OBSERVAÇÕES",
            "SERVIDOR",
            "JAN",
            "FEV",
            "MAR",
            "ABR",
            "MAI",
            "JUN",
            "JUL",
            "AGO",
            "SET",
            "OUT",
            "NOV",
            "DEZ",
        ]
        planilha_base: pd.DataFrame = planilha_base[colunas]
        col_siape_planilha_base: pd.DataFrame = planilha_base["Matrícula"].apply(
            lambda x: str(x).zfill(7)
        )

        return col_siape_planilha_base

    def new_spreadsheet_higienization(self) -> pd.DataFrame:
        """Realiza a higienizacao da planilha nova"""
        planilha_nova: pd.DataFrame = self.utils.xlsx_to_df(
            self.name_file_planilha_nova
        )
        rows_to_drop_sit_func: list[int] = []

        for ind in planilha_nova.index:
            if planilha_nova["SITUAÇÃO FUNCIONAL"][ind] in [
                "EST-02",
                "EST-15",
                "ETG-70",
            ]:
                rows_to_drop_sit_func.append(ind)

        planilha_nova_func_droped: pd.DataFrame = planilha_nova.drop(
            planilha_nova.index[rows_to_drop_sit_func]
        )

        col_siape_planilha_nova: pd.DataFrame = planilha_nova_func_droped[
            "VÍNCULO SERVIDOR"
        ].apply(lambda x: str(x[6:]))

        return col_siape_planilha_nova

    def create_spreadsheet_compared(self) -> None:
        """Retorna planilha de comparacao da planilha base com a nova planilha"""

        planilha_base_higienizada: pd.DataFrame = self.base_spreadsheet_higienization()
        planilha_nova_higienizada: pd.DataFrame = self.new_spreadsheet_higienization()

        nova_planilha_base: pd.DataFrame = self.utils.xlsx_to_df(
            self.name_file_planilha_base
        )

        for ind in planilha_base_higienizada.index:
            if planilha_base_higienizada[ind] in set(planilha_nova_higienizada):
                nova_planilha_base.loc[ind, [self.mes]] = ["OK"]

        nova_planilha_base.to_excel("output.xlsx", index=False)
