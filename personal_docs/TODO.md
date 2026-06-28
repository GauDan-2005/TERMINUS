# ideas generation -

I want to generate several ideas on all topics.
Take reference from these files:
/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/web/terminal-bench-task-creation.md
/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/.cursor/rules/difficulty-calibration.mdc
/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/.cursor/rules/idea-validation.mdc
and should fall in the range below:
1)Automated or AI-generated tasks.
2)Synthetic or spam submissions.
3)Templated content with little to no originality.
4)Tasks copied from previously accepted work with only minor modifications.
5)Low-effort or otherwise non-compliant submissions.
6)All submissions are expected to be original, unique
and language :- Rust go
Also please mention category of the each idea and
Note:- Moving forward, Software Engineering and Debugging category tasks can no longer be submitted.

# choose topic

---

# generate tasks

## data-processing

### bitemporal-asof-correction

- **Task shape:** reverse_engineering
- **Profile:** file_format_serialization (temporal data)
- **Language:** Go
- **Idea:** A bitemporal store (valid-time + transaction-time) answers as-of queries wrong when
  **retroactive valid-time corrections** interact with transaction-time snapshots. Infer the
  temporal semantics from query/result examples and generalize.
- **Hard because:** bitemporal as-of reasoning is notoriously error-prone; corrections vs snapshots
  is the exact trap.
- **Distinct from:** nothing temporal-data in the bank.
- **Real source:** SQL:2011 temporal tables; XTDB / Crux.

Use this idea and generate tasks according to this:
/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/.cursor/rules
/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/personal_docs/docs

---

# generate test cases medium and hard x3

I want you to generate test cases for this task in medium-to-hard range.

---

# difficulty calibiration

Make sure you follow this document and calibrate it as difficult.
/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/.cursor/rules/difficulty-calibration.mdc

---

# check on terminal - run tests - oracle command

Give me orracle command that I can use and test if the tests are running perfectly.
And run the tests yourself as well.

after testing make sure you cleanup any docker images, networks, containers etc.

---

# fix-check-loop

check that tasks passes these tests in here and loop on it until it passes:

- /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/approve_task.py
- /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/run_static_checks.py
- /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/quality_check_adjudicate.py

after testing make sure you cleanup any docker images, networks, containers etc.

---

# model test

Use this for testing

# create zip

create zip for the task based on this file:
/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/validate_submission_zip.py

---

# generate rubrics

generate rubrics for me based on this document:
/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/TASK_PROPOSAL_RUBRIC.md
/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/web/TASK_PROPOSAL_RUBRIC.md

and store it here: /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/personal_docs/rubrics

# time 70-90

# dont change complexity

===

# REVIEW

I got reviews for the task and they need to be altered accordingly.
MAKE SURE YOU DONT CHANGE THE COMPLEXITY OF THE TASK.
reviews: /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/personal_docs/reviews/staged_snapshot
Check all the reviews and only fix the items that require fixing.
Then again test and then zip, ie, follow this:

- task follows the rules: /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/.cursor/rules
- Make sure you follow this document and calibrate it as difficult.
  /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/.cursor/rules/difficulty-calibration.mdc
- check that tasks passes these tests in here and loop on it until it passes:
  -- /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/approve_task.py
  -- /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/run_static_checks.py
  -- /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/quality_check_adjudicate.py
- create zip for the task based on this file:
  /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/validate_submission_zip.py
- after testing make sure you cleanup any docker images, networks, containers etc.

---

Now, since you know about all the things it takes to create a compelte end-to-end zip file and the standards of the task.
Create a document, outlining all the steps, rules and documents to be refered, commands to be used, etc. for all the items we do from creating a task to creating tests, to creating zip and rubriks. all of it.
Place the document here: /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/personal_docs/STEPS_TO_FOLLOW.md

---

Use these references and the announcement.md file to update the workflow file.

Use these files, since there are new changes, so adhere to these files and make relevant changes to the task, then test and rezip as required.

Workflow Proposal file: /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/workflow-prompts.md

References files: /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/personal_docs/references_announcement
New announcement changes: /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS-gaurav/personal_docs/announcement.md

---

stb submissions list --project-id bfe79c33-8ab0-4061-9849-08d3207c9927

---

rev === codex --ask-for-approval never --sandbox danger-full-access resume 019eedfd-0cdd-7010-89de-b1d3cb8f28d2
overlays === cl --resume 58ddf92e-a63b-4321-956b-62cea350e3f1
