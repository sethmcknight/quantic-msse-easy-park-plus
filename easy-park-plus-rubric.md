# Software Design & Architecture Project Guide

## Project Overview

For this project, you will be presented with an existing preliminary prototype code base, and you will need to decide on patterns to improve it, while also identifying anti-patterns and removing them. This project will give you hands-on experience in implementing patterns, identifying anti-patterns, and designing software architectures. You can complete this project either individually or as a group of no more than three people.

## Learning Outcomes

When completed successfully, this project will enable you to:

- Pinpoint bad design, problematic source code, and bad coding practices in need of improvement
- Identify and justify opportunities for including software design patterns
- Implement software design patterns in an existing code base
- Utilize object-oriented design principles in this process
- Utilize UML, both structural and behavioral diagrams, to represent software designs
- Utilize domain-driven design principles to model a system and develop a high-level microservices architecture

## Project Description

Understanding, updating, and extending from an existing codebase is a crucial skill to develop if you plan to work in the software industry. A substantial portion of what you will work on will be fixing, maintaining, and extending from existing source code. It can be quite rare to code directly from scratch, and even in such cases, your own code will evolve over time and demand more polish and refinement.

Key to this process of improving software quality is the identification and implementation of design patterns, handy solutions to common software problems. As code becomes more unwieldy, we can use patterns to shore it up. Structural patterns might enhance reusability, architectural patterns can reduce duplication, and behavioral patterns simplify objects and divvy up responsibilities. All patterns bring something to the table. The trick is knowing when to employ them and to justify their existence, not simply using them for the sake of it.

On the other hand, just like patterns are tools for best practices, there are also "anti-patterns". These are poor coding practices and design choices that can complicate and weaken source code, making it difficult to read and prone to errors. Some common "anti-patterns" include:

- Poor/non-explicit variable names
- Lack of comments or useless comments
- Passing mutable arguments
- Returning different types in a function
- Clumsy, unnecessary loop statements
- Superfluous/lengthy/nested if statements
- Global variables
- Using try/except blocks without handling exceptions
- Broad import statements
- Deprecated, unused code blocks ("Dead Code")
- Unnecessary abstractions

The source code you will be using for this project is an initial prototype parking lot manager application for a single parking lot. It is an initial prototype of parking lot management company EasyParkPlus developed internally, and they have now contacted you as a software engineering expert. Download and run the baseline source code for the Parking Lot Manager as provided.

Take some time to explore the code and understand what it is doing. You should draw out some of the code's structure, logic, and flow of data using appropriate UML diagrams; this can help clarify areas of overlap and confusion. Once you are comfortable with the operations of the program, begin improving it, utilizing at least two distinct patterns from the OO-related ones you have studied so far. In addition, remove any anti-patterns and poor coding elements you encounter, while adding in your own comments and clarification. These fixes and improvements should not simply be cosmetic; they should provide significant structural and architectural improvements to the system. In a separate document, prepare a written justification outlining the fixes you have made and why you chose your selected patterns.

Additionally, EasyParkPlus is planning to scale up this prototype application to handle their operations across multiple parking lot facilities. The parking lot company will also add a new business activity related to electric vehicle charging and add a new feature to the parking lot application: **Electric Vehicle (EV) Charging Station Management**.

To extend their system you will consider their business and system from a domain-driven design perspective, with an eye to developing a scalable microservices architecture-based solution. In architecting this software, including the new EV charging capability, you should use a domain-driven design approach, and propose a resultant microservices-based architecture to support the overall application. You are asked to describe the microservice-based software architecture, but you are not required to develop the extended microservices software implementation at this stage.

### To apply domain-driven design:

- Identify the core domain and core subdomains
- Define bounded contexts
- Design sample ubiquitous language for each context
- Model domain entities, value objects, and aggregates

To help you with any questions you may have about the technical and operational details and language and vocabulary used, the Technical Manager at EasyParkPlus, Michael, has conveniently made himself available.

### Design a preliminary microservices architecture:

- Identify services (align with bounded contexts)
- Identify key responsibilities of each service
- Describe APIs/endpoints (external facing and service-to-service endpoints)
- Identify separate DBs per service

## Tips & Resources

- The latest version of Python 3 is required.
- If libraries are missing, use `pip` to install them.
- The written justification should adequately address your chosen patterns, why they were included, and how you fixed the anti-patterns.
- The written portion describing the microservices-based architecture should provide a high-level architecture as per the submission instructions.
- [The Gang of Four - Design Patterns](https://springframework.guru/gang-of-four-design-patterns/)
- [Refactoring: Improving the Design of Existing Code](https://books.google.com/books?hl=en&lr=&id=2H1_DwAAQBAJ)
- [When and Why Your Code Starts to Smell Bad](https://ieeexplore.ieee.org/abstract/document/7817894)
- [Domain-Driven Design & Microservices](https://www.geeksforgeeks.org/domain-oriented-microservice-architecture/)

## Submission Guidelines

Your final submission should consist of a packaged `.zip` or `.rar` file containing your written justifications for your design choices, including:

- Two UML diagrams (one structural, one behavioral) representing the design of the code you first downloaded
- Two UML diagrams (one structural, one behavioral) representing the re-designed code you have developed and submitted
- Your updated source code for the parking application
- Screenshots (or brief video) of the application running on your computer
- Written document of how you used domain-driven design to model the Parking Management System, including the Electric Vehicle (EV) Charging Station Management extension to the system, and your proposed high-level microservices-based architecture of the system including:
  - A high-level bounded context diagram
  - Basic domain models for parking management and EV charging
  - A proposed microservices architecture diagram including services, APIs/endpoints, and per service DBs

To submit your project, click on the "Submit Project" button on your dashboard and follow the steps provided in the Google Form. If you are submitting your Software Design and Architecture project as a group, ensure only ONE member submits on behalf of the group. You will also be prompted to upload the final page of your Group Project Agreement, which must be completed and signed by all group members. For questions, contact msse+projects@quantic.edu. Project grading typically takes about 3-4 weeks after the submission due date. There is no score penalty for late submissions, but grading may be delayed.

## Plagiarism Policy

Quantic defines plagiarism as: "Knowingly representing the work of others as one's own, engaging in any acts of plagiarism, or referencing the works of others without appropriate citation." This includes both misusing or not using proper citations for the works referenced, and submitting someone else's work as your own. All submissions are monitored for instances of plagiarism and all plagiarism, even unintentional, is considered a conduct violation. When in doubt, cite!

## Project Rubric

| Score | Description |
|-------|-------------|
| 5 | - Addresses all project requirements<br>- Design and code improvements use two relevant design patterns<br>- Written report is detailed and documents changes and reasons for patterns<br>- Original and redesign represented correctly using UML diagrams<br>- All bad coding practices identified and improved<br>- Appropriate bounded context diagram<br>- Detailed DDD-based domain models<br>- High-quality microservices architecture diagram<br>- Submission includes updated code, screenshots, and written report |
| 4 | - Addresses most project requirements<br>- Design and code improvements use two relevant design patterns<br>- Written report explains changes and reasons for patterns<br>- UML diagrams mostly correct<br>- Most bad coding practices identified and improved<br>- Appropriate bounded context diagram<br>- Good DDD-based domain models<br>- Good microservices architecture diagram<br>- Proper submission format |
| 3 | - Addresses some project requirements<br>- Some relevant design patterns used<br>- Written report explains some changes and reasons<br>- UML diagrams mostly correct<br>- Some bad coding practices identified and improved<br>- Adequate bounded context diagram<br>- Adequate DDD-based domain models<br>- Adequate microservices architecture diagram<br>- Proper submission format |
| 2 | - Addresses few project requirements<br>- Design and code improvements did not appropriately use some relevant design patterns<br>- Written report explains few changes and reasons<br>- At least one UML diagram for original design<br>- Two UML diagrams for redesign<br>- Few bad coding practices identified and improved<br>- Basic bounded context diagram<br>- Adequate DDD-based domain models<br>- Adequate microservices architecture diagram<br>- Proper submission format |
| 1 | - Addresses the project but missing most requirements<br>- Design and code improvements did not appropriately use some relevant design patterns<br>- Written report does not explain changes and/or reasons<br>- Original and redesign not represented correctly<br>- Most bad coding practices not identified or improved<br>- Minimal diagrams and models<br>- Proper submission format |
| 0 | - Did not complete the assignment, plagiarized all or part of the assignment, or completely failed to address the project requirements |

