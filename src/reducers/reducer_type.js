import { FETCH_USERS,UPLOAD_PAN } from "../actions";

export default function(state = {}, action) {
    switch (action.type) {
      case FETCH_USERS:
        return action.payload;
      case UPLOAD_PAN:
        return action.payload;
      default:
        return state;
    }
  }