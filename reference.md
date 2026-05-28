<center><h1>Reference Guide</h1></center>

This serves as a **reference guide** regarding the functions involved within our code
as we go on with this project.

## Model
### Phase 2 Model
Here are the variables used in the `__init__` part:
```py
self._width  # The width of the screen
self._height  # The height of the screen
self._is_game_over  # Sets to true if game over conds satisfied
self._dimensions  # (columns, rows) of the gridded map
self._grid_size  # side length of a cell in pixels
self._total_grid_height  # height of the map UI in pixels
self._path  # The coordinates of the tiles
self._start_row  # Row of the first appearance of enemy
self._start_col  # Col of the first appearance of enemy
self._enemies  # The types of enemies to appear
self._rounds  # Total rounds of a certain game phase
self._current_round  # Tracks the current round
self._displayed enemies  # List of Enemy() objects displayed on the screen
self._tick  # Records the number of frames through time (increments per frame)
self._gun_coords  # The coordinate of the shooter
self._pending_bullets  # List of Bullet() object/s that will be shot next
self._displayed_bullets  # List of Bullet() objects displayed on the screen
self._next_color  # Tracks the color of the next bullet to be shot. Used to assign the color of the cursor as a visual aid tell what color will the next bullet have.
self._exp  # Tracks the exp
self._hp  # Tracks the hp
```
Those with `?` comments are variables I cannot identify yet, please help me add details
to these.

## View
```py
start_game(width, height)
display_map(height, total_grid_height, row_count, col_count, grid_size)
display_path(height, total_grid, height, row_count, col_count, grid_size, path_cells)
display_enemies(height, total_grid_height, row_count, col_count, grid_size, enemies: list[Enemy])
is_left_clicked()
is_gun_wasd_clicked()
display_bullets(height, total_grid_height, row_count, col_count, grid_size, bullets: list[Bullet])
display_gun(height, total_grid_height, grid_size, gun_col, gun_row)
display_text(current_round, rounds, hp, exp, font_addrss, size)
display_cursor(next_color)
reset_screen()
```

## Controller