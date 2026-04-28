SKY Messages Project - Student 3

HOW TO RUN:

1. Open this folder in VS Code.
2. Open Terminal.
3. Run:

   python -m pip install -r requirements.txt
   python manage.py makemigrations
   python manage.py migrate
   python create_demo_users.py
   python manage.py runserver

4. Open Chrome:

   http://127.0.0.1:8080/

Demo login:
   Username: ceyda
   Password: password123

Second test user:
   Username: manager
   Password: password123

Pages:
   /messages/inbox/
   /messages/sent/
   /messages/drafts/
   /messages/new/

If port 8080 refuses to connect, the server is not running.
Run: python manage.py runserver
