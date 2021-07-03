import React from "react";
import { Card, Input } from "antd";

export const KeySearch = () => {
  const { Search } = Input;
  const onSearch = (value) => console.log(value);
  return (
    <Card
      type="inner"
      style={{ width: "70%", margin: "auto" }}
      title="Keyword Search"
    >
      <Search placeholder="Input a keyword" onSearch={onSearch} enterButton />
    </Card>
  );
};

export default KeySearch;
