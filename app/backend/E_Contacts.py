import flet as ft
from backend.A_database_functions import ContactsModel, DatabaseManager
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


class ContactsPage(ft.Container):
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
        self.contact_name = ft.TextField(
            **text_field_style,
            label="Nombre *",
            max_length=50,
            hint_text="Ingrese el nombre(Dato obligatorio)",
        )
        self.contact_phone = ft.TextField(
            **text_field_style,
            label="Telefono *",
            hint_text="Ingrese el telefon(Dato obligatorio)",
            max_length=50,
        )
        self.email = ft.TextField(
            **text_field_style,
            label="Email",
            hint_text="Ingrese el email.",
            max_length=50,
        )
        self.job_position = ft.TextField(
            **text_field_style,
            label="Cargo",
            hint_text="Ingrese su puesto laboral.",
            max_length=50,
        )

        self.company = ft.Dropdown(
            **text_field_style,
            label="Nombre de la empresa. *",
            hint_content="Seleccionar el nombre del cliente(Dato obligatorio)",
        )

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
                        on_change=self.dic_change,
                        controls=[
                            ft.Container(height=20),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(content=self.contact_name, width=300),
                                    ft.Container(content=self.contact_phone, width=300),
                                ],
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(content=self.email, width=300),
                                    ft.Container(content=self.job_position, width=300),
                                ],
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(content=self.company, width=600),
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
        query = """SELECT * FROM Contacts ORDER BY Contact_id DESC"""
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
                ft.DataColumn(ft.Text("Telefono")),
                ft.DataColumn(ft.Text("Email")),
                ft.DataColumn(ft.Text("Puesto laboral")),
                ft.DataColumn(ft.Text("Empresa")),
            ],
        )

    def dic_build(self):
        query = """SELECT * FROM Companies ORDER BY Company_id DESC"""
        data = self.dbm.get_table(query=query)
        return {i[0]: i[1] for i in data}
    
    def dic_change(self, e):
        diccionario = self.dic_build()
        self.company.options = [
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

    def show_data(self):
        query = """SELECT * FROM Contacts ORDER BY Contact_id DESC"""
        data = self.dbm.get_table(query=query)
        self.data_loader(data)
        self.page.update()

    def search_data(self, e):
        search_text = self.search_field.value
        query = f"""SELECT * FROM Contacts WHERE Contact_name LIKE '{search_text}' || '%' ORDER BY Contact_id DESC;"""
        data = self.dbm.get_table(query=query)
        self.data_loader(data)
        self.page.update()

    def clean_fields(self):
        self.contact_name.value = ""
        self.contact_phone.value = ""
        self.email.value = ""
        self.job_position.value = ""
        self.company.value = ""

    def snack(self, label: str, color: str):
        self.page.snack_bar = ft.SnackBar(ft.Text(label), bgcolor=color, duration=1000)
        self.page.snack_bar.open = True

    def add_data(self, e):
        self.diccionario = self.dic_build()
        inverted_diccionario = {v: k for k, v in self.diccionario.items()}
        company_id = inverted_diccionario[self.company.value]

        data_model = ContactsModel(
            Contact_name=self.contact_name.value,
            Contact_phone=self.contact_phone.value,
            Contact_email=self.email.value,
            Job_position=self.job_position.value,
            Company_id=company_id,
        )
        if data_model.Contact_name and data_model.Company_id and data_model.Contact_phone:
            try:
                self.clean_fields()
                data_tuple = (
                    data_model.Contact_name,
                    data_model.Contact_phone,
                    data_model.Contact_email,
                    data_model.Job_position,
                    data_model.Company_id,
                )
                query = """INSERT INTO Contacts  (Contact_name, Contact_phone, Contact_email, Job_position, Company_id)
                    VALUES (?, ?, ?, ?, ?)"""
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

            self.contact_name.value = self.selected_row[1]
            self.contact_phone.value = self.selected_row[2]
            self.email.value = self.selected_row[3]
            self.job_position.value = self.selected_row[4]
            self.company.value = self.diccionario[self.selected_row[5]]
            self.page.update()
        except Exception as ex:
            print(f"An error occurred: {ex}")

    def handle_close(self, e):
        self.diccionario = self.dic_build()
        clicked_button_text = e.control.text
        if clicked_button_text == "Si":
            query = "DELETE FROM Contacts WHERE Contact_id = ?"
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
        company_id = inverted_diccionario[self.company.value]
        data_model = ContactsModel(
            Contact_name=self.contact_name.value,
            Contact_phone=self.contact_phone.value,
            Contact_email=self.email.value,
            Job_position=self.job_position.value,
            Company_id=company_id,
        )
        if data_model.Contact_name and data_model.Company_id and data_model.Contact_phone:
            try:
                self.clean_fields()
                data_tuple = (
                    data_model.Contact_name,
                    data_model.Contact_phone,
                    data_model.Contact_email,
                    data_model.Job_position,
                    data_model.Company_id,
                    self.selected_row[0],
                )
                query = """UPDATE Contacts SET Contact_name = ?, Contact_phone = ?, Contact_email = ?, Job_position = ?, Company_id = ?
                            WHERE Contact_id = ?;
                        """
                self.dbm.update_table(
                    query=query,
                    data_model=data_tuple,
                )
                self.snack("Actualizado correctamente.", "green")
            except:
                self.snack("No puede haber dos clientes con el mismo nombre.", "red")

        else:
            self.snack("El nombre es obligatorio.", "red")
        self.show_data()
