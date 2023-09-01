"""Graphical User Interface module"""
import textwrap
import PySimpleGUI as sg


class MakeWindow:
    """Classe que cria a tela"""

    def __init__(self, theme=None) -> None:
        self.theme = theme
        self.window = None

    def make_window(self):
        """Create the Graphical User Interface"""
        sg.theme(self.theme)

        text_1 = "Compara a planilha base da COAPE com a nova planilha de dados."

        layout_l = [
            [
                sg.T("Nome do arquivo da planilha base: ", font=("", 14), pad=(0, 10)),
                sg.In(
                    default_text="coordenadas_mouse.txt",
                    key="nome_arq_coordenadas",
                    font=("", 14),
                    pad=(0, 10),
                ),
            ],
            [
                sg.T(
                    "Nome do arquivo da nova planilha: ", font=("", 14), pad=((0, 10))
                ),
                sg.In(
                    default_text="ctc_inss_serv.csv",
                    key="nome_arq_planilha",
                    font=("", 14),
                    pad=(0, (10)),
                ),
            ],
            [
                sg.Button(
                    "Executar", font=("", 16), pad=(300, (30, 10)), bind_return_key=True
                )
            ],
            [
                sg.T(
                    "",
                    key="text_execucao",
                    font=("", 16),
                    justification="c",
                    pad=(200, 0),
                )
            ],
        ]
        # Note - LOCAL Menu element is used (see about for how that's defined)
        layout = [
            [
                sg.T(
                    textwrap.fill(text_1, 80),
                    pad=(0, (0, 30)),
                    font="_ 16",
                    justification="c",
                    expand_x=False,
                )
            ],
            [sg.Col(layout_l, p=0)],
        ]

        self.window = sg.Window(
            "Compara planilhas COAPE",
            layout,
            finalize=True,
            right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT,
            keep_on_top=True,
            element_justification="c",
            size=(750, 250),
        )

        return self.window
