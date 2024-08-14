import flet as ft

############################################################
# Main


class NavFeatures(ft.NavigationRailDestination):
    def __init__(self, icon_name: ft.icons, label: str):
        super().__init__(icon_name, label)
        self.icon = ft.NavigationRailDestination(
            icon_content= ft.Icon(
                name=icon_name,
                color="#C0C0C0"
            ),
            label_content=ft.Text(label, color="#C0C0C0")
        )
