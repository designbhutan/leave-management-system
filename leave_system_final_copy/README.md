# Leave Management System — Django + PostgreSQL

This is the ready-made leave management system for staff and a supervisor.

## What the system does

### Staff
- Individual username and password
- Mobile-friendly and PC-friendly login
- View total leave entitlement, used leave and remaining balance
- Apply for leave
- Working-day leave calculation (Monday-Friday)
- Public holidays can be excluded through Admin
- View complete leave history
- Filter own leave history by status
- See Pending / Approved / Rejected status
- See supervisor remarks and reviewer
- Change own password

### Supervisor
- Individual supervisor login
- Supervisor dashboard
- See all staff leave applications
- Filter by person name, username or employee ID
- Filter by status
- Filter by leave type
- Filter by start/end date
- Open an application and approve or reject it
- Record supervisor remarks
- See who reviewed an application and when
- Reopen a reviewed record back to Pending
- See total staff and pending application counts

## Important: local vs internet access

`python manage.py runserver` is for development on the computer running Django. It does **not** publish the system to the internet.

To allow different staff to use their own mobile phones from home, using different Wi-Fi/mobile-data networks, the system must be deployed to a public web server. This project is prepared for Render with PostgreSQL and HTTPS.

After deployment, staff will use one URL such as:

`https://your-service-name.onrender.com/`

The same URL works from a PC, Android phone, iPhone, home Wi-Fi and mobile data, subject to the network having internet access.

## PART A — Run and test on your Windows PC in Visual Studio Code

### 1. Extract the ZIP

Extract this folder somewhere such as:

`C:\Users\LENOVO\Downloads\leave_management_system_final`

Open that folder in Visual Studio Code.

### 2. Create the virtual environment and install packages

Open the VS Code Terminal (PowerShell):

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Create the local environment file

```powershell
copy .env.example .env
```

### 4. Create the database tables

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

### 5. Create the supervisor account and Annual Leave type

Example:

```powershell
.\.venv\Scripts\python.exe manage.py bootstrap_demo --supervisor-username supervisor --supervisor-password ChangeMe123!
```

Replace the username and password with your real supervisor login details.

### 6. Optional one-time Windows setup shortcut

You can also double-click `SETUP_WINDOWS.bat` and enter the supervisor username/password. After the first setup, use `START_WINDOWS.bat` for normal starts. The normal start script does not reset passwords.

### 7. Start Django

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Open:

`http://127.0.0.1:8000/`

### 8. Create staff accounts

Create a Django admin user:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Then open:

`http://127.0.0.1:8000/admin/`

Under **Users**, create each staff login. Under **Accounts → Staff profiles**, create the matching profile and set:
- Employee ID
- Department
- Phone
- Role = Staff

Each staff member then signs in with their own username/password.

## PART B — Publish the system to the internet for all staff

The recommended setup is:

**Staff phone/PC → HTTPS → Render Web Service → PostgreSQL database**

Do not try to solve this by keeping the Django development server running on your personal PC. A cloud web service is what makes the system reachable from different networks.

### 1. Create a GitHub repository

In GitHub, create a new repository, for example:

`leave-management-system`

Do not upload `.env`, passwords or the local `db.sqlite3` file.

From the project folder in VS Code:

```powershell
git init
git add .
git commit -m "Ready leave management system"
git branch -M main
git remote add origin https://github.com/YOUR-GITHUB-USERNAME/leave-management-system.git
git push -u origin main
```

Replace the repository URL with your own GitHub repository URL.

### 2. Create the Render deployment

1. Open Render and sign in.
2. Connect your GitHub account.
3. Open **Blueprints** and choose **New Blueprint Instance**.
4. Select the GitHub repository containing this project.
5. Render will read the included `render.yaml` file.
6. Apply the Blueprint.

The project already contains:
- a Render web service
- a PostgreSQL database connection
- the build command
- Gunicorn start command
- `DEBUG=False`
- generated `SECRET_KEY`
- Asia/Thimphu timezone

Render publishes the web service at an `onrender.com` address after deployment.

### 3. Wait for the first deployment to become Live

Open the service URL shown by Render.

You should reach:

`https://YOUR-SERVICE.onrender.com/login/`

The connection is HTTPS, so the login cookie and CSRF settings are enabled for production.

### 4. Create the supervisor login in the live database

Open the Render service **Shell** and run:

```bash
python manage.py bootstrap_demo --supervisor-username supervisor --supervisor-password ChangeMe123!
```

Use your chosen real username and a strong password instead of the example values.

Important: do not put a real password into `render.yaml` or GitHub.

### 5. Create the first admin account in the live database

In the Render Shell:

```bash
python manage.py createsuperuser
```

Follow the prompts.

### 6. Create the staff accounts

Go to:

`https://YOUR-SERVICE.onrender.com/admin/`

Sign in with the superuser you just created.

Create each staff **User**, then create the matching **Staff Profile**.

For every staff account:
- give it a unique username
- set its own password
- set the employee ID
- set Role = Staff

The staff member can later change their own password from **Change Password**.

### 7. Add public holidays

In the live admin page:

**Leaves → Public holidays → Add Public Holiday**

Enter each official holiday date you want excluded from the working-day calculation.

## PART C — How staff will use it from their phones

After the Render deployment is live, give every staff member the same website address:

`https://YOUR-SERVICE.onrender.com/`

They do **not** need Visual Studio Code, Python or Django installed on their phone.

They simply open the link in Chrome/Safari/another modern mobile browser and log in with their own account.

Example:

- Staff A → phone/mobile data → same URL → Staff A credentials
- Staff B → home Wi-Fi → same URL → Staff B credentials
- Supervisor → office PC → same URL → Supervisor credentials

All users work against the same PostgreSQL database, so a leave application submitted by one staff member becomes visible to the supervisor from the same live system.

## PART D — Updating the system later

When you change the code in VS Code:

```powershell
git add .
git commit -m "Update leave system"
git push
```

Render can redeploy from the repository. The database is separate from the application code.

## PART E — Very important production warning

Do not use SQLite as the production database for this multi-user internet version.

This project uses PostgreSQL on Render for the deployed system.

Render's current Free Postgres databases expire after 30 days and have no backups. For an actual organizational leave system, use a paid/persistent database plan and maintain backups.

## Troubleshooting

### A. `This site can't be reached`

Check that the Render service is **Live** and that you are using the Render HTTPS URL, not `127.0.0.1`.

### B. `Bad Request (400)` after deployment

Check the Render environment variables and the service hostname. This project automatically includes Render's `RENDER_EXTERNAL_HOSTNAME` in Django's allowed hosts.

### C. Login gives CSRF error

Open the site using the exact HTTPS Render URL. Do not mix HTTP and HTTPS or use an old hostname.

### D. Database table does not exist

The deployment build automatically runs:

```bash
python manage.py migrate --noinput
```

Check the Render deploy log. If a deploy was interrupted, redeploy the service.

### E. I only want to test from another device on the same office Wi-Fi

For temporary development testing, Django can listen on `0.0.0.0`, but that is not the correct solution for staff using different home/mobile networks. Use the public deployment described above.

## Security checklist

- Use a strong unique password for every user.
- Do not publish `.env`.
- Do not commit real passwords.
- Use HTTPS in production.
- Use PostgreSQL for the live application.
- Restrict Django Admin to authorized administrators.
- Back up the production database.
- Review staff accounts regularly.

## Production files included in this ZIP

- `build.sh` — Render build script
- `render.yaml` — Render web service + PostgreSQL definition
- `leave_management/settings.py` — production-aware Django settings
- `requirements.txt` — Django, Gunicorn, WhiteNoise and PostgreSQL dependencies
- responsive staff/supervisor templates and leave workflow
