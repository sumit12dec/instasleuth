import _ from "lodash";
import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import reduxThunk from 'redux-thunk';
import { BrowserRouter, Route, Switch } from "react-router-dom";

import LeadershipBoard from './components/leadershipboard';
import PanUpload from './components/panupload';
import VerifyPAN from './components/verifypan';
import reducers from './reducers';

const createStoreWithMiddleware = applyMiddleware(reduxThunk)(createStore);

ReactDOM.render(
  <Provider store={createStoreWithMiddleware(reducers)}>
     <BrowserRouter>
      <div>
        <Switch>  
          <Route path="/upload/:id" component={PanUpload} />
          <Route path="/verify/:id" component={VerifyPAN} />
          <Route path="/" component={LeadershipBoard} />
        </Switch>
      </div>
    </BrowserRouter>
  </Provider>
  , document.querySelector('.container'));
