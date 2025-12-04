import flet


class MiTextButton(flet.TextButton):
    def __init__(
            self,
            texto: str,
            on_click: flet.OptionalEventCallable,
            icon: flet.Icons = flet.Icons.ADD):
        super().__init__(
            text=texto,
            icon=icon,
            on_click=on_click,
            style=flet.ButtonStyle(
                bgcolor={
                    flet.ControlState.DEFAULT: flet.Colors.PRIMARY,
                    flet.ControlState.HOVERED: flet.Colors.with_opacity(
                        opacity=0.8,
                        color=flet.Colors.ON_PRIMARY_CONTAINER
                    )
                },
                shape=flet.RoundedRectangleBorder(radius=3),
                color=flet.Colors.ON_PRIMARY,
            ),
        )
