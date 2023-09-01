"""Principal"""
import PySimpleGUI as sg
from src.gui_layer import MakeWindow


def main():
    """Funcao principal"""
    window_started = MakeWindow()
    window_show = window_started.make_window()
    while True:
        # event, values = window_show.read()
        tuple_response = window_show.read()
        event = tuple_response[0]
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        if event == "Executar":
            pass
    window_show.close()


if __name__ == "__main__":
    main()
