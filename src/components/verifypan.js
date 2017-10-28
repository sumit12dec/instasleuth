import React, { Component } from 'react';
import { Field, reduxForm } from "redux-form";
// import { connect } from "react-redux";
// import { verifyPANDetails } from "../actions";

class VerifyPAN extends Component {

    renderField(field) {
        console.log(field);
        const { meta: { touched, error } } = field;
        const className = `form-group ${touched && error ? "has-danger" : ""}`;
    
        return (
          <div className={className}>
            <label className="text-left">{field.label}</label>
            <input className="form-control" type="text" {...field.input} />
            <div className="text-danger">
              {touched ? error : ""}
            </div>
          </div>
        );
    }

    onSubmit(values) {
       console.log('Submit',values);
    }

    render() {
    
      const { handleSubmit } = this.props;

      return (
        <div>
            <img  className="rounded mx-auto d-block p-5 logo" src="../../images/logo.png"></img>
            <div className="row">
                <div className="col-6">
                    <div className="card text-center">
                        <div className="card-header">
                            Uploaded PAN Card
                        </div>
                        <div className="card-body">
                            <img  className="rounded mx-auto verify-card" src="../../images/sample.jpg"></img>                              
                        </div>                        
                    </div>  
                </div>   
                <div className="col-6">
                    <div className="card text-center">
                        <div className="card-header">
                            Validate the PAN Card Details
                        </div>
                        <div className="card-body">
                            <form className="capitalise-content" onSubmit={handleSubmit(this.onSubmit.bind(this))}>
                                <Field
                                label="Full Name"
                                name="name"
                                component={this.renderField}  
                                value="raja"                             
                                />
                                <Field
                                label="Date of Birth"
                                name="dob"
                                component={this.renderField}
                                value="raja"     
                                />
                                <Field
                                label="PAN"
                                name="pan"
                                component={this.renderField}
                                value="raja"     
                                />
                                <button type="submit" className="btn btn-primary">Submit</button>
                            </form>             
                        </div>                        
                    </div>  
                </div>                           
            </div>
        </div>
      );
    }
  }

  function validate(values) {
   // console.log('Validate',values);
    const errors = {};
  
    // Validate the inputs from 'values'
    if (!values.name) {
      errors.name = "Enter full name";
    }
    if (!values.dob) {
      errors.dob = "Enter date of birth";
    }
    if (!values.pan) {
      errors.pan = "Enter PAN";
    }
  
    // If errors is empty, the form is fine to submit
    // If errors has *any* properties, redux form assumes form is invalid
    return errors;
  }

  export default reduxForm({
    validate,
    form: "VerifyPANForm"
  })(VerifyPAN);