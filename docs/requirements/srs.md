# Software Requirements Specification

## 1. Introduction

### 1.1 Purpose

### 1.2 Project Scope

### 1.3 Intended Users

### 1.4 Definitions and Abbreviations

## 2. Overall Description

### 2.1 Product Perspective

### 2.2 Product Functions

### 2.3 User Characteristics

### 2.4 Operating Environment

The initial system will be developed and tested in a Linux environment.

The current development environment is:

- Operating System: Linux Mint
- Programming Language: Python 3.x
- Database: SQLite
- Machine Learning: scikit-learn
- Dashboard: Streamlit
- Visualization: Plotly
- Version Control: Git
- Repository: GitHub

The architecture is intended to remain compatible with commonly used Linux distributions. Distribution-specific commands or interfaces will be isolated within appropriate system-integration modules where necessary.

### 2.5 Constraints

Technical Constraints
Initial implementation targets one Linux server.
ML performance depends on available training data.
Some telemetry may require elevated privileges.
The system should avoid excessive monitoring overhead.
Corrective actions must be restricted for safety.

Project Constraints
Approximately 12–15 weeks available.
Approximately 1–2 hours of development per day.
Undergraduate project scope.
Limited access to real production failure datasets.

Resource Constraints
Prefer free/open-source technologies.
Avoid unnecessary cloud infrastructure.
Avoid complex distributed architecture unless justified.

### 2.6 Assumptions

We'll explicitly state:

 The monitored machine is running Linux. 
 The system has access to required telemetry interfaces. 
 The administrator has appropriate permissions for authorized monitoring/remediation tasks. 
 Training data can be collected through normal operation and controlled test scenarios. 
 Selected failure scenarios can be safely reproduced in a test environment. 
 The dashboard is accessed by an authorized administrator. 
 ML predictions represent risk estimates rather than guaranteed failures.

## 3. Functional Requirements

## 4. Non-Functional Requirements

## 5. External Interface Requirements

### 5.1 User Interface

### 5.2 Hardware Interface

### 5.3 Software Interface

### 5.4 Communication Interface

## 6. Data Requirements

## 7. Safety and Security Requirements

## 8. Acceptance Criteria
