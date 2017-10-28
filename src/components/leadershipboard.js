import React, { Component } from 'react';
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import { fetchUsers } from "../actions";

class LeadershipBoard extends Component {

  componentDidMount() {
    this.props.fetchUsers();
  }

  renderUsers() {
    return _.map(this.props.users, user => {
      return (
        <li className="list-group-item" key={user.user_id}>
          <Link to={`/upload/${user.user_id}`}>
            {user.user_name}
          </Link>
            <button type="button" className="btn btn-primary float-right">
                Points <span className="badge badge-light">{user.user_points}</span>
                <span className="sr-only">unread messages</span>
            </button>
          
        </li>
      );
    });
  }

  render() {
    return (
      <div>
        <img  className="rounded mx-auto d-block p-5 logo" src="../../images/logo.png"></img>
        <h3 className="pb-3 text-center">Leadership Board</h3>     
        <ul className="list-group leadership-board">
          {this.renderUsers()}
        </ul>   
      </div>
    );
  }
}

function mapStateToProps(state) {
    return { users: state.instamojo.all_data };
}
  
export default connect(mapStateToProps, { fetchUsers })(LeadershipBoard);
