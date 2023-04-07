import { useEffect, useState, useRef } from 'react';
import React from 'react';
import './App.css';
import axiosClient from './router/apiClient'
import Slider from "@material-ui/core/Slider";
import * as d3 from "d3";
import { styled } from "@material-ui/core/styles";






const VerticalSlider = styled(Slider)({
  height: "100px !important",
  margin: "auto 0 !important",
  display: "flex",
  flexDirection: "column",
  justifyContent: "space-between",
});

interface BoxScores {
  AST: number;
  FG3_PCT: number;
  FG_PCT: number;
  FT_PCT: number;
  PTS: number;
  REB: number;
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
    FG3_PCT: 0,
    FG_PCT: 0,
    FT_PCT: 0,
    PTS: 0,
    REB: 0,
  };

  const maxValueMapping: { [key: string]: number } = {
    AST: 40,
    FG3_PCT: 1,
    FG_PCT: 1,
    FT_PCT: 1,
    PTS: 200,
    REB: 100,
  };

  return (
    <>
      <div className="box">
        <h2>Aggregated box score data</h2>
        <div style={{ display: "flex", alignItems: "center" }}>
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
                onChangeCommitted ={() => {onMouseUp();console.log("drag end")}}
              />
            </div>
          ))}
        </div>
      </div>
    </>
  );
};










interface Props {
  ids: number[];
  onSelection: (selectedId: number) => void;
}

const DropdownMenu: React.FC<Props> = ({ ids, onSelection }) => {
  const [selectedId, setSelectedId] = useState<number | null>(null);

  const handleSelection = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const id = parseInt(event.target.value);
    setSelectedId(id);
    onSelection(id);
  };

  return (
    <select value={selectedId ?? ''} onChange={handleSelection}>
      {ids.map((id) => (
        <option key={id} value={id}>
          {id}
        </option>
      ))}
    </select>
  );
};









interface ShapValues {
  "2FG%": number;
  "3FG%": number;
  "Assists": number;
  "Average_score": number;
  "Difference": number;
  "Rebounds": number;
}

interface ShapDisplayProps {
  values: ShapValues;
}

const ShapDisplay: React.FC<ShapDisplayProps> = ({ values }) => {

  return (
    <>
      <div className="box">
        <h2>Shap values</h2>
        {Object.entries(values).map(([key, value]) => (
          <div key={key}>
            <p>{key}:{value}</p>
          </div>
        ))}
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
  cluster_index: number;
  hover_details: string;
}

interface ScatterplotProps {
  points: Point[];
}

const colorMap: { [key: number]: string } = {
  0: "red",
  1: "blue",
  2: "green",
  3: "orange",
  4: "purple",
};

const Scatterplot: React.FC<ScatterplotProps> = ({ points }) => {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    const svg = d3.select(svgRef.current);

    // Create scales for x and y coordinates
    const xScale = d3.scaleLinear().domain([0, 1]).range([0, 100]);
    const yScale = d3.scaleLinear().domain([0, 1]).range([0, 100]);

    // Add points to the scatterplot
    svg
      .selectAll("circle")
      .data(points)
      .enter()
      .append("circle")
      .attr("cx", (d) => xScale(d.x_coord))
      .attr("cy", (d) => yScale(d.y_coord))
      .attr("r", 2)
      .attr("fill", (d) => colorMap[d.cluster_index])
      .on("mouseover", function (event, d) {
        // Show hover details on mouseover
        d3.select("#tooltip")
          .style("opacity", 1)
          .html(`<div>${d.hover_details}</div>`)
          .style("left", `${event.pageX+10}px`)
          .style("top", `${event.pageY}px`);
      })
      .on("mousemove", function (event) {

      })
      .on("mouseout", function (event, d) {
        // Hide hover details on mouseout
        d3.select("#tooltip").style("opacity", 0);
      });
  }, [points]);

  return (
    <>
      <div className="box">
        <h2>Tactical clustering</h2>
        <svg ref={svgRef} viewBox="0 0 100 100" width="100%"></svg>
      </div>
    </>
  );
};










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



  const ids = [
    1610612737,
    1610612738,
    1610612740,
  ];
  const [selectedTeamLeft, setSelectedTeamLeft] = useState<Number>(1610612737);
  const [selectedTeamRight, setSelectedTeamRight] = useState<Number>(1610612738);
  const [boxScoresLeft, setBoxScoresLeft] = useState<any>({});
  const [boxScoresRight, setBoxScoresRight] = useState<any>({});
  const [shapRight, setShapRight] = useState<any>({});
  const [shapLeft, setShapLeft] = useState<any>({});
  const [probabilityLeft, setProbabilityLeft] = useState<number>(0.4);
  const [pointsLeft, setPointsLeft] = useState<any>([]);
  const [pointsRight, setPointsRight] = useState<any>([]);


  // load list of teams when page is loaded
  useEffect(() => {
    // loadData(`api/teams/`).then(data => {
    //   console.log(data);
    // });
    handleSelectionLeft(1610612737);
    handleSelectionRight(1610612738);
  }, []);




  const handleSelectionLeft = (selectedId: number) => {
    setSelectedTeamLeft(selectedId);
    loadData(`api/teams/${selectedId}`).then(data => {
      console.log(data);
      setBoxScoresLeft(data[0]);
    });
    updateEverything();
  };

  const handleSelectionRight = (selectedId: number) => {
    setSelectedTeamRight(selectedId);
    loadData(`api/teams/${selectedId}`).then(data => {
      console.log(data);
      setBoxScoresRight(data[0]);
    });
    updateEverything();
  };

  const handleSliderChangeLeft = (key: keyof BoxScores, value: number) => {
    var copy = {...boxScoresLeft};
    copy[key] = value;
    setBoxScoresLeft(copy);
    // updateEverything();
  };

  const handleSliderChangeRight = (key: keyof BoxScores, value: number) => {
    // console.log(key, value,"right");
    var copy = {...boxScoresRight};
    copy[key] = value;
    setBoxScoresRight(copy);
    // console.log(copy);
    // updateEverything();
  };

  const onSliderMouseUp = (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
    console.log("mouse up");
    updateEverything();
  };

  //this function updates the shap values, winning probability and tactical clustering points
  const updateEverything = () => {
    console.log("updateEverything")
    loadData(`api/prediction/xai/${selectedTeamLeft}-${selectedTeamRight}`).then(data => {
      console.log(data);
      setShapLeft(data);
      setShapRight(data);
    });
    loadData(`api/prediction/${selectedTeamLeft}-${selectedTeamRight}`).then(data => {
      console.log(data);
      setProbabilityLeft(data);
    });
    loadData(`api/clustering`).then(data => {
      console.log(data);
      setPointsLeft(data);
      setPointsRight(data);
    });
  }




  return (
    <div className="App">
      <header className="App-header"> Winning odds predictions
      </header>
      <div className="left container">
        <div className="box">
          <h1>HOME</h1>
          <DropdownMenu ids={ids} onSelection={handleSelectionLeft} />
        </div>
        <BoxScoreSlider boxScores={boxScoresLeft} onSliderChange={handleSliderChangeLeft} onMouseUp={onSliderMouseUp}/>
        <ShapDisplay values={shapLeft}/>
        <WinChanceDisplay probability={probabilityLeft}/>
        <Scatterplot points={pointsLeft}/>
      </div>
      <div className="right container">
        <div className="box">
          <h1>AWAY</h1>
          <DropdownMenu ids={ids} onSelection={handleSelectionRight} />
        </div>
        <BoxScoreSlider boxScores={boxScoresRight} onSliderChange={handleSliderChangeRight} onMouseUp={onSliderMouseUp}/>
        <ShapDisplay values={shapRight}/>
        <WinChanceDisplay probability={1-probabilityLeft}/>
        <Scatterplot points={pointsRight}/>
      </div>
      <div
        id="tooltip"
        style={{
          position: "absolute",
          backgroundColor: "white",
          padding: "5px",
          border: "1px solid black",
          opacity: 0,
        }}
        />
    </div>
  )
}

export default App;
