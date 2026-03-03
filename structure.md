Description
Milestone 1 of the Gruha Alankara project establishes the structural and environmental foundation necessary for a robust Flask-based AI application. Activity 1.1 focuses on a modular directory hierarchy, ensuring that backend logic, frontend assets, and user data are cleanly separated for better maintainability. The root directory centralizes essential files like app.py for routing, models.py for database schema, and config.py for secure settings.

The frontend is organized into a static folder for CSS and JavaScript and a templates folder for HTML, facilitating the use of Jinja2 for dynamic page rendering. An uploads directory is specifically designated to store user-submitted room images, requiring configured permissions for secure file handling. Activity 1.2 transitions the project into the development phase by prioritizing environment isolation through a Python virtual environment.

By using venv, the project prevents version conflicts between global system libraries and specific requirements like Flask-SQLAlchemy or LangChain. Once the environment is activated, the requirements.txt file is used to batch-install all necessary dependencies, including the Transformers library for AI tasks. This setup phase concludes with a verification step where key modules are imported in a Python shell to confirm a successful installation. Ultimately, these activities ensure that the platform has a stable, scalable, and portable architecture before any feature development begins.


Description
● Organize your project with a well-structured directory hierarchy.

● The root directory should contain the main application file (app.py), database models

(models.py), configuration settings (config.py), and dependencies list (requirements.txt).

● Create a static folder to hold CSS stylesheets, JavaScript files, and image assets organized in

subdirectories.

● Establish a templates folder for all HTML files including base template and page-specific

templates.

● Set up an uploads directory for storing user-uploaded design images with proper

permissions.

Fig: Shows the html templates and .py files of my project

