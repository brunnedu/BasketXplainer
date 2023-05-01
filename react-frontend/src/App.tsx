import { useEffect, useState, useRef } from 'react';
import React from 'react';
import './App.css';
import axiosClient from './router/apiClient'
import Popup from './components/Popup';
import ParallelCoordinates from './components/ParallelCoordinates';
import Slider from "@material-ui/core/Slider";
import * as d3 from "d3";
import { styled } from "@material-ui/core/styles";
import BASE_URL from './router/apiClient'
import { Steps, Hints } from "intro.js-react";
import "intro.js/introjs.css";





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
  boxScoreBoundaries: any;
}

const BoxScoreSlider: React.FC<PlayerStatsSliderProps> = ({
  boxScores,
  onSliderChange,
  onMouseUp,
  boxScoreBoundaries,
}) => {

  const handleSliderChange = (
    key: keyof BoxScores,
    event: any,
    value: number | number[]
  ) => {
    onSliderChange(key, value as number);
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
                min={boxScoreBoundaries[key][0]}
                max={boxScoreBoundaries[key][1]}
                step={(boxScoreBoundaries[key][1] - boxScoreBoundaries[key][0]) / 100}
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
  title: string;
}

const DropdownMenu: React.FC<Props> = ({ ids, onSelection, selectedTeam, title }) => {

  const handleSelection = (event: React.ChangeEvent<HTMLSelectElement>) => {
    // console.log("handleSelection");
    let teams:Team[] = ids;
    let target: string = event.target.value;
    let team:Team = {TEAM_ID: 0, name: "Unknown Team"};
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
        <option key={team.TEAM_ID + "_" + title} value={team.name}>
          {team.name}
        </option>
      ))}
    </select>
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
      <div className="box teamselector">
        <h1>{title}</h1>
        {/* {selectedTeam.TEAM_ID !== 0 && <img className="team_logo" src={BASE_URL + "api/logo/" + selectedTeam.TEAM_ID} alt="team logo" />} */}
        <img className="team_logo" src={selectedTeam.TEAM_ID !== 0 ? BASE_URL + "api/logo/" + selectedTeam.TEAM_ID : "https://i.imgur.com/fStsxCy.png"} alt="team logo" />
        <DropdownMenu ids={availableTeams} onSelection={setSelectedTeam} selectedTeam={selectedTeam} title={title} />
      </div>
    </>
  );
};











interface ShapDisplayProps {
  param: string;
}

const ShapDisplay: React.FC<ShapDisplayProps> = ({ param }) => {

  return (
    <>
      <div className="box" id="shapbox">
        <h2>Feature importance</h2>
        <iframe id="shapframe" srcDoc={param}></iframe>
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
  is_home: number;
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
        .attr("fill", (d) => colorMap[d===points[0] ? 4 : (d===points[1] ? 5 : (d.is_home ? 1 : 2))])
        .on("mouseover", function (event, d) {
          // Show hover details on mouseover
          d3.select("#tooltip")
            .style("opacity", 1)
            .html(`${JSON.stringify(d).replaceAll("{", "").replaceAll("}", "").replaceAll(",", "<br>").replaceAll("\"", "")}`)
            .style("left", `${event.pageX+10}px`)
            .style("top", `${event.pageY-1100}px`);
        })
        .on("mousemove", function (event) {
          // Move hover details on mousemove
          d3.select("#tooltip")
            .style("left", `${event.pageX+10}px`)
            .style("top", `${event.pageY-1100}px`);   
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










// args are an array of these objects:
// AST_away : 24 AST_home : 28 Away Team : "Boston Celtics" FG3_PCT_away : 0.268 FG3_PCT_home : 0.351 FG_PCT_away : 0.44 FG_PCT_home : 0.506 FT_PCT_away : 0.824 FT_PCT_home : 0.833 GAME_DATE_EST : "2021-11-17" GAME_ID : 22100215 GAME_STATUS_TEXT : "Final" Game Date : "17. November 2021" HOME_TEAM_ID : 1610612737 HOME_TEAM_WINS : 1 Home Team : "Atlanta Hawks" PTS_away : 99 PTS_home : 110 REB_away : 42 REB_home : 40 SEASON : 2021 Score : "110-99" TEAM_ID_away : 1610612738 TEAM_ID_home : 1610612737 VISITOR_TEAM_ID : 1610612738 Winning Team : "Home (Atlanta Hawks)" date : "Wed, 17 Nov 2021 00:00:00 GMT"

// interface SimilarMatchupsProps {
//   away_team: string;
//   game_date: string;
//   home_team: string;
//   score: string;
//   winning_team: string;
// }

interface SimilarMatchupsDisplayProps {
  matchups: any[];
  selectedTeamLeft: Team;
  selectedTeamRight: Team;
}

const SimilarMatchupsDisplay: React.FC<SimilarMatchupsDisplayProps> = ({ matchups, selectedTeamLeft, selectedTeamRight }) => {
  const BASE_URL = process.env.NODE_ENV==="production"? `http://be.${window.location.hostname}/api/v1`:"http://localhost:8000/"
  console.log(matchups)

  return (
    <>
      <div className="box">
        <h2>Similar matchups</h2>
        {/* {matchup["Game Date"]}: <img className="small_team_logo" src={BASE_URL + "api/logo/" + selectedTeamLeft.TEAM_ID} alt="team logo" /> {matchup["Score"]} <img className="small_team_logo" src={BASE_URL + "api/logo/" + selectedTeamRight.TEAM_ID} alt="team logo" /> */}
        {/* For each matchup, display the date, the score and the 2 team logos on each side of the score  */}
        <table>
          <tbody>
            {matchups.map((matchup) => (
              <tr className="matchup" key={matchup["Game Date"] + " " + matchup["Score"]}>
                <td>{matchup["Game Date"]}</td>
                <td>{matchup["Home Team"]}<img className="small_team_logo" src={BASE_URL + "api/logo/" + matchup["TEAM_ID_home"]} alt="team logo" /></td>
                <td>{matchup["Score"]}</td>
                <td><img className="small_team_logo" src={BASE_URL + "api/logo/" + matchup["TEAM_ID_away"]} alt="team logo" />{matchup["Away Team"]}</td>
              </tr>
            ))}
          </tbody>
        </table>

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



  const [availableTeams, setAvailableTeams] = useState<any>([{TEAM_ID: 0, name: "Unknown Team"}]);
  const [selectedTeamLeft, setSelectedTeamLeft] = useState<Team>({TEAM_ID: 0, name: "Unknown Team"});
  const [selectedTeamRight, setSelectedTeamRight] = useState<Team>({TEAM_ID: 0, name: "Unknown Team"});

  const [boxScoresLeft, setBoxScoresLeft] = useState<any>({});
  const [boxScoresRight, setBoxScoresRight] = useState<any>({});
  const [boxScoreBoundaries, setBoxScoreBoundaries] = useState<any>({});

  const [shap, setShap] = useState<string>("");
  const [probabilityLeft, setProbabilityLeft] = useState<number>(0.5);
  const [points, setPoints] = useState<any>([]);

  const [parallelCoordinatesDataHome, setParallelCoordinatesDataHome] = useState<string>("");
  const [parallelCoordinatesDataAway, setParallelCoordinatesDataAway] = useState<string>("");
  const [SimilarMatchups, setSimilarMatchups] = useState<any>([]);

  const [DisplayRestOfApp, setDisplayRestOfApp] = useState<boolean>(false);

  //User tutorial stuff
  // const [ShowTeamSelectorPopup, setDisplayRestOfApp] = useState<boolean>(false);
  

  


  // load list of teams when page is loaded
  useEffect(() => {
    loadData(`api/boxscore/bounds`).then(data => {
      // console.log(data);
      setBoxScoreBoundaries(data)
      loadData(`api/boxscores/home`).then(data => {
        // console.log(data);
        setParallelCoordinatesDataHome(data);
      });
      loadData(`api/boxscores/away`).then(data => {
        // console.log(data);
        setParallelCoordinatesDataAway(data);
      });
      loadData(`api/teams`).then(data => {
        // console.log(data);
        data = data.concat({TEAM_ID: 0, name: "Unknown Team"})
        setAvailableTeams(data);
        // handleSelectionLeft({TEAM_ID: 1610612737, name: "Atlanta Hawks"})
        // handleSelectionRight({TEAM_ID: 1610612738, name: 'Boston Celtics'});
        // setSelectedTeamLeft({TEAM_ID: 0, name: "Unknown Team"});
      });
    });
  }, []);



  const handleSelectionLeft = (selectedTeam: Team) => {
    setSelectedTeamLeft(selectedTeam);
    loadData(`api/boxscore/${selectedTeam.TEAM_ID}-1`).then(data => {
      // console.log(data[0]);
      setBoxScoresLeft(data[0]);
    });
    if(selectedTeamRight.TEAM_ID !== 0 && selectedTeam.TEAM_ID !== 0){
      console.log("displaying rest of app");
      setDisplayRestOfApp(true);
    }
  };

  const handleSelectionRight = (selectedTeam: Team) => {
    setSelectedTeamRight(selectedTeam);
    loadData(`api/boxscore/${selectedTeam.TEAM_ID}-0`).then(data => {
      // console.log(data[0]);
      setBoxScoresRight(data[0]);
    });
    if(selectedTeamLeft.TEAM_ID !== 0 && selectedTeam.TEAM_ID !== 0){
      console.log("displaying rest of app");
      setDisplayRestOfApp(true);
    }
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
    loadData(`api/similar_games/${s}`).then(data => {
      console.log(data);
      setSimilarMatchups(data);
    });
  }




  return (
    <div className="App">
      <header className="App-header"> Winning odds predictions
      </header>
      <div className="left container">
        <TeamSelector title='HOME' availableTeams={availableTeams} selectedTeam={selectedTeamLeft} setSelectedTeam={handleSelectionLeft}/>
        {DisplayRestOfApp && <>
          <BoxScoreSlider boxScores={boxScoresLeft} onSliderChange={handleSliderChangeLeft} onMouseUp={onSliderMouseUp} boxScoreBoundaries={boxScoreBoundaries} />
          <WinChanceDisplay probability={probabilityLeft} /><div className="box">
            <h2>Parallel Coordinates</h2>
            <ParallelCoordinates data_orig={parallelCoordinatesDataHome} limits={boxScoreBoundaries}></ParallelCoordinates>
          </div>
        </>}

      </div>
      <div className="right container">
        <TeamSelector title='AWAY' availableTeams={availableTeams} selectedTeam={selectedTeamRight} setSelectedTeam={handleSelectionRight}/>
        <Popup text="This is the text that will be displayed in the popup" />
        {DisplayRestOfApp && <>
          <BoxScoreSlider boxScores={boxScoresRight} onSliderChange={handleSliderChangeRight} onMouseUp={onSliderMouseUp} boxScoreBoundaries={boxScoreBoundaries}/>
          <WinChanceDisplay probability={1-probabilityLeft}/>   
          <div className="box">
            <h2>Parallel Coordinates</h2>
            <ParallelCoordinates data_orig={parallelCoordinatesDataAway} limits={boxScoreBoundaries}></ParallelCoordinates>
          </div>
        </>}   
      </div>
      {DisplayRestOfApp && <>
        <div className="center container">
          <SimilarMatchupsDisplay matchups={SimilarMatchups} selectedTeamLeft={selectedTeamLeft} selectedTeamRight={selectedTeamRight}/>
          <ShapDisplay param={shap}/>     
          <Scatterplot points={points}/>
        </div>
      </>} 
    </div>
  )
}

export default App;
