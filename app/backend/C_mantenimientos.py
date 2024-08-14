import flet as ft
import datetime
from backend.A_database_functions import MaintenancesModel, DatabaseManager
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


def get_next_time(data: list, column: int):
    today = datetime.datetime.today()
    col = [tuple_lis[column] for tuple_lis in data]
    return [
        (datetime.datetime.strptime(fecha, "%d/%m/%Y") - today).days for fecha in col
    ]


def add_days_remaining(data: list, date_column: int):
    # Obtener los días restantes hasta la fecha en la columna especificada
    days_remaining = get_next_time(data, date_column)

    # Crear una nueva lista de tuplas agregando la columna de días restantes
    return [tuple_lis + (days,) for tuple_lis, days in zip(data, days_remaining)]


def sort_by_days_remaining(data: list, sort_column: int):
    # Ordenar la lista de tuplas por la columna de días restantes (última columna)
    return sorted(data, key=lambda x: x[sort_column])


class MaintenencePage(ft.Container):
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

        self.type = ft.Dropdown(
            **text_field_style,
            label="Tipo.",
            hint_content="Seleccione el tipo de mantenimiento.",
            options=[
                ft.dropdown.Option("Preventivo"),
                ft.dropdown.Option("Correctivo"),
            ],
            padding=15,
        )

        self.description = ft.TextField(
            **text_field_style, label="Descripcion.", max_length=40
        )

        self.last = ft.TextField(
            **text_field_style,
            label="Fecha ultima revision.",
            hint_text="Ingresas DD/MM/YYYY.",
            max_length=20,
        )
        self.next = ft.TextField(
            **text_field_style,
            label="Fecha siguiente revision",
            hint_text="Ingresas DD/MM/YYYY.",
            max_length=20,
        )

        self.items = ft.Dropdown(
            **text_field_style,
            label="Nombre del item. *",
            hint_content="Seleccionar el nombre del item(Dato obligatorio)",
        )

        self.form_inputs = ft.Container(
            **form_inputs_style,
            content=ft.Column(
                scroll=ft.ScrollMode.ALWAYS,
                controls=[
                    ft.ExpansionTile(
                        ft.Text(
                            "Ingrese sus mantenimientos.", **expansion_tile_title_style
                        ),
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
                                        content=self.description,
                                        width=400,
                                    ),
                                    ft.Container(
                                        content=self.last,
                                        width=200,
                                    ),
                                    ft.Container(
                                        content=self.next,
                                        width=200,
                                    ),
                                ],
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        content=self.type,
                                        width=400,
                                    ),
                                    ft.Container(content=self.items, width=400),
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
            controls=[
                ft.ResponsiveRow([self.form_inputs, self.edit, self.table_container])
            ],
            # controls=[self.form_inputs, self.edit, self.table_container],
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
        query = """SELECT * FROM  Maintenances ORDER BY Maintenance_id DESC"""
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
                ft.DataColumn(ft.Text("Indce")),
                ft.DataColumn(ft.Text("Tipo")),
                ft.DataColumn(ft.Text("Descripcion")),
                ft.DataColumn(ft.Text("Ultima revision")),
                ft.DataColumn(ft.Text("Proxima revision")),
                ft.DataColumn(ft.Text("Item")),
            ],
            width=1000,
            data_row_max_height=float("inf"),
        )

    def dic_build(self):
        query = """SELECT * FROM Items ORDER BY Item_id DESC"""
        data = self.dbm.get_table(query=query)
        return {i[0]: i[1] for i in data}

    def dic_change(self, e):
        diccionario = self.dic_build()
        self.items.options = [
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
                        ft.DataCell(ft.Text(dicc[i[5]])),
                    ],
                )
            )

    def sort_date(self, data: list, column: int):
        rdo = add_days_remaining(data, column)
        return sort_by_days_remaining(rdo, -1)

    def show_data(self):
        query = """SELECT * FROM  Maintenances ORDER BY Maintenance_id DESC"""
        data = self.dbm.get_table(query=query)
        data_sort = self.sort_date(data, 4)
        self.data_loader(data_sort)
        self.page.update()

    def search_data(self, e):
        search_text = self.search_field.value
        query = f"""SELECT * FROM Maintenances  WHERE Description  LIKE '{search_text}' || '%' ORDER BY Maintenance_id DESC;"""
        data = self.dbm.get_table(query=query)
        self.data_loader(data)
        self.page.update()

    def clean_fields(self):
        self.type.value = ""
        self.description.value = ""
        self.last.value = ""
        self.next.value = ""
        self.items.value = ""

    def snack(self, label: str, color: str):
        self.page.snack_bar = ft.SnackBar(ft.Text(label), bgcolor=color, duration=1000)
        self.page.snack_bar.open = True

    def add_data(self, e):
        self.diccionario = self.dic_build()
        inverted_diccionario = {v: k for k, v in self.diccionario.items()}
        items_id = inverted_diccionario[self.items.value]
        data_model = MaintenancesModel(
            Type=self.type.value,
            Description=self.description.value,
            Last_maintenance=self.last.value,
            Next_maintenance=self.next.value,
            Item_id=items_id,
        )
        if data_model.Description:
            try:
                self.clean_fields()
                data_tuple = (
                    data_model.Type,
                    data_model.Description,
                    data_model.Last_maintenance,
                    data_model.Next_maintenance,
                    data_model.Item_id,
                )
                query = """INSERT INTO Maintenances  (Type, Description, Last_maintenance, Next_maintenance, Item_id)
                         VALUES (?, ?, ?, ?, ?)"""
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

            self.type.value = self.selected_row[1]
            self.description.value = self.selected_row[2]
            self.last.value = self.selected_row[3]
            self.next.value = self.selected_row[4]
            self.items.value = self.diccionario[self.selected_row[5]]
            self.page.update()
        except Exception as ex:
            print(f"An error occurred: {ex}")

    def handle_close(self, e):
        clicked_button_text = e.control.text
        if clicked_button_text == "Si":
            query = "DELETE FROM Maintenances WHERE Maintenance_id = ?"
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
        items_id = inverted_diccionario[self.items.value]
        data_model = MaintenancesModel(
            Type=self.type.value,
            Description=self.description.value,
            Last_maintenance=self.last.value,
            Next_maintenance=self.next.value,
            Item_id=items_id,
        )
        if data_model.Description:
            try:
                self.clean_fields()
                data_tuple = (
                    data_model.Type,
                    data_model.Description,
                    data_model.Last_maintenance,
                    data_model.Next_maintenance,
                    data_model.Item_id,
                    self.selected_row[0],
                )
                query = """UPDATE Maintenances  SET Type = ?, Description = ?,
                          Last_maintenance = ?, Next_maintenance = ?, Item_id = ?
                        WHERE Maintenance_id = ?;
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
