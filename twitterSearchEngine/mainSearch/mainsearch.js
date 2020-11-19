import React,{Component,Fragment} from 'react';
import './mainsearch.css'
import logo from '../../assets/index.png'
import { TextField } from '@material-ui/core';

import { Bar, Line, Pie,Doughnut } from 'react-chartjs-2';
import {Button} from '@material-ui/core';

import {Grid} from '@material-ui/core';
import { Typography } from '@material-ui/core';
import {Checkbox} from '@material-ui/core'
import {FormControlLabel} from '@material-ui/core'
import {Paper} from '@material-ui/core'
import Collapse from '@material-ui/core/Collapse';
import FormGroup from '@material-ui/core/FormGroup';
import axios from 'axios'

let userDetails=[]

class Mainsearch extends Component{
	constructor(props) {
	    super(props);

			this.state={

				     value: '',
			       CheckedCountry:false,
             CheckedIndia:false,
			       CheckedUSA:false,
		         CheckedBrazil:false,
						 CheckedLanguage:false,
						 CheckedHindi:false,
						 CheckedEnglish:false,
						 CheckedPortuguese:false,
						 CheckedTopic:false,
						 CheckedEnvironment:false,
						 CheckedPolitics:false,
						 CheckedSports:false,
						 CheckedUser:false,
						 tweets: [],
						 total:0,
						 zero:'No results retrieved',
						 chartDataSentiment:{},
						 charDataLang:{},
						 chartDataCont:{},
						 chartDataPoiact:{},
						 chartTopic:{},

					 }



		this.handleChange = this.handleChange.bind(this);
    this.onCheckChange=this.onCheckChange.bind(this);
	  this.handleSubmit = this.handleSubmit.bind(this);
		this.handleSocialChange=this.handleSocialChange.bind(this);
	  }



		handleChange(event) {
	    this.setState({value: event.target.value});
	  }
	onCheckChange(e)
	{
		this.setState({
			[e.target.name]:e.target.checked
		})
	}
	  handleSubmit(event) {
			event.preventDefault();
			this.setState({tweets:[]})
			userDetails=[this.state.value,this.state.CheckedIndia,this.state.CheckedUSA,this.state.CheckedBrazil,this.state.CheckedHindi,this.state.CheckedEnglish,this.state.CheckedPortuguese,this.state.CheckedUser,this.state.CheckedEnvironment,this.state.CheckedPolitics,this.state.CheckedSports]
     //this.props.data(userDetails)
		 var self = this
	     axios.post('http://192.168.1.173:5000/' + userDetails).then(function(res){
			 //console.log(res.data)
			//handleRequest(res.data);
			//self.setState({tweets:[
			 //...self.state.tweets,
			 //res.data]});
			 const tweet = res.data.map(item=>{
				 return item;

			 })
			 self.setState({tweets:tweet});
			 self.setState({total:tweet.length});


			 self.setState({chartDataSentiment: {labels:['Positive','Neutral','Negative'],

		 datasets:[
			 {

					 label:'Sentiment Analysis',
				 data:[tweet[0].count_positive,tweet[0].count_neutral,tweet[0].count_negative],
				 backgroundColor:[
					 'rgba(0,137,123,0.6)',
					 'rgba(79,195,247,0.6)',
					 'rgba(236,64,122,0.6)'
				 ]
		 }]
	 }}
 );

 self.setState({chartDataLang: {labels:['Hindi','English','Portuguese','Others'],

datasets:[
 {

		 label:'Tweets per Language',
	 data:[tweet[0].count_hi,tweet[0].count_en,tweet[0].count_pt,tweet[0].count_ot],
	 backgroundColor:[
		 'rgba(53,104,89,0.6)',
		 'rgba(74,21,75,0.6)',
		 'rgba(229,9,20,0.6)',
		 'rgba(74,20,140,0.8)'
	 ]
}]
}}
);


self.setState({chartDataCont: {labels:['India','USA','BRAZIL'],

datasets:[
{

		label:'Tweets per Language',
	data:[tweet[0].count_India,tweet[0].count_USA,tweet[0].count_Brazil],
	backgroundColor:[
		'rgba(176,0,32,0.6)',
		'rgba(27,94,32,0.6)',
		'rgba(98,0,238,0.6)'
	]
}]
}}
);


self.setState({chartDataPoiact: {labels:['Andrew Yang','Joe Biden','Amb John Bolton','Kamala Harris','VP','Bolsonaro SP','Cirogomes','David Mirandario','Dilmabr','Lula oficial','Akhilesh Yadav','Amit Shah','Arvind Kejriwal','Piyush Goyal','Rajnath Singh','RS Prasad'],

datasets:[
{

		label:'POI Twitter Activity per month',
	data:[tweet[0].AndrewYang,tweet[0].JoeBiden,tweet[0].AmbJohnBolton,tweet[0].KamalaHarris,tweet[0].VP,tweet[0].BolsonaroSP,tweet[0].cirogomes,tweet[0].davidmirandario,tweet[0].dilmabr,tweet[0].LulaOficial,tweet[0].yadavakhilesh,tweet[0].AmitShah,tweet[0].ArvindKejriwal,tweet[0].PiyushGoyal,tweet[0].rajnathsingh,tweet[0].rsprasad],
	backgroundColor:[
		'rgba(176,0,32,0.6)',
		'rgba(27,94,32,0.6)',
		'rgba(79,195,247,0.6)',
		'rgba(98,0,238,0.6)',
		'rgba(176,0,32,0.6)',
		'rgba(27,94,32,0.6)',
		'rgba(79,195,247,0.6)',
		'rgba(98,0,238,0.6)',
		'rgba(176,0,32,0.6)',
		'rgba(27,94,32,0.6)',
		'rgba(79,195,247,0.6)',
		'rgba(98,0,238,0.6)',
		'rgba(176,0,32,0.6)',
		'rgba(27,94,32,0.6)',
		'rgba(79,195,247,0.6)',
		'rgba(98,0,238,0.6)'
	]
}]
}}
);


self.setState({chartTopic: {labels:['Thanking Government','Presedential elections','Health','Debate','Climate Change','Vehicle act','Others'],

datasets:[
{

		label:'Tweets per Language',
	data:[tweet[0].Thanking_Government,tweet[0].Presidential_Election,tweet[0].Helath,tweet[0].Climate_Change,tweet[0].Debate[0],tweet[0].Vehicle_Act,tweet[0].Others],
	backgroundColor:[
		'rgba(176,0,32,0.6)',
		'rgba(27,94,32,0.6)',
		'rgba(79,195,247,0.6)',
		'rgba(98,0,238,0.6)',
		'rgba(176,0,32,0.6)',
		'rgba(229,9,20,0.6)',
		'rgba(74,20,140,0.8)'
	]
}]
}}
);



 self.setState({width1:100});
 self.setState({height1:100});
			 })

//this.setState({tweets:[
 //...this.state.tweets,
 //res.data]});
.catch(function(error){
	console.log(error)
});
  //console.log(this.state.tweets)
	this.props.data(this.state.tweets)
  }


		handleSocialChange= name => event =>{
    this.setState({[event.target.name]: event.target.value });
     this.setState({CheckedCountry : !this.state.CheckedCountry})
  }
	handleLanguageChange= name => event =>{
	this.setState({[event.target.name]: event.target.value });
	 this.setState({CheckedLanguage : !this.state.CheckedLanguage})
}
handleTopicChange= name => event =>{
this.setState({[event.target.name]: event.target.value });
 this.setState({CheckedTopic : !this.state.CheckedTopic})
}

	render(){

  return (

		<Fragment>
		<Paper style={{width:"60%",margin:"0px auto",padding:"30px",backgroundColor:"#ff8A65"}} className="Mainsearch">
			<Typography variant="h3" className="fnts"> <center><b> TWEET SEARCH </b></center></Typography>
  	<Fragment>
  	<form onSubmit={this.handleSubmit}>
  	<Grid container spacing={0}  style={{marginTop:'1px'}}>
  		<Grid item xs={12} sm={6} md={6} lg={12}>
   			<TextField
				 type='text'
				 name="query"
				 label='Please enter Query'
				 margin='normal'
         value={this.state.value} onChange={this.handleChange}
				 required></TextField><br/>
   		</Grid>
	 </Grid>
	 <Grid container style={{marginTop:'1px'}}>


		<Grid container>
	 		<Grid item xs={12} sm={6} md={6} lg={4} >
			 <FormControlLabel
				 control={
					 <Checkbox
						 checked={this.state.CheckedCountry}
						 onChange={this.handleSocialChange("CheckedCountry")}
						 value="Country"
						 color="primary"
					 />
				 }
				 label="Country"
			 />
		 <Collapse
				 in={this.state.CheckedCountry}>
				 {this.state.CheckedCountry ? (
					 <FormGroup row style={{marginLeft:"200px"}}>
			 <FormControlLabel
				 control={
					 <Checkbox
					 checked={this.state.CheckedIndia}
              onChange={this.onCheckChange}
							name='CheckedIndia'
						 value="India"
						 color="primary"
					 />
				 }
				 label="India"
			 />
			 <FormControlLabel
				 control={
					 <Checkbox
					 checked={this.state.CheckedUSA}
		 				 onChange={this.onCheckChange}
            name='CheckedUSA'
						 value="USA"
						 color="primary"
					 />
				 }
				 label="USA"
			 />
			 <FormControlLabel
				 control={
					 <Checkbox
					 checked={this.state.CheckedBrazil}
		 				 onChange={this.onCheckChange}
              name='CheckedBrazil'
						 value="Brazil"
						 color="primary"
					 />
				 }
				 label="Brazil"
			 />
</FormGroup>
 ) : null}
 </Collapse>
 </Grid>


 <Grid item xs={12} sm={6} md={6} lg={4} >
	<FormControlLabel
		control={
			<Checkbox
				checked={this.state.CheckedLanguage}
				onChange={this.handleLanguageChange("CheckedLanguage")}
				value="Language"
				color="primary"
			/>
		}
		label="Language"
	/>
<Collapse
		in={this.state.CheckedLanguage}>
		{this.state.CheckedLanguage ? (
			<FormGroup row style={{marginLeft:"200px"}}>
	<FormControlLabel
		control={
			<Checkbox
			checked={this.state.CheckedHindi}
				 onChange={this.onCheckChange}
				 name='CheckedHindi'
				value="Hindi"
				color="primary"
			/>
		}
		label="Hindi"
	/>
	<FormControlLabel
		control={
			<Checkbox
			checked={this.state.CheckedEnglish}
				 onChange={this.onCheckChange}
			 name='CheckedEnglish'
				value="English"
				color="primary"
			/>
		}
		label="English"
	/>
	<FormControlLabel
		control={
			<Checkbox
			checked={this.state.CheckedPortuguese}
				 onChange={this.onCheckChange}
				 name='CheckedPortuguese'
				value="Portuguese"
				color="primary"
			/>
		}
		label="Portuguese"
	/>
</FormGroup>
) : null}
</Collapse>
</Grid>

<Grid item xs={12} sm={6} md={6} lg={4} >
 <FormControlLabel
	 control={
		 <Checkbox
			 checked={this.state.CheckedTopic}
			 onChange={this.handleTopicChange("CheckedTopic")}
			 value="Topic"
			 color="primary"
		 />
	 }
	 label="Topic"
 />
<Collapse
	 in={this.state.CheckedTopic}>
	 {this.state.CheckedTopic ? (
		 <FormGroup row style={{marginLeft:"200px"}}>
 <FormControlLabel
	 control={
		 <Checkbox
		 checked={this.state.CheckedEnvironment}
				onChange={this.onCheckChange}
				name='CheckedEnvironment'
			 value="Environment"
			 color="primary"
		 />
	 }
	 label="Environment"
 />
 <FormControlLabel
	 control={
		 <Checkbox
		 checked={this.state.CheckedPolitics}
				onChange={this.onCheckChange}
			name='CheckedPolitics'
			 value="politics"
			 color="primary"
		 />
	 }
	 label="Politics"
 />
 <FormControlLabel
	 control={
		 <Checkbox
		 checked={this.state.CheckedSports}
				onChange={this.onCheckChange}
				name='CheckedSports'
			 value="sports"
			 color="primary"
		 />
	 }
	 label="Sports"
 />
</FormGroup>
) : null}
</Collapse>
</Grid>


<Grid container style={{margin:'10px'}}>
			<Grid item xs={12} sm={12} md={12} lg={12}>
				<FormControlLabel
				control={
					<Checkbox
					checked={this.state.CheckedUser}
						 onChange={this.onCheckChange}
						 name='CheckedUser'color='primary'
					 />
			}
			label="Verified?"
			/></Grid>
	 		<Grid style={{margin:'10px'}} item xs={12} sm={6} md={6} lg={12} >
       	<Button color="primary" variant="contained" type="submit">submit</Button>
			</Grid>
   </Grid>
</Grid>
 </Grid>
   </form>
   </Fragment>
	 </Paper>


	 <div style={{backgroundColor:'#ffffff'}}>
	 <div style={{backgroundColor:'#ffffff',marginTop:'10px', marginBottom:'10px' }}><h3>Results retrieved:{this.state.total?this.state.total:this.state.zero}</h3></div>
	 <Grid container spacing={0} style={{marginTop:'0px'}}>
	 	<Grid item xs={12} sm={6} md={6} lg={4}>

	 	<div className="appointment-list ">
	 {
		 this.state.tweets.map(item=>(
			 <div className="pet-item" >

				 <div className="pet-info ">
					 <div className="pet-head ">
					 <br />
						 <span><img src={item.profile_image_url} height="42" width="62"/></span>


						 <span className="pet-name">{item.poi_name}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
						 <span className="apt-date ">{item.tweet_date}</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
						 <a href={item.tweet_url} target="_blank">redirect to twitter</a>

					 </div>

					 <div className="owner-name">
						 <span className="label-item">{item.tweet_text} </span>
					 </div>
				 </div>
			 </div>

		 ))
	 }
	 </div>

	 </Grid>
		<Grid item xs={12} sm={6} md={6} lg={4}>
	     <div>
			 <Pie
         data={this.state.chartDataSentiment}
         width={100}
          height={200}
          options={{ maintainAspectRatio:false }}
        />
			 </div>
			 <div>
			<Doughnut
				 data={this.state.chartDataLang}
				 width={100}
					height={200}
					options={{ maintainAspectRatio:false }}
				/>
			</div>
			<div>
			<Bar
				data={this.state.chartDataPoiact}
				width={100}
				 height={200}
				 options={{ maintainAspectRatio:false }}
			 />
			</div>
		</Grid>
		<Grid item xs={12} sm={6} md={6} lg={4}>
	     <div>
			 <Pie
         data={this.state.chartTopic}
         width={100}
          height={200}
          options={{ maintainAspectRatio:false }}
        />
			 </div>
			 <div>

	    <img src={logo} height="200" width="500"/>
			</div>
			<div>
			<Pie
				data={this.state.chartDataCont}
				width={100}
				 height={200}
				 options={{ maintainAspectRatio:false }}
			 />
			</div>
		</Grid>
		</Grid>
</div>
	 </Fragment>


  );
}
}

export default Mainsearch;
