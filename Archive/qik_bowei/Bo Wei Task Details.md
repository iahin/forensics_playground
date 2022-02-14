# QIK Interface Requirements

| Project Title        | <span style="font-weight:normal">Smart Learning Analytics for Digital Crime</span> |
| -------------------- | ------------------------------------------------------------ |
| **Period**           | 31 May 2021 to 22 Aug 2021                                   |
| **Service provider** | Teo Bo Wei                                                   |
| **Project Lead**     | Peter Loh Kok Keong                                          |
| **Lead Developer**   | Isfaque AL Kaderi Tuhin                                      |

## Overview

SLADE is an post incidence forensics investigation platform that allows collaboration of investigators to perform intelligent analysis and deduce the cyber attack scenario. QIK interface acts as a low complexity man-machine interface between SLADE and the crime investigation team, which is designed as a dialogue-based dashboard that facilitates individual or group interaction with SLADE. 

## Project Setup and management

The following libraries and frameworks are currently being used for the development environment. You will be working on the wireframe for first few weeks so you can set up the environment once you have understand the functionality of the QIK interface.

- Operating system: Windows 10
- Frontend: React.js, Ant Design UI Framework, Vis.js
- Backend: MongoDB, Neo4j Graph DB, Python Flask API, Networkx Library 
- Wireframing: Adobe XD or as preferred
- Source Code, Version control and documentation: [Github repository](https://github.com/16sic013j/sitslade_qik)
- Collaboration: Zoom, Whatsapp
- [Reference wireframe for layout and colour scheme](https://app.mockplus.com/s/E8aWtYYtVd5)

## Requirements

### System Requirements

| #    | Requirement                                                  | Remarks                                                      |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 1    | QIK-Script Dictionary translates human inputs to executable commands and parameters to control SLADE. It also translates information requests, inferences and deductions from SLADE to human comprehensible outputs. | Query builder for Hypothesis creation.                       |
| 2    | Uses QIK dashboard to input available facts, expert inferences and specific queries related to the case. This can be in the form of a subset of natural language constructs or as a check box menu. These inputs may be segregated into expert inferences, queries and specific domain knowledge (new facts regarding the case) and fed to SLADE. | Adding of additional details for existing case or result     |
| 3    | The investigation team can also reference past casefiles in the Historical Crime Archive to segregate some expert inferences into specific domain knowledge based on the already known facts. | View historical case details, related conclusion and inferences made |
| 4    | Translates user queries, inferences and knowledge into command scripts and script parameters to control execution of selected Playbook Library APIs, Threat Intelligence Hunter and the Interactive Reinforcement Learning. | TBC                                                          |

### UI Requirements

| #    | Requirement                                                  | Remarks |
| ---- | ------------------------------------------------------------ | ------- |
| 1    | User friendly dashboard interface with mainly search, textual information and visualization layout |         |
| 2    | Get user input and make API calls for querying, searching, sorting and filtering of results |         |
| 3    | Visualize the results in the form of network graph with filtering capabilities |         |
| 4    | Display the textual results in clean and user-friendly way   |         |
| 5    | User should be able to come up with queries using query builder |         |
| 6    | Save queries as hypothesis, Group it into                    |         |

### Project tasks

| #    | Tasks                               | Deadline     |
| ---- | ----------------------------------- | ------------ |
| 1    | Wire Frame Design                   | 13 JUNE 21   |
| 2    | Preliminary QIK Interface           | 18 JULY 21   |
| 3    | Project Documentation               | 22 AUGUST 21 |
| 4    | Final QIK Interface for integration | 22 AUGUST 21 |

# Reference

1. [User friendly query builder](https://github.com/ukrbublik/react-awesome-query-builder)
2. [Neo4j Graph and Querying](https://neo4j.com/developer/cypher/intro-cypher/)

3. [Sample interface](https://www.hsleiden.nl/binaries/content/assets/hsl/lectoraten/digital-forensics-en-e-discovery/publicaties/2019/technology-assisted_analysis_of_timeline_and_connections.henseler_hyde_rev.pdf)

