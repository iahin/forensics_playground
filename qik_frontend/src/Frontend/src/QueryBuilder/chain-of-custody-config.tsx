import merge from "lodash/merge";
import {
  Operators, Widgets, Fields, Config, Types, Conjunctions, Settings, LocaleSettings, OperatorProximity, Funcs,
} from "react-awesome-query-builder";
import ru_RU from "antd/lib/locale-provider/en_US";
import { ruRU } from "@material-ui/core/locale";
import AntdConfig from "react-awesome-query-builder/lib/config/antd";
const InitialConfig = AntdConfig; // or BasicConfig or MaterialConfig


//////////////////////////////////////////////////////////////////////

const fields: Fields = {
  CaseID:{
    label: "Case ID",
    type: "text"
  },
  Filename:{
    label: "Filename",
    type: "text"
  },
  Hashtype:{
    label: "Hash Type",
    type: "text"
  },
  Hashvalue:{
    label: "Hash Value",
    type: "text"
  },
};


//////////////////////////////////////////////////////////////////////

const conjunctions: Conjunctions = {
  AND: InitialConfig.conjunctions.AND,
  OR: InitialConfig.conjunctions.OR,
};


const proximity: OperatorProximity = {
  ...InitialConfig.operators.proximity,
  valueLabels: [
    { label: "Word 1", placeholder: "Enter first word" },
    { label: "Word 2", placeholder: "Enter second word" },
  ],
  textSeparators: [
    //'Word 1',
    //'Word 2'
  ],
  options: {
    ...InitialConfig.operators.proximity.options,
    optionLabel: "Near", // label on top of "near" selectbox (for config.settings.showLabels==true)
    optionTextBefore: "Near", // label before "near" selectbox (for config.settings.showLabels==false)
    optionPlaceholder: "Select words between", // placeholder for "near" selectbox
    minProximity: 2,
    maxProximity: 10,
    defaults: {
      proximity: 2
    },
    customProps: {}
  }
};

const operators: Operators = {
  ...InitialConfig.operators,
  // examples of  overriding
  between: {
    ...InitialConfig.operators.between,
    valueLabels: [
      "Value from",
      "Value to"
    ],
    textSeparators: [
      "from",
      "to"
    ],
  },
  proximity,
};

const widgets: Widgets = {
  ...InitialConfig.widgets,
  // examples of  overriding
  text: {
    ...InitialConfig.widgets.text,
  },
  slider: {
    ...InitialConfig.widgets.slider,
    customProps: {
      width: "300px"
    }
  },
  rangeslider: {
    ...InitialConfig.widgets.rangeslider,
    customProps: {
      width: "300px"
    }
  },
  date: {
    ...InitialConfig.widgets.date,
    dateFormat: "DD.MM.YYYY",
    valueFormat: "YYYY-MM-DD",
  },
  time: {
    ...InitialConfig.widgets.time,
    timeFormat: "HH:mm",
    valueFormat: "HH:mm:ss",
  },
  datetime: {
    ...InitialConfig.widgets.datetime,
    timeFormat: "HH:mm",
    dateFormat: "DD.MM.YYYY",
    valueFormat: "YYYY-MM-DD HH:mm:ss",
  },
  func: {
    ...InitialConfig.widgets.func,
    customProps: {
      showSearch: true
    }
  },
  treeselect: {
    ...InitialConfig.widgets.treeselect,
    customProps: {
      showSearch: true
    }
  },
};


const types: Types = {
  ...InitialConfig.types,
  // examples of  overriding
  boolean: merge(InitialConfig.types.boolean, {
    widgets: {
      boolean: {
        widgetProps: {
          hideOperator: true,
          operatorInlineLabel: "is",
        }
      },
    },
  }),
};


const localeSettings: LocaleSettings = {
  locale: {
    moment: "ru",
    antd: ru_RU,
    material: ruRU,
  },
  valueLabel: "Value",
  valuePlaceholder: "Value",
  fieldLabel: "Field",
  operatorLabel: "Operator",
  fieldPlaceholder: "Select field",
  operatorPlaceholder: "Select operator",
  deleteLabel: null,
  addGroupLabel: "Add group",
  addRuleLabel: "Add rule",
  addSubRuleLabel: "Add sub rule",
  delGroupLabel: null,
  notLabel: "Not",
  valueSourcesPopupTitle: "Select value source",
  removeRuleConfirmOptions: {
    title: "Are you sure delete this rule?",
    okText: "Yes",
    okType: "danger",
  },
  removeGroupConfirmOptions: {
    title: "Are you sure delete this group?",
    okText: "Yes",
    okType: "danger",
  },
};

const settings: Settings = {
  ...InitialConfig.settings,
  ...localeSettings,

  valueSourcesInfo: {
    value: {
      label: "Value"
    },
    field: {
      label: "Field",
      widget: "field",
    },
    func: {
      label: "Function",
      widget: "func",
    }
  },
  // canReorder: false,
  // canRegroup: false,
  // showNot: false,
  // showLabels: true,
  maxNesting: 3,
  canLeaveEmptyGroup: true, //after deletion
    
  // renderField: (props) => <FieldCascader {...props} />,
  // renderOperator: (props) => <FieldDropdown {...props} />,
  // renderFunc: (props) => <FieldSelect {...props} />,
};


const funcs: Funcs = {
  LOWER: {
    label: "Lowercase",
    mongoFunc: "$toLower",
    jsonLogic: ({str}) => ({ "method": [ str, "toLowerCase" ] }),
    returnType: "text",
    args: {
      str: {
        label: "String",
        type: "text",
        valueSources: ["value", "field"],
      },
    }
  },
  LINEAR_REGRESSION: {
    label: "Linear regression",
    returnType: "number",
    formatFunc: ({coef, bias, val}, _) => `(${coef} * ${val} + ${bias})`,
    sqlFormatFunc: ({coef, bias, val}) => `(${coef} * ${val} + ${bias})`,
    mongoFormatFunc: ({coef, bias, val}) => ({"$sum": [{"$multiply": [coef, val]}, bias]}),
    jsonLogic: ({coef, bias, val}) => ({ "+": [ {"*": [coef, val]}, bias ] }),
    renderBrackets: ["", ""],
    renderSeps: [" * ", " + "],
    args: {
      coef: {
        label: "Coef",
        type: "number",
        defaultValue: 1,
        valueSources: ["value"],
      },
      val: {
        label: "Value",
        type: "number",
        valueSources: ["value"],
      },
      bias: {
        label: "Bias",
        type: "number",
        defaultValue: 0,
        valueSources: ["value"],
      }
    }
  },
};


const config: Config = {
  conjunctions,
  operators,
  widgets,
  types,
  settings,
  fields,
  funcs
};

export default config;

