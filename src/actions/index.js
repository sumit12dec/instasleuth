import axios from "axios";

export const VERIFY_PAN = "verify_PAN";
export const FETCH_USERS = "fetch_users";
export const UPLOAD_PAN = "upload_PAN";
export const FETCH_PAN = "fetch_pan";

export function verifyPANDetails(values,id, callback) {    
  
  values = JSON.stringify(values)
  const request = axios
  .post(`http://34.227.56.111/edit_data/${id}/`, values)
  .then(() => callback());

  return {
    type: VERIFY_PAN,
    payload: request
  };
}

export function getPANDetails(id) {
  const request = axios.get(`http://34.227.56.111/verify/${id}/`);  
  return (dispatch) => {
    request.then(({data}) => {
      dispatch({ type: FETCH_PAN, payload: data })
    });
  };
}

export function uploadPAN(id,imageDetails) {
    var data = new FormData();
    data.append('file', imageDetails[0]);
    const request = axios.post(`http://34.227.56.111/upload/${id}/`,data);  
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
