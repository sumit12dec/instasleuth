import React, { Component } from 'react';
import { Field, reduxForm, change  } from "redux-form";
import { connect } from "react-redux";
import { verifyPANDetails,getPANDetails } from "../actions";

class VerifyPAN extends Component {

    constructor(props){
        super(props);
        this.state={
            panCardImage:''
        }           
      }

    componentDidMount(){
        const { id } = this.props.match.params;
        this.state.panCardImage ? '' : this.setState({ panCardImage : '../../images/loader.gif' });        
        this.props.getPANDetails(id);        
    }

    componentWillReceiveProps(nextProps){
        this.props.dispatch(change('VerifyPANForm', 'image_name', nextProps.panDetails.image_name ));
        this.props.dispatch(change('VerifyPANForm', 'image_dob',  nextProps.panDetails.image_dob));
        this.props.dispatch(change('VerifyPANForm', 'image_pan',  nextProps.panDetails.image_pan));
        this.setState({ panCardImage : nextProps.panDetails.image_url });
    }

    renderField(field) {
        const { meta: { touched, error } } = field;
        const className = `form-group ${touched && error ? "has-danger" : ""}`;
    
        return (
          <div className={className}>
            <label className="float-left">{field.label}</label>
            <input className="form-control" type="text" {...field.input} />
            <div className="form-invalid-entry">
              {touched ? error : ""}
            </div>
          </div>
        );
    }

    onSubmit(values) {
        const { id } = this.props.match.params;
        this.props.verifyPANDetails(values,id, () => {
            this.props.history.push("/");
        });
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
                            <img  className="pancard-image-loader" src={this.state.panCardImage}></img>                              
                        </div>                        
                    </div>  
                </div>   
                <div className="col-6">
                    <div className="card">
                        <div className="card-header text-center">
                            Validate the PAN Card Details
                        </div>
                        <div className="card-body">
                            <form className="capitalise-content" onSubmit={handleSubmit(this.onSubmit.bind(this))}>
                                <Field
                                label="Full Name"
                                name="image_name"
                                component={this.renderField}  
                                />
                                <Field
                                label="Date of Birth"
                                name="image_dob"
                                component={this.renderField}
                                />
                                <Field
                                label="PAN"
                                name="image_pan"
                                component={this.renderField}
                                />
                                <button type="submit" className="btn btn-primary btn-block">Submit</button>
                            </form>             
                        </div>                        
                    </div>  
                </div>                           
            </div>
        </div>
      );
    }
  }

  function validateDate(date){
        let flag=0;
        if(date.length == 10)
        {
            let dateArray=date.split('/');
            for(let i=0;i<3;i++)
            {
                if(dateArray[i].isNaN)
                    flag=1;
            }
            if(dateArray[0]>31)
            flag=1;
            if(dateArray[1]>12)
            flag=1;
            if(dateArray[2]>new Date().getFullYear())
            flag=1;
        } else flag=1;
        return flag;
  }

  function validate(values) {
   // console.log('Validate',values);
    const errors = {};
  
    // Validate the inputs from 'values'
    if (!values.image_name) {
      errors.image_name = "Enter full name";
    }
    if (!values.image_dob || values.image_dob.length>10 || validateDate(values.image_dob)) {
      errors.image_dob = "Enter valid date of birth";
    }
    if (!values.image_pan || values.image_pan.length>10) {
      errors.image_pan = "Enter valid PAN";
    }
  
    // If errors is empty, the form is fine to submit
    // If errors has *any* properties, redux form assumes form is invalid
    return errors;
  }

  function mapStateToProps(state) {
    return { panDetails: state.instamojo };
  }

  export default reduxForm({
    validate,
    form: "VerifyPANForm"
  })(connect(mapStateToProps, { verifyPANDetails,getPANDetails })(VerifyPAN));