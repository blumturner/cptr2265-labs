\# Grade Tracker DORA Metrics



\## Deployment Frequency



The Grade Tracker completed 1 successful automated Docker deployment during the initial measurement period in November 2026. This gives the project a starting baseline for tracking future deployments.



\## Lead Time for Changes



The Docker deployment change was committed at 10:00 and successfully deployed at 10:03. This gives the project an approximate lead time of \*\*3 minutes\*\*.



\## Pipeline Improvement



I chose to add pip dependency caching to the unit and integration test jobs. This allows GitHub Actions to reuse downloaded Python packages instead of downloading them every time the pipeline runs. The goal is to reduce test setup time and help changes reach deployment faster.

