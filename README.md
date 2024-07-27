# MotoHub

MotoHub is a SaaS application designed to help automobile workshops streamline their operations. With MotoHub, workshops can manage customers, inventory, job orders, and billing, and also track their monthly profit/loss.

## Features

- **Customer Management**: Maintain a database of customers.
- **Inventory Management**: Track parts and supplies.
- **Job Management**: Create and manage job orders with multiple vehicles and services.
- **Billing**: Generate bills for completed jobs.
- **Profit/Loss Calculation**: Calculate monthly profit/loss based on completed jobs and expenses.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/motohub.git
   cd motohub
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## Usage

1. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:8000/`.

2. **Log in:**
   Log in with the superuser credentials you created.

3. **Manage Customers:**
   - Add, edit, or delete customers.

4. **Manage Inventory:**
   - Add, edit, or delete parts and supplies.

5. **Create Jobs:**
   - Create a new job order.
   - Select the job type (Machining or Repairing).
   - Add multiple vehicles and services to the job.
   - Track job status and completion time.

6. **Billing:**
   - Generate bills for completed jobs.
   - Update paid amount when the job status is marked as completed.

7. **Reports:**
   - View monthly profit/loss reports.

## Models Overview

- **Customer**: Stores customer details.
- **Vehicle**: Represents vehicles owned by customers.
- **Job**: Represents a job order with fields like job number, customer, job type, status, completion time, and paid amount.
- **Service**: Represents services that can be performed on vehicles.
- **Inventory**: Tracks parts and supplies.
- **PurchaseOrder**: Manages purchase orders with fields like PO number, vendor, and PO amount.
- **PurchaseOrderItem**: Tracks items in each purchase order.

## Key Functionality

- **Job Number Generation**: Generates unique job numbers.
- **Job Status Update**: Automatically updates job completion time and handles payment logic.
- **Form Validation**: Custom error messages and form validation logic.
- **Static Files**: Utilizes CSS and Bootstrap for frontend styling.

## Contributing

1. **Fork the repository.**
2. **Create a new branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes and commit them:**
   ```bash
   git commit -m "Add some feature"
   ```
4. **Push to the branch:**
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Create a new Pull Request.**

## License

This project is licensed under the MIT License 

## Contact

For questions or suggestions, please contact jawed.aquib42@gmail.com or open an issue on GitHub.

---

MotoHub is continually evolving, and we welcome contributions from the community to make it even better. Thank you for using MotoHub!
