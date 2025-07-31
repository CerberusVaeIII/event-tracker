-- Event Manager App -- 

Welcome to my Event Manager App, a full-stack web app designed for event management, built with FastAPI and JavaScript. Here, users can create accounts, log in, and manage their own events, through a simple token-based application and experience.

 - Below are some of its features:

JWT token based authentication;
Create, Read, Update, Delete events once logged in, with minor validation;
Password hashing within the database;
Active redirects based on login status, presence and validity of token;
Token expiration handling;
Alembic database migrations;
Intuitive UI through JavaScript, HTML and CSS;
Deployed and fully functional on Render.

 - Stack:

Front end:
 - HTML
 - CSS
 - JavaScript (vanilla)
 - DOM manipulation and fetch requests

Back end:
 - FastAPI (Python 3)
 - SQLite as easier to deploy alternative to PostgreSQL (via SQLAlchemy ORM)
 - Alembic (database versioning and migrations)
 - Jinja2 (templating, serving HTML pages)
 - CORS and OAuth2 token-based security

 - Installation: (Listed below are terminal commands)

 1. Clone the repo. 
    git clone https://github.com/CerberusVaeIII/event-manager.git
    cd event-manager
 2. Create a virtual environment
    python -m venv venv
    source venv/bin/activate  (for Mac, Linux)
    venv\Scripts\activate     (for Windows)
 3. Install dependencies with pip
    pip install -r requirements.txt
 4. Set environment variables
    Create a .env file in the root folder:
    SECRET_KEY=secret_key (You can manually enter this too as any string, or generate one online or through an LLM)
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=60
 5. Run alembic migrations
    alembic upgrade head
 6. Start the app
    uvicorn app.main:app --reload

 - Usage: 

Visit http://localhost:8000/signup (If hosting locally) to create an account.
You will be redirected to http://localhost:8000/login, where you should enter your information. If the information is correct,
you will be redirected to http://localhost:8000/events.

Once logged in, users can create, read, update and delete events. The current user's events are bound to them through a foreign key, and each request is validated through the token, so the current user will only see their events. On every action, the event list is refreshed. 

In the top right, you will have a prompt telling you your username, and then two buttons. One for deleting your account, and one for logging out. Both will redirect you to the login page, however the delete button will delete your account from the database, and all your created events.

 - Alembic migrations

Alembic tracks all migrations in the ./alembic/versions folder. For more info, please check out ./alembic/README.md

 - Deployment on Render

This app can be deployed on Render. It provides automatic hosting of GitHub repos, and automatic HTTPS. The Render startup command is:
uvicorn app.main:app --host 0.0.0.0 --port ${PORT}

 - Future improvements:

    - Dockerization
    - Better admin paths and dashboard
    - Frontend calendar integration
    - Event search function (for really busy people!)
    - Reimplementation of a more serious database in the form of PostgreSQL

 - License

This project is licensed under the MIT License.

 - Author

Robert Hatos
GitHub: @CerberusVaeIII