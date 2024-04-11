# Imports at the top
import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly, render_widget
from shinyswatch import theme
from palmerpenguins import load_penguins
import palmerpenguins
import seaborn as sns
from shiny import reactive, render
from faicons import icon_svg

#Load Penguins Dataset
penguins_df = palmerpenguins.load_penguins()

#Reactive Calc to Filter Data
@reactive.calc
def filtered_data():
    return penguins_df[
        (penguins_df["species"].isin(input.selected_species_list())) &
        (penguins_df["island"].isin(input.selected_island_list()))
    ]

# Page Title
ui.page_opts(title="Penguins Dashboard", fillable=True)

# Add a theme
theme.morph()

#Add a sidebar
with ui.sidebar(open="open"):
    with ui.accordion():
        with ui.accordion_panel("Select Species", style="background-color: #FFDAB9;"):
          ui.input_checkbox_group("selected_species_list", 
                                 "Select Species", 
                                 ["Adelie", "Gentoo", "Chinstrap"], 
                                 selected=["Adelie"], 
                                 inline=True)
        with ui.accordion_panel("Select Island", style="background-color: #FFDAB9;"):
          ui.input_checkbox_group("selected_island_list", 
                                 "Select Island", 
                                 ["Torgersen", "Biscoe", "Dream"], 
                                 selected=["Torgersen"], 
                                 inline=True)
        with ui.accordion_panel("Select Attribute", style="background-color: #FFDAB9;"):
            ui.input_selectize("selected_attribute",
                            "Select Attribute",
                            ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
                           )
        with ui.accordion_panel("Plotly Bins", style="background-color: #FFDAB9;"):
            ui.input_slider("plotly_bin_count", "Plotly bin count", 1, 25, 15)
        with ui.accordion_panel("Seaborn Bins", style="background-color: #FFDAB9;"):
            ui.input_slider("seaborn_bin_count", "Seaborn bin count", 1, 25, 15)
        with ui.accordion_panel("Body Mass", style="background-color: #FFDAB9;"):
            ui.input_slider("body_mass_count", "Body Mass Range", 2700, 6300, 2700)
        with ui.accordion_panel("Sex", style="background-color: #FFDAB9;"):
            ui.input_checkbox_group(
        "sex",
        "Sex",
        ["male", "female"],
        selected=["male", "female"],
    )    

    ui.hr()
    ui.a("Github", href="https://github.com/ryankrabbe/cintel-06-custom", target="_blank", style="color: Red;")

    #The main section with according, cards, value boxes, and space for grids and charts
    with ui.accordion():
        with ui.accordion_panel("Penguins Dashboard"):
            with ui.layout_columns():
                with ui.value_box(showcase=icon_svg("snowman"),max_height="200px", theme="bg-gradient-blue-light-blue"):
                    "Total Penguins"
                @render.text
                def display_penguin_count():
                    df = filtered_data()
                    

