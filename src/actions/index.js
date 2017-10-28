import axios from "axios";

export const VERIFY_PAN = "verify_PAN";
export const FETCH_USERS = "fetch_users";
export const UPLOAD_PAN = "upload_PAN";

export function verifyPANDetails(values, callback) {      
    return {
      type: CREATE_POST,
      payload: request
    };
}

export function uploadPAN(imageDetails) {
    var data = new FormData();
    data.append('file', imageDetails[0]);
    const request = axios.post('http://34.227.56.111/cloud_extract_data/',data);  
    return (dispatch) => {
      request.then(({data}) => {
        dispatch({ type: UPLOAD_PAN, payload: data })
      });
    };
  }
  
  export function fetchUsers() {
    const request = axios.get('http://34.227.56.111/user_points/');  
    return (dispatch) => {
      request.then(({data}) => {
        dispatch({ type: FETCH_USERS, payload: data })
      });
    };
  }
