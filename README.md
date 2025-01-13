# Introduction
This is the backend for the CSEDUIC project. It provides the necessary APIs and services to support the frontend application.

# Tech Stack
- **Python**: The primary programming language used for backend development.
- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **SQLAlchemy**: An SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **PyTest**: This library is used for unit testing for the application.
- **PostgreSQL**: The database used for storing application data.
- **Docker**: Used for containerizing the application to ensure consistency across different environments.

## How to Run Using Docker
1. **Install Docker**: Ensure Docker is installed on your machine. You can download it from [here](https://www.docker.com/products/docker-desktop).

2. **Create .env file**: create a .env file in the base directory with the fields 
of the **.env.template** file. set the **DB_URL** like this

   ```sh
   DB_URL = postgresql://username:password@host.docker.internal:5432/db_name
   ```
   create a local postgres database and change the **username**, **password** and 
   **db_name** accordingly.

3. **Build the Docker Image**:
   when in the base directory run this to create the docker image.
   ```sh
   docker build -t cseduic-backend .
   ```

4. **Run the Docker Image**: after building the docker image run this command to start the application.
   ```sh
   docker run -p 8000:8000 cseduic-backend
   ```
   the application will now be available on ```localhost:8000```. 
   <br>
   Go to [this link](http://localhost:8000/docs) to access the APIs.

