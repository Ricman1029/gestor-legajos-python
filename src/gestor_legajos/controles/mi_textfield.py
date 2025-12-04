import flet


class MiTextField(flet.TextField):
    def __init__(
            self,
            label,
            width=300,
            on_submit=None,
            value: str | None = None,
            hint_text: str | None = None,
            error_text: bool = True,
            requerido: bool = True,
            autofocus: bool = False,
            max_length: int | None = None,
    ):
        super().__init__(
            width=width,
            label=label,
            value=value,
            hint_text=hint_text,
            autofocus=autofocus,
            max_length=max_length,
            border=flet.InputBorder.UNDERLINE,
            filled=True,
            dense=True,
            error_text="Requerido" if error_text else None,
            on_change=self.campo_requerido if requerido else None,
            on_submit=on_submit,
        )
    
    def campo_requerido(self, e):
        if e.control.value == "":
            e.control.error_text = "Requerido"
        else:
            e.control.error_text = None
        self.update()