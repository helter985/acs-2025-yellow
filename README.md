# PricePulse


## 1.Introduction

The project PricePulse is a software that aims to provide updated prices to the vendors of the distribuitor in real time.

## 1.1 Purpose

The purpose of this document is to outline the requirements for the app that the vendors will be using daily. This document will be used by all stakeholders, developers and testers.

## 1.2 Scope

The scope of this project is limited to the testing of the features described in the succeding sections of this document.
Non-functional testing like stress, performance is beyond scope of this project.
Automation testing is beyond scope.
Functional testing and a basic external interface are in scope and need to be tested.

## 1.3 Definitions, Acronyms, and Abbrevations 
| Abbreviation | Word     |
|--------------|----------|
| A            | Admin    |
| D            | Distributor|
| D            | Developer|
| S            |Stakeholder|
| T            | Tester   |  
| V            | Vendor   |
## 2. Requirements

### 2.1 Roles Description

| Role         | Description                                                                 |
|--------------|-----------------------------------------------------------------------------|
| **Vendor**   | User of the mobile application. Queries product prices in real time.        |
| **Distributor** | Provides updated product data to be consumed by the app.                |
| **Admin**    | Manages user access and system configurations.                              |
| **Tester**   | Validates that the app behaves according to the specified requirements.     |
| **Developer**| Implements and maintains app features based on stakeholder input.           |

### 2.2 Features per Role

| Role         | Features                                                                                 |
|--------------|------------------------------------------------------------------------------------------|
| **Vendor**   | - Search product by code or name  <br> - View updated prices in real time                |
| **Admin**    | - Manage vendor accounts  <br> - Reset passwords  <br> - Monitor system status           |
| **Tester**   | - Execute functional test cases  <br> - Report bugs  <br> - Verify bug fixes             |
| **Developer**| - Develop backend API  <br> - Implement front-end components  <br> - Fix issues          |
| **Distributor** | - Feed price updates to the system  <br> - Ensure data accuracy                      |
