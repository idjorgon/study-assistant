---
on: daily
permissions: read-all
safe-outputs:
  create-issue:
    title-prefix: "[news] "
---
Analyze the recent activity in the repository and:
- create an upbeat daily status report about the activity
- provide an agentic task description to improve the project based on the activity.
Create an issue with the report.
