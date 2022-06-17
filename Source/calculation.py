from ast import parse
from cmath import e
from tabnanny import check
from unicodedata import digit
from discord.ext import commands

class Calculation(commands.Cog):
    operators = ['+', '-', '*', '/', '^','(', ')', '.']

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='계산')
    async def calculation(self, ctx, *args):        
        text = ""
        for arg in args:
            text += arg

        if text == "지원연산자":
            await ctx.send(self.print_operator())
            return
        
        if not self.operator_check(text) or not self.bracket_check(text):
            await ctx.send("계산식이 유효하지 않습니다.")
            return
        
        try:
            result = self.parse(text)
        except Exception as e:
            await ctx.send(f"에러: {e}")
            return

        await ctx.send(result)

    def print_operator(self) -> str:
        return f'지원되는 연산자 목록: {self.operators}'
    
    # 괄호 유효성 체크
    def bracket_check(self, text: str) -> bool:
        check_count = 0

        for char in list(text):
            check_count += 1 if char == "(" else -1 if char == ")" else 0

        return check_count == 0

    # 오퍼레이터 유효성 체크
    def operator_check(self, text: str) -> bool():
        for char in list(text):
            if not (self.operators.__contains__(char) or char.isdecimal()):
                return False
        return True

    def parse(self, text):
        expr = self.transformExpr(text)
        stack = []

        for oper in expr:
            try:
                stack.append(float(oper))
                continue
            except ValueError:
                a = stack.pop()
                b = stack.pop()

            if oper == '+':
                stack.append(a + b)
            elif oper == '-':
                stack.append(a - b)
            elif oper == '*':
                stack.append(a * b)
            elif oper == '/':
                stack.append(a / b)
            elif oper == '^':
                stack.append(self.pow(a, b))
            else:
                raise Exception('계산도중 오류가 발생하였습니다.')
        
        return stack[0]

    def transformExpr(self, text: str):
        op = [] #연산자들을 담아두는 stack
        exrp = []
        temp = ''
        for ch in text:
            if not ch.isdigit() and ch != '.' and temp != '':
                exrp.append(temp)
                temp = ''

            if ch == '(': #여는 괄호가 나올 경우 다음 글자로 진행합니다.
                continue
            elif ch.isdigit() or ch == '.': #피연산자가 등장하면 그대로 결과 표현에 붙여줍니다.
                temp += ch
            elif ch == ')': #닫는 괄호가 나올 경우 표현이 끝난 것이므로 마지막으로 stack에 넣어놨던 연산자를 빼서 붙여줍니다.
                exrp.append(op.pop())
            else: #연산자가 등장할 경우 stack에 넣어줍니다.
                op.append(ch)
        
        if temp != "":
            exrp.append(temp)
        
        for ch in op:
            exrp.append(ch)
        
        return exrp

    def pow(self, a, b):
        result = 1
        for x in range(int(b)):
            result * a
        return result