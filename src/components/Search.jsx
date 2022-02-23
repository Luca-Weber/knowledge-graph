import { useState, useEffect} from "react";
import "antd/dist/antd.css";
import { AutoComplete } from "antd";
import React, { useContext } from 'react';

function Search({childToParent}) { 

    const [result, setResult] = useState({})

    async function handleSearch(e) {
        
        const { value } = e.target;
        setResult({ result: await fetchData(value) })

    }
    async function fetchData(val) {
        const trimVal = val.trim().toLowerCase();
        if (trimVal.length > 0) {
            const api = `https://en.wikipedia.org/w/api.php?action=query&list=search&prop=info&inprop=url&utf8=&format=json&origin=*&srlimit=10&srsearch=${trimVal}`;

            const response = await fetch(api);
            
            if (!response.ok) {
                throw Error(response.statusText)
            }
            return await response.json();
        }
    }
    var sd = []
    result.result && result.result.query.search.map(obj => {
        let rObj = {}
        rObj["value"] = obj.title 
        sd.push(rObj)
        //console.log(sd)
        return sd


    })

    return (
            
        <AutoComplete style={{width: 250}} options={sd} onKeyUp={handleSearch} onSelect = {function(value){childToParent(value)}}/> 

    );
    
}
export default Search;
