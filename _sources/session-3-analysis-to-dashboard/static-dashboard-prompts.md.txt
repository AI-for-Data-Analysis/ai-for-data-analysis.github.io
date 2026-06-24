# Build and Deploy a Static Dashboard: Prompt Notes

These notes collect the prompts and deployment steps for the static dashboard lesson. The lesson follows {doc}`multi-agent-workflows`.

See the GitLab Pages deployment example: [dashboard-starter-with-examples-8c1afe.pages.oit.duke.edu](https://dashboard-starter-with-examples-8c1afe.pages.oit.duke.edu/)

## Create a Dashboard

```text
Create a static dashboard website using plain HTML, CSS, and JavaScript that loads data directly at runtime from dashboard_data/digital_material_type_shares_by_year.csv, do not embed it; use Plotly.js to render exactly one interactive chart and one clearly written interesting finding derived from the CSV data, make the page responsive and visually polished.
```

## Try a New Chart

```text
Change to a stacked bar chart in Plotly.js
```

## Try a New Library

- [Plotly.js](https://plotly.com/javascript/)
- [Apache ECharts](https://echarts.apache.org/examples/en/index.html#chart-type-bar)
- [Leaflet](https://leafletjs.com/examples.html)

```text
Change to Apache Echarts
```

## Try the Bar Race Chart

```text
Change to a bar race chart
```

## Create a Table

```text
Create a table below the chart showing the most popular material type of each year using AG Grid Community 32
```

## Create a New Data Visualization

```text
Create a new data visualization that loads data directly at runtime from dashboard_data/digital_top_sampled_titles_by_year.csv, do not embed it; render exactly one interactive chart and one clearly written interesting finding derived from the CSV data. Adds it below the exisitng ones.
```

## Create a Subagent

```text
Create a repo-local subagent definition for CSV data visualization work, saved under agents/. The subagent should accept a CSV path and output location, inspect the CSV schema first, build a static responsive HTML/CSS/JS visualization, load the CSV directly at runtime with fetch() and never embed data or derived full datasets, use a browser visualization library such as Plotly.js, Apache ECharts, AG Grid Community 32 for tables, or Leaflet for map-style views, render exactly one interactive chart or requested table, compute exactly one clear finding from the runtime-loaded CSV, keep edits scoped to the requested output files, and verify syntax plus confirm the CSV is referenced rather than embedded.
```

## Use Data Viz Accessibility Skill

```text
use $data-viz-accessibility to audit the dashboard
```

## Deploy on GitLab Pages

### Set Up SSH Key

Ensure you have an SSH key added to your Duke OIT GitLab account inside <https://gitlab.oit.duke.edu/>. If you already have one, continue to the check below. If not, do the following:

1. Generate an SSH public/private key pair on your laptop as explained in the [Duke OIT GitLab SSH documentation](https://gitlab.oit.duke.edu/help/user/ssh.md#generate-an-ssh-key-pair).
2. Upload the public half of that key pair to Duke OIT GitLab as explained in the [add an SSH key documentation](https://gitlab.oit.duke.edu/help/user/ssh.md#add-an-ssh-key-to-your-gitlab-account).

To check if you have set up your SSH key successfully, use the following command in your terminal:

```bash
ssh -T git@gitlab.oit.duke.edu
```

You should see the following message, with your NetID filled in for `NETID`:

```text
Welcome to GitLab, @NETID!
```

### Set Up the Repository

1. Move `index.html`, `index.css`, and `dashboard_data/` into a `public/` folder.
2. Create a new empty repository.
3. Fill in the form. Make sure the `README.md` option is not selected.
4. Add a new origin.

```bash
git init --initial-branch=main
git remote add origin2 git@gitlab.oit.duke.edu:ay114/mydashboard.git
git add .
git commit -m "Initial commit"
git push --set-upstream origin2 main
```

5. Refresh the GitLab repository and confirm that you can see your code.

### Set Up GitLab Pages

1. Visit **Settings -> General -> Visibility**.
2. Make sure the GitLab Pages setting is on.
3. Go to **Deploy -> Pages**, create a runner, and copy and paste the following setting:

```yaml
image: alpine:latest

pages:
  stage: deploy
  script:
    - echo "Deploying static assets..."
  artifacts:
    paths:
      - public
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
```

4. Press commit. This step will generate a `.gitlab-ci.yml` file.
5. Check the pipeline.
6. View the pipeline and see it run.
7. When the pipeline succeeds, visit the Pages link.
8. Confirm that the dashboard is deployed.

## Discuss

