# Project Title

[[_TOC_]]

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
├── README.md  
├── backend-project
│   ├── README.md
│   ├── setup.py   # main app
│   ├── pyproject.toml
│   ├── src
│   │   ├── dummy_server
│   │   │     ├── router
│   │   │     │    ├── routes.py
│   │   │     │    ├── app.py
│   │   │     │    └── __init__.py
│   │   │     └── resources
│   │   │         ├── scatter_data.py
│   │   │         └── __init__.py
│   │   └── __init__.py 
│   ├── data
│   │   ├── dataset_blobs.csv
│   │   ├── dataset_circles.csv
│   │   ├── dataset_moons.csv
│   │   └── generate_data.py    # script to create data
│   └── MANIFEST.in
├── react-frontend
│   ├── README.md
│   ├── package-lock.json
│   ├── package.json
│   ├── src
│   │   ├── App.css
│   │   ├── App.test.tsx
│   │   ├── App.tsx
│   │   ├── Visualization.tsx
│   │   ├── router
│   │   │   ├── resources
│   │   │   │   └── data.ts
│   │   │   └── apiClient.ts
│   │   ├── components
│   │   │   ├── utils.ts
│   │   │   ├── ScatterPlot.tsx
│   │   │   ├── DataChoice.tsx
│   │   │   └── ScatterPlot.css
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
└── Dockerfile
```

## Requirements
Write here all intructions to build the environment and run your code.\
**NOTE:** If we cannot run your code following these requirements we will not be able to evaluate it.

## How to Run
Write here **DETAILED** intructions on how to run your code.\
**NOTE:** If we cannot run your code following these instructions we will not be able to evaluate it.

As an example here are the instructions to run the Dummy Project:
To run the dummy project you have to:
- clone the repository;
- open a new terminal instance;
- move to the folder where the project has been downloaded using the command ```cd```;
- open the folder called "dummy-fullstack-main";
To run the backend
- open the backend folder called "backend-project";
- create a virtual environment using the command ```conda create -n nameOfTheEnvironment```;
- activate the virtual environment run the command ```conda activate nameOfTheEnvironment```;
- install the requirements from the txt file using the command ```pip3 install -r requirements.txt```;
- start the backend with the command ```python3 setup.py run```;
To run the frontend
- open a new terminal instance and once again go to the folder called "dummy-fullstack-main"
- open the frontend folder called "react-frontend";
- start the front end by using the following two commands ```npm install```, ```npm start```;
If all the steps have been successfully executed a new browser window will open automatically.

## Milestones
Document here the major milestones of your code and future planned steps.\
- [x] Milestone 1
  - [x] Completed Sub-task: [Video of our project proposal](https://polybox.ethz.ch/index.php/s/xL8F1FTcjtHjGXG)

- [x] Milestone 2
  - [x] Completed Sub-task: Add some endpoints
  - [x] Completed Sub-task: Create a [Mockup](https://www.figma.com/proto/f18XbpkllZJ8DrXw9BkxT4/AIX-Mockup?node-id=11-177&scaling=scale-down&page-id=0%3A1&starting-point-node-id=4%3A2)

- [ ] Milestone 3
  - [ ] Sub-task: Static dashboard

- [ ] Milestone 4

- [ ] Milestone 5

- [ ] Final Submission


Create a list subtask.\
Open an issue for each subtask. Once you create a subtask, link the corresponding issue.\
Create a merge request (with corresponding branch) from each issue.\
Finally accept the merge request once issue is resolved. Once you complete a task, link the corresponding merge commit.\
Take a look at [Issues and Branches](https://www.youtube.com/watch?v=DSuSBuVYpys) for more details. 

This will help you have a clearer overview of what you are currently doing, track your progress and organise your work among yourselves. Moreover it gives us more insights on your progress.  

## Weekly Summary 
Write here a short summary with weekly progress, including challenges and open questions.\
We will use this to understand what your struggles and where did the weekly effort go to.

#### Week 4 (13.03.23)
Because of our limited domain knowledge, the idea we suggested in our video pitch was quite complex and possibly infeasible. Luckily, we had a very helpful discussion with our TA during the office hour that helped us refine our idea. Currently, we are still working on further refining our idea and improving our backend skills to start implementing our backend next week.
 
#### Week 5 (20.03.23)
We proposed three different project ideas to Javi and decided to go with the second one, creating a dashboard for basketball coaches and data analysts. We made ourselves familiar with the dummy-fullstack repository and started implementing the backend. We created some API endpoints for accessing selected parts of our dataset (boxscore) as well as aggregations.

#### Week 6 (27.03.23)
We accomplished several tasks to advance our project: we developed a visual encoding sketch for the user interface, reached out to Fran to schedule a meeting for feedback on our idea, finalized the API design for front-end and back-end communication, and collaboratively compiled a requirements document that thoroughly details all project features.

#### Week 7 & 8 (03.04.23 & 10.04.23)
We added a help button to our visual encoding sketch and successfully built the front-end based on it. Additionally, we were able to update the back-end from a mock state to a functional state, which allowed us to make actual predictions on real data. Furthermore, we scheduled a meeting with Fran to discuss the project, ensuring that we stay on track and continue moving forward.

## Versioning
Create stable versions of your code each week by using gitlab tags.\
Take a look at [Gitlab Tags](https://docs.gitlab.com/ee/topics/git/tags.html) for more details. 

Then list here the weekly tags. \
We will evaluate your code every week, based on the corresponding version.

Tags:
- Week 1: [Week 1 Tag](https://gitlab.inf.ethz.ch/COURSE-XAI-IML22/dummy-fullstack/-/tags/stable-readme)
- Week 5: [Week 5 Tag](https://gitlab.inf.ethz.ch/course-xai-iml23/b5-winning-in-basketball/-/tags/v1.0)


