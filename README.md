# 📚 Bookstore Inventory & Sales Management System

A simple Python-based inventory and sales management system for a bookstore using **Pandas**, **NumPy**, **Matplotlib**, and **Seaborn**.

---

## 🚀 Features

- Add, update, and remove books in the inventory
- Record book sales with real-time stock validation
- Generate inventory and sales summary reports
- Perform NumPy-based sales analytics
- Persist data using CSV files
- Visual-ready structure using Matplotlib and Seaborn (optional)

---

## 🛠️ Technologies Used

- Python 3.x
- pandas
- numpy
- matplotlib
- seaborn
- datetime
- CSV file handling

---

## 📁 Project Structure

```
bookstore/
├── inventory.csv       # Inventory data (auto-created if not found)
├── sales.csv           # Sales data (auto-created if not found)
├── main.py        # Main class implementation
└── README.md           # Project documentation
```

---

## 🔧 How to Use

1. **Clone the Repository**
   ```bash
   git clone https://github.com/patelneel9080/Bookstore-Inventory-and-Analytics-System.git
   cd bookstore-management
   ```

2. **Install Dependencies**
   ```bash
   pip install pandas numpy matplotlib seaborn
   ```

3. **Run the Code**
   Import and use the `Bookstore` class in your Python script or interactive shell:
   ```python
   from bookstore import Bookstore

   store = Bookstore()
   store.add_book("Atomic Habits", "James Clear", "Self-help", 499, 20)
   store.record_sale("Atomic Habits", 2)
   store.generate_report()
   store.analyze_sales_with_numpy()
   ```

---

## 📈 Reporting

### Inventory Report:
- Total stock
- Total inventory value
- Average book price
- Top 5 most expensive books

### Sales Report:
- Total revenue
- Total books sold
- Average sale value
- Top 5 best-selling books

### NumPy Analysis:
- Revenue statistics (mean, median, std dev, min, max)
- Quantity sold analysis

---

## 📌 Notes

- If `inventory.csv` or `sales.csv` does not exist, they are automatically created.
- Input validation is performed before adding or updating records.
- Sales are recorded only if sufficient inventory is available.

---


## 🙌 Acknowledgements

Built with ❤️ using Python, NumPy, and Pandas.
