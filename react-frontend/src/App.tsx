import { useEffect, useState, useRef } from 'react';
import React from 'react';
import './App.css';
import axiosClient from './router/apiClient'
import Slider from "@material-ui/core/Slider";
import * as d3 from "d3";
import { styled } from "@material-ui/core/styles";

import BASE_URL from './router/apiClient'





const VerticalSlider = styled(Slider)({
  height: "100px !important",
  margin: "auto 0 !important",
  display: "flex",
  flexDirection: "column",
  justifyContent: "space-between",
});

//for some reason defining this doesn't do anything
interface BoxScores {
  AST: number;
}

interface PlayerStatsSliderProps {
  boxScores: BoxScores;
  onSliderChange: (key: keyof BoxScores, value: number) => void;
  onMouseUp: any;
}

const BoxScoreSlider: React.FC<PlayerStatsSliderProps> = ({
  boxScores,
  onSliderChange,
  onMouseUp,
}) => {

  const handleSliderChange = (
    key: keyof BoxScores,
    event: any,
    value: number | number[]
  ) => {
    onSliderChange(key, value as number);
  };

  const minValueMapping: { [key: string]: number } = {
    AST: 0,
    BLK: 0,
    DREB: 0,
    FG3A: 0,
    FG3M: 0,
    FGA: 0,
    FGM: 0,
    FTA: 0,
    FTM: 0,
    OREB: 0,
    PF: 0,
    STL: 0,
    TO: 0,
  };

  const maxValueMapping: { [key: string]: number } = {
    AST: 100,
    BLK: 100,
    DREB: 100,
    FG3A: 100,
    FG3M: 100,
    FGA: 100,
    FGM: 100,
    FTA: 100,
    FTM: 100,
    OREB: 100,
    PF: 100,
    STL: 100,
    TO: 100,
  };

  return (
    <>
      <div className="box">
        <h2>Aggregated box score data</h2>
        <div className='allSliders'>
          {Object.entries(boxScores).map(([key, value]) => (
            <div key={key} className='slidercontainer'>
              <p>{key}</p>
              <VerticalSlider
                orientation="vertical"
                value={value}
                onChange={(event, value) =>
                  handleSliderChange(key as keyof BoxScores, event, value)
                }
                aria-labelledby="continuous-slider"
                min={minValueMapping[key]}
                max={maxValueMapping[key]}
                step={(maxValueMapping[key] - minValueMapping[key]) / 100}
                draggable 
                onChangeCommitted ={() => {onMouseUp()}}
              />
            </div>
          ))}
        </div>
      </div>
    </>
  );
};








interface Team {
  TEAM_ID: number;
  name: string;
}

interface Props {
  ids: Team[];
  onSelection: (selectedId: Team) => void;
  selectedTeam: Team | undefined;
}

const DropdownMenu: React.FC<Props> = ({ ids, onSelection, selectedTeam }) => {

  const handleSelection = (event: React.ChangeEvent<HTMLSelectElement>) => {
    let teams:Team[] = ids;
    let target: string = event.target.value;
    let team:Team = {TEAM_ID: 0, name: "placeholder"};
    // find the team with the matching id
    for (let i = 0; i < teams.length; i++) {
      if (teams[i].name == target) {
        team = teams[i];
      }
    }
    onSelection(team);
  };

  return (
    <select value={selectedTeam?.name ?? ''} onChange={handleSelection}>
      {ids.map((team) => (
        <option key={team.TEAM_ID} value={team.name}>
          {team.name}
        </option>
      ))}
    </select>
  );
};











interface ShapDisplayProps {
  param: string;
}

const ShapDisplay: React.FC<ShapDisplayProps> = ({ param }) => {

  return (
    <>
      <div className="box" id="shapbox">
        <h2>Shap values</h2>
        <iframe id="shapframe" srcDoc={param}></iframe>
      </div>
    </>
  );
};








interface TeamSelectorProps {
  title: string;
  availableTeams: Team[];
  selectedTeam: Team;
  setSelectedTeam: (selectedId: Team) => void;
}

const TeamSelector: React.FC<TeamSelectorProps> = ({ title, availableTeams, selectedTeam, setSelectedTeam }) => {
  const BASE_URL = process.env.NODE_ENV==="production"? `http://be.${window.location.hostname}/api/v1`:"http://localhost:8000/"

  return (
    <>
      <div className="box">
        <h1>{title}</h1>
        <img id="team_logo" src={BASE_URL + "api/logo/" + selectedTeam.TEAM_ID} alt="team logo" />
        <DropdownMenu ids={availableTeams} onSelection={setSelectedTeam} selectedTeam={selectedTeam} />
      </div>
    </>
  );
};









interface WinChanceDisplayProps {
  probability: number;
}

const WinChanceDisplay: React.FC<WinChanceDisplayProps> = ({ probability }) => {

  return (
    <>
      <div className="box">
        <h2>Winning probability</h2>
        <p>{probability*100}%</p>
      </div>
    </>
  );
};







interface Point {
  x_coord: number;
  y_coord: number;
  cluster: number;
  hover_details: string;
}

interface ScatterplotProps {
  points: Point[];
}


let addedPoints:boolean = false;
const Scatterplot: React.FC<ScatterplotProps> = ({ points }) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const xScale = d3.scaleLinear().domain([-5, 5]).range([10, 90]);
  const yScale = d3.scaleLinear().domain([-5, 5]).range([10, 90]);
  const colorMap: { [key: number]: string } = {
    0: "red",
    1: "blue",
    2: "green",
    3: "orange",
    4: "purple",
    5: "yellow",
  };
  

  useEffect(() => {
    if(points.length === 0){
      return;
    }
    const svg = d3.select(svgRef.current);

    if(!addedPoints){
      addedPoints = true;
      // Add points to the scatterplot
      console.log("adding points");
      svg
        .selectAll("circle")
        .data(points)
        .enter()
        .append("circle")
        .attr("cx", (d) => xScale(d.x_coord))
        .attr("cy", (d) => yScale(d.y_coord))
        .attr("r", 2)
        .attr("fill", (d) => colorMap[d===points[0] ? 4 : (d===points[1] ? 5 : d.cluster)])
        .on("mouseover", function (event, d) {
          // Show hover details on mouseover
          d3.select("#tooltip")
            .style("opacity", 1)
            .html(`${JSON.stringify(d).replaceAll("{", "").replaceAll("}", "").replaceAll(",", "<br>")}`)
            .style("left", `${event.pageX+10}px`)
            .style("top", `${event.pageY}px`);
        })
        .on("mousemove", function (event) {
          // Move hover details on mousemove
          d3.select("#tooltip")
            .style("left", `${event.pageX+10}px`)
            .style("top", `${event.pageY}px`);   
        })
        .on("mouseout", function (event, d) {
          // Hide hover details on mouseout
          d3.select("#tooltip").style("opacity", 0).html("");
        });
    } else {
      // Update point locations
      console.log("updating points");
      svg
      .selectAll("circle")
      .data(points)
      .transition()
      .duration(1000)
      .attr("cx", (d) => xScale(d.x_coord))
      .attr("cy", (d) => yScale(d.y_coord))
    }





  }, [points]);


  return (
    <>
      <div className="box">
        <h2>Tactical clustering</h2>
        <div id="tooltip"/>
        <svg ref={svgRef} viewBox="0 0 100 100" id="clustering"></svg>
      </div>
    </>
  );
};







let scrolling = false;


function App() {

  function loadData(url: string): Promise<any | undefined> {
    console.log(url)
    const promise = axiosClient.get<any>(url)
    return promise
      .then((res) => {
        if (res.status !== 204) {
          return res.data;
        }
        return undefined;
      })
      .catch((err) => {
        console.error(err);
        throw err;
      });
  }



  const [availableTeams, setAvailableTeams] = useState<any>([{TEAM_ID: 1610612737, name: "Atlanta Hawks"}]);
  const [selectedTeamLeft, setSelectedTeamLeft] = useState<Team>({TEAM_ID: 1610612737, name: "Atlanta Hawks"});
  const [selectedTeamRight, setSelectedTeamRight] = useState<Team>({TEAM_ID: 1610612737, name: "Atlanta Hawks"});
  const [boxScoresLeft, setBoxScoresLeft] = useState<any>({});
  const [boxScoresRight, setBoxScoresRight] = useState<any>({});
  const [shap, setShap] = useState<string>("");
  const [probabilityLeft, setProbabilityLeft] = useState<number>(0.5);
  const [points, setPoints] = useState<any>([]);
  


  // load list of teams when page is loaded
  useEffect(() => {
    loadData(`api/teams`).then(data => {
      // console.log(data);
      setAvailableTeams(data);
    });
    handleSelectionLeft({TEAM_ID: 1610612737, name: "Atlanta Hawks"});
    handleSelectionRight({TEAM_ID: 1610612737, name: "Atlanta Hawks"});
  }, []);



  const handleSelectionLeft = (selectedTeam: Team) => {
    setSelectedTeamLeft(selectedTeam);
    loadData(`api/boxscore/${selectedTeam.TEAM_ID}-1`).then(data => {
      // console.log(data[0]);
      setBoxScoresLeft(data[0]);
    });
  };

  const handleSelectionRight = (selectedTeam: Team) => {
    setSelectedTeamRight(selectedTeam);
    loadData(`api/boxscore/${selectedTeam.TEAM_ID}-0`).then(data => {
      // console.log(data[0]);
      setBoxScoresRight(data[0]);
    });
  };

  const handleSliderChangeLeft = (key: keyof BoxScores, value: number) => {
    var copy = {...boxScoresLeft};
    copy[key] = value;
    setBoxScoresLeft(copy);
    scrolling = true;
  };

  const handleSliderChangeRight = (key: keyof BoxScores, value: number) => {
    // console.log(key, value,"right");
    var copy = {...boxScoresRight};
    copy[key] = value;
    setBoxScoresRight(copy);
    // console.log(copy);
    scrolling = true;
  };

  const onSliderMouseUp = (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
    console.log("mouse up");
    scrolling = false;
    updateEverything();
  };

  useEffect(() => {
    if(boxScoresLeft["AST"] && boxScoresRight["AST"])
      updateEverything();
  }, [boxScoresLeft, boxScoresRight]);

  //this function uses the 2 saved box scores to updates the shap values, winning probability and tactical clustering points
  // <float:AST_home>-<float:BLK_home>-<float:DREB_home>-<float:FG3A_home>-<float:FG3M_home>-<float:FGA_home>-<float:FGM_home>-<float:FTA_home>-<float:FTM_home>-<float:OREB_home>-<float:PF_home>-<float:STL_home>-<float:TO_home>_<float:AST_away>-<float:BLK_away>-<float:DREB_away>-<float:FG3A_away>-<float:FG3M_away>-<float:FGA_away>-<float:FGM_away>-<float:FTA_away>-<float:FTM_away>-<float:OREB_away>-<float:PF_away>-<float:STL_away>-<float:TO_away>")
  const updateEverything = () => {
    if(scrolling)return;
    console.log("updateEverything")
 
    let h = boxScoresLeft;
    let a = boxScoresRight;
    //convert box scores to string
    let s: string = "";
    for(let key in h){
      s += h[key].toFixed(4) + "-";
    }
    s = s.slice(0, -1);
    s += "_";
    for(let key in a){
      s += a[key].toFixed(4) + "-";
    }
    s = s.slice(0, -1);


    loadData(`api/shap/${s}`).then(data => {
      // console.log(data);
      setShap(data);
    });


    loadData(`api/prediction/${s}`).then(data => {
      // console.log(data);
      setProbabilityLeft(data["winning_odds_home"]);
    });
    loadData(`api/clustering/${s}`).then(data => {
      // console.log(data);
      // console.log("COORDINATE OF FIRST POINT:" + data[0]["x_coord"] + " " + data[0]["y_coord"]);
      setPoints(data);
    });
  }




  return (
    <div className="App">
      <header className="App-header"> Winning odds predictions
      </header>
      <div className="left container">
        <TeamSelector title='HOME' availableTeams={availableTeams} selectedTeam={selectedTeamLeft} setSelectedTeam={handleSelectionLeft}/>
        <BoxScoreSlider boxScores={boxScoresLeft} onSliderChange={handleSliderChangeLeft} onMouseUp={onSliderMouseUp}/>
        <WinChanceDisplay probability={probabilityLeft}/>   
      </div>
      <div className="right container">
        <TeamSelector title='AWAY' availableTeams={availableTeams} selectedTeam={selectedTeamRight} setSelectedTeam={handleSelectionRight}/>
        <BoxScoreSlider boxScores={boxScoresRight} onSliderChange={handleSliderChangeRight} onMouseUp={onSliderMouseUp}/>
        <WinChanceDisplay probability={1-probabilityLeft}/>      
      </div>
      <div className="center container">
        <ShapDisplay param={shap}/>     
        <Scatterplot points={points}/>
      </div>

    </div>
  )
}

export default App;
