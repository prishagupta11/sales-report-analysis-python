import pandas as pd
import matplotlib.pyplot as plt

# Function to collect data from the user
def collect_data():
    data = {
        'Sr.No.': [],
        'ProductName': [],
        'Category': [],
        'Brand': [],
        'SellingPrice': [],
        'UnitSold': [],
        'Rating': [],
        'CostPrice': [],
    }

    categories = ['Clothing', 'Footwear', 'Accessories', 'Beauty', 'Home & Living']
    brands = ['Gucci', 'H&M', 'Prada', 'Zara', 'Louis Vuitton']  # Example brands

    print("\nEnter details for the product:")
    data['Sr.No.'].append(int(input("Product ID: ")))
    data['ProductName'].append(input("Product Name: "))

    print("Select a category from the following options:")
    for idx, category in enumerate(categories, 1):
        print(f"{idx}. {category}")
    category_choice = int(input("Category (enter the number): "))
    while category_choice < 1 or category_choice > len(categories):
        print("Invalid choice! Please select a valid category number.")
        category_choice = int(input("Category (enter the number): "))
    data['Category'].append(categories[category_choice - 1])

    print("Select a brand from the following options:")
    for idx, brand in enumerate(brands, 1):
        print(f"{idx}. {brand}")
    brand_choice = int(input("Brand (enter the number): "))
    while brand_choice < 1 or brand_choice > len(brands):
        print("Invalid choice! Please select a valid brand number.")
        brand_choice = int(input("Brand (enter the number): "))
    data['Brand'].append(brands[brand_choice - 1])
    
    data['SellingPrice'].append(float(input("Selling Price: ")))
    data['CostPrice'].append(float(input("Cost Price: ")))
    data['UnitSold'].append(int(input("Unit Sold: ")))
    data['Rating'].append(float(input("Rating: ")))

    return pd.DataFrame(data)

# Function to add data to CSV file
def add_data_to_csv():
    new_data = collect_data()
    csv_file_path = 'Sales_Report.csv'
    
    try:
        # Try to read existing data
        existing_data = pd.read_csv(csv_file_path)
        
        # Append new data to the existing data
        combined_data = pd.concat([existing_data, new_data], ignore_index=True)
    except FileNotFoundError:
        # If the file doesn't exist, just use the new data
        combined_data = new_data
    
    # Save the combined data to the CSV file
    combined_data.to_csv(csv_file_path, index=False)
    print(f"\nData saved to {csv_file_path}")

# Function for monthly analysis
def monthly_analysis():
    csv_file_path = 'Sales_Report.csv'
    try:
        df = pd.read_csv(csv_file_path)
        if df.empty:
            raise ValueError("The CSV file is empty.")
    except pd.errors.EmptyDataError:
        print("The CSV file is empty or improperly formatted.")
        return
    except pd.errors.ParserError:
        print("The CSV file is improperly formatted.")
        return
    except FileNotFoundError:
        print("The CSV file was not found.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    print("☆" * 25)
    print("\nMonthly Analysis")
    print("1. Sales by Category")
    print("2. Profit/Loss by Brand within Each Category")
    print("3. List of Top 10 Rated Products")
    print("4. Sales by Brand")
    print("5. Return to Main Menu")
    print("☆" * 25)
    
    while True:
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            # Calculate sales by category
            sales_by_category = df.groupby('Category')['UnitSold'].sum()
            
            # Define colors for each category to match the line chart
            category_colors = {
                'Clothing': '#a3c2c2',  # Pastel Blue
                'Footwear': '#b5e7a0',  # Pastel Green
                'Home & Living': '#f7a1a1',  # Pastel Red
                'Beauty': '#d3d3d3',  # Pastel Black (Light Gray)
                'Accessories': '#c2a2c2'  # Pastel Purple
            }

            # Plot sales by category (Bar Chart)
            plt.figure(figsize=(10, 6))
            sales_by_category.plot(kind='bar', 
            color=[category_colors.get(cat, 'gray') for cat in sales_by_category.index])
            plt.title('Sales by Category')
            plt.xlabel('Category')
            plt.ylabel('Total Unit Sold')
            plt.xticks(rotation=45)
            plt.grid(axis='y')
            plt.tight_layout()

            # Prompt to save the plot
            save_plot = input("Do you want to save the plot? (yes/no): ").strip().lower()
            if save_plot == 'yes':
                file_name = input("Enter file name (without extension): ").strip()
                plt.savefig(f"{file_name}.png")
            
            plt.show()
        
        elif choice == '2':
            # Calculate profit/loss
            df['ProfitLoss'] = df['SellingPrice'] - df['CostPrice']
            
            # Create a pivot table for profit/loss by brand and category
            pivot_table = df.pivot_table(index='Brand', columns='Category', values='ProfitLoss', aggfunc='sum', fill_value=0)

            plt.figure(figsize=(12, 8))

            # Define line styles and markers
            styles = {
                'Clothing': {'color': 'blue', 'linestyle': 'solid', 'marker': 'o'},  # Dot-dashed line
                'Footwear': {'color': 'green', 'linestyle': '--', 'marker': 's'},  # Dashed line
                'Home & Living': {'color': 'red', 'linestyle': '-.', 'marker': '^'},  # Solid line
                'Beauty': {'color': 'black', 'linestyle': '-', 'marker': 'D'},  # Dotted line
                'Accessories': {'color': 'purple', 'linestyle': '--', 'marker': 'x'}  # Dashed line
            }

            for category, style in styles.items():
                if category in pivot_table.columns:
                    plt.plot(
                        pivot_table.index, 
                        pivot_table[category], 
                        marker=style['marker'], 
                        linestyle=style['linestyle'], 
                        color=style['color'], 
                        label=category
                    )

            plt.title('Profit/Loss by Brand within Each Category')
            plt.xlabel('Brand')
            plt.ylabel('Total Profit/Loss')
            plt.legend(title='Category')
            plt.grid(True)
            plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
            plt.tight_layout()  # Adjust layout to make room for labels

            # Prompt to save the plot
            save_plot = input("Do you want to save the plot? (yes/no): ").strip().lower()
            if save_plot == 'yes':
                file_name = input("Enter file name (without extension): ").strip()
                plt.savefig(f"{file_name}.png")

            plt.show()

        elif choice == '3':
            # Display list of top 10 rated products (Product ID and Product Name)
            top_10_rated = df.nlargest(10, 'Rating')[['Sr.No.', 'ProductName']]
            print("\nTop 10 Rated Products")
            print(top_10_rated.to_string(index=False))
            print("☆" * 25)

        elif choice == '4':
            # Calculate sales by brand
            sales_by_brand = df.groupby('Brand')['UnitSold'].sum()
            
            # Define pastel colors
            pastel_colors = ['#FFB3BA', '#FFDFBA', '#FFFFBA', '#BAFFC9', '#BAE1FF']
            
            # Plot sales by brand (Bar Chart)
            plt.figure(figsize=(10, 6))
            sales_by_brand.plot(kind='bar', color=pastel_colors[:len(sales_by_brand)])
            plt.title('Sales by Brand')
            plt.xlabel('Brand')
            plt.ylabel('Total Unit Sold')
            plt.xticks(rotation=45)
            plt.grid(axis='y')
            plt.tight_layout()

            # Prompt to save the plot
            save_plot = input("Do you want to save the plot? (yes/no): ").strip().lower()
            if save_plot == 'yes':
                file_name = input("Enter file name (without extension): ").strip()
                plt.savefig(f"{file_name}.png")
            
            plt.show()

        elif choice == '5':
            print("Returning to the main menu...")
            break
        
        else:
            print("Invalid choice! Please enter a number between 1 and 5.")

# Function to display sales report
def display_sales_report():
    csv_file_path = 'Sales_Report.csv'
    try:
        df = pd.read_csv(csv_file_path)
        if df.empty:
            raise ValueError("The CSV file is empty.")
        print("\nSales Report")
        print(df.to_string(index=False))
    except pd.errors.EmptyDataError:
        print("The CSV file is empty or improperly formatted.")
    except FileNotFoundError:
        print("The CSV file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Main function to run the application
def main():
    while True:
        print("☆" * 25)
        print("\nMain Menu")
        print("1. Add Data")
        print("2. Monthly Analysis")
        print("3. Display Sales Report")
        print("4. Exit")
        print("☆" * 25)
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            add_data_to_csv()
        elif choice == '2':
            monthly_analysis()
        elif choice == '3':
            display_sales_report()
        elif choice == '4':
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
