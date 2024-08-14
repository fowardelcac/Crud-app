import flet as ft
from backend.A_database_functions import ItemsModel, DatabaseManager
from styles.styles import (
    modal_style,
    table_style,
    text_field_style,
    expansion_tile_title_style,
    form_inputs_style,
    subtitle_expansion_tile_style,
    elevated_button_style,
    Colors,
)


class ItemPage(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.dbm = DatabaseManager()
        self.selected_row = None
        self.diccionario = self.dic_build()
        self.modal = ft.AlertDialog(
            **modal_style,
            actions=[
                ft.TextButton("Si", on_click=self.handle_close),
                ft.TextButton("No", on_click=self.handle_close),
            ],
        )

        self.item_name = ft.TextField(
            **text_field_style,
            label="Nombre *",
            max_length=30,
            hint_text="Ingrese el nombre(Dato obligatorio)",
        )

        self.description = ft.TextField(
            **text_field_style, label="Ubicacion", max_length=40
        )

        self.start_date = ft.TextField(
            **text_field_style, label="Fecha de inicio", max_length=20
        )
        self.end_date = ft.TextField(
            **text_field_style, label="Fecha de finalizacion", max_length=20
        )

        self.completed = ft.Dropdown(
            **text_field_style,
            label="Estado.",
            hint_content="Seleccione el tipo de estado.",
            options=[
                ft.dropdown.Option("Terminado."),
                ft.dropdown.Option("En proceso."),
            ],
            padding=15,
        )

        self.construction = ft.Dropdown(
            **text_field_style,
            label="Nombre de la construccion. *",
            hint_content="Seleccionar el nombre de la construccion(Dato obligatorio)",
        )

        self.form_inputs = ft.Container(
            **form_inputs_style,
            content=ft.Column(
                scroll=ft.ScrollMode.ALWAYS,
                controls=[
                    ft.ExpansionTile(
                        ft.Text("Ingrese sus obras.", **expansion_tile_title_style),
                        subtitle=ft.Text(
                            "Click sobre el panel para abrir el formulario.",
                            **subtitle_expansion_tile_style,
                        ),
                        affinity=ft.TileAffinity.LEADING,
                        text_color=ft.colors.BLACK,
                        on_change=self.dic_change,
                        controls=[
                            ft.Container(height=20),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        content=self.item_name,
                                        width=400,
                                    ),
                                    ft.Container(
                                        content=self.description,
                                        width=400,
                                    ),
                                ],
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        content=self.start_date,
                                    ),
                                    ft.Container(
                                        content=self.end_date,
                                    ),
                                ],
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(content=self.completed),
                                    ft.Container(content=self.construction),
                                ],
                            ),
                            ft.Container(height=20),
                            ft.Container(
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.ElevatedButton(
                                            **elevated_button_style,
                                            text="Insertar",
                                            icon=ft.icons.SAVE,
                                            on_click=self.add_data,
                                        ),
                                        ft.ElevatedButton(
                                            **elevated_button_style,
                                            text="Actualizar",
                                            icon=ft.icons.UPDATE,
                                            on_click=self.update_data,
                                        ),
                                        ft.ElevatedButton(
                                            **elevated_button_style,
                                            text="Eliminar",
                                            icon=ft.icons.DELETE,
                                            on_click=lambda e: self.page.open(
                                                self.modal
                                            ),
                                        ),
                                    ],
                                ),
                            ),
                            ft.Container(height=20),
                        ],
                    )
                ],
            ),
        )

        self.search_field = ft.TextField(
            **text_field_style,
            label="Buscar por el nombre.",
            suffix_icon=ft.icons.SEARCH,
            color=ft.TextStyle("black"),
            expand=True,
            on_change=self.search_data,
        )

        self.edit = ft.Column(
            controls=[
                ft.Container(
                    padding=10,
                    content=ft.Row(
                        controls=[
                            self.search_field,
                            ft.IconButton(
                                tooltip="Editar",
                                icon=ft.icons.EDIT,
                                icon_color=Colors.Button.value,
                                on_click=self.edit_filled_text,
                            ),
                        ]
                    ),
                ),
            ]
        )

        self.data_table = self.datatable_build()

        self.table_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.ResponsiveRow(
                        [self.data_table],
                    )
                ],
            ),
        )

        self.show_data()
        self.content = ft.Column(
            controls=[self.form_inputs, self.edit, self.table_container],
            scroll=ft.ScrollMode.ALWAYS,
        )

    def build(self):
        return self.content

    def get_index(self, e):
        if e.control.selected:
            e.control.selected = False
            self.clean_fields()
        else:
            e.control.selected = True

        id = e.control.cells[0].content.value
        query = """SELECT * FROM  Items ORDER BY Item_id DESC"""
        data = self.dbm.get_table(query=query)
        for row in data:
            if row[0] == id:
                self.selected_row = row
                break
        self.page.update()

    def datatable_build(self):
        return ft.DataTable(
            **table_style,
            columns=[
                ft.DataColumn(ft.Text("Indice")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Direccion")),
                ft.DataColumn(ft.Text("Fecha inicio")),
                ft.DataColumn(ft.Text("Fecha fin")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Construccion")),
            ],
            width=1000,
            data_row_max_height=float("inf"),
        )

    def dic_build(self):
        query = """SELECT * FROM Constructions ORDER BY Construction_id DESC"""
        data = self.dbm.get_table(query=query)
        return {i[0]: i[1] for i in data}

    def dic_change(self, e):
        diccionario = self.dic_build()
        self.construction.options = [
            ft.dropdown.Option(value) for value in diccionario.values()
        ]
        self.page.update()

    def data_loader(self, data):
        dicc = self.dic_build()
        self.data_table.rows = []
        for i in data:
            self.data_table.rows.append(
                ft.DataRow(
                    on_select_changed=self.get_index,
                    cells=[
                        ft.DataCell(ft.Text(i[0])),
                        ft.DataCell(ft.Text(i[1])),
                        ft.DataCell(ft.Text(i[2])),
                        ft.DataCell(ft.Text(i[3])),
                        ft.DataCell(ft.Text(i[4])),
                        ft.DataCell(ft.Text(i[5])),
                        ft.DataCell(ft.Text(dicc[i[6]])),
                    ],
                )
            )

    def show_data(self):
        query = """SELECT * FROM  Items ORDER BY Item_id DESC"""
        data = self.dbm.get_table(query=query)
        self.data_loader(data)
        self.page.update()

    def search_data(self, e):
        search_text = self.search_field.value
        query = f"""SELECT * FROM Items WHERE Item_name  LIKE '{search_text}' || '%' ORDER BY Item_id DESC;"""
        data = self.dbm.get_table(query=query)
        self.data_loader(data)
        self.page.update()

    def clean_fields(self):
        self.item_name.value = ""
        self.description.value = ""
        self.start_date.value = ""
        self.end_date.value = ""
        self.completed.value = ""
        self.construction.value = ""

    def snack(self, label: str, color: str):
        self.page.snack_bar = ft.SnackBar(ft.Text(label), bgcolor=color, duration=1000)
        self.page.snack_bar.open = True

    def add_data(self, e):
        self.diccionario = self.dic_build()
        inverted_diccionario = {v: k for k, v in self.diccionario.items()}
        construction_id = inverted_diccionario[self.construction.value]
        data_model = ItemsModel(
            Item_name=self.item_name.value,
            Direction=self.description.value,
            Start_date=self.start_date.value,
            Possible_end_date=self.end_date.value,
            Completed=self.completed.value,
            Construction_id=construction_id,
        )
        if data_model.Item_name and data_model.Construction_id:
            try:
                self.clean_fields()
                data_tuple = (
                    data_model.Item_name,
                    data_model.Direction,
                    data_model.Start_date,
                    data_model.Possible_end_date,
                    data_model.Completed,
                    data_model.Construction_id,
                )
                query = """INSERT INTO Items (Item_name, Description, Start_date, Possible_end_date, Completed, Construction_id)
                         VALUES (?, ?, ?, ?, ?, ?)"""
                self.dbm.insert_table(
                    query=query,
                    data_model=data_tuple,
                )
                self.snack("Agregado correctamente.", "green")
            except Exception as ex:
                print("ERROR", ex)
                self.snack("No puede haber dos clientes con el mismo nombre.", "red")

        else:
            self.snack("El nombre es obligatorio.", "red")
        self.show_data()

    def edit_filled_text(self, e):
        try:
            if self.selected_row is None:
                raise ValueError("selected_row is None. Please select a row first.")

            self.item_name.value = self.selected_row[1]
            self.description.value = self.selected_row[2]
            self.start_date.value = self.selected_row[3]
            self.end_date.value = self.selected_row[4]
            self.completed.value = self.selected_row[5]
            self.construction.value = self.diccionario[self.selected_row[6]]
            self.page.update()
        except Exception as ex:
            print(f"An error occurred: {ex}")

    def handle_close(self, e):
        clicked_button_text = e.control.text
        if clicked_button_text == "Si":
            query = "DELETE FROM Items WHERE Item_id = ?"
            self.dbm.delete_table(query=query, id=self.selected_row[0])

            self.clean_fields()
            self.snack("Eliminado correctamente.", "green")
        else:
            self.snack("Cancelado.", "orange")

        self.page.close(self.modal)
        self.show_data()

    def update_data(self, e):
        self.diccionario = self.dic_build()
        inverted_diccionario = {v: k for k, v in self.diccionario.items()}
        construction_id = inverted_diccionario[self.construction.value]
        data_model = ItemsModel(
            Item_name=self.item_name.value,
            Description=self.description.value,
            Start_date=self.start_date.value,
            Possible_end_date=self.end_date.value,
            Completed=self.completed.value,
            Construction_id=construction_id,
        )
        if data_model.Item_name and data_model.Construction_id:
            try:
                self.clean_fields()
                data_tuple = (
                    data_model.Item_name,
                    data_model.Description,
                    data_model.Start_date,
                    data_model.Possible_end_date,
                    data_model.Completed,
                    data_model.Construction_id,
                    self.selected_row[0],
                )
                query = """UPDATE Items SET Item_name = ?, Description = ?,
                          Start_date = ?, Possible_end_date = ?, Completed = ?, Construction_id = ?
                        WHERE Item_id = ?;
                        """
                self.dbm.update_table(
                    query=query,
                    data_model=data_tuple,
                )
                self.snack("Actualizado correctamente.", "green")
            except Exception as ex:
                print("~" * 100)
                print(ex)
                self.snack("No puede haber dos clientes con el mismo nombre.", "red")

        else:
            self.snack("El nombre es obligatorio.", "red")
        self.show_data()
