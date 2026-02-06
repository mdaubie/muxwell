from __future__ import annotations

import typer


def MutuallyExclusiveGroup():
    param_name: str | None = None

    def callback(
        ctx: typer.Context, param: typer.CallbackParam, value: bool | str | int | None
    ):
        # Add cli option to group if it was called with a value
        if value is not None and value is not False:
            nonlocal param_name
            if param_name is None:
                param_name = param.name
            else:
                raise typer.BadParameter(
                    f"{param.name} is mutually exclusive with {param_name}"
                )

        return value

    return callback
