---

# Smart Warehouse & Inventory Management System

![Laravel](https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white)![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)![Metabase](https://img.shields.io/badge/Metabase-5094E3?style=for-the-badge&logo=metabase&logoColor=white)![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

A full-stack, multi-container application demonstrating a modern smart warehousing solution. This project simulates inventory transactions, stores the data in a normalized database, and visualizes the insights through a dynamic web application and an embedded business intelligence dashboard.

---

## System Architecture

This project utilizes a microservices-oriented architecture orchestrated with Docker Compose. Each service runs in its own container, ensuring modularity and scalability. The data flow is API-driven, with a Laravel backend acting as the main interface and a Flask service handling dedicated tasks.

```
                                                     ┌─────────────────┐
                                              ┌─────>│    Metabase     │
                                              │      │ (BI Analytics)  │
                                              │      └─────────────────┘
                                              │               ▲
                                              │               │ SQL
┌───────────────┐      ┌─────────────────┐    │      ┌─────────────────┐
│               │ HTTP │                 │    │      │                 │
│ User's Browser├─────>│      Nginx      │────┼─────>│   PostgreSQL    │
│               │      │   (Web Server)  │    │      │ (Data Storage)  │
└───────────────┘      └─────────────────┘    │      └─────────────────┘
                             │                │               ▲
                             │ PHP-FPM          │               │ SQL (INSERT)
                             ▼                │      ┌─────────────────┐
                       ┌─────────────────┐    │      │                 │
                       │                 │────┘      │    Flask API    │
                       │  Laravel App    │  HTTP POST │ (Scanner Logic) │
                       │ (Web Dashboard) │───────────>└─────────────────┘
                       └─────────────────┘
```

### Key Technologies:
*   **Backend:** Laravel (PHP)
*   **Microservice:** Flask (Python) for scan processing
*   **Database:** PostgreSQL
*   **Frontend:** Laravel Blade with Tailwind CSS
*   **Analytics:** Metabase
*   **Containerization:** Docker & Docker Compose
*   **Web Server:** Nginx

---

## Features

*   **Normalized Database Schema:** Models a realistic warehouse with `products`, `suppliers`, `locations`, and `inventory_transactions` tables.
*   **Dynamic Web Dashboard:** A beautiful dark-mode dashboard built with Laravel and Tailwind CSS that seamlessly embeds the Metabase analytics.
*   **Embedded Business Intelligence:** A full Metabase dashboard with multiple charts (Pie, Bar, Line, Table) is embedded directly into the Laravel application.
*   **Decoupled Scan Processing:** A Flask microservice handles the logic for recording new inventory scans, separating it from the main application.
*   **Persistent Data Storage:** PostgreSQL database managed with a Docker volume to ensure all warehouse and Metabase data is saved between sessions.
*   **Robust Data Seeding:** A powerful Python script populates the database with hundreds of randomized and logically consistent records to simulate a real, active warehouse.

---

## Getting Started

Follow these instructions to get the entire system up and running on your local machine.

### Prerequisites

*   [Docker](https://www.docker.com/products/docker-desktop/) installed and running.
*   [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop).
*   A terminal or command prompt (like PowerShell, Windows Terminal, or WSL).

### First-Time Setup

This process will build the containers, install all dependencies, and run the necessary setup commands.

**1. Clone the Repository**
```bash
git clone https://github.com/your-username/smart-warehouse-project.git
cd smart-warehouse-project
```
*(Replace `your-username` with your actual GitHub username).*

**2. Copy the Environment File**
The Laravel application requires a `.env` file for its configuration.
```bash
# For Windows (Command Prompt)
copy laravel-backend\.env.example laravel-backend\.env

# For PowerShell, macOS, or Linux
# cp laravel-backend/.env.example laravel-backend/.env
```

**3. Build and Start All Services**
This is the main command. It will build all your custom images and start the containers in the background. The first time you run this, it may take several minutes.
```bash
docker-compose up -d --build
```

**4. Install Laravel Dependencies**
This command runs `composer install` inside the Laravel container to download all the necessary PHP packages.
```bash
docker-compose exec backend composer install
```

**5. Run Laravel Setup Commands**
After the containers are running, we need to run a few commands inside the Laravel container to finalize the setup.

   *   **Generate Application Key:**
     ```bash
     docker-compose exec backend php artisan key:generate
     ```
   *   **Run Database Migrations:** (This creates all warehouse tables like `products`, `sessions`, etc.)
     ```bash
     docker-compose exec backend php artisan migrate:fresh
     ```
   *   **Set Permissions:** (This is crucial to prevent errors)
     ```bash
     docker-compose exec backend chown -R www-data:www-data storage bootstrap/cache
     docker-compose exec backend chmod -R 775 storage bootstrap/cache
     ```

**6. Seed the Database with Mock Data**
Run this command to populate your new tables with hundreds of realistic records.
```bash
# For Windows (Command Prompt)
type seed.py | docker-compose exec -T -e DB_HOST=db -e DB_DATABASE=warehouse -e DB_USERNAME=postgres -e DB_PASSWORD=your_secure_password scanner python

# For PowerShell, macOS, or Linux
# cat seed.py | docker-compose exec -T -e DB_HOST=db -e DB_DATABASE=warehouse -e DB_USERNAME=postgres -e DB_PASSWORD=your_secure_password scanner python
```
*(Remember to replace `your_secure_password` if you changed it in `docker-compose.yml`).*

**7. Configure Metabase**
*   Open your browser and navigate to **`http://localhost:3030`**.
*   Follow the on-screen instructions to create your admin account.
*   When prompted to add your data, select **PostgreSQL** and use these details:
    *   **Host:** `db`
    *   **Port:** `5432`
    *   **Database name:** `warehouse`
    *   **Username:** `postgres`
    *   **Password:** `your_secure_password` (or whatever you set)
*   Explore your data and build your dashboards! Remember to **enable public sharing** for your dashboard to get the embed link, then paste that link into the `src` attribute of the `<iframe>` in `laravel-backend/resources/views/dashboard.blade.php`.

---

## How to Use the Application

Once the setup is complete, your system is live and ready to view.

*   **Main Laravel Dashboard:** `http://localhost:8000/dashboard`
*   **Metabase Analytics Portal:** `http://localhost:3030`

**To simulate a new scan via API:**
```bash
# This command posts directly to the Laravel API, which then forwards to the Flask service.
curl -X POST http://localhost:8000/api/inventory -H "Content-Type: application/json" -d "{\"sku\": \"SKU-ABC-123\", \"product_name\": \"New Item\", \"quantity\": 15, \"status\": \"IN\"}"
```

**To watch the live logs from the scanner service:**
```bash
docker-compose logs -f scanner
```

---

## Stopping the Environment

To stop the entire application stack and remove the containers, run:
```bash
docker-compose down
```Your PostgreSQL and Metabase data will be preserved in Docker volumes. If you want to delete **everything** (including all data) for a completely fresh start, use:
```bash
docker-compose down -v
```
