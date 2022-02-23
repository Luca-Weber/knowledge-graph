import React, { useState } from 'react';
import 'antd/dist/antd.css';
import { Drawer, Button } from 'antd';
import Parent from './Parent';
import Search from './Search';

export const BasicDrawer = ({drawerToParent}) => {
  const [data, setData] =  useState(undefined);
  const [visible, setVisible] = useState(false);
  const childToParent = (childdata) => {
    setData(childdata); 
  }

  const showDrawer = () => {
    setVisible(true);
  };
  

  const onClose = () => {
    setVisible(false);
  };


  return (  
    <> 
      <Button type="ghost" position ="relative" onClick={showDrawer}>
        Open
      </Button>
      <Drawer title="Basic Drawer" placement="right" onClose={onClose} visible={visible}>
        <p><Search childToParent={childToParent} drawerToParent = {drawerToParent(data)}> </Search></p>
      </Drawer>
        
      
    </>
  );
};



