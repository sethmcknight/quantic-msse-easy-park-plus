# GitHub Issues for EasyParkPlus Project

### Issue #2: Baseline Application Analysis
**Priority:** High  
**Estimated Time:** 4 hours  
**Description:** Run and thoroughly understand the existing parking lot manager application.
- [X] Create a document summarizing application functionality
- [X] Document the current features and behavior
- [X] Identify key components and their relationships

### Issue #5: Original UML Diagrams
**Priority:** Medium  
**Estimated Time:** 6 hours  
**Description:** Create structural and behavioral UML diagrams for the original codebase.
- [X] Create a class/component diagram (structural)
- [X] Create a sequence/activity diagram (behavioral)
- [X] Ensure diagrams accurately represent the current code structure
- [X] Add appropriate annotations and explanations


### Issue #3: Anti-Pattern Identification
**Priority:** High  
**Estimated Time:** 4 hours  
**Description:** Review the codebase to identify all anti-patterns and problematic code practices.
- [X] Review variable naming conventions
- [X] Identify poor code structure and organization
- [X] Look for dead code and unnecessary abstractions
- [X] Document all identified anti-patterns with line references
- [X] Prioritize anti-patterns to be fixed

### Issue #4: Design Pattern Opportunities
**Priority:** High  
**Estimated Time:** 3 hours  
**Description:** Identify where design patterns could improve the architecture and functionality.
- [X] Research applicable design patterns for parking management systems
- [X] Identify at least 4 potential patterns to consider
    1. Observer
    2. Abstract Factory
    3. State Pattern
    4.
- [ ] Document how each pattern could benefit the application
- [X] Select the 2 most impactful patterns to implement
    1. Observer (ParkingLotObserver)
    2. Abstract Factory (Vehicle/ElectricVehicle)
    3. State Pattern (ParkingSlotState)


## Week 2: Implementation and Redesign

### Issue #6: Implement Design Pattern #1
**Priority:** High  
**Estimated Time:** 8 hours  
**Description:** Implement the first selected design pattern into the codebase.
- [X] Create necessary new classes/interfaces
- [X] Modify existing code to implement the pattern
- [X] Add appropriate comments explaining the pattern implementation
- [X] Test to ensure functionality is preserved

### Issue #7: Implement Design Pattern #2
**Priority:** High  
**Estimated Time:** 8 hours  
**Description:** Implement the second selected design pattern into the codebase.
- [ ] Create necessary new classes/interfaces
- [ ] Modify existing code to implement the pattern
- [ ] Add appropriate comments explaining the pattern implementation
- [ ] Test to ensure functionality is preserved

### Issue #8: Anti-Pattern Removal
**Priority:** High  
**Estimated Time:** 10 hours  
**Description:** Refactor code to remove all identified anti-patterns and improve code quality.
- [ ] Improve variable naming
- [X] Improve code organization
- [X] Remove dead code and unnecessary abstractions
- [X] Implement proper error handling
- [X] Refactor complex methods and improve readability
- [X] Add appropriate comments throughout the codebase

### Issue #9: Redesigned UML Diagrams
**Priority:** Medium  
**Estimated Time:** 5 hours  
**Description:** Create UML diagrams for the refactored and improved codebase.
- [ ] Create updated class/component diagram (structural)
- [ ] Create updated sequence/activity diagram (behavioral)
- [ ] Highlight where design patterns have been implemented
- [ ] Add appropriate annotations and explanations

### Issue #10: Application Testing
**Priority:** High  
**Estimated Time:** 4 hours  
**Description:** Test the refactored application thoroughly and document results.
- [ ] Test all original functionality
- [ ] Verify improvements from implemented patterns
- [ ] Capture screenshots/record video of the application running
- [ ] Document any issues and fix them

## Week 3: DDD, Microservices Design, and Documentation

### Issue #11: Domain-Driven Design Analysis
**Priority:** High  
**Estimated Time:** 6 hours  
**Description:** Analyze the extended requirements using domain-driven design principles.
- [ ] Identify core domain and subdomains
- [ ] Define bounded contexts for parking management and EV charging
- [ ] Create a bounded context diagram
- [ ] Develop ubiquitous language for each context

### Issue #12: Domain Modeling
**Priority:** High  
**Estimated Time:** 8 hours  
**Description:** Create detailed domain models for the extended system.
- [ ] Identify and model domain entities
- [ ] Define value objects
- [ ] Design aggregates and aggregate roots
- [ ] Create domain model diagrams

### Issue #13: Microservices Architecture Design
**Priority:** High  
**Estimated Time:** 8 hours  
**Description:** Design a microservices architecture for the extended system.
- [ ] Identify services aligned with bounded contexts
- [ ] Define responsibilities for each service
- [ ] Specify API endpoints (external and internal)
- [ ] Design database strategy for each service
- [ ] Create architecture diagram

### Issue #14: Pattern Implementation Justification
**Priority:** Medium  
**Estimated Time:** 3 hours  
**Description:** Write detailed justification for the patterns implemented and anti-patterns removed.
- [ ] Explain why each pattern was chosen
- [ ] Document benefits achieved from pattern implementation
- [ ] Describe how anti-patterns were addressed
- [ ] Include before/after comparisons where relevant

### Issue #15: DDD and Microservices Documentation
**Priority:** Medium  
**Estimated Time:** 5 hours  
**Description:** Document the DDD approach and microservices architecture.
- [ ] Explain the DDD methodology used
- [ ] Document domain models in detail
- [ ] Describe the proposed microservices architecture
- [ ] Explain how the architecture supports scalability and the new EV charging feature

### Issue #16: Final Project Compilation
**Priority:** High  
**Estimated Time:** 4 hours  
**Description:** Compile all project components for submission.
- [ ] Organize all UML diagrams
- [ ] Compile screenshots/video
- [ ] Package updated source code
- [ ] Format all written documentation
- [ ] Review submission against rubric requirements
- [ ] Create final .zip or .rar archive

### Issue #17: Final Review and Submission
**Priority:** High  
**Estimated Time:** 2 hours  
**Description:** Conduct a final review of all deliverables and submit the project.
- [ ] Verify all requirements are met according to rubric
- [ ] Check that all documentation is clear and well-formatted
- [ ] Ensure source code is properly commented and functional
- [ ] Submit final project package

## Variable Naming Refactoring (Complete)
- All variable naming anti-patterns in UI, business logic, and vehicle classes have been resolved.
- Widget references and usages in ParkingLotUI are now descriptive and consistent.
- All business logic and vehicle class variables use clear, meaningful names.
- See anti-patterns.md for documentation of resolved issues.