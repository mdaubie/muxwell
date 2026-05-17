from __future__ import annotations

import typer


def MutuallyExclusiveGroup():
    group_key = object()

    def callback(
        ctx: typer.Context, param: typer.CallbackParam, value: bool | str | int | None
    ):
        # Add cli option to group if it was called with a value
        if value is not None and value is not False:
            groups = ctx.meta.setdefault("_mutually_exclusive_groups", {})
            param_name = groups.get(group_key)
            if param_name is None:
                groups[group_key] = param.name
            else:
                raise typer.BadParameter(
                    f"{param.name} is mutually exclusive with {param_name}"
                )

        return value

    return callback
