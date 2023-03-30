import re
from loguru import logger

from ChatGPT import ChatGPT
import cfgs


class STEP():
    def __init__(self, step_text):
        self.step_text = step_text
        self.action, self.target, self.input = self.step_parse()

    def step_parse(self):
        m = re.findall(r'\[(.*?)\]', self.step_text)
        if not self.is_step(m):
            print(f'Error: No actions found: {self.step_text}')
            return None

        action = None
        target = None
        input = None

        if len(m) == 1:
            action = m[0]
            target = self.step_text.split(f"[{m[0]}]")[-1].strip()
        elif len(m) >= 2:
            if 'input' not in m[0].lower():
                action = m[0]
                target = m[1]
            else:
                action = m[0]
                target = m[1].strip()
                
                if len(m) > 2: 
                    input = m[2].strip()
                else:
                    input = cfgs.RANDOM_INPUT_TEXT

        return action, target, input

    def is_step(self, list_of_variable):
        for v in list_of_variable:
            if v.lower() in cfgs.ACTION_LISTS:
                return True
        return False




class Extract_Steps():
    def __init__(self):
        self.chatgpt = ChatGPT()
        self.chatgpt.initialize_chatgpt()

    def infer(self, question):
        response = self.chatgpt.infer(question)

        output = []
        step = 1
        for line in response.split('\n'):
            line = line.strip()
            if re.match(f"{step}. "+r'\[([A-Za-z0-9.^_]+)\]', line) is not None:
                s = STEP(line.split(f"{step}. ",1)[-1])
                logger.info('\n{} \n  >>>> STEP-{}: [{}] [{}] [{}]'.format(
                                        line, step, s.action, s.target, s.input))
                output.append(s)
                step += 1
        return output




if __name__ == '__main__':
    None