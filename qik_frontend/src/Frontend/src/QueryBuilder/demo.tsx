import React, {Component} from "react";
import {
  Query, Builder, Utils, 
  //types:
  ImmutableTree, Config, BuilderProps, JsonTree, JsonLogicTree
} from "react-awesome-query-builder";
import throttle from "lodash/throttle";
import ChainOfCustodyConfig from "./chain-of-custody-config";
import CasesConfig from "./cases-config";
import loadedInitValue from "./init_value";
//import loadedInitLogic from "./init_logic";
import { Button } from 'antd';
import { Dropdown, Selection } from 'react-dropdown-now';
import 'react-dropdown-now/style.css';
import axios from 'axios';
import { Input } from 'antd';
import "react-awesome-query-builder/lib/css/styles.css";
import "antd/dist/antd.css";
import moment from 'moment';
import Data from './Data.json';


const { TextArea } = Input;

const stringify = JSON.stringify;
const {queryBuilderFormat, jsonLogicFormat, queryString, mongodbFormat, sqlFormat, getTree, checkTree, loadTree, uuid, loadFromJsonLogic} = Utils;
const preStyle = { backgroundColor: "darkgrey", margin: "10px", padding: "10px" };
const preErrorStyle = { backgroundColor: "lightpink", margin: "10px", padding: "10px" };

const emptyInitValue: JsonTree = {"id": uuid(), "type": "group"};

var chainOfCustodyInitValue: JsonTree = loadedInitValue && Object.keys(loadedInitValue).length > 0 ? loadedInitValue as JsonTree : emptyInitValue;
var chainOfCustodyTree: ImmutableTree = checkTree(loadTree(chainOfCustodyInitValue), ChainOfCustodyConfig);
var casesInitValue: JsonTree = loadedInitValue && Object.keys(loadedInitValue).length > 0 ? loadedInitValue as JsonTree : emptyInitValue;
var casesTree: ImmutableTree = checkTree(loadTree(casesInitValue), CasesConfig);

interface DemoQueryBuilderState {
  tree: ImmutableTree;
  config: Config;
  descriptionValue: string;
  titleValue: string;
  dropdownSelection: string;
  queryOwner: string;
  id: string;
}

const staticInvestigator = 'Stephanie';

export default class DemoQueryBuilder extends Component<{}, DemoQueryBuilderState> 
{
    private immutableTree: ImmutableTree;
    private config: Config;
    private params = '';

    state = {
      tree: casesTree,
      config: CasesConfig,
      descriptionValue: '',
      titleValue: '',
      dropdownSelection: 'Cases',
      queryOwner: '',
      id: ''
    };    

    onChangeDescription(event: { target: { value: any; }; }) {
      this.setState({descriptionValue: event.target.value});
    }

    onChangeTitle(event: { target: { value: any; }; }) {
      this.setState({titleValue: event.target.value});
    }

    async componentDidMount(): Promise<void> {
      this.params = window.location.search;
      if(this.params != ''){
        axios.get('/api/Repo/RetrieveOne'+this.params)
        .then(res => {
          console.log(res)
          if(res.data.queryBuilder == 'Cases'){
            casesInitValue = res.data.repository;
          }
          else{
            chainOfCustodyInitValue = res.data.repository;
            this.setState({
              config: ChainOfCustodyConfig
            });
          }
          this.setState({
            config: res.data.queryBuilder == 'Cases'?CasesConfig:ChainOfCustodyConfig,
            tree: loadTree(res.data.repository),
            descriptionValue: res.data.description, 
            dropdownSelection: res.data.queryBuilder,
            queryOwner: res.data.investigator,
            titleValue: res.data.title,
            id: res.data._id
          });
        })
        .catch((error) => {
          console.log(error)
        });
      }
    }

    submitQuery = () => {
      console.log("submit had been triggered")
      const QIKRepository = {
        datetimecreated: moment(new Date()).format("DD/MM/YYYY H:mm"),
        description: this.state.descriptionValue,
        investigator: 'Stephanie',
        query: stringify(mongodbFormat(this.state.tree, this.state.config), undefined, 2),
        repository: stringify(getTree(this.state.tree), undefined, 2),
        queryBuilder: this.state.dropdownSelection,
        nodesData: stringify(Data),
        title: this.state.titleValue,
        crimetype: "CrimeType placeholder",
        status: "Status placeholder"
      };

      axios.post('/api/Repo/Create', QIKRepository,
      )
        .then(res => {
          console.log(res);
          console.log(res.data);
          window.location.href='../qik-repository';
        })
        .catch((error) => {
          console.log(error)
        });
    }

    updateQuery = () => {
      console.log("update had been triggered")
      console.log(this.state.id)
      const QIKRepository = {
        datetimecreated: moment(new Date()).format("DD/MM/YYYY H:mm"),
        description: this.state.descriptionValue,
        investigator: 'Stephanie',
        query: stringify(mongodbFormat(this.state.tree, this.state.config), undefined, 2),
        repository: stringify(getTree(this.state.tree), undefined, 2),
        queryBuilder: this.state.dropdownSelection,
        nodesData: stringify(Data),
        title: this.state.titleValue,
        crimetype: "CrimeType placeholder",
        status: "Status placeholder"
      };

      axios.post('/api/Repo/Update?id=' + this.state.id, QIKRepository,
      )
        .then(res => {
          console.log(res);
          console.log(res.data);
          window.location.href='../qik-repository';
        })
        .catch((error) => {
          console.log(error)
        });
    }

    dropdownOnChange = (value: any) => {
      if(value.value == 'Chain of Custody'){
        this.setState({
          config : ChainOfCustodyConfig
        })
        this.state.tree = loadTree(chainOfCustodyInitValue);
      }
      else{
        this.setState({
          config : CasesConfig
        })
        this.state.tree = loadTree(casesInitValue);
      }
      this.state.dropdownSelection = value.value;
      }

    back(){
      window.history.back();
    }

    render = () => (
      <div style={{width:'100%'}}>

        Query Builder

        <Query 
          {...this.state.config} 
          value={this.state.tree}
          onChange={this.onChange}
          renderBuilder={this.renderBuilder}
        />

        {/* <div className="query-builder-result">
          {this.renderResult(this.state)}
        </div> */}

        <br></br>
        <div style={{float: 'right',width:'80%'}}>
        Title: 
        <TextArea
          value={this.state.titleValue}
          onChange={this.onChangeTitle.bind(this)}
          placeholder="Title of this query..."
          style={{ width: '80%' }}
          autoSize={{ minRows: 1, maxRows: 1 }}
        />
        <br></br>
        Description: 
        <TextArea
          value={this.state.descriptionValue}
          onChange={this.onChangeDescription.bind(this)}
          placeholder="Description of this query..."
          style={{ width: '80%' }}
          autoSize={{ minRows: 3, maxRows: 5 }}
        />
        <br></br>
        
          <Button type="primary" onClick={()=>this.back()}>Cancel</Button>
          {this.state.queryOwner == staticInvestigator ? 
          <Button type="primary" onClick={()=>{this.updateQuery()}}>Update</Button> : 
          <Button type="primary" onClick={()=>{this.submitQuery()}}>Submit</Button>}
          
        </div>
      </div>
    )

    resetValue = () => {
      this.setState({
        tree: casesTree, 
      });
    };

    clearValue = () => {
      this.setState({
        tree: loadTree(emptyInitValue), 
      });
    };

    renderBuilder = (props: BuilderProps) => (
      <div className="query-builder-container" style={{padding: "10px"}}>
        <div className="query-builder qb-lite">
          <Builder {...props} />
        </div>
      </div>
    )
    
    onChange = (immutableTree: ImmutableTree, config: Config) => {
      this.immutableTree = immutableTree;
      this.config = config;
      this.updateResult();

      // `jsonTree` or `logic` can be saved to backend
      // (and then loaded with `loadTree` or `loadFromJsonLogic` as seen above)
      const jsonTree = getTree(immutableTree);
      const {logic, data, errors} = jsonLogicFormat(immutableTree, config);
    }

    updateResult = throttle(() => {
      this.setState({tree: this.immutableTree, config: this.config});
      console.log(stringify(mongodbFormat(this.state.tree, this.state.config), undefined, 2))
    }, 100)

    renderResult = ({tree: immutableTree, config} : {tree: ImmutableTree, config: Config}) => {
      const {logic, data, errors} = jsonLogicFormat(immutableTree, config);
      return (
        <div>
          <br />
          <div>
          stringFormat: 
            <pre style={preStyle}>
              {stringify(queryString(immutableTree, config), undefined, 2)}
            </pre>
          </div>
          <hr/>
          <div>
          humanStringFormat: 
            <pre style={preStyle}>
              {stringify(queryString(immutableTree, config, true), undefined, 2)}
            </pre>
          </div>
          <hr/>
          <div>
          mongodbFormat: 
            <pre style={preStyle}>
              {stringify(mongodbFormat(immutableTree, config), undefined, 2)}
            </pre>
          </div>
          <hr/>
          <div>
            <a href="http://jsonlogic.com/play.html" target="_blank" rel="noopener noreferrer">jsonLogicFormat</a>: 
            { errors.length > 0 
              && <pre style={preErrorStyle}>
                {stringify(errors, undefined, 2)}
              </pre> 
            }
            { !!logic
              && <pre style={preStyle}>
                {"// Rule"}:<br />
                {stringify(logic, undefined, 2)}
                <br />
                <hr />
                {"// Data"}:<br />
                {stringify(data, undefined, 2)}
              </pre>
            }
          </div>
          <hr/>
          <div>
          Tree: 
            <pre style={preStyle}>
              {stringify(getTree(immutableTree), undefined, 2)}
            </pre>
          </div>
          </div>
      );
    }

}
