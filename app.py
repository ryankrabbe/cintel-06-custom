import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly, render_widget
import palmerpenguins
import pandas as pd 
import seaborn as sns
from shiny import reactive, render, req
from shinyswatch import theme
from faicons import icon_svg
from ipyleaflet import Map
import asyncio


penguins_df = palmerpenguins.load_penguins()

ui.page_opts(title="Penguins Dashboard", fillable=True)

# Add a theme
theme.morph()

    # Add a Shiny UI sidebar for user interaction
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

    ui.a("Github", href="https://github.com/ryankrabbe/cintel-06-custom", target="_blank", style="color: Red;")

# Add Main Content
with ui.accordion():
    with ui.accordion_panel("Penguin Information", style="padding: 10px;"):
        with ui.layout_columns():
            with ui.value_box(showcase=icon_svg("snowflake"), max_height="150px", theme="bg-gradient-blue-cyan"):
                "Penguin Count"
                @render.text
                def display_penguin_count():
                    df = filtered_data()
                    return f"{len(df)} penguins"

            with ui.value_box(showcase=icon_svg("snowman"), max_height="150px", theme="bg-gradient-blue-cyan"):
                "Average Bill Length"
                @render.text
                def average_bill_length():
                    df = filtered_data()
                    return f"{df['bill_length_mm'].mean():.2f} mm" if not df.empty else "N/A"

            with ui.value_box(showcase=icon_svg("icicles"), max_height="150px", theme="bg-gradient-blue-purple"):
                "Average Bill Depth"
                @render.text
                def average_bill_depth():
                    df = filtered_data()
                    return f"{df['bill_depth_mm'].mean():.2f} mm" if not df.empty else "N/A"

    with ui.accordion_panel("Penguin Environment", style="padding: 10px;"):
        with ui.card(full_screen=True):
            ui.card_header("Penguin Habitat")
            @render_widget
            def small_map(width="100%", height="300px"):
                return Map(center=(62.1014, 57.9296), zoom=6)

    with ui.accordion_panel("Penguin Charts and Plots", style="padding: 10px;"):
        with ui.layout_columns():
            with ui.card(full_screen=True):
                ui.card_header("Plotly Histogram")
                @render_plotly
                def plotly_histogram():
                    data = filtered_data() 
                    return px.histogram(
                        data,
                        x=input.selected_attribute(),
                        nbins=input.plotly_bin_count(),
                        color="species"
                    )

            with ui.card(full_screen=True):
                ui.card_header("Seaborn Histogram")
                @render.plot(alt="Seaborn Histogram")
                def seaborn_histogram():
                    data = filtered_data()
                    seaborn_hist = sns.histplot(
                        data=data,
                        x=input.selected_attribute(),
                        bins=input.seaborn_bin_count(),
                        color="skyblue"
                    )
                    seaborn_hist.set_title("Seaborn Histogram")
                    seaborn_hist.set_ylabel("Count")

            with ui.card(full_screen=True):
                ui.card_header("Plotly Scatterplot")
                @render_plotly
                def plotly_scatterplot():
                    data = filtered_data()  
                    return px.scatter(
                        data,
                        title="Plotly Scatterplot",
                        x="bill_length_mm",
                        y="bill_depth_mm",
                        color="species",
                        size_max=8,
                    )

@reactive.calc
def filtered_data():
    return penguins_df[
        (penguins_df["species"].isin(input.selected_species_list())) &
        (penguins_df["island"].isin(input.selected_island_list()))]
