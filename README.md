# BasketXplainer

## Team Members
1. Dustin Brunner
2. Jonathan Koch
3. Liule Yang
4. Timothé Laborie

## Contribution Statement

Every team member contributed approximately equally to the project. Below we list the contributions of each member in descending order of importance:

- Dustin Brunner: Backend, Research, Report, Frontend
- Jonathan Koch: Wireframe, Design, Backend, Tutorial, Report
- Liule Yang: Backend, Research, Report
- Timothé Laborie: Main contributor to frontend (Implementation and Styling)

## Deployment Link

Try out our deployed dashboard [here](http://b5-winning-in-basketball.course-xai-iml23.isginf.ch/)

## How to Run Locally

### Requirements
In this project we are using LightGBM for the ML pipeline. This package can be a bit tricky to install depending on the OS. If the usual installation steps as described below fail, more information for troubleshooting can be found [here](https://lightgbm.readthedocs.io/en/latest/Installation-Guide.html).

### Installation Instructions

To run this project you have to:
- clone the repository;
- open a new terminal instance;
- move to the folder where the project has been downloaded using the command ```cd```;
- open the folder called "b5-winning-in-basketball";
- create a virtual environment from the environment.yml file using the command ```conda env create --file environment.yml```;
- activate the virtual environment run the command ```conda activate b5-winning-in-basketball```;
To run the backend
- open the backend folder called "backend-project";
- install the requirements using the command ```pip install .```. If you plan on editing the requirements, you may want to use the command ```pip install -e .```;
- start the backend with the command ```start-server```;
To run the frontend
- open a new terminal instance and once again go to the folder called "b5-winning-in-basketball"
- open the frontend folder called "react-frontend";
- start the front end by using the following two commands ```npm install```, ```npm start```;
If all the steps have been successfully executed a new browser window will open automatically.

## Project Description 
The goal of our project is to create an interactive dashboard that allows basketball coaches/analysts to determine the most important factors for predicting the winning odds of a given matchup.

### Users
- Basketball Data Analysts (specifically Fran Camba Rodriguez of the Obradoiro CAB team) 
- Basketball Coaches

### Datasets
Add here all used datasets.\
Document here where to find the data and how to download it.
- [NBA Kaggle Dataset](https://www.kaggle.com/datasets/nathanlauga/nba-games) 

### Tasks
Define all the tasks you want your dashboard solve.
- Determine feature importance for predicting winning odds
- Modifying boxscore data for interventional predictions (what-if analysis)
- Positioning teams in comparison to other teams according to defensive and offensive performance

### Dashboard Structure

#### Components
- Introductory Tutorial
  - Overlay when first launching the app
  - Help button in the corner
- Team Selector
  - Team logos
  - Scrollable dropdown (search)
- Interactive Box Score Statistics
  - Parallel Coordinates Plot (adjustable ordering)
  - Adjust Box Scores by sliding directly in plot (direct manipulation)
  - Provide some realistic constraints for the box score values
- Winning Odds Prediction
  - If not dynamically updated, indicate the change in winning odds after recalculating
- Explainability Plot
  - SHAP force plot to better comprehend prediction of model
  - Indicate which features contribute to increasing / decreasing the winning odds of the home team
- League Overview
  - Plot the different teams in the league based on offensive and defensive capabilities
  - On-Hover details

- - -
## Folder Structure
Specify here the structure of you code and comment what the most important files contain

``` bash
├── README.md  # project readme
├── backend-project
│   ├── README.md
│   ├── setup.py   # main app
│   ├── pyproject.toml
│   ├── src
│   │   ├── dummy_server
│   │   │     ├── router
│   │   │     │    ├── routes.py  # api endpoint routes
│   │   │     │    ├── app.py
│   │   │     │    └── __init__.py
│   │   │     └── resources
│   │   │         ├── clustering.py  # league overview endpoint
│   │   │         ├── explainability.py  # feature importance endpoint
│   │   │         ├── games_data.py  # box score endpoints
│   │   │         ├── prediction.py  # prediction endpoint
│   │   │         ├── utils.py  # utility functions
│   │   │         └── __init__.py
│   │   └── __init__.py 
│   ├── data
│   │   ├── precomputed  # precomputed models & box scores
│   │   ├── team_logos  # NBA team logos
│   │   ├── dataset_games.csv  # NBA Kaggle datasets
│   │   ├── dataset_games_details.csv
│   │   ├── dataset_players.csv
│   │   ├── dataset_ranking.csv
│   │   └── generate_teams.csv
│   └── MANIFEST.in
├── dev_notebooks  # development notebooks (including model training)
├── react-frontend
│   ├── README.md
│   ├── Dockerfile
│   ├── package-lock.json
│   ├── package.json
│   ├── src
│   │   ├── App.css
│   │   ├── App.test.tsx
│   │   ├── App.tsx  # main frontend code
│   │   ├── router
│   │   │   ├── resources
│   │   │   │   └── data.ts
│   │   │   └── apiClient.ts
│   │   ├── components
│   │   │   ├── utils.ts
│   │   │   ├── ParallelCoordinates.tsx  # parallel coordinates component
│   │   ├── index.css
│   │   ├── index.tsx
│   │   ├── logo.svg
│   │   ├── react-app-env.d.ts
│   │   ├── reportWebVitals.ts
│   │   ├── setupTests.ts
│   │   └── types
│   │       ├── margin.ts
│   │       └── data.ts
│   ├── tsconfig.json
│   └── public
│        ├── robot.txt
│        ├── manifest.json
│        ├── logo512.png
│        ├── logo192.png
│        ├── index.html
│        └── favicon.ico
├── environment.yml  # package dependencies
└── report.pdf  # project report

```

## Versioning
Create stable versions of your code each week by using gitlab tags.\
Take a look at [Gitlab Tags](https://docs.gitlab.com/ee/topics/git/tags.html) for more details. 

Then list here the weekly tags. \
We will evaluate your code every week, based on the corresponding version.

Tags:
- Week 1: [Week 1 Tag](https://gitlab.inf.ethz.ch/COURSE-XAI-IML22/dummy-fullstack/-/tags/stable-readme)
- Week 5: [Week 5 Tag](https://gitlab.inf.ethz.ch/course-xai-iml23/b5-winning-in-basketball/-/tags/v1.0)


