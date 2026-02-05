# POS Microservices Platform (Python / Docker / gRPC)

Microservices-based backend platform developed using containerized services, combining REST APIs with a dedicated Identity Management gRPC service. The system integrates both NoSQL and relational databases and is orchestrated using Docker Compose.

## Features
- Microservices architecture orchestrated with Docker Compose
- Client management service backed by MongoDB
- Event management service backed by MariaDB
- Centralized Identity Management service using gRPC
- Token-based authentication and authorization
- Inter-service communication via REST and gRPC
- Fully containerized setup for local development

## Tech Stack
- Python
- FastAPI
- gRPC & Protocol Buffers
- MongoDB
- MariaDB
- Docker & Docker Compose

## Architecture
The platform is composed of the following services:

### client-webservice
REST-based service responsible for client-related operations.  
Uses MongoDB as the primary data store and communicates with other backend services using REST and gRPC.

### event-webservice
REST-based service responsible for event management.  
Uses MariaDB as the relational database and relies on the Identity Management service for access validation.

### idm-grpc-service
gRPC-based Identity Management service responsible for:
- User authentication
- Token validation
- User logout

This service acts as a centralized authorization component for all other services.

### Databases
- **MongoDB** – used by `client-webservice`
- **MariaDB** – used by `event-webservice`

## Ports
- client-webservice: `8000`
- event-webservice: `8001`
- idm-grpc-service: `50051`
- MongoDB: `27017`
- MariaDB: `3306`

## Running the Project Locally

### Requirements
- Docker
- Docker Compose

### Start all services
```bash
docker compose up --build
docker compose down
```

All services start automatically and communicate over an internal Docker network.

### gRPC API
The Identity Management service exposes the following gRPC methods (defined in idm.proto):
Login(email, password) – returns an authentication token

ValidateToken(token) – validates token and returns user details

Logout(token) – invalidates the token

### Project Context
This project was developed as part of a university backend systems course, focusing on microservices architecture, containerization, and inter-service communication using REST and gRPC.

### Author
Andrei Avramescu