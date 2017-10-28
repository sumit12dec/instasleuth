import { combineReducers } from 'redux';
import TypeReducer from "./reducer_type";


const rootReducer = combineReducers({
  type : TypeReducer
});

export default rootReducer;
