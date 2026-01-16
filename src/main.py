import flet as ft

colors = [
    "Amber",
    "Blue Grey",
    "Brown",
    "Deep Orange",
    "Green",
    "Light Blue",
    "Orange",
    "Red",
]


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def build_tiles(items: list[str]) -> list[ft.Control]:
        return [
            ft.Container(
                content=ft.Text(item, color=ft.Colors.BLUE),
                on_click=handle_tile_click,
                on_hover=handle_tile_hover,
                bgcolor=ft.Colors.RED,
            )
            for item in items
        ]

    async def handle_tile_click(e: ft.Event[ft.ListTile]):
        await anchor.close_view()
        handle_submit(e.control.content)

    current_tile = -1

    async def on_keyboard(e: ft.KeyboardEvent):
        nonlocal current_tile
        if e.ctrl:
            if e.key.lower() == "n" or e.key == "Arrow Down":
                current_tile += 1
                if current_tile == len(anchor.controls):
                    current_tile = 0
                hover_event = ft.ControlEvent(
                    name="hover_down",
                    control=anchor.controls[current_tile],
                )
                await handle_tile_hover(hover_event)

            elif e.key.lower() == "p" or e.key == "Arrow Up":
                if current_tile == -1 or current_tile == 0:
                    current_tile = len(anchor.controls)
                current_tile -= 1
                print(current_tile)
                hover_event = ft.ControlEvent(
                    name="hover_up",
                    control=anchor.controls[current_tile],
                )
                await handle_tile_hover(hover_event)

            elif e.key.lower() == "f":
                await anchor.open_view()

    async def handle_tile_hover(e: ft.Event[ft.ListTile]):
        for tile in anchor.controls:
            tile.bgcolor = ft.Colors.RED
            tile.content.color = ft.Colors.BLUE
        e.control.bgcolor = (
            ft.Colors.BLUE if e.control.bgcolor == ft.Colors.RED else ft.Colors.RED
        )
        e.control.content.color = (
            ft.Colors.RED
            if e.control.content.color == ft.Colors.BLUE
            else ft.Colors.BLUE
        )
        e.control.update()
        anchor.value = e.control.content.value

    async def handle_change(e: ft.Event[ft.SearchBar]):
        nonlocal current_tile
        current_tile = -1
        query = e.control.value.strip().lower()
        matching = (
            [color for color in colors if query in color.lower()] if query else colors
        )
        anchor.controls = build_tiles(matching)

    def handle_submit(e: ft.Event[ft.SearchBar]):
        if e.data:
            print(f"Submit: {e.data}")
        else:
            print(f"Submit: {e.value}")

    async def handle_tap(e: ft.Event[ft.SearchBar]):
        await anchor.open_view()

    page.on_keyboard_event = on_keyboard
    page.add(
        anchor := ft.SearchBar(
            view_elevation=4,
            divider_color=ft.Colors.AMBER,
            bar_hint_text="Search database...",
            view_hint_text="Choose an item from database",
            on_change=handle_change,
            on_submit=handle_submit,
            on_tap=handle_tap,
            controls=build_tiles(colors),
        ),
    )


if __name__ == "__main__":
    ft.run(main)
