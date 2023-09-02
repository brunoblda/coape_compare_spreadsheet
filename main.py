"""Principal"""
import PySimpleGUI as sg
from src.gui_layer import MakeWindow
from src.utils_layer import Utils
from src.logical_layer import Comparation


def execute_comparation(window_show):
    """Executa a comparacao entre as planilhas"""
    comparation = Comparation(
        name_file_planilha_base=window_show["nome_arq_planilha_base"].get(),
        name_file_planilha_nova=window_show["nome_arq_nova_planilha"].get(),
        mes=window_show["-DROP-"].get(),
    )
    comparation.create_spreadsheet_compared()
    window_show["text_execucao"].update("                Executado.")


def main() -> None:
    """Funcao principal"""
    utils: Utils = Utils()
    window_started: MakeWindow = MakeWindow()
    window_show: sg.Window = window_started.make_window()
    while True:
        # event, values = window_show.read()
        tuple_response: tuple[str, list[str | int]] = window_show.read()
        event: str = tuple_response[0]
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        if event == "Executar":
            window_show["text_execucao"].update("               Em execução.")
            if not utils.validate_file_exist(
                file_name=window_show["nome_arq_planilha_base"].get()
            ):
                window_show["text_execucao"].update("Planilha base não encontrada.")
            elif not utils.validate_file_exist(
                file_name=window_show["nome_arq_nova_planilha"].get()
            ):
                window_show["text_execucao"].update("Nova planilha não encontrada.")
            elif window_show["-DROP-"].get() == "":
                window_show["text_execucao"].update("       Mês não selecionado.")
            else:
                execute_comparation(window_show=window_show)

    window_show.close()


if __name__ == "__main__":
    main()
