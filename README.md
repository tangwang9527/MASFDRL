# MASFDRL

## Overview
This repository contains the source code and deployment files for a reinforcement learning (RL) simulation environment. The project is designed to be deployed in a Kubernetes (K8S) environment with significant hardware resources.

## Files Included
- **masfd-rl-start-0.0.1-SNAPSHOT.jar**: This JAR file contains the compiled Java code for the RL simulation environment.
- **masfd.py**: This Python script is used to execute the simulation.
- **Dockerfile**: This file is used to build a Docker image based on the JAR file, making it easier to deploy the simulation environment.
- **masfd-rl.yaml**: This YAML file is used to deploy the simulation environment in a Kubernetes cluster.

## Prerequisites
- A Kubernetes (K8S) environment with sufficient hardware resources.
- Docker installed on your machine to build the Docker image.
- Python 3.x installed to run the `masfd.py` script.

## Getting Started
### Building the Docker Image
1. Navigate to the root directory of the project.
2. Run the following command to build the Docker image:
   ```sh
   docker build -t masfd-rl .
   ```

### Running the Simulation
1. Deploy the simulation environment using the `masfd-rl.yaml` file:
   ```sh
   kubectl apply -f masfd-rl.yaml
   ```
2. Verify that the deployment is successful by running:
   ```sh
   kubectl get pods
   ```
3. Once the pod is running, you can interact with the simulation using the `masfd.py` script.

## Contributing
We welcome contributions to this project. Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Create a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For any questions or issues, please open an issue on this GitHub repository.
