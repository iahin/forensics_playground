import pandas as pd
import json
import yaml
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

schema_common = pd.read_csv('schema_common.csv')
schema_eventid = pd.read_csv('schema_eventid.csv')


def yamlmaper(df):
    try:
        mapping_obj = yaml.safe_load(open('evtxmapper.yml', 'r'))
        # if df contians eventid, check agains sub keys in yml
        if 'eventid' in df.columns:
            for k, v in mapping_obj.items():
                if isinstance(v, dict):
                    for subk, subv in v.items():
                        df.loc[df['eventid'].astype('str') == subk.split('=')[
                            1], ['source']] = subv
                        df.loc[df['eventid'].astype('str') == subk.split('=')[
                            1], ['target']] = subv
                else:
                    df['source'].replace(k, v, inplace=True)
                    df['target'].replace(k, v, inplace=True)
        # if df does not contain event id
        else:
            for k, v in mapping_obj.items():
                if not isinstance(v, dict):
                    df['source'].replace(k, v, inplace=True)
                    df['target'].replace(k, v, inplace=True)

    except yaml.YAMLError as exc:
        print(exc)

    return df


yamlmaper(schema_common).to_csv('schema_common1.csv', index=False)
yamlmaper(schema_eventid).to_csv('schema_eventid1.csv', index=False)
