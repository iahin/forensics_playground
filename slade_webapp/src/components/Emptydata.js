import React from "react";
import { Card, Empty } from "antd";

export const EmptyData = () => {
  return (
    <Card bordered="True">
      <Empty
        image="https://gw.alipayobjects.com/zos/antfincdn/ZHrcdLPrvN/empty.svg"
        description={<span>Not enough data. Please add more evidence.</span>}
      ></Empty>
    </Card>
  );
};

export default EmptyData;
