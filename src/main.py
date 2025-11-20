import flet
from src.app_layout import AppLayout


class LegajosAutomaticosApp(AppLayout):
    def __init__(self, page: flet.Page):
        self.page = page
        super().__init__(
            page=self.page,
            expand=True,
        )
        self.page.theme = flet.Theme(
            color_scheme=flet.ColorScheme(
                primary="#6750A4",
                on_primary="#FFFFFF",
                primary_container="#EADDFF",
                on_primary_container="#4F378B",
                secondary="#625B71",
                on_secondary="#FFFFFF",
                secondary_container="#E8DEF8",
                on_secondary_container="#4A4458",
                tertiary="#7D5260",
                on_tertiary="#FFFFFF",
                tertiary_container="#FFD8E4",
                on_tertiary_container="#633B48",
                error="#B3261E",
                on_error="#FFFFFF",
                error_container="#F9DEDC",
                on_error_container="#8C1D18",
                surface="#FEF7FF",
                on_surface="#1D1B20",
                surface_variant="#E7E0EC",
                on_surface_variant="#49454F",
                surface_container_high="#ECE6F0",
                surface_container="#F3EDF7",
                surface_container_low="#F7F2FA",
                surface_container_lowest="#FFFFFF",
                inverse_surface="#322F35",
                on_inverse_surface="#F5EFF7",
                surface_tint="#6750A4",
                outline="#79747E",
                outline_variant="#CAC4D0",
                primary_fixed="#EADDFF",
                on_primary_fixed="#21005D",
                background="#FEF7FF",
                on_background="#1D1B20",
                surface_dim="#DED8E1",
                surface_bright="#FEF7FF",
                secondary_fixed="#E8DEF8",
                on_secondary_fixed="#1D192B",
                secondary_fixed_dim="#CCC2DC",
                on_secondary_fixed_variant="#4A4458",
                tertiary_fixed="#FFD8E4",
                on_tertiary_fixed="#31111D",
                tertiary_fixed_dim="#EFB8C8",
                on_tertiary_fixed_variant="#633B48",
                inverse_primary="#D0BCFF",
                primary_fixed_dim="#EADDFF",
                on_primary_fixed_variant="#4F378B",
                scrim="#000000",
                shadow="#000000",
            )
        )
        self.page.dark_theme = flet.Theme(
            color_scheme=flet.ColorScheme(
                primary="#D0BCFF",
                on_primary="#381E72",
                primary_container="#4F378B",
                on_primary_container="#EADDFF",
                secondary="#CCC2DC",
                on_secondary="#332D41",
                secondary_container="#4A4458",
                on_secondary_container="#E8DEF8",
                tertiary="#EFB8C8",
                on_tertiary="#492532",
                tertiary_container="#633B48",
                on_tertiary_container="#FFD8E4",
                error="#F2B8B5",
                on_error="#601410",
                error_container="#8C1D18",
                on_error_container="#F9DEDC",
                surface="#141218",
                on_surface="#E6E0E9",
                surface_variant="#49454F",
                on_surface_variant="#CAC4D0",
                surface_container_high="#2B2930",
                surface_container="#211F26",
                surface_container_low="#1D1B20",
                surface_container_lowest="#0F0D13",
                inverse_surface="#E6E0E9",
                on_inverse_surface="#322F35",
                surface_tint="#D0BCFF",
                outline="#938F99",
                outline_variant="#49454F",
                primary_fixed="#EADDFF",
                on_primary_fixed="#21005D",
                primary_fixed_dim="#D0BCFF",
                on_primary_fixed_variant="#4F378B",
                inverse_primary="#6750A4",
                secondary_fixed="#E8DEF8",
                on_secondary_fixed="#1D192B",
                secondary_fixed_dim="#CCC2DC",
                on_secondary_fixed_variant="#4A4458",
                tertiary_fixed="#FFD8E4",
                on_tertiary_fixed="#31111D",
                tertiary_fixed_dim="#EFB8C8",
                on_tertiary_fixed_variant="#633B48",
                background="#141218",
                on_background="#E6E0E9",
                surface_bright="#3B383E",
                surface_dim="#141218",
                scrim="#000000",
                shadow="#000000",
            )
        )
        self.appbar = flet.AppBar(
            leading=flet.Icon(flet.Icons.GRID_GOLDENRATIO),
            leading_width=100,
            title=flet.Text(
                value="Legajos Automáticos",
                size=32,
                text_align=flet.TextAlign.CENTER,
                weight=flet.FontWeight.W_600,
                color=flet.Colors.ON_SURFACE,
            ),
            center_title=False,
            toolbar_height=75,
            actions=[
                flet.IconButton(
                    icon=flet.Icons.DARK_MODE,
                    on_click=self.cambiar_tema
                )
            ]
        )
        self.page.theme_mode = "light"
        self.page.padding = 0
        self.page.title = "Flet App"
        self.page.appbar = self.appbar

    def cambiar_tema(self, e):
        if self.page.theme_mode == "dark":
            self.page.theme_mode = "light"
            self.appbar.actions[0].icon = flet.Icons.LIGHT_MODE
        else:
            self.page.theme_mode = "dark"
            self.appbar.actions[0].icon = flet.Icons.DARK_MODE
        self.page.update()


def main(page: flet.Page):
    app = LegajosAutomaticosApp(page)
    page.add(app)
    page.go("/empresas")


flet.app(main)
