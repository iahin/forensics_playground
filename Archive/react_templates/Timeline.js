import React from "react";
import { Timeline } from "antd";
import {
  Box,
  Grommet,
  Card,
  Text,
  CardBody,
  Header,
  Button,
  Menu,
  Grid,
  Anchor, 
  Nav,
} from "grommet";
import { Blank, Home } from "grommet-icons";

//const Graphcontext = React.createContext()

function RouteTimeline() {
  //global customisation
  const theme = {
    themeMode: "light",
    global: {
      colors: {
        focus: "#fff", // added focus color on click
      },
      font: {
        family: `-apple-system,
                BlinkMacSystemFont, 
                "Segoe UI"`,
      },
      text: {
        dark: "teal",
        light: "purple",
      },
    },
    card: {
      container: {
        background: "#FFFFFF12",
        elevation: "small",
      },
      footer: {
        pad: { horizontal: "medium", vertical: "small" },
        background: "#FFFFFF06",
      },
    },
  };

  //Header and subtitle template
  const Identifier = ({ children, title, subTitle, size, ...rest }) => (
    <Box gap="small" align="center" direction="row" pad="small" {...rest}>
      {children}
      <Box>
        <Text size={size} weight="bold">
          {title}
        </Text>
        <Text size={size}>{subTitle}</Text>
      </Box>
    </Box>
  );

  const timeline_data = [
    {
      time: "2020-08-07 14:32:25",
      msg: "Processed accessed in host abc.123",
    },
    {
      time: "2020-08-07 14:32:25",
      msg: "Processed accessed in host abc.123",
    },
    {
      time: "2020-08-07 14:32:25",
      msg: "Processed accessed in host abc.123",
    },
    {
      time: "2020-08-07 14:32:25",
      msg: "Processed accessed in host abc.123",
    },
    {
      time: "2020-08-07 14:32:25",
      msg: "Processed accessed in host abc.123",
    },
  ];

  return (
    <Grommet theme={theme} full>
        <Header background="dark-2" pad="small">
          <Blank></Blank>
          <Nav direction="row" >
              Filter by:
        <Anchor label="Month" href="#" />
        <Anchor label="Year" href="#" />
        <Anchor label="Range" href="#" />
      </Nav>
        </Header>
      <Box pad="large" background="light-1" height="100%">
        
        <Grid gap="small" columns={{ count: "fill", size: "medium" }}>
          <Timeline mode="left">
            {timeline_data.map((data, key) => {
              return (
                <Timeline.Item label={data.time}>
                  <Card>
                    <CardBody pad="small">
                      <Box align="left">
                        <Identifier
                          title="Header Title"
                          subTitle={data.msg}
                          size="small"
                        ></Identifier>
                      </Box>
                    </CardBody>
                  </Card>
                </Timeline.Item>
              );
            })}
          </Timeline>
        </Grid>
      </Box>
    </Grommet>
  );
}

export default RouteTimeline;
