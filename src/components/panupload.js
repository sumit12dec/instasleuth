import React, { Component } from 'react';
import Dropzone from 'react-dropzone';
import { connect } from "react-redux";
import { uploadPAN } from "../actions";

class ImageUpload extends Component {

    constructor(props){
        super(props);
        this.state={
            fileError:0,
            processing:0
        }
      }

      componentWillReceiveProps(nextProps) {
        console.log(nextProps.panDetails.user_id);
        console.log(nextProps);
        if(nextProps.panDetails.user_id){ 
            console.log('redirect');
                this.props.history.push(`/verify/${nextProps.panDetails.user_id}`);
        }       
      }

      showMessage(){
        if(this.state.fileError==0){ 
            return null;
        } else {
            return (
                <div className="card-footer">
                    <div className="alert alert-danger" role="alert">
                        Invalid file type. Please upload only png/jpg files.
                    </div>
                </div>
            ); 
        }         
      }

      showLoading(){
        if(this.state.processing==0){ 
            return null;
        } else {
            return (
                <img className="loader" src="../../images/loader.gif"></img>
            ); 
        }    
      }

      onDrop(acceptedFiles) {

        if(acceptedFiles[0].type=="image/jpeg" || acceptedFiles[0].type=="image/png") {
            this.setState({ fileError : 0 });
            const { id } = this.props.match.params;
            console.log('Accepted files: ', id, acceptedFiles);
            this.setState({ processing : 1 });   
            this.props.uploadPAN(id,acceptedFiles);                     
        } else {
            this.setState({ fileError : 1 });
        }       
        
     }

    render() {

      const dropzoneVisibility = this.state.processing ? "dropzone d-none" : "dropzone";
        
      return (
        <div>
            <img  className="rounded mx-auto d-block p-5 logo" src="../../images/logo.png"></img>
            <div className="card text-center">
                <div className="card-header">
                    Upload the PAN Card
                </div>
                {this.showLoading()}       
                <div className="card-body">                     
                    <Dropzone className={dropzoneVisibility} onDrop={(files) => this.onDrop(files)}>
                        <div>Try dropping some files here, or click to select files to upload.</div>
                    </Dropzone>               
                </div>
                {this.showMessage()}            
            </div> 
        </div>
      ); 
    }
}

function mapStateToProps(state) {
    console.log(state.instamojo);
    return { panDetails: state.instamojo };
}

export default connect(mapStateToProps, { uploadPAN })(ImageUpload);
