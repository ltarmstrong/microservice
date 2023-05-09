# READ ME

Communication Contract

Overview:

This document outlines the communication contract between the client application and the Windows 10/11 Optimization Program microservice. The microservice is responsible for generating a list of installed programs and uninstalling specified programs on the client's machine.

Install Programs

Request:

‘GET /installed_programs’

Parameters:

None

Example call:

curl http://localhost:5000/installed_programs

Response:

{
  "installed_programs": [
    "Program 1",
    "Program 2",
    "Program 3"
  ]
}

Uninstall Programs

Request:

‘POST /uninstall_programs’

Parameters:

programs_to_uninstall: A list of program names to uninstall.


Example call:

curl -H "Content-Type: application/json" -X POST -d '{"programs_to_uninstall": ["Program 1", "Program 2"]}' http://localhost:5000/uninstall_programs



Response:

{
  "uninstall_results": {
    "Program 1": "Uninstalled successfully",
    "Program 2": "Failed to uninstall"
  }
}

UML Sequence Diagram

Here is a UML sequence diagram that shows how the client application communicates with the microservice:


Client Application          Microservice
        |                           |
        |        GET /installed_programs
        |-------------------------->|
        |                           |
        |          List of installed programs
        |<--------------------------|
        |                           |
        |       POST /uninstall_programs
        |-------------------------->|
        |                           |
        |    List of programs to uninstall
        |<--------------------------|
        |                           |
        |       Uninstall specified programs
        |-------------------------->|
        |                           |
        |    Results of uninstallation
        |<--------------------------|
        |                           |



In this diagram, the client application sends a GET request to the /installed_programs endpoint to retrieve a list of installed programs. The microservice receives the request, generates the list of installed programs, and sends it back as a JSON response.


The client application can also send a POST request to the /uninstall_programs endpoint to uninstall specific programs. The request payload should include a list of program names to uninstall. The microservice receives the request, uninstalls the specified programs, and sends a JSON response back with the results of each uninstall attempt.
