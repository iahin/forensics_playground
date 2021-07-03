import React, {Component} from 'react'
import axios from 'axios'
import { Graph } from "react-d3-graph";

const Graphcontext = React.createContext()

class NetworkGraph extends Component {

    constructor(props){
        super(props);
        this.state = {
            items: [],
            query1: "",
            query2: "",
            isLoaded: false
        }
    }

    componentDidMount(){
        
        fetch('/get_srcimg2destimg')
        .then(res => res.json())
        .then(data => { 
            this.setState({
                isLoaded:true,
                items: data
            })
        });
        
    
    }
    
    async get_srcip2destip(){
        this.setState({isLoaded:false})
        fetch('/get_srcip2destip')
        .then(res => res.json())
        .then(data => { 
            console.log(data)
            this.setState({
                isLoaded:true,
                items: data
            })
        });
        
    }

    async get_srcimg2destimg(){
        this.setState({isLoaded:false})
        fetch('/get_srcimg2destimg')
        .then(res => res.json())
        .then(data => { 
            this.setState({
                isLoaded:true,
                items: data
            })
        });
        
    }

    async post_dataAtrlistQuery(){
        this.setState({isLoaded:false})
        fetch('/post_dataAtrlistQuery')
        .then(res => res.json())
        .then(data => { 
            console.log(data)
            this.setState({
                isLoaded:true,
                items: data
            })
        });
    }

    handleQuery1change = (event) =>{
        this.setState({
            query1: event.target.value
        })
    }

    handleQuery2change = (event) =>{
        this.setState({
            query2: event.target.value
        })
    }


    async post_dataQuery(){
        this.setState({isLoaded:false})

        axios.post('/post_dataQuery',
            JSON.stringify({
                query1: this.state.query1,
                query2: this.state.query2
            }),
            {headers:{"Content-Type" : "application/json"}})
        .then(res => res.data)
        .then(json => {
            console.log(json)
            this.setState({
                isLoaded:true,
                items: json
            })
        })
        .catch(err=>{
            console.log(err)
        })
        
        
    }

    render(){

        

        const myConfig = {
            height: 600,
            width: 1000,
            nodeHighlightBehavior: true,
            node: {
              color: "lightgreen",
              size: 120,
              highlightStrokeColor: "blue",
            },
            link: {
              highlightColor: "lightblue",
            },
          };

        const graphContainer =(
            <Graph id="graph-id" 
            //data={items} 
            config={myConfig} />
            
        );

        const loading =(   
            <div> Loading...</div>
        );
        
        return (
            <div className="App">
                <div>
                    <label>Query1</label>
                    <input type='text' value={this.state.username} onChange={this.handleQuery1change} ></input>
                    <label>Query2</label>
                    <input type='text' value={this.state.username} onChange={this.handleQuery2change} ></input>
                    <button onClick={()=>this.post_dataQuery()}>Submit</button>
                    <br></br>
                    <input type='text' value={this.state.username} onChange={this.handleQuery2change} ></input>
                    <button onClick={()=>this.post_dataAtrlistQuery()}>Multi Attribute Query(underConstruction)</button>
                </div>
                <button onClick={()=>this.get_srcimg2destimg()}>Process</button>
                <button onClick={()=>this.get_srcip2destip()}>IP Address</button>
                { this.state.isLoaded ? graphContainer : loading }
            </div>
        )
            
    }
}

export default NetworkGraph;