import Search from './Search';
import { ForceGraph3D } from 'react-force-graph';
import React, { useState, useEffect, useRef } from 'react';
import { BasicDrawer } from './BasicDrawer';
import SpriteText from 'three-spritetext';
import 'antd/dist/antd.css';
import * as d3 from 'd3-force-3d';
//import * as d3 from "d3";


export default function Parent() {
  const fgRef = useRef();
  const [drawer, setDrawer] = useState(0);
  const drawerToParent = (drawerdata) => {
    setDrawer(drawerdata);  
  }
    
  
  const [currentTime, setCurrentTime] = useState(undefined);

  const fetchUser = async () =>{
    const apiCall = await fetch ("/time/"+ drawer)
    const time = await apiCall.json();
    setCurrentTime (time);
    
   
  }
  useEffect(() => {
    fgRef.current.d3Force("charge", d3.forceManyBody().strength(-10000))

    fetchUser();
  }, [drawer])

  console.log(currentTime)
  


    return (
        <div>
        <BasicDrawer drawerToParent={drawerToParent}/>
        <ForceGraph3D ref={fgRef} graphData={currentTime} dagMode='td' dagLevelDistance={500} nodeRelSize={10} nodeId='name' nodeVal='size' nodeLabel='name' linkDirectionalParticles={2} linkDirectionalParticleWidth={0.8} linkDirectionalParticleSpeed={0.006} nodeAutoColorBy='group' nodeThreeObject={node => { const sprite = new SpriteText(node.name); sprite.color = node.color; sprite.textHeight = 20; return sprite}}></ForceGraph3D>
        
        </div>
  );
}