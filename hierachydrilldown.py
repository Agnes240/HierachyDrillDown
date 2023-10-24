#Creating different visualization using different product category levels
import pandas as pd
import random

# Create a list of categories, subcategories, and products.
categories = ['Men\'s Shoes', 'Women\'s Shoes', 'Unisex Shoes']
subcategories = ['Athletic Shoes', 'Casual Shoes', 'Dress Shoes', 'Boots', 'Sandals', 'Slippers']
product_names = {
    'Athletic Shoes': ['Running Shoe A', 'Basketball Shoe B', 'Trail Running Shoe C', 'Tennis Shoe D', 'CrossFit Shoe E'],
    'Casual Shoes': ['Sneaker F', 'Loafer G', 'Canvas Shoe H', 'Driving Moccasin I', 'Slip-On Shoe J'],
    'Dress Shoes': ['Oxford Shoe K', 'Derby Shoe L', 'Monk Strap Shoe M', 'Dress Boot N', 'Formal Pump O'],
    'Boots': ['Hiking Boot P', 'Chelsea Boot Q', 'Work Boot R', 'Winter Boot S', 'Cowboy Boot T'],
    'Sandals': ['Flip-Flop Sandal U', 'Sport Sandal V', 'Slide Sandal W', 'Wedge Sandal X', 'Platform Sandal Y'],
    'Slippers': ['Moccasin Slipper Z', 'Clog Slipper AA', 'Bootie Slipper BB', 'Slide Slipper CC', 'Scuff Slipper DD']
}

# Create a list of regions.
regions = ['North', 'South', 'East', 'West']

# Create a list of time periods.
time_periods = ['2021-Q1', '2021-Q2', '2021-Q3', '2021-Q4', '2022-Q1', '2022-Q2', '2022-Q3', '2022-Q4']

# Generate random data for sales and revenue.
data = []
for _ in range(1000):
    category = random.choice(categories)
    subcategory = random.choice(subcategories)
    product = random.choice(product_names[subcategory])
    region = random.choice(regions)
    time_period = random.choice(time_periods)
    days_to_sell = random.randint(1, 90)
    sales = random.randint(1, 100)
    revenue = round(random.uniform(50, 200), 2)
    data.append([category, subcategory, product, region, time_period,days_to_sell, sales, revenue])

# Create a DataFrame.
df = pd.DataFrame(data, columns=['Category', 'Subcategory', 'Product', 'Region', 'Time_Period', 'Days_to_sell','Sales', 'Revenue'])

# Save the DataFrame to a CSV file.
df.to_csv('shoe_catalog_data.csv', index=False)

df.head(10)

#Performing the Hierachy Based Drill Down for better visualizations
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import ipywidgets as widgets
from IPython.display import display

#Creating a basic-level visualization showing total sales by category
category_data = df.groupby('Category')['Revenue'].sum()
plt.bar(category_data.index, category_data)
plt.xlabel('Category')
plt.ylabel('Total Revenue')
plt.title('Sales by Category')
plt.show()

# Get a list of unique categories from your DataFrame.
category_list = df['Category'].unique()

# Create a dropdown widget for selecting a category.
category_dropdown = widgets.Dropdown(
    options=category_list,
    description='Select a Category:',
    style={'description_width': 'initial', 'handle_color': 'lightblue'}
)

# Define a function to update the subcategory-level visualization based on the selected category.
def update_subcategory_chart(category):
    subcategory_data = df[df['Category'] == category].groupby('Subcategory')['Revenue'].sum()
    plt.bar(subcategory_data.index, subcategory_data)
    plt.xlabel('Subcategory')
    plt.ylabel('Total Revenue')
    plt.title(f'Sales by Subcategory in {category}')
    plt.show()

# Connect the widget to the function.
widgets.interactive(update_subcategory_chart, category=category_dropdown)

import matplotlib.pyplot as plt
import pandas as pd
import ipywidgets as widgets
from IPython.display import display

# Get a list of unique subcategories from your DataFrame.
subcategories_list = df['Subcategory'].unique()

# Create a dropdown widget for selecting a subcategory.
subcategory_dropdown = widgets.Dropdown(
    options=subcategories_list,
    description='Select a Subcategory:'
)

def plot_product_level(subcategory):
    # Filter the DataFrame for the selected subcategory.
    filtered_data = df[df['Subcategory'] == subcategory]

    # Create a histogram of 'Sales' for the selected subcategory.
    plt.figure(figsize=(8, 4))
    plt.hist(filtered_data['Sales'], bins=10, edgecolor='k')
    plt.xlabel('Sales')
    plt.ylabel('Frequency')
    plt.title(f'Sales Distribution for {subcategory}')
    plt.show()

# Connect the widget to the function.
widgets.interactive(plot_product_level, subcategory=subcategory_dropdown)

pip install pandas matplotlib ipywidgets

import pandas as pd
import random
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display

# Get a list of unique subcategories from your DataFrame.
subcategories_list = df['Subcategory'].unique()

# Create a dropdown widget for selecting a visualization type.
visualization_dropdown = widgets.Dropdown(
    options=['Line Chart', 'Pie Chart', 'Histogram', 'Box Plot', 'Scatter Plot'],
    description='Select a Visualization Type:'
)

# Create buttons to trigger the selected visualization.
plot_button = widgets.Button(description='Plot')

output = widgets.Output()

def on_plot_button_clicked(b):
    with output:
        output.clear_output()
        visualization = visualization_dropdown.value
        if visualization == 'Line Chart':
            plt.figure(figsize=(12, 6))
            for subcategory in subcategories_list:
                filtered_data = df[df['Subcategory'] == subcategory]
                for product, data in filtered_data.groupby('Product')[['Time_Period', 'Sales']].sum().iterrows():
                    plt.plot(data['Time_Period'], data['Sales'], label=f'{product} - {subcategory}')
            plt.xlabel('Time Period')
            plt.ylabel('Sales')
            plt.title(f'Sales Over Time')
            plt.legend()
            plt.xticks(rotation=45)
            plt.show()
        elif visualization == 'Pie Chart':
            plt.figure(figsize=(6, 6))
            total_sales = df.groupby('Product')['Sales'].sum()
            plt.pie(total_sales, labels=total_sales.index, autopct='%1.1f%%')
            plt.title('Sales Distribution')
            plt.show()
        elif visualization == 'Histogram':
            plt.figure(figsize=(10, 6))
            plt.hist(df['Sales'], bins=20, edgecolor='k')
            plt.xlabel('Sales')
            plt.ylabel('Frequency')
            plt.title('Sales Histogram')
            plt.show()
        elif visualization == 'Box Plot':
            plt.figure(figsize=(8, 6))
            plt.boxplot(df['Sales'])
            plt.ylabel('Sales')
            plt.title('Sales Box Plot')
            plt.show()
        elif visualization == 'Scatter Plot':
            plt.figure(figsize=(10, 6))
            plt.scatter(df['Time_Period'], df['Sales'], alpha=0.5)
            plt.xlabel('Time Period')
            plt.ylabel('Sales')
            plt.title('Scatter Plot of Time Period vs. Sales')
            plt.show()

plot_button.on_click(on_plot_button_clicked)

display(visualization_dropdown)
display(plot_button)
display(output)

#Using Click buttons to enhance visualization
import pandas as pd
import random
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display

# Get a list of unique subcategories from your DataFrame.
subcategories_list = df['Subcategory'].unique()

# Create a dropdown widget for selecting a subcategory.
subcategory_dropdown = widgets.Dropdown(
    options=subcategories_list,
    description='Select a Subcategory:'
)

# Create a dropdown widget for selecting a visualization type.
visualization_dropdown = widgets.Dropdown(
    options=['Line Chart', 'Pie Chart', 'Histogram', 'Box Plot', 'Scatter Plot'],
    description='Select a Visualization Type:'
)

# Create buttons to trigger the selected subcategory and visualization.
plot_button = widgets.Button(description='Plot')

output = widgets.Output()

def on_plot_button_clicked(b):
    with output:
        output.clear_output()
        subcategory = subcategory_dropdown.value
        visualization = visualization_dropdown.value

        if subcategory and visualization:
            if visualization == 'Line Chart':
                filtered_data = df[df['Subcategory'] == subcategory]
                plt.figure(figsize=(12, 6))
                for product, data in filtered_data.groupby('Product')[['Time_Period', 'Sales']].sum().iterrows():
                    plt.plot(data['Time_Period'], data['Sales'], label=f'{product} - {subcategory}')
                plt.xlabel('Time Period')
                plt.ylabel('Sales')
                plt.title(f'Sales Over Time')
                plt.legend()
                plt.xticks(rotation=45)
                plt.show()
            elif visualization == 'Pie Chart':
                filtered_data = df[df['Subcategory'] == subcategory]
                plt.figure(figsize=(6, 6))
                total_sales = filtered_data.groupby('Product')['Sales'].sum()
                plt.pie(total_sales, labels=total_sales.index, autopct='%1.1f%%')
                plt.title(f'Sales Distribution for {subcategory}')
                plt.show()
            elif visualization == 'Histogram':
                filtered_data = df[df['Subcategory'] == subcategory]
                plt.figure(figsize=(10, 6))
                plt.hist(filtered_data['Sales'], bins=20, edgecolor='k')
                plt.xlabel('Sales')
                plt.ylabel('Frequency')
                plt.title(f'Sales Histogram for {subcategory}')
                plt.show()
            elif visualization == 'Box Plot':
                filtered_data = df[df['Subcategory'] == subcategory]
                plt.figure(figsize=(8, 6))
                plt.boxplot(filtered_data['Sales'])
                plt.ylabel('Sales')
                plt.title(f'Sales Box Plot for {subcategory}')
                plt.show()
            elif visualization == 'Scatter Plot':
                filtered_data = df[df['Subcategory'] == subcategory]
                plt.figure(figsize=(10, 6))
                plt.scatter(filtered_data['Time_Period'], filtered_data['Sales'], alpha=0.5)
                plt.xlabel('Time Period')
                plt.ylabel('Sales')
                plt.title(f'Scatter Plot of Time Period vs. Sales for {subcategory}')
                plt.show()

plot_button.on_click(on_plot_button_clicked)

display(subcategory_dropdown)
display(visualization_dropdown)
display(plot_button)
display(output)
