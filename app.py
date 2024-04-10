# Imports at the top
import plotly.express as px
import faicons as fa
from faicons import icon_svg
from shiny import reactive, render, req
from shiny.express import input, render, ui
from shinyswatch import theme

tips = px.data.tips()
bill_rng = (min(tips.total_bill), max(tips.total_bill))

# Page Title
ui.page_opts(title="Restaurant gratuity in America by Regions", fillable=True)

# Add a theme
theme.morph()

#Add a sidebar
with ui.sidebar():
    ui.input_slider("total_bill", "Bill Cost", min=bill_rng[0], max=bill_rng[1], value=bill_rng, pre="$")
    ui.input_checkbox_group("time", "Time of Meal", ["Breakfast", "Lunch"], selected=["Breakfast", "Lunch"], inline=True)
    ui.input_checkbox_group("sex", "Gender", ["Male", "Female"], selected=["Male", "Female"], inline=True)
    ui.input_action_button("reset", "Reset filter")

#Links
ui.h6("Links:")
ui.a("GitHub", href="https://github.com/ryankrabbe/cintel-06-custom", target="_blank", style="color: red;",)

ICONS = {
    "user": fa.icon_svg("user", "regular"),
    "tag": fa.icon_svg("tag"),
    "receipt": fa.icon_svg("receipt"),
}

with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=ICONS["user"]):
        "Total Customers"

        @render.express
        def total_tippers():
            tips.shape[0]

with ui.value_box(showcase=ICONS["tag"]):
    "Average Gratuity"

    @render.express
    def average_tip():
        d = tips
        if d.shape[0] > 0:
            perc = d.tip / d.total_bill
            (f"{perc.mean():.1%}")

with ui.value_box(showcase=ICONS["receipt"]):
        "Average Check"

        @render.express
        def average_bill():
            d = tips
            if d.shape[0] > 0:
                bill = d.total_bill.mean()
                f"${bill:.2f}"
