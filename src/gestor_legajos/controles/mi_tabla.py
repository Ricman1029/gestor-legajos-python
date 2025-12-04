import flet
import flet.core.datatable


class MyScrollableDataTable(flet.Container):
    """
    Una tabla en la que se puede scrollear libremente.

    Para activar el scrolling hay que setear el atributo height
    """
    def __init__(
            self,
            columns: [flet.DataColumn],
            rows: [flet.DataRow],
            auto_scroll: bool = False,
            column_spacing: int | float | None = None,
            vertical_lines: flet.BorderSide | None = None,
            height: int | float | None = None,
            border_radius: flet.BorderRadius | int | None = 5,
            border: flet.Border | None = None,
    ):
        super().__init__(
            padding=10,
            border_radius=border_radius,
            border=border,
            content=flet.Column(
                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                controls=[
                    flet.DataTable(
                        columns=[
                            columna for columna in columns
                        ],
                        rows=[
                            row for row in rows
                        ],
                        heading_row_color=flet.Colors.PRIMARY,
                        heading_text_style=flet.TextStyle(
                            color=flet.Colors.ON_PRIMARY,
                            weight=flet.FontWeight.W_600,
                        ),
                        data_row_max_height=0,
                        data_row_min_height=0,
                        column_spacing=column_spacing,
                    ),
                    flet.Column(
                        scroll=flet.ScrollMode.ALWAYS,
                        height=height,
                        auto_scroll=auto_scroll,
                        controls=[
                            flet.DataTable(
                                columns=[columna for columna in columns],
                                rows=[
                                    row for row in rows
                                ],
                                heading_row_height=0,
                                column_spacing=column_spacing,
                                vertical_lines=vertical_lines,
                                data_row_color={
                                    flet.ControlState.HOVERED: flet.Colors.ON_SURFACE_VARIANT,
                                    flet.ControlState.DEFAULT: flet.Colors.with_opacity(
                                        opacity=0.5,
                                        color=flet.Colors.SURFACE),
                                },
                                data_text_style=flet.TextStyle(
                                    color=flet.Colors.ON_SURFACE,
                                )
                            )
                        ],
                    ),
                ],
            ),
        )
