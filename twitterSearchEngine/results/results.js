import React,{Component} from 'react';
import './results.css'
import logo from '../../assets/logo1.jpg'
import {Grid} from '@material-ui/core';
class Results extends Component{
	constructor(props) {
			super(props);
			this.state={
				tweets:[],
				results:0,
				zero:'no results retrieved'
			};
		console.log(this.props.ClientDetails);


}
	render(){

  return (
		<div style={{backgroundColor:'#d3d3d3'}}>
    <div style={{backgroundColor:'#d3d3d3',marginTop:'0px', marginBottom:'0px' }}><h6>Results retrieved:{this.state.results?this.state.results:this.state.zero}</h6></div>

		<Grid container spacing={0} style={{marginTop:'0px'}}>
  		<Grid item xs={12} sm={6} md={6} lg={6}>


		 </Grid>
		 </Grid>


		 <Grid container spacing={0}  style={{marginTop:'2px'}}>
	 		<Grid item xs={12} sm={6} md={6} lg={6}>



			</Grid>
			</Grid>
		</div>
  );
}
}

export default Results;
