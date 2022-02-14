export default 
{
  "type": "group",
  "id": "9a99988a-0123-4456-b89a-b1607f326fd8",
  "children1": {
    "89a9a99a-cdef-4012-b456-717ba6bec60b": {
      "type": "group",
      "properties": {
        "conjunction": "AND"
      },
      "children1": {
        "88ab8998-89ab-4cde-b012-317ba6bec60c": {
          "type": "rule_group",
          "properties": {
            "conjunction": "AND",
            "field": "Query"
          },
          "children1": {
            "a9aa8aba-4567-489a-bcde-f17ba6becca6": {
              "type": "rule",
              "properties": {
                "field": "Query.Collection",
                "operator": "select_equals",
                "value": [
                  null
                ],
                "valueSrc": [
                  "value"
                ],
                "valueType": [
                  "select"
                ]
              }
            }
          }
        }
      }
    }
  }
};