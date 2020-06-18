import json
from adapter import StreamAdapter
from typing import Dict, Hashable, Iterable,Tuple


"""
在下面定义CourseWareB
答案状态在commonComponentState下的4cb5f12f9e164c6c545a55202bc818f2下的answer字段
正确答案是1，2，0，3
"""
class CourseWareB(StreamAdapter):

    @classmethod
    def load_raw_state(cls, raw_state: str) -> Hashable:
        """
        答案状态在commonComponentState下的4cb5f12f9e164c6c545a55202bc818f2下的answer字段
        """
        state = json.loads(raw_state).get("commonComponentState")
        panel_answers = (0, 0, 0, 0)
        if state is not None:

            if "4cb5f12f9e164c6c545a55202bc818f2" in state:
                 panel_answers = tuple(state["4cb5f12f9e164c6c545a55202bc818f2"]["answer"])
        return panel_answers

    @classmethod
    def is_user_right(cls, stream: Tuple) -> bool:
        """
        正确答案是1，2，0，3
        """
        right_ans = (1, 2, 0, 3)
        return stream== right_ans

if __name__ == "__main__":
    """
    在这里处理日志输出，输出结果为result.csv，三个字段为：学生ID，状态，是否为正确状态
    """
    import pandas as pd
    data = pd.read_csv('data.csv', sep='\t')
    data_student_id=data["uid"]
    raw_state=data["state"]
    data_state=[]
    data_right_state=[]
    for i in range(len(raw_state)):
        panel_answer_temp=CourseWareB.load_raw_state(raw_state[i])
        data_right_state_temp=CourseWareB.is_user_right(panel_answer_temp)
        data_state.append(panel_answer_temp)
        data_right_state.append(data_right_state_temp)
    result = pd.concat([data_student_id, pd.Series(data_state), pd.Series(data_right_state)], axis=1)
    result.columns = ["学生ID", "状态", "是否为正确状态"]
    result.to_csv('result.csv', index=False)