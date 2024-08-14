import flet as ft
from backend.A_database_functions import CompanyModel, DatabaseManager
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


class CompanyPage(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.selected_row = None
        self.dbm = DatabaseManager()

        self.modal = ft.AlertDialog(
            **modal_style,
            actions=[
                ft.TextButton("Si", on_click=self.handle_close),
                ft.TextButton("No", on_click=self.handle_close),
            ],
        )

        self.company_name = ft.TextField(
            **text_field_style,
            label="Nombre *",
            max_length=50,
            hint_text="Ingrese el nombre(Dato obligatorio)",
        )
        self.location = ft.TextField(
            **text_field_style, label="Ubicacion", max_length=100
        )
        self.phone = ft.TextField(
            **text_field_style,
            label="Telefono",
            max_length=50,
        )
        self.mail = ft.TextField(**text_field_style, label="Email", max_length=50)

        self.form_inputs = ft.Container(
            **form_inputs_style,
            content=ft.Column(
                scroll=ft.ScrollMode.ALWAYS,
                controls=[
                    ft.ExpansionTile(
                        ft.Text("Ingrese sus clientes.", **expansion_tile_title_style),
                        subtitle=ft.Text(
                            "Click sobre el panel para abrir el formulario.",
                            **subtitle_expansion_tile_style,
                        ),
                        affinity=ft.TileAffinity.LEADING,
                        text_color=ft.colors.BLACK,
                        controls=[
                            ft.Container(height=20),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(content=self.company_name, width=300),
                                    ft.Container(content=self.location, width=300),
                                ],
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(content=self.phone, width=300),
                                    ft.Container(content=self.mail, width=300),
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
                expand=True,
                controls=[ft.ResponsiveRow([self.data_table])],
                scroll=ft.ScrollMode.ALWAYS,
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
        query = """SELECT * FROM Companies ORDER BY Company_id DESC"""
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
                ft.DataColumn(ft.Text("Ubicacion")),
                ft.DataColumn(ft.Text("Telefono")),
                ft.DataColumn(ft.Text("Email")),
            ],
        )

    def data_loader(self, data):
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
                    ],
                )
            )
        self.page.update()

    def show_data(self):
        query = """SELECT * FROM Companies ORDER BY Company_id DESC"""
        data = self.dbm.get_table(query=query)
        self.data_loader(data)

    def search_data(self, e):
        search_text = self.search_field.value
        query = f"""SELECT * FROM Companies WHERE Company_name LIKE '{search_text}' || '%' ORDER BY Company_id DESC;"""
        data = self.dbm.get_table(query=query)
        self.data_loader(data)

    def clean_fields(self):
        self.company_name.value = ""
        self.location.value = ""
        self.phone.value = ""
        self.mail.value = ""

    def snack(self, label: str, color: str):
        self.page.snack_bar = ft.SnackBar(ft.Text(label), bgcolor=color, duration=1000)
        self.page.snack_bar.open = True

    def add_data(self, e):
        data_model = CompanyModel(
            Company_name=self.company_name.value,
            Location=self.location.value,
            Company_phone=self.phone.value,
            Company_email=self.mail.value,
        )
        if data_model.Company_name:
            try:
                self.clean_fields()
                data_tuple = (
                    data_model.Company_name,
                    data_model.Location,
                    data_model.Company_phone,
                    data_model.Company_email,
                )
                query = """INSERT INTO Companies (Company_name, Location, Company_phone, Company_email)
                            VALUES (?, ?, ?, ?)"""
                self.dbm.insert_table(
                    query=query,
                    data_model=data_tuple,
                )
                self.snack("Agregado correctamente.", "green")
            except:
                self.snack("No puede haber dos clientes con el mismo nombre.", "red")

        else:
            self.snack("El nombre es obligatorio.", "red")
        self.show_data()

    def edit_filled_text(self, e):
        try:
            if self.selected_row is None:
                raise ValueError("selected_row is None. Please select a row first.")

            self.company_name.value = self.selected_row[1]
            self.location.value = self.selected_row[2]
            self.phone.value = self.selected_row[3]
            self.mail.value = self.selected_row[4]
            self.page.update()
        except Exception as ex:
            print(f"An error occurred: {ex}")

    def handle_close(self, e):
        clicked_button_text = e.control.text
        if clicked_button_text == "Si":
            query = "DELETE FROM Companies WHERE Company_id = ?"
            self.dbm.delete_table(query=query, id=self.selected_row[0])

            self.clean_fields()
            self.snack("Eliminado correctamente.", "green")
        else:
            self.snack("Cancelado.", "orange")

        self.page.close(self.modal)
        self.show_data()

    def update_data(self, e):
        data_model = CompanyModel(
            Company_name=self.company_name.value,
            Location=self.location.value,
            Company_phone=self.phone.value,
            Company_email=self.mail.value,
        )
        if data_model.Company_name:
            try:
                self.clean_fields()
                data_tuple = (
                    data_model.Company_name,
                    data_model.Location,
                    data_model.Company_phone,
                    data_model.Company_email,
                    self.selected_row[0],
                )
                query = """UPDATE Companies SET Company_name = ?, Location = ?, Company_phone = ?, Company_email = ?
                        WHERE Company_id = ?;
                        """
                self.dbm.update_table(
                    query=query,
                    data_model=data_tuple,
                )
                self.snack("Actualizado correctamente.", "green")
            except Exception as e:
                print("-" * 100)
                print(e)
                self.snack("No puede haber dos clientes con el mismo nombre.", "red")

        else:
            self.snack("El nombre es obligatorio.", "red")
        self.show_data()
