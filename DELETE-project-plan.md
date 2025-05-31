# GitHub Issues for EasyParkPlus Project

### Issue #2: Baseline Application Analysis

**Priority:** High  
**Estimated Time:** 4 hours  
**Description:** Run and thoroughly understand the existing parking lot manager application.

- [x] Create a document summarizing application functionality
- [x] Document the current features and behavior
- [x] Identify key components and their relationships

### Issue #5: Original UML Diagrams

**Priority:** Medium  
**Estimated Time:** 6 hours  
**Description:** Create structural and behavioral UML diagrams for the original codebase.

- [x] Create a class/component diagram (structural)
- [x] Create a sequence/activity diagram (behavioral)
- [x] Ensure diagrams accurately represent the current code structure
- [x] Add appropriate annotations and explanations

### Issue #3: Anti-Pattern Identification

**Priority:** High  
**Estimated Time:** 4 hours  
**Description:** Review the codebase to identify all anti-patterns and problematic code practices.

- [x] Review variable naming conventions
- [x] Identify poor code structure and organization
- [x] Look for dead code and unnecessary abstractions
- [x] Document all identified anti-patterns with line references
- [x] Prioritize anti-patterns to be fixed

### Issue #4: Design Pattern Opportunities

**Priority:** High  
**Estimated Time:** 3 hours  
**Description:** Identify where design patterns could improve the architecture and functionality.

- [x] Research applicable design patterns for parking management systems
- [x] Identify at least 4 potential patterns to consider
  1. Observer Pattern
  2. Factory Pattern
  3. Strategy Pattern
  4. Manager Pattern
- [x] Document how each pattern could benefit the application
- [x] Select the most impactful patterns to implement
  1. Observer (ParkingLotObserver)
  2. Factory (Vehicle creation)
  3. Strategy (Search strategies)
  4. Manager (Separation of concerns)

## Week 2: Implementation and Redesign

### Issue #6: Implement Design Pattern #1

**Priority:** High  
**Estimated Time:** 8 hours  
**Description:** Implement the first selected design pattern into the codebase.

- [x] Create necessary new classes/interfaces
- [x] Modify existing code to implement the pattern
- [x] Add appropriate comments explaining the pattern implementation
- [x] Test to ensure functionality is preserved

### Issue #7: Implement Design Pattern #2

**Priority:** High  
**Estimated Time:** 8 hours  
**Description:** Implement the second selected design pattern into the codebase.

- [x] Create necessary new classes/interfaces
- [x] Modify existing code to implement the pattern
- [x] Add appropriate comments explaining the pattern implementation
- [x] Test to ensure functionality is preserved

### Issue #8: Anti-Pattern Removal

**Priority:** High  
**Estimated Time:** 10 hours  
**Description:** Refactor code to remove all identified anti-patterns and improve code quality.

- [x] Improve variable naming
- [x] Improve code organization
- [x] Remove dead code and unnecessary abstractions
- [x] Implement proper error handling
- [x] Refactor complex methods and improve readability
- [x] Add appropriate comments throughout the codebase

### Issue #9: Redesigned UML Diagrams

**Priority:** Medium  
**Estimated Time:** 5 hours  
**Description:** Create UML diagrams for the refactored and improved codebase.

- [x] Create updated class/component diagram (structural)
- [x] Create updated sequence/activity diagram (behavioral)
- [x] Highlight where design patterns have been implemented
- [x] Add appropriate annotations and explanations

### Issue #10: Application Testing

**Priority:** High  
**Estimated Time:** 4 hours  
**Description:** Test the refactored application thoroughly and document results.

- [x] Test all original functionality
- [x] Verify improvements from implemented patterns
- [ ] Capture screenshots/record video of the application running
- [x] Document any issues and fix them

## Week 3: DDD, Microservices Design, and Documentation

### Issue #11: Domain-Driven Design Analysis

**Priority:** High  
**Estimated Time:** 6 hours  
**Description:** Analyze the extended requirements using domain-driven design principles.

- [x] Identify core domain and subdomains
- [x] Define bounded contexts for parking management and EV charging
- [x] Create a bounded context diagram
- [x] Develop ubiquitous language for each context

### Issue #12: Domain Modeling

**Priority:** High  
**Estimated Time:** 8 hours  
**Description:** Create detailed domain models for the extended system.

- [x] Identify and model domain entities
- [x] Define value objects
- [x] Design aggregates and aggregate roots
- [x] Create domain model diagrams

### Issue #13: Microservices Architecture Design

**Priority:** High  
**Estimated Time:** 8 hours  
**Description:** Design a microservices architecture for the extended system.

- [x] Identify services aligned with bounded contexts
- [x] Define responsibilities for each service
- [x] Specify API endpoints (external and internal)
- [x] Design database strategy for each service
- [x] Create architecture diagram

### Issue #14: Pattern Implementation Justification

**Priority:** Medium  
**Estimated Time:** 3 hours  
**Description:** Write detailed justification for the patterns implemented and anti-patterns removed.

- [x] Explain why each pattern was chosen
- [x] Document benefits achieved from pattern implementation
- [x] Describe how anti-patterns were addressed
- [x] Include before/after comparisons where relevant

### Issue #15: DDD and Microservices Documentation

**Priority:** Medium  
**Estimated Time:** 5 hours  
**Description:** Document the DDD approach and microservices architecture.

- [x] Explain the DDD methodology used
- [x] Document domain models in detail
- [x] Describe the proposed microservices architecture
- [x] Explain how the architecture supports scalability and the new EV charging feature

### Issue #16: Final Project Compilation

**Priority:** High  
**Estimated Time:** 4 hours  
**Description:** Compile all project components for submission.

- [x] Organize all UML diagrams
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

- [x] All variable naming anti-patterns in UI, business logic, and vehicle classes have been resolved.
- [x] Widget references and usages in ParkingLotUI are now descriptive and consistent.
- [x] All business logic and vehicle class variables use clear, meaningful names.
- [x] See identified-anti-patterns-after-refactor.md for documentation of resolved issues.

## Project Status Summary

### COMPLETED WORK:

1. **Core Development & Refactoring** (Issues #2-#10): ✅ COMPLETE

   - Baseline analysis, anti-pattern identification and removal
   - Design pattern implementation (Observer, Factory, Strategy, Manager patterns)
   - UML diagram creation and updates
   - Comprehensive testing and validation

2. **Advanced Architecture Design** (Issues #11-#15): ✅ COMPLETE
   - Domain-driven design analysis with bounded contexts
   - Detailed domain modeling with entities, value objects, and aggregates
   - Comprehensive microservices architecture design
   - Complete documentation of patterns and architectural decisions

### REMAINING WORK:

**Issues #16-#17: Final Compilation and Submission**

- Organize all project deliverables
- Create submission package
- Final review against rubric
- Project submission

**Estimated remaining time:** 6 hours total
---

## RUBRIC COMPLIANCE REVIEW

### Score 5 Requirements Analysis:

#### ✅ COMPLETED REQUIREMENTS:

- **Design and code improvements use two relevant design patterns**: ✅
  - Implemented 4 patterns: Observer, Factory, Strategy, Manager
- **Written report is detailed and documents changes and reasons for patterns**: ✅
  - Pattern justification documentation completed
- **Original and redesign represented correctly using UML diagrams**: ✅
  - Both structural and behavioral diagrams for original and redesigned code
- **All bad coding practices identified and improved**: ✅
  - Comprehensive anti-pattern removal documented
- **Appropriate bounded context diagram**: ✅
  - DDD analysis with bounded contexts completed
- **Detailed DDD-based domain models**: ✅
  - Domain entities, value objects, and aggregates modeled
- **High-quality microservices architecture diagram**: ✅
  - Complete microservices design with APIs and databases

#### ⚠️ POTENTIALLY MISSING REQUIREMENTS:

- **Updated code**: ✅ (Assuming code files exist but not shown in current file list)
- **Screenshots**: ❓ NEEDS VERIFICATION
  - Issue #10 marked complete but screenshots not confirmed in submission package
- **Written report**: ❓ NEEDS VERIFICATION
  - Multiple documentation files exist but final consolidated report format unclear

#### 🔍 SUBMISSION FORMAT REQUIREMENTS:

- **Packaged .zip or .rar file**: ❌ NOT YET CREATED
- **All components organized for submission**: ❌ PENDING

### CRITICAL GAPS IDENTIFIED:

1. **Screenshots/Video Evidence** (Issue #10 follow-up needed)

   - Need to verify screenshots of running application are captured
   - Need to confirm they're organized for submission

2. **Final Report Consolidation**

   - Multiple documentation files may need to be consolidated into main report
   - Ensure all written requirements are in proper submission format

3. **Submission Package Creation** (Issues #16-#17)
   - Create organized .zip/.rar file with all components
   - Verify all required files are included and properly formatted

### UPDATED REMAINING WORK:

#### Issue #16A: Verify Screenshot Documentation ⚠️ HIGH PRIORITY

**Estimated Time:** 1 hour

- Confirm screenshots of running application exist
- Verify they demonstrate all functionality
- Organize for submission package

#### Issue #16B: Final Report Organization ⚠️ HIGH PRIORITY

**Estimated Time:** 2 hours

- Consolidate all written documentation into required format
- Ensure pattern justifications are complete
- Verify DDD and microservices documentation meets requirements

#### Issue #16C: Submission Package Creation ⚠️ CRITICAL

**Estimated Time:** 2 hours

- Create organized .zip/.rar file structure
- Include all UML diagrams, code, screenshots, and documentation
- Verify against rubric checklist

#### Issue #17: Final Submission ⚠️ CRITICAL

**Estimated Time:** 1 hour

- Final quality check against Score 5 rubric requirements
- Submit project package

**REVISED ESTIMATED REMAINING TIME:** 6 hours total

### CONFIDENCE LEVEL:

- **Technical Requirements**: 95% Complete (pending screenshot verification)
- **Documentation Requirements**: 90% Complete (pending final organization)
- **Submission Requirements**: 0% Complete (critical path item)

**OVERALL PROJECT STATUS**: Ready for final compilation and submission phase
