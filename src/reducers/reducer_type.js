import { ACTION_TYPE } from "../actions";

export default function(state = {}, action) {
    switch (action.type) {
      case ACTION_TYPE:
        return action.payload.data;
      default:
        return state;
    }
  }