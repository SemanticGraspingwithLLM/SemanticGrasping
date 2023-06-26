import demjson
import openai

class GraspPartDetector:
    def __init__(self, api_key):
        openai.api_key = api_key

    def receive_response_from_API(self, object_nm):
        content = f"""
        ロボットが{object_nm}を把持します．{object_nm}をいくつかの部位に分解してください．
        どの部位を把持すれば，安定して把持できますか？
        """
        assistant_list = [
            """
        次のjson形式で答えてください．
        選択した部位は，Trueに，選択しなかった部位は，Falseにしてください．

        {
        　"部位の名前": "True or False"
        }
        """,
            """
        部位の名前は英語で答えてください．
        """,
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "assistant", "content": output_type}
                for output_type in assistant_list
            ]
            + [
                {"role": "system", "content": content},
            ],
            temperature=0,
        )
        return self.load_json_str(response.choices[0]["message"]["content"].strip())


    def load_json_str(self, res_json_str):
        try:
            json_data = demjson.decode(res_json_str)
            return json_data
        except demjson.JSONDecodeError as e:
            print("Invalid JSON format:", e)