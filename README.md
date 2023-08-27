### Used libraries

#### FastAPI
- Chosen due to its simplicity, performance, and automatic generation of documentation
- Has built-in support for asynchronous operations, and is well-suited for creating REST APIs

#### SqlAlchemy
- One of the most popular and complete ORMs for python, has great async support in newer versions


### Local setup
- **Prerequisite**: Docker installed and running
- Rename `.env.example` file to `.env`
- Installs dependencies and run the container: `docker-compose up --build`
- Open up an API documentation and enjoy: `http://0.0.0.0:8000/docs`
