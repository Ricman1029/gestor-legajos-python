import flet


class BotonCarta(flet.IconButton):
    def __init__(
            self,
            icon: flet.Icons,
            tooltip: str,
            on_click: flet.OptionalEventCallable | None = None,
            on_blur: flet.OptionalEventCallable | None = None,
            on_focus: flet.OptionalEventCallable | None = None,
    ):
        super().__init__(
            visible=False,
            animate_opacity=200,
            offset=flet.Offset(0, 0.75),
            animate_offset=flet.Animation(duration=200, curve=flet.AnimationCurve.EASE),
            bgcolor=flet.Colors.PRIMARY,
            icon=icon,
            icon_color=flet.Colors.ON_PRIMARY,
            icon_size=30,
            tooltip=tooltip,
            on_click=on_click,
            on_blur=on_blur,
            on_focus=on_focus,
        )


class CartaAnimada(flet.Container):
    def __init__(
            self,
            botones: [BotonCarta],
            cuerpo: [flet.Control],
            on_click: flet.OptionalEventCallable | None = None,
            on_tap_down: flet.OptionalEventCallable | None = None,
            on_long_press: flet.OptionalEventCallable | None = None,
            width: int = 280,
            height: int = 380,
            bgcolor: flet.Colors = flet.Colors.PRIMARY_CONTAINER,
            border_color: flet.Colors = flet.Colors.ON_PRIMARY_CONTAINER,
    ):
        self.cuerpo = cuerpo
        self.border_color = border_color
        self._row_iconos = flet.Row(
            controls=[
                *botones,
            ],
            alignment=flet.MainAxisAlignment.CENTER
        )
        self._container_animado = flet.Container(
            width=width,
            height=height,
            bgcolor=bgcolor,
            border_radius=12,
            animate=flet.Animation(duration=600, curve=flet.AnimationCurve.EASE),
            border=flet.border.all(2, bgcolor),
            content=flet.Column(
                offset=flet.Offset(0, 0),
                animate_offset=flet.Animation(300, flet.AnimationCurve.EASE),
                alignment=flet.MainAxisAlignment.CENTER,
                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                spacing=0,
                controls=[
                    *cuerpo,
                ]
            )
        )
        self._card = flet.Card(
            elevation=0,
            content=self._container_animado
        )
        super().__init__(
            on_hover=self.animar_card,
            on_click=on_click,
            on_tap_down=on_tap_down,
            on_long_press=on_long_press,
            content=flet.Stack(
                width=width + 40,
                height=height + 60,
                alignment=flet.alignment.top_center,
                controls=[
                    self._card,
                    flet.Container(
                        bottom=40,
                        content=self._row_iconos
                    )
                ]
            )
        )

    def animar_card(self, e):
        for icono in self._row_iconos.controls:
            icono.visible = True
        self._row_iconos.update()

        if e.data == "true":
            # Animación de elevación de la card
            for _ in range(20):
                self._card.elevation += 1
                self._card.update()

            # Animación del borde de la card
            self._container_animado.border = flet.border.all(4, self.border_color)
            self._container_animado.content.offset = flet.Offset(0, -0.02)
            self._container_animado.update()

            # Animación de la posición del botón
            for icono in self._row_iconos.controls:
                icono.offset = flet.Offset(0, 0)
                icono.opacity = 1
                icono.update()

        else:
            # Animación de elevación de la card
            for _ in range(20):
                self._card.elevation -= 1
                self._card.update()

            # Animación del borde de la card
            self._container_animado.border = None
            self._container_animado.content.offset = flet.Offset(0, 0)
            self._container_animado.update()

            # Animación de la posición del botón
            for icono in self._row_iconos.controls:
                icono.offset = flet.Offset(0, 0.75)
                icono.opacity = 0
                icono.update()
