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
        self.planilha_base: pd.DataFrame = self.utils.xlsx_to_df_base_spreadsheet(
            self.name_file_planilha_base
        )
        self.planilha_nova: pd.DataFrame = self.utils.xlsx_to_df(
            self.name_file_planilha_nova
        )
        self.planilha_base_higienizada: pd.DataFrame = (
            self.base_spreadsheet_higienization(self.planilha_base)
        )
        self.planilha_nova_higienizada: pd.DataFrame = (
            self.new_spreadsheet_higienization()
        )

    def base_spreadsheet_higienization(self, planilha_base) -> pd.DataFrame:
        """Realiza a higienizacao da planilha base"""
        col_siape_planilha_base: pd.DataFrame = planilha_base["Matrícula"].apply(
            lambda x: str(x).zfill(7)
        )

        return col_siape_planilha_base

    def new_spreadsheet_higienization(self) -> pd.DataFrame:
        """Realiza a higienizacao da planilha nova"""

        planilha_nova: pd.DataFrame = self.planilha_nova.copy()
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

    def return_row_base_spreedsheat_checked(self) -> pd.DataFrame:
        """Retorna planilha de comparacao da planilha base com a nova planilha inserindo
        o OK na coluna do mes da planilha base"""

        planilha_base: pd.DataFrame = self.planilha_base.copy()

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

        planilha_base_higienizada: pd.DataFrame = self.planilha_base_higienizada.copy()
        planilha_nova_higienizada: pd.DataFrame = self.planilha_nova_higienizada.copy()

        nova_planilha_base: pd.DataFrame = planilha_base

        for ind in planilha_base_higienizada.index:
            if planilha_base_higienizada[ind] in set(planilha_nova_higienizada):
                nova_planilha_base.loc[ind, [self.mes]] = [str("OK")]

        return nova_planilha_base

    def return_base_spreadsheet_with_new_rows(
        self, nova_planilha_base: pd.DataFrame
    ) -> pd.DataFrame:
        """Retorna uma planilha base com adicao da matricula, situacao funcional e nome
        dos servidores que estao na planilha nova mas nao estavam na planilha base"""

        planilha_base_higienizada: pd.DataFrame = self.planilha_base_higienizada.copy()
        planilha_nova_higienizada: pd.DataFrame = self.planilha_nova_higienizada.copy()
        planilha_nova: pd.DataFrame = self.planilha_nova.copy()

        index_people_out_of_planilha_base: list[int] = []

        for ind in planilha_nova_higienizada.index:
            if planilha_nova_higienizada[ind] not in set(planilha_base_higienizada):
                index_people_out_of_planilha_base.append(int(ind))

        list_of_people_to_add_in_planilha_base: list[dict[int, str, str]] = []

        for ind in index_people_out_of_planilha_base:
            list_of_people_to_add_in_planilha_base.append(
                {
                    "Matrícula": int(planilha_nova.loc[ind]["VÍNCULO SERVIDOR"][6:]),
                    "SITUAÇÃO FUNCIONAL": planilha_nova.loc[ind]["SITUAÇÃO VÍNCULO"],
                    "SERVIDOR": planilha_nova.loc[ind]["NOME SERVIDOR"],
                }
            )

        nova_planilha_base_added: pd.DataFrame = nova_planilha_base

        for row in list_of_people_to_add_in_planilha_base:
            new_row = pd.DataFrame(row, index=[0])
            nova_planilha_base_added = pd.concat(
                [nova_planilha_base_added.loc[:], new_row]
            ).reset_index(drop=True)

        return nova_planilha_base_added

    def create_spreadsheet_compared(self) -> None:
        """Executa a comparacao e realiza a exportacao da tabela base atualizada"""

        base_spreadsheet_checked: pd.DataFrame = (
            self.return_row_base_spreedsheat_checked()
        )
        base_spreadsheet_with_new_rows = self.return_base_spreadsheet_with_new_rows(
            base_spreadsheet_checked
        )

        self.export_to_excel(base_spreadsheet_with_new_rows)

    def export_to_excel(self, planilha: pd.DataFrame) -> None:
        """Realiza a exportacao da tabela para excel"""

        planilha.to_excel("output.xlsx", index=False)
