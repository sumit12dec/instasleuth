import { combineReducers } from 'redux';
import { reducer as formReducer } from "redux-form";
import TypeReducer from "./reducer_type";


const rootReducer = combineReducers({
  instamojo : TypeReducer,
  form: formReducer
});

export default rootReducer;
