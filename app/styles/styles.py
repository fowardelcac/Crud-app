from enum import Enum
import flet as ft


class Colors(Enum):
    Background = "#D3D3D3"
    NavBar = "#191970"
    IconsNavBar = "#C0C0C0"
    Button = "#000080"
    Forms = "#E6E6FA"


class Borders(Enum):
    BorderWitdh = 0.2


rail_style = {
    "selected_index": 0,
    "label_type": ft.NavigationRailLabelType.ALL,
    "expand": True,
    "bgcolor": Colors.NavBar.value,
    "group_alignment": -0.9,
    "width": 120,
}


modal_style = {
    "modal": True,
    "title": ft.Text("Porfavor confirmar."),
    "content": ft.Text(
        "Si elimina uno de estos archivos, la aplicacion eliminara toda su informacion relacionada."
    ),
    "actions_alignment": ft.MainAxisAlignment.END,
}

table_style = {
    "expand": True,
    "border_radius": Borders.BorderWitdh.value,
    "bgcolor": Colors.Forms.value,
    "column_spacing": 25,
    #"width": 300,
    #"data_row_max_height": float("inf"),
    "show_checkbox_column": True,
    "on_select_all": False,
}

text_field_style = {
    "bgcolor": Colors.Forms.value,
    "border_width": Borders.BorderWitdh.value,
}
form_inputs_style = {
    "width": float("inf"),
    "border_radius": 0,
    "padding": 0,
}

expansion_tile_title_style = {
    "size": 30,
    "text_align": "center",
    "color": "black",
}
subtitle_expansion_tile_style = {
    "color": "black",
    "weight": "BOLD",
}

elevated_button_style = {
    "style": ft.ButtonStyle(
        shape={"": ft.RoundedRectangleBorder(radius=8)}, color=Colors.Button.value
    )
}
