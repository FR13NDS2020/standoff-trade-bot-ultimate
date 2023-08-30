import os
import random
import json
import dearpygui.dearpygui as dpg
from functions import get_pixels_json, configure_colors, coordinate_calculator, save_data, save_refresh_buy, load_data, \
    save_recognize, load_recognize
from text_recognize import text_recognition

with open("config.json", "r") as f:
    config = json.load(f)
row_count = config["row_count"]

image_files = [file for file in os.listdir("./waifu") if file.lower().endswith((".png", ".jpg", ".jpeg"))]
random_image = random.choice(image_files)
image_path = os.path.join("./waifu", random_image)

width, height, channels, data = dpg.load_image(image_path)
aspect_ratio = height / width
aspect_ratio2 = width / height

with open("data.json", "r") as f:
    pixel_data = json.load(f)

dpg.create_context()

with dpg.window(tag="Main window", autosize=True, no_collapse=True, no_title_bar=True):
    with dpg.menu_bar():
        with dpg.menu(label="Coordinate Calculator"):
            x1 = dpg.add_input_int(label="First X")
            y1 = dpg.add_input_int(label="First Y")
            x2 = dpg.add_input_int(label="Last X")
            y2 = dpg.add_input_int(label="Last Y")
            rows = dpg.add_input_int(label="Rows")
            dpg.add_button(label="Calculate", callback=lambda: coordinate_calculator(
                dpg.get_value(x1), dpg.get_value(x2), dpg.get_value(y1), dpg.get_value(y2), dpg.get_value(rows)
            ))

        with dpg.menu(label="Refresh and Buy Button"):
            dpg.add_button(label="Save Values", callback=save_refresh_buy)
            dpg.add_input_int(label="Buy X", tag="buy x")
            dpg.add_input_int(label="Refresh X", tag="refresh x")
            dpg.add_input_int(label="Refresh Y", tag="refresh y")
            dpg.add_text("Confirm Cords")
            dpg.add_input_int(label="Confirm X", tag="confirm x")
            dpg.add_input_int(label="Confirm Y", tag="confirm y")
    with dpg.tab_bar():
        with dpg.tab(label="Catch stickers"):

            with dpg.child_window(autosize_x=True, height=19, no_scrollbar=True):
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Save", callback=lambda: save_data(row_count=row_count), parent="Actions")
                    dpg.add_button(label="Load", callback=load_data, parent="Actions")
                    dpg.add_button(label="catch 4 stickers",
                                   callback=lambda: get_pixels_json(pixel_data, test_mode=False), parent="Actions")
                    dpg.add_button(label="catch 3 stickers",
                                   callback=lambda: get_pixels_json(pixel_data, sticker=2, test_mode=False),
                                   parent="Actions")
                    dpg.add_button(label="catch 2 stickers",
                                   callback=lambda: get_pixels_json(pixel_data, sticker=3, test_mode=False),
                                   parent="Actions")

                    dpg.add_button(label="Test4", callback=lambda: (get_pixels_json(pixel_data, test_mode=True)),
                                   parent="Actions")
                    dpg.add_button(label="Test3",
                                   callback=lambda: (get_pixels_json(pixel_data, sticker=2, test_mode=True)),
                                   parent="Actions")
                    dpg.add_button(label="Test2",
                                   callback=lambda: (get_pixels_json(pixel_data, sticker=3, test_mode=True)),
                                   parent="Actions")

            with dpg.group(horizontal=True):
                with dpg.child_window(label="Setup", width=530, autosize_y=True):
                    with dpg.table(
                            header_row=False,
                            resizable=True,
                            policy=dpg.mvTable_SizingStretchProp,
                            borders_outerV=True,
                            borders_innerV=True,
                            borders_innerH=True,
                            borders_outerH=True,
                            width=500
                    ):
                        dpg.add_table_column(label="1", width=90)
                        dpg.add_table_column(label="2", width=90)
                        dpg.add_table_column(label="3", width=90)

                        for i in range(row_count):
                            with dpg.table_row(label=f"{i}"):
                                for j in range(3):
                                    with dpg.table_cell():
                                        dpg.add_text("Pos:")
                                        dpg.add_input_int(label=f"X##{i}{j}", tag=f"X##{i}{j}", width=90)
                                        dpg.add_input_int(label=f"Y##{i}{j}", tag=f"Y##{i}{j}", width=90)
                                        dpg.add_text("RGB:")
                                        dpg.add_input_int(label=f"R##{i}{j}", tag=f"R##{i}{j}", width=90)
                                        dpg.add_input_int(label=f"G##{i}{j}", tag=f"G##{i}{j}", width=90)
                                        dpg.add_input_int(label=f"B##{i}{j}", tag=f"B##{i}{j}", width=90)
                                        dpg.add_slider_int(max_value=25, label="Tol", tag=f"tolerance##{i}{j}",
                                                           width=90)

                with dpg.child_window(label="Configure Colors", width=400, autosize_y=True, border=False):
                    dpg.add_button(tag="Configure_button", label="Configure",
                                   callback=lambda: configure_colors(duration=dpg.get_value("duration"),
                                                                     row_count=row_count),
                                   parent="Configure Colors")
                    with dpg.tooltip("Configure_button"):
                        dpg.add_text(
                            "  when pass changes need to run the and configure colors if background changed   ")

                    dpg.add_slider_int(label="Duration in sec", tag="duration", min_value=5, max_value=40)
                    with dpg.table(
                            header_row=False,
                            resizable=True,
                            policy=dpg.mvTable_SizingStretchProp,
                            borders_outerH=True,
                            borders_innerV=True,
                            borders_innerH=True,
                            borders_outerV=True,
                    ):
                        dpg.add_table_column(label="1")
                        dpg.add_table_column(label="2")
                        dpg.add_table_column(label="3")

                        for i in range(row_count):
                            with dpg.table_row():
                                for j in range(3):
                                    with dpg.table_cell():
                                        dpg.add_text("Sticker Position:")
                                        dpg.add_input_int(label=f"X", parent="Configure Colors", tag=f"X#{i}{j}")
                                        dpg.add_input_int(label=f"Y", parent="Configure Colors", tag=f"Y#{i}{j}")


                def update_window_size():
                    window_width = dpg.get_viewport_width()
                    window_height = dpg.get_viewport_height()

                    image_width = window_width - 964
                    aspect_height = image_width * aspect_ratio
                    image_height = window_height - 85

                    if image_height < aspect_height:
                        dpg.set_item_width("image_tag", image_height * aspect_ratio2)
                        dpg.set_item_height("image_tag", image_height)
                    else:
                        dpg.set_item_width("image_tag", image_width)
                        dpg.set_item_height("image_tag", aspect_height)


                with dpg.child_window(border=False, tag="wallpaper", no_scrollbar=True) as wallpaper_window:
                    with dpg.texture_registry(show=False):
                        dpg.add_static_texture(width=width, height=height, default_value=data, tag="texture_tag")

                    dpg.add_image("texture_tag", tag="image_tag")

                with dpg.item_handler_registry(tag="wallpaper handler") as handler:
                    dpg.add_item_resize_handler(callback=update_window_size)

                with dpg.theme() as global_theme:
                    with dpg.theme_component(dpg.mvAll):
                        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 2)
                        dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)
                        dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
                        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 6)
                        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)
                        dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 12)

        with dpg.tab(label="Lovlja peredach"):
            with dpg.group(horizontal=True):
                dpg.add_button(label="Save Data", callback=lambda: save_recognize())
                dpg.add_button(label="Load Data", callback=lambda: load_recognize())
                min_price_input = dpg.add_input_int(label="Min price", tag="Min_price", default_value=50, width=80)
                dpg.add_button(label="start",
                               callback=lambda: text_recognition())

            with dpg.group(horizontal=True):
                with dpg.child_window(label="configure sell button", width=550, autosize_y=True, border=False):
                    with dpg.table(header_row=True, resizable=True, policy=dpg.mvTable_SizingStretchProp):
                        dpg.add_table_column(label="Item")
                        dpg.add_table_column(label="X")
                        dpg.add_table_column(label="Y")

                        # Sell Button
                        with dpg.table_row():
                            dpg.add_text("Sell Button")
                            sell_x = dpg.add_input_int(label="X##Sell", tag="SellButton_X")
                            sell_y = dpg.add_input_int(label="Y##Sell", tag="SellButton_Y")

                        # First Item
                        with dpg.table_row():
                            dpg.add_text("First Item")
                            first_item_x = dpg.add_input_int(label="X##FirstItem", tag="FirstItem_X")
                            first_item_y = dpg.add_input_int(label="Y##FirstItem", tag="FirstItem_Y")

                        # Select Button
                        with dpg.table_row():
                            dpg.add_text("Select Button")
                            select_x = dpg.add_input_int(label="X##Select", tag="SelectButton_X")
                            select_y = dpg.add_input_int(label="Y##Select", tag="SelectButton_Y")

                        # Enter Price
                        with dpg.table_row():
                            dpg.add_text("Enter Price")
                            enter_price_x = dpg.add_input_int(label="X##EnterPrice",
                                                              tag="EnterPrice_X")
                            enter_price_y = dpg.add_input_int(label="Y##EnterPrice",
                                                              tag="EnterPrice_Y")

                        # Create Listing Button
                        with dpg.table_row():
                            dpg.add_text("Create Listing Button")
                            create_listing_x = dpg.add_input_int(label="X##CreateListing",
                                                                 tag="CreateListing_X")
                            create_listing_y = dpg.add_input_int(label="Y##CreateListing",
                                                                 tag="CreateListing_Y")

                        # Wait time
                        with dpg.table_row():
                            dpg.add_text("Add Wait Time")
                            wait_time = dpg.add_input_int(label="time", tag="WaitTime")

                with dpg.child_window(label="Configure text recognize", width=600, autosize_y=True, border=False):
                    with dpg.table(header_row=False,
                                   resizable=True,
                                   policy=dpg.mvTable_SizingStretchProp,
                                   borders_outerH=True,
                                   borders_innerV=True,
                                   borders_innerH=True,
                                   borders_outerV=True, ):
                        dpg.add_table_column(label="Item")
                        # Row for "Sell Button"
                        with dpg.table_row():
                            with dpg.table_cell():
                                dpg.add_text("Monitor:")
                                dpg.add_input_int(label=f"top", tag=f"top")
                                dpg.add_input_int(label=f"left", tag=f"left")
                                dpg.add_input_int(label=f"width", tag=f"width")
                                dpg.add_input_int(label=f"height", tag=f"height")

                                dpg.add_text("Refresh button")
                                refresh_x = dpg.add_input_int(label="refresh_x", tag="refresh_x")
                                refresh_y = dpg.add_input_int(label="refresh_y", tag="refresh_y")

        with dpg.tab(label="lovlja 0.03"):
            with dpg.child_window(label="somethingaa", width=550, autosize_y=True, border=False):
                dpg.add_text("some text ehre")

dpg.bind_theme(global_theme)
dpg.bind_item_handler_registry("Main window", "wallpaper handler")

dpg.create_viewport(title="Sticker Stealer", width=1380, height=920, min_width=1240, min_height=700)
dpg.set_viewport_large_icon("./icons/256.ico")
dpg.set_viewport_always_top(True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Main window", True)
dpg.start_dearpygui()
dpg.destroy_context()
