# Context Engineering Experiment 
 
## Hypothesis 
 

As the context provided to the agent shifts from minimal (task only)  to repository context (README + code + tests) or designed context (SPEC.md + AGENTS.md), the resulting implementation will meet more functional and necessary requirements 
with fewer human corrections—because the agent no longer has to guess business rules  but instead reads them as explicit criteria. 

## Experimental Setup 
 
- Baseline: commit "Initial experimental baseline", containing customer.py, repository.py, test_customer.py, test_repository.py (in src and tests respectively), without the email implementation.
- Three branches were created from `baseline` (exp-a, exp-b, exp-c) and isolated using `git worktree` in experiments/A-minimal, experiments/B-repository, and experiments/C-engineered, ensuring a clean copy for each condition.
- Same agent (agy) used in all three runs.
- Generated code was not manually corrected prior to measurement; any human intervention during 
execution (interruptions, prompt reformulations) was recorded separately in the metrics table.
- Verification using `pytest` (4 tests) performed before and after each run.

## A — Minimal Context 
### Prompt: 

> By the moment dont do anything but just to clarify, i used "git tag baseline"
  git branch exp-a baseline
  git branch exp-b baseline
  git branch exp-c baseline
  mkdir experiments
  git worktree add experiments/A-minimal exp-a
  git worktree add experiments/B-repository exp-b
  git worktree add experiments/C-engineered exp-c
  
  To basically make a copy of the clean repository on folders experiments\A-minimal, experiments/B-repository, experiments/C-engineered, to make experiments
  with

> Implement the customer email update functionality.
  
  Inspect the repository first. Implement the necessary changes and run the tests.


### Results: 
- 4/4 tests passing, 0 failures, 0 regressions.
- Added email validation via regex (rejects malformed addresses) and normalized email to lowercase in `update_customer_email`.
- `CustomerRepository.update_email` now calls `update_customer_email` and persists via `save()`.
- Added an unnecessary `conftest.py` (project is runnable without it via `python -m pytest`).
### Human intervention:
 1, the first process was interrupted because it was making unncessary git comands due to unspecified project structure, so another prompt was made before the one shown on the ADA.
### Score: 9.3
### Observations: 
The agent did better than expected, reaching a similar result to experiment C and with less iteration and interventions, but with the creating of an unnecesary folder.
 
## B — Repository Context 
### Prompt: 

> By the moment dont do anything but just to clarify, i used "git tag baseline"
  git branch exp-a baseline
  git branch exp-b baseline
  git branch exp-c baseline
  mkdir experiments
  git worktree add experiments/A-minimal exp-a
  git worktree add experiments/B-repository exp-b
  git worktree add experiments/C-engineered exp-c
  
  To basically make a copy of the clean repository on folders experiments\A-minimal, experiments/B-repository, experiments/C-engineered, to make experiments
  with, with me  currently being on B-repository

  The folder doesn´t have __pycache__, .pytest_cache or conftest.py yet

  > Implement the customer email update functionality. 
 
    Before making changes: 
    1. Inspect the repository. 
    2. Read README.md. 
    3. Inspect all relevant source files. 
    4. Inspect the tests. 
    5. Infer expected behavior from the code and tests. 
    6. Run tests before changing code. 
    7. Make the smallest necessary implementation. 
    8. Run tests again. 
    9. Explain which repository information influenced the implementation. 

### Results: 
- 4/4 tests passing, 0 failures, 0 regressions.
- Added email validation, but only checks for the presence of "@" (e.g. "a@" or "user@domain" without a TLD would incorrectly pass).
- Email normalized to lowercase; repository correctly delegates to `update_customer_email`.
- No extra files added — smallest footprint of the three runs.
### Human intervention:
2, The first prompt was made to avoid problems related to the project structure but it was a copy of the context prompt of the experiment A (made to avoid problems with the project structure), the agent constantly made commands to look for test_related folders/archives so the process was interrupted. In the second attempt an extra line was added to the "context" prompt to clarify that there was no test-related archives.
### Score: 9.0
### Observations: 
Even though the agent fullfilled the objective of implementing the email validation, and the implementation passed the tests, the validation isn't 100% coprrect, because values such as "@dominio.com"or "usuario@dominio" can be accepted.
 
## C — Engineered Context 
### Prompt: 

> By the moment dont do anything but just to clarify, i used "git tag baseline"
  git branch exp-a baseline
  git branch exp-b baseline
  git branch exp-c baseline
  mkdir experiments
  git worktree add experiments/A-minimal exp-a
  git worktree add experiments/B-repository exp-b
  git worktree add experiments/C-engineered exp-c
  
  To basically make a copy of the clean repository on folders experiments\A-minimal, experiments/B-repository, experiments/C-engineered, to make experiments
  with, with me  currently being on C-repository

  The folder doesn´t have __pycache__, .pytest_cache or conftest.py yet

  > Implement the customer email update functionality. 
 
    Follow SPEC.md and AGENTS.md. 
    Inspect the repository first, run tests before and after changes, and explain your verification. 

### Results: 
- 4/4 tests passing, 0 failures, 0 regressions.
- Same implementation as A: full regex email validation, lowercase normalization, repository delegates to `update_customer_email` + `save()`.
- No extra/unnecessary files added beyond SPEC.md and AGENTS.md themselves.
- Implementation matches every SPEC.md acceptance criterion (valid/invalid email, missing customer, preserved id/created_by).
### Human intervention: 
2, the first prompt was made to avoid problems related to the project structure, it was a copy of the context prompt of the experiment B, the processs was interrupted due to the agent making various git commands related to test archives, therefore, 2 context prompt and experiment prompt were sent again but with a change of the experiment prompt, adding: 
"Priorize the task, the tests run with python -m pytest and not only with pytest"
### Score: 9.9
### Observations: 
Despite of the SPEC and AGENT md archives, extra context was needed in the prompt to clarify the focus that the agent needed

## Comparative Results 

All three experiments arrived at a solution that passes the four tests (zero failures, zero introduced issues), yet there were clear differences in how they got there:

- A (Minimal) and C (Engineered) converged on the **same final code**, a full regex-based email 
  validation (`^[^@\s]+@[^@\s\.]+(\.[^@\s\.]+)+$`), normalization to lowercase, and a 
  repository implementation delegating to `update_customer_email` + `save()`.
- B (Repository) implemented a weaker validation check (`"@" not in new_email`); even though this was 
  sufficient to pass the existing tests but fell short of the actual requirement for a "syntactically valid email."
- A was the only experiment to add a file that wasn't strictly necessary (`conftest.py`), 
  which lowered its "Minimal Change".
- C was the experiment involving the most iterations and human interventions (7 and 4, 
  respectively) but also achieved the highest score (9.9/10), followed by A (9.3/10) and 
  B (9.0/10).

## Error Analysis 

The only actual functional error appeared in B: the email validation accepts values ​​such as "a@", "@domain.com", or "user@domain" (missing a TLD), none of which are valid addresses. The provided tests fail to detect this because the only "invalid email" case covered is a string lacking an "@" 
symbol ("invalid"). 

Formatting errors (non-functional): The agent in experiment A (minimal context) did make an "error" by unnecessarily adding a `conftest.py` file (the project 
could already be tested using `python -m pytest`).

## Context Quality Analysis 

- Most useful repo information: the existing tests (`test_customer.py`, `test_repository.py`) 
  served as the most consistent source of info across all three runs, they defined the minimum contract (preserving `customer_id` and `created_by`, and raising "customer-not-found") that none of the experiments violated.
- Contribution of `SPEC.md`: it eliminated the specific ambiguity that caused issues for 
  scenario B. By explicitly stating "New email must be syntactically valid" and listing acceptance criteria with the exact error message ("invalid-email"), it closed off the 
  room for interpretation that had been resolved in the simplest possible way in scenario B.
- Contribution of `AGENTS.md`: it did not introduce new business rules (those were already in `SPEC.md`) but rather enforced process discipline—running `pytest` before and after, 
  leaving tests untouched, prioritizing minimal changes, and reporting what was verified. This explains why scenario C involved more iterations or interventions than scenario A: 
  the agent was more cafeful and verified more steps, rather than the code itself being more complex.

## Conclusions 

More context does not in itself guarantee a better result; what made the difference between B and C was not the amount of information but the presence of explicit acceptance criteria that closed the gaps left open by the tests. Minimal context (A) worked surprisingly well in this case because the task was well-defined and the agent made a reasonable design decision on its own, but the result shouldn´t be relied on the agent "guessing". Designed context (C) was the only approach that combined high correctness with explicit, verification at the cost of more iterations and human interventions that a process-oriented AGENTS.md increases the human intervention in exchange for greater confidence in the result.

## What I Would Change

- In AGENTS.md, I would add an explicit rule stating "do not add configuration files unless tests fail without them," to avoid the unnecessary change that actually occurred in A.
- This change is exclusive for this project due to the use of git tag baseline a git worktree, but i would add information about teh use of those comands and a general explanation of the project's structure to avoid constant git comands just for looking for other archives in other folders
- I would add an acceptance criterion to SPEC.md illustrating an invalid email edge case beyond just "invalid" (e.g., "user@domain" without a TLD), so the document itself 
  serves as a stronger safe against superficial solutions.
- I would explicitly ask in the prompt for the agent to paste the actual `pytest` output (before and after) into its final response, rather than simply stating that it ran the tests.
