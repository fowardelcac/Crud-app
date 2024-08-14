import flet as ft
from styles.styles import Colors, rail_style
from backend.C_mantenimientos import MaintenencePage
from backend.D_Company import CompanyPage
from backend.E_Contacts import ContactsPage
from backend.F_Constrruction import ConstructionPage
from backend.G_Items import ItemPage


class MyApp(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        self.page = page
        self.current_tabs = {
            0: [
                ft.Tab(
                    text="Mantenimientos",
                    icon=ft.icons.WORK_HISTORY,
                    content=MaintenencePage(self.page),
                ),
            ],
            1: [
                ft.Tab(
                    text="Empresas",
                    icon=ft.icons.BUSINESS,
                    content=CompanyPage(page=self.page),
                ),
                ft.Tab(
                    text="Contactos",
                    icon=ft.icons.PEOPLE_ALT,
                    content=ContactsPage(page=self.page),
                ),
                ft.Tab(
                    text="Obras",
                    icon=ft.icons.HOME,
                    content=ConstructionPage(page=self.page),
                ),
                ft.Tab(
                    text="Items", icon=ft.icons.WAREHOUSE, content=ItemPage(self.page)
                ),
            ],
        }

        self.t = ft.Tabs(
            selected_index=0,
            animation_duration=200,
            expand=True,
            divider_color=ft.colors.BLACK,
            tabs=self.current_tabs[0],
            tab_alignment=ft.TabAlignment.START,
            label_color="black",
        )
        self.rail = ft.Container(
            width=120,
            content=ft.Column(
                controls=[
                    ft.Container(
                        expand=True,
                        content=ft.NavigationRail(
                            **rail_style,
                            destinations=[
                                ft.NavigationRailDestination(
                                    icon_content=ft.Icon(
                                        name=ft.icons.CALENDAR_MONTH_ROUNDED,
                                        color="black",
                                    ),
                                    label_content=ft.Text(
                                        "Mantenimientos", color="black"
                                    ),
                                ),
                                ft.NavigationRailDestination(
                                    icon_content=ft.Icon(
                                        name=ft.icons.DATASET,
                                        color="#C0C0C0",
                                    ),
                                    label_content=ft.Text("Tablas", color="#C0C0C0"),
                                ),
                            ],
                            on_change=self.on_navigation_change,
                        ),
                    )
                ]
            ),
        )

        self.content = ft.Row(
            [self.rail, self.t],
            expand=True,
        )

    def build(self):
        return self.content

    def on_navigation_change(self, e):
        selected_index = e.control.selected_index
        self.t.tabs = self.current_tabs.get(selected_index, [])
        self.page.update()


def main(page: ft.Page):
    page.padding = 0
    page.window.resizable = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = Colors.Background.value

    bar = MyApp(page)
    page.add(bar)


ft.app(main)
