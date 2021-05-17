<!-- TABLE OF CONTENTS -->
## Inventory System

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)




<!-- ABOUT THE PROJECT -->
## About The Project

Second assignment done for the Data-Driven Microservices module, it uses Kubernetes deployment files to setup the system and control number of replicas.
Communication between the microservices is done through gRPC, each microservice is a Flask server. It has been load tested with Gatling and there are API tests written in Postman.
Monitoring is done through Prometheus and Kubernetes dashboard. Serverless function implemented in Kubeless is a part of the cluster, it checks for profanities in the post/video title using a Python library. 

Flask client shows statistics compiled by the analytics client about the data read from the servers, Chart.js is used to for the graphs, the rest is shown as a simple webpage with a jQuery AJAX call to fetch the new data.

Main features of my application:
* Deploys as a K8s cluster of microservices.
* Processes data from CSV files which then is sent to another microservice through gRPC.
* Uses a Serverless function, which is a part of the cluster.
* Monitors the client services and cluster as a whole with Prometheus.
* Tested with Gatling and Postman.

### Built With
Major components that I have used in building this application, smaller ones not mentioned here can be found in my pom.xml:
* [Kubernetes](https://kubernetes.io/)
* [Kubeless](https://kubeless.io/)
* [gRPC](https://grpc.io/)
* [Docker](https://www.docker.com/)
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [Gatling](https://gatling.io/)
* [Prometheus](https://prometheus.io/)
* [Helm](https://helm.sh/)



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

For the Serverless function to work you need to have Kubeless CLI installed [here's a guide](https://kubeless.io/docs/quick-start/).
You obviously need Kubernetes installed, for the Prometheus monitoring you will need Helm.

### Running the Cluster
1. Clone the repo ```git clone https://github.com/pomyslowynick/ddm-assignment_2```
2. Run *createCluster.sh*
3. The cluster should be created in a few minutes, run ```kubectl get pods``` to see it's status.
4. If all pods are running then go to [localhost:30001](localhost:30001)
5. You should see the analytics data being updated.
6. In the folder */serverless* run *create_kubeless_function_script.sh*
7. The cluster is fully functional now.