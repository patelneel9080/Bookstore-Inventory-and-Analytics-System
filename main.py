import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os
# import warnings
# warnings.filterwarnings('ignore')

class Bookstore:
    
    def __init__(self, inventory_file='inventory.csv', sales_file='sales.csv'):
        self.inventory_file = inventory_file
        self.sales_file = sales_file
        self.inventory_df = self.load_inventory()
        self.sales_df = self.load_sales()
        
    def load_inventory(self):
        try:
            df = pd.read_csv(self.inventory_file)
            return df
        except FileNotFoundError:
            print(f"Inventory file {self.inventory_file} not found. Creating new inventory.")
            df = pd.DataFrame(columns=['Title', 'Author', 'Genre', 'Price', 'Quantity'])
            return df
    
    def load_sales(self):
        try:
            df = pd.read_csv(self.sales_file)
            df['Date'] = pd.to_datetime(df['Date'])
            return df
        except FileNotFoundError:
            print(f"Sales file {self.sales_file} not found. Creating new sales log.")
            df = pd.DataFrame(columns=['Date', 'Title', 'Quantity Sold', 'Total Revenue'])
            df['Date'] = pd.to_datetime(df['Date'])
            return df
    
    def validate_book_data(self, title, author, genre, price, quantity):
        errors = []
      
        if not title or title.strip() == "":
            errors.append("Title cannot be empty")

        if not author or author.strip() == "":
            errors.append("Author cannot be empty")

        if not genre or genre.strip() == "":
            errors.append("Genre cannot be empty")

        try:
            price = float(price)
            if price <= 0:
                errors.append("Price must be positive")
        except (ValueError, TypeError):
            errors.append("Price must be a valid number")
        

        try:
            quantity = int(quantity)
            if quantity < 0:
                errors.append("Quantity cannot be negative")
        except (ValueError, TypeError):
            errors.append("Quantity must be a valid integer")
        
        return errors, price, quantity
    
    def add_book(self, title, author, genre, price, quantity):

        errors, validated_price, validated_quantity = self.validate_book_data(
            title, author, genre, price, quantity
        )
        
        if errors:
            print("Validation errors:")
            for error in errors:
                print(f"- {error}")
            return False
 
        existing_book = self.inventory_df[self.inventory_df['Title'].str.lower() == title.lower()]
        
        if not existing_book.empty:
            print(f"Book '{title}' already exists. Use update_inventory to modify quantity.")
            return False
        

        new_book = pd.DataFrame({
            'Title': [title],
            'Author': [author],
            'Genre': [genre],
            'Price': [validated_price],
            'Quantity': [validated_quantity]
        })
        
        self.inventory_df = pd.concat([self.inventory_df, new_book], ignore_index=True)
        self.save_inventory()
        print(f"Book '{title}' added successfully!")
        return True
    
    def update_inventory(self, title, quantity):

        try:
            quantity = int(quantity)
            if quantity < 0:
                print("Quantity cannot be negative")
                return False
        except (ValueError, TypeError):
            print("Quantity must be a valid integer")
            return False

        book_index = self.inventory_df[self.inventory_df['Title'].str.lower() == title.lower()].index
        
        if book_index.empty:
            print(f"Book '{title}' not found in inventory")
            return False

        self.inventory_df.loc[book_index[0], 'Quantity'] = quantity
        self.save_inventory()
        print(f"Inventory updated for '{title}'. New quantity: {quantity}")
        return True
    
    def record_sale(self, title, quantity):

        try:
            quantity = int(quantity)
            if quantity <= 0:
                print("Sale quantity must be positive")
                return False
        except (ValueError, TypeError):
            print("Quantity must be a valid integer")
            return False

        book_index = self.inventory_df[self.inventory_df['Title'].str.lower() == title.lower()].index
        
        if book_index.empty:
            print(f"Book '{title}' not found in inventory")
            return False

        available_quantity = self.inventory_df.loc[book_index[0], 'Quantity']
        if available_quantity < quantity:
            print(f"Insufficient stock. Available: {available_quantity}, Requested: {quantity}")
            return False
        

        book_price = self.inventory_df.loc[book_index[0], 'Price']
        total_revenue = book_price * quantity
        

        self.inventory_df.loc[book_index[0], 'Quantity'] -= quantity
        

        new_sale = pd.DataFrame({
            'Date': [datetime.now().strftime('%Y-%m-%d')],
            'Title': [title],
            'Quantity Sold': [quantity],
            'Total Revenue': [total_revenue]
        })
        
        self.sales_df = pd.concat([self.sales_df, new_sale], ignore_index=True)
        self.sales_df['Date'] = pd.to_datetime(self.sales_df['Date'])
        

        self.save_inventory()
        self.save_sales()
        
        print(f"Sale recorded: {quantity} copies of '{title}' for ${total_revenue:.2f}")
        return True
    
    def remove_book(self, title):

        book_index = self.inventory_df[self.inventory_df['Title'].str.lower() == title.lower()].index
        
        if book_index.empty:
            print(f"Book '{title}' not found in inventory")
            return False
        
        self.inventory_df = self.inventory_df.drop(book_index[0]).reset_index(drop=True)
        self.save_inventory()
        print(f"Book '{title}' removed from inventory")
        return True
    
    def save_inventory(self):

        self.inventory_df.to_csv(self.inventory_file, index=False)
    
    def save_sales(self):

        self.sales_df.to_csv(self.sales_file, index=False)
    
    def generate_report(self):

        print("\n" + "="*60)
        print("BOOKSTORE INVENTORY AND SALES REPORT")
        print("="*60)

        print("\nINVENTORY SUMMARY")
        print("-" * 30)
        if not self.inventory_df.empty:
            total_books = self.inventory_df['Quantity'].sum()
            total_value = (self.inventory_df['Price'] * self.inventory_df['Quantity']).sum()
            avg_price = self.inventory_df['Price'].mean()
            
            print(f"Total Books in Stock: {total_books}")
            print(f"Total Inventory Value: ${total_value:.2f}")
            print(f"Average Book Price: ${avg_price:.2f}")
            print(f"Number of Unique Titles: {len(self.inventory_df)}")

            print("\nTop 5 Most Expensive Books:")
            top_expensive = self.inventory_df.nlargest(5, 'Price')[['Title', 'Author', 'Price']]
            for idx, row in top_expensive.iterrows():
                print(f"  • {row['Title']} by {row['Author']} - ${row['Price']:.2f}")
        else:
            print("No books in inventory")

        print("\nSALES SUMMARY")
        print("-" * 30)
        if not self.sales_df.empty:
            total_revenue = self.sales_df['Total Revenue'].sum()
            total_books_sold = self.sales_df['Quantity Sold'].sum()
            avg_sale_value = self.sales_df['Total Revenue'].mean()
            
            print(f"Total Revenue: ${total_revenue:.2f}")
            print(f"Total Books Sold: {total_books_sold}")
            print(f"Average Sale Value: ${avg_sale_value:.2f}")
            print(f"Number of Transactions: {len(self.sales_df)}")
            

            print("\nTop 5 Best Selling Books:")
            best_sellers = self.sales_df.groupby('Title')['Quantity Sold'].sum().nlargest(5)
            for title, quantity in best_sellers.items():
                print(f"  • {title}: {quantity} copies sold")
        else:
            print("No sales recorded")
    
    def analyze_sales_with_numpy(self):

        if self.sales_df.empty:
            print("No sales data available for analysis")
            return
        
        print("\nNUMPY ANALYSIS")
        print("-" * 30)
        

        revenues = self.sales_df['Total Revenue'].values
        quantities = self.sales_df['Quantity Sold'].values
        

        revenue_stats = {
            'Total Revenue': np.sum(revenues),
            'Average Revenue per Sale': np.mean(revenues),
            'Median Revenue per Sale': np.median(revenues),
            'Revenue Standard Deviation': np.std(revenues),
            'Maximum Sale': np.max(revenues),
            'Minimum Sale': np.min(revenues)
        }
        
        print("Revenue Analysis:")
        for key, value in revenue_stats.items():
            print(f"  {key}: ${value:.2f}")
        

        print("\nQuantity Analysis:")
        print(f"  Total Books Sold: {np.sum(quantities)}")
        print(f"  Average Books per Sale: {np.mean(quantities):.2f}")
        print(f"  Most Books in Single Sale: {np.max(quantities)}")
        

        if len(revenues) > 1:

            recent_sales = revenues[-min(5, len(revenues)):]
            older_sales = revenues[:min(5, len(revenues))]
            
            if len(older_sales) > 0 and len(recent_sales) > 0:
                growth_rate = (np.mean(recent_sales) - np.mean(older_sales)) / np.mean(older_sales) * 100
                print(f"\nSales Growth Rate: {growth_rate:.2f}%")
    
    def analyze_with_pandas(self):

        if self.sales_df.empty:
            print("No sales data available for analysis")
            return
        
        print("\nPANDAS ANALYSIS")
        print("-" * 30)

        sales_with_inventory = self.sales_df.merge(
            self.inventory_df[['Title', 'Author', 'Genre']], 
            on='Title', 
            how='left'
        )

        if 'Genre' in sales_with_inventory.columns:
            print("Sales by Genre:")
            genre_sales = sales_with_inventory.groupby('Genre').agg({
                'Quantity Sold': 'sum',
                'Total Revenue': 'sum'
            }).round(2)
            print(genre_sales)
        

        print("\nSales by Author:")
        author_sales = sales_with_inventory.groupby('Author').agg({
            'Quantity Sold': 'sum',
            'Total Revenue': 'sum'
        }).round(2)
        print(author_sales.head())
        

        if len(self.sales_df) > 0:
            print("\nMonthly Sales Trends:")
            monthly_sales = self.sales_df.groupby(self.sales_df['Date'].dt.strftime('%Y-%m')).agg({
                'Quantity Sold': 'sum',
                'Total Revenue': 'sum'
            }).round(2)
            print(monthly_sales)
    
    def create_visualizations(self):
            if self.sales_df.empty:
                print("No sales data available for visualization")
                return
            
            plt.style.use('seaborn-v0_8-darkgrid')
            sns.set_palette("husl")
            
            fig = plt.figure(figsize=(12, 10))

            sales_with_inventory = self.sales_df.merge(
                self.inventory_df[['Title', 'Author', 'Genre']], 
                on='Title', 
                how='left'
            )

            # Bar Chart
            plt.subplot(2, 2, 1)
            if 'Genre' in sales_with_inventory.columns:
                genre_sales = sales_with_inventory.groupby('Genre')['Total Revenue'].sum().sort_values(ascending=False)
                genre_sales.plot(kind='bar', color='skyblue')
                plt.title('Total Revenue by Genre', fontsize=14, fontweight='bold')
                plt.xlabel('Genre')
                plt.ylabel('Revenue ($)')
                plt.xticks(rotation=45)

            #Line Chart
            plt.subplot(2, 2, 2)
            monthly_revenue = self.sales_df.groupby(self.sales_df['Date'].dt.strftime('%Y-%m'))['Total Revenue'].sum()
            monthly_revenue.plot(kind='line', marker='o', color='green', linewidth=2, markersize=6)
            plt.title('Monthly Sales Trends', fontsize=14, fontweight='bold')
            plt.xlabel('Month')
            plt.ylabel('Revenue ($)')
            plt.xticks(rotation=45)
            
            # Pie Chart
            plt.subplot(2, 2, 3)
            if 'Genre' in sales_with_inventory.columns:
                genre_revenue = sales_with_inventory.groupby('Genre')['Total Revenue'].sum()
                plt.pie(genre_revenue.values, labels=genre_revenue.index, autopct='%1.1f%%', startangle=90)
                plt.title('Revenue Share by Genre', fontsize=14, fontweight='bold')

            #Heatmap
            plt.subplot(2, 2, 4)
            if len(sales_with_inventory) > 1:
                price_sales_data = sales_with_inventory.merge(
                    self.inventory_df[['Title', 'Price']], 
                    on='Title', 
                    how='left'
                )
                
                if not price_sales_data.empty and 'Price' in price_sales_data.columns:
                    corr_data = price_sales_data[['Price', 'Quantity Sold', 'Total Revenue']].corr()
                    sns.heatmap(corr_data, annot=True, cmap='coolwarm', center=0, 
                            square=True, fmt='.2f')
                    plt.title('Price vs Sales Correlation', fontsize=14, fontweight='bold')
            
            plt.tight_layout()
            plt.savefig('bookstore_analytics_dashboard.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            print("Visualization saved as 'bookstore_analytics_dashboard.png'")

def generate_sample_inventory():

    sample_books = [
        ("The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 12.99, 25),
        ("To Kill a Mockingbird", "Harper Lee", "Fiction", 14.50, 30),
        ("1984", "George Orwell", "Dystopian", 13.99, 20),
        ("Pride and Prejudice", "Jane Austen", "Romance", 11.99, 15),
        ("The Catcher in the Rye", "J.D. Salinger", "Fiction", 12.50, 18),
        ("Lord of the Flies", "William Golding", "Adventure", 10.99, 22),
        ("Animal Farm", "George Orwell", "Political Satire", 9.99, 28),
        ("Brave New World", "Aldous Huxley", "Science Fiction", 13.50, 16),
        ("The Hobbit", "J.R.R. Tolkien", "Fantasy", 15.99, 12),
        ("Fahrenheit 451", "Ray Bradbury", "Science Fiction", 12.75, 20),
        ("Jane Eyre", "Charlotte Brontë", "Romance", 11.50, 14),
        ("Wuthering Heights", "Emily Brontë", "Gothic", 10.75, 17),
        ("The Picture of Dorian Gray", "Oscar Wilde", "Gothic", 12.25, 19),
        ("Dracula", "Bram Stoker", "Horror", 11.99, 21),
        ("Frankenstein", "Mary Shelley", "Horror", 10.50, 23)
    ]
    
    df = pd.DataFrame(sample_books, columns=['Title', 'Author', 'Genre', 'Price', 'Quantity'])
    df.to_csv('inventory.csv', index=False)
    print("Sample inventory.csv created!")

def generate_sample_sales():

    np.random.seed(42) 
    books = [
        "The Great Gatsby", "To Kill a Mockingbird", "1984", "Pride and Prejudice",
        "The Catcher in the Rye", "Lord of the Flies", "Animal Farm", "Brave New World",
        "The Hobbit", "Fahrenheit 451"
    ]
    
    sales_data = []
    current_date = datetime.now() - timedelta(days=90) 
    for _ in range(150):
        date = current_date + timedelta(days=np.random.randint(0, 90))
        title = np.random.choice(books)
        quantity = np.random.randint(1, 6) 
        prices = {
            "The Great Gatsby": 12.99,
            "To Kill a Mockingbird": 14.50,
            "1984": 13.99,
            "Pride and Prejudice": 11.99,
            "The Catcher in the Rye": 12.50,
            "Lord of the Flies": 10.99,
            "Animal Farm": 9.99,
            "Brave New World": 13.50,
            "The Hobbit": 15.99,
            "Fahrenheit 451": 12.75
        }
        
        price = prices.get(title, 12.00)
        total_revenue = price * quantity
        
        sales_data.append([
            date.strftime('%Y-%m-%d'),
            title,
            quantity,
            round(total_revenue, 2)
        ])
    
    df = pd.DataFrame(sales_data, columns=['Date', 'Title', 'Quantity Sold', 'Total Revenue'])
    df.to_csv('sales.csv', index=False)
    print("Sample sales.csv created!")

def main_menu():
    if not os.path.exists('inventory.csv'):
        generate_sample_inventory()
    if not os.path.exists('sales.csv'):
        generate_sample_sales()
    
    bookstore = Bookstore()
    
    while True:
        print("\n" + "="*50)
        print("BOOKSTORE INVENTORY AND ANALYTICS SYSTEM")
        print("="*50)
        print("1. Add New Book")
        print("2. Update Book Quantity")
        print("3. Record Sale")
        print("4. Remove Book")
        print("5. View Inventory")
        print("6. Generate Report")
        print("7. NumPy Analysis")
        print("8. Pandas Analysis")
        print("9. Create Visualizations")
        print("10. Exit")
        print("-"*50)
        
        choice = input("Enter your choice (1-10): ").strip()
        
        if choice == '1':
            print("\n ADD NEW BOOK")
            title = input("Enter book title: ").strip()
            author = input("Enter author name: ").strip()
            genre = input("Enter genre: ").strip()
            price = input("Enter price: $").strip()
            quantity = input("Enter quantity: ").strip()
            
            bookstore.add_book(title, author, genre, price, quantity)
        
        elif choice == '2':
          
            print("\n UPDATE BOOK QUANTITY")
            title = input("Enter book title: ").strip()
            quantity = input("Enter new quantity: ").strip()
            
            bookstore.update_inventory(title, quantity)
        
        elif choice == '3':
  
            print("\n RECORD SALE")
            title = input("Enter book title: ").strip()
            quantity = input("Enter quantity sold: ").strip()
            
            bookstore.record_sale(title, quantity)
        
        elif choice == '4':
    
            print("\n REMOVE BOOK")
            title = input("Enter book title to remove: ").strip()
            
            bookstore.remove_book(title)
        
        elif choice == '5':
        
            print("\n CURRENT INVENTORY")
            print("-"*80)
            if not bookstore.inventory_df.empty:
                print(bookstore.inventory_df.to_string(index=False))
            else:
                print("No books in inventory")
        
        elif choice == '6':
          
            bookstore.generate_report()
        
        elif choice == '7':
         
            bookstore.analyze_sales_with_numpy()
        
        elif choice == '8':
         
            bookstore.analyze_with_pandas()
        
        elif choice == '9':
          
            print("\n Generating visualizations...")
            bookstore.create_visualizations()
        
        elif choice == '10':
   
            print("\nThank you for using the Bookstore System!")
            break
        
        else:
            print("\nInvalid choice. Please select a number between 1-10.")
     
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main_menu()