# Billing App & System Integration Resume

This document explains the internal structure of the `billing-app` and how it interacts with the API Gateway and the broader system.

## 1. Billing App: Internal File Structure

The `billing-app` is a hybrid service that runs both a **REST API** and an **Asynchronous Worker**.

| File / Folder | Responsibility |
| :--- | :--- |
| **`server.py`** | The entry point. It starts the Flask web server and launches the RabbitMQ consumer (worker) in a background thread. |
| **`app/worker.py`** | Contains the RabbitMQ logic. It listens to the `billing_queue`, parses incoming JSON orders, and saves them to the PostgreSQL database. |
| **`app/models/models.py`** | Defines the `Order` database schema (user_id, number_of_items, total_amount). |
| **`app/controllers/orders.py`** | Defines the REST API endpoints (e.g., `GET /api/orders/`) to retrieve recorded orders from the database. |
| **`app/__init__.py`** | Initializes the Flask application, connects the database (SQLAlchemy), and registers the blueprints (routes). |
| **`requirement.txt`** | Lists Python dependencies: `Flask`, `Flask-SQLAlchemy`, `pika` (for RabbitMQ), and `psycopg2` (for Postgres). |
| **`.env`** | Stores sensitive configuration like Database URLs and RabbitMQ credentials. |

---

## 2. System Connectivity: How it all talks

### A. API Gateway $\leftrightarrow$ Billing App
The connection is **dual-mode**:

1.  **Asynchronous (Write)**: When a user sends a `POST` to `/api/billing/`, the Gateway **does not** talk to the Billing App directly. Instead, it drops a message into **RabbitMQ**. The Billing App's worker picks it up later. This ensures orders aren't lost if the Billing service is temporarily down.
2.  **Synchronous (Read)**: When a user sends a `GET` to `/api/billing/`, the Gateway acts as a proxy and sends a direct HTTP request to the Billing App's REST API to fetch order history.

### B. Billing App $\leftrightarrow$ Inventory App
*   Currently, these two services are **decoupled**. They do not talk to each other directly. 
*   The **API Gateway** acts as the orchestrator that manages the flow to both.

### C. Infrastructure Integration
*   **Vagrant**: Defines the `billing` virtual machine.
*   **Scripts (`provision_billing.sh`)**: Automates the installation of RabbitMQ and PostgreSQL specifically for the billing service.
*   **PM2**: Manages the `server.py` process to ensure the worker and API are always online.

---

## 3. Data Flow Summary
1.  **User** $\rightarrow$ `POST /api/billing/` $\rightarrow$ **Gateway**
2.  **Gateway** $\rightarrow$ **RabbitMQ** (`billing_queue`)
3.  **Billing Worker** (Background) $\rightarrow$ **PostgreSQL** (`orders` db)
4.  **User** $\rightarrow$ `GET /api/billing/` $\rightarrow$ **Gateway** $\rightarrow$ **Billing API** $\rightarrow$ **Database**
