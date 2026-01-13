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

    async def handle_tile_hover(e: ft.Event[ft.ListTile]):
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
