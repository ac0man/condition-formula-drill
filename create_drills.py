"""Excel関数やSQLにおける条件の論理式ドリルを生成する."""
import math
import random
import sys


class gen:
    """条件式のジェネレータ"""
    # ランダムでループを回しても operators と sentences の位置を同期する
    op_index = [0, 1, 2, 3, 4, 5]
    # python の比較演算子リスト（問題集として利用するには、' == ' と ' != ' をそれぞれ '=', '<>' に変換する）
    operators = {
        0: ' == ', 1: ' != ', 2: ' < ', 3: ' > ', 4: ' <= ', 5: ' >= '
    }
    # AとBが等しい,AとBが等しくない,AはBより大きい,AはB未満,AはB以上,AはB以下
    sentences = {
        0: ['と', 'が等しい'],
        1: ['と', 'が等しくない'],
        2: ['は', 'より大きい'],
        3: ['は', '未満'],
        4: ['は', '以上'],
        5: ['は', '以下']
    }

    logi_index = [0, 1]
    # python の論理演算子リスト
    logical = [' and ', ' or ']
    logi_sentences = ['、かつ', '、または']

    # 大文字リスト
    lchars = [chr(i) for i in range(65, 90)]
    # 小文字リスト
    schars = [chr(i) for i in range(97, 122)]

    def int_condition(self, number: int):
        """整数の条件式と穴埋め問題を生成し、文字列として返却する.引数として受け取った number の範囲で乱数を選択する"""
        pair = random.choices(range(0, number), k=2)
        indx = random.choice(self.op_index)

        exp = str(pair[0]) + self.operators[indx] + str(pair[1])
        return [exp, self.sentences[indx]]

    def float_condition(self, number: int):
        """小数点数の条件式と穴埋め問題を生成し、文字列として返却する.引数として受け取った number の範囲で乱数を選択する"""
        boolean_list = [i / 10 for i in range(0, 200, 1)]
        pair = random.choices(boolean_list, k=2)

        index = random.choice(self.op_index)
        exp = str(pair[0]) + self.operators[index] + str(pair[1])
        return [exp, self.sentences[index]]

    def string_condition(self, number: int):
        """文字列の条件式と穴埋め問題を生成し、文字列として返却する.引数として受け取った number の範囲で乱数を選択する"""
        # TODO 文字列を比較演算子で演算しているケースに対応する（sql, excel 関数の仕様に倣う）
        char_lists = self.lchars + self.schars
        str_list = []

        for i in range(2):
            string = '"'
            for j in range(1, random.choice(range(3, 7))):
                string += random.choice(char_lists)
            string += '"'
            str_list.append(string)

        index = random.choice(self.op_index)
        exp = str(str_list[0]) + self.operators[index] + str(str_list[1])
        return [exp, self.sentences[index]]

    def select_logical(self):
        """論理式を取得する"""
        index = random.choice(self.logi_index)
        return [self.logical[index], self.logi_sentences[index]]


def convert_expression(exp: str):
    """sqlやexcel関数の条件式の形式へ置換する"""
    if ' == ' in exp:
        return exp.replace(' =', ' ')
    elif ' != ' in exp:
        return exp.replace(' !=', ' <>')
    else:
        return exp


def eval_expression(exp: str):
    """eval で条件式を評価し真偽値を返却する.構文エラーにより失敗した場合はNoneを返却する"""
    result = ''
    try:
        result = str(eval(exp))
    except SyntaxError:
        # 文字列を等号、不等号以外の比較演算子で比較した場合
        result = str(None)
    return result


def format_basic_question(exp_list: list):
    """体裁を整えて返却する.（例：6 <= 3,False,,は,より大きい）"""
    res = eval_expression(exp_list[0])
    question = ',' + res + ',,' + exp_list[1][0] + ',,' + exp_list[1][1]
    return convert_expression(exp_list[0]) + question


def create_basic_conditions(number: int):
    """生成する問題数を number として受け取る.問題リストを返却する."""
    question_list = []
    for _ in range(number):
        exp_list = gen.int_condition(number)
        question_list.append(format_basic_question(exp_list))

    for _ in range(math.ceil(number)):
        exp_list = gen.float_condition(number)
        question_list.append(format_basic_question(exp_list))

    for _ in range(number):
        exp_list = gen.string_condition(number)
        question_list.append(format_basic_question(exp_list))

    return question_list


def convert_logi_exp(logi: str):
    """sqlやexcel関数で使われるような大文字表記に変換する"""
    return str.upper(logi)


def format_logical_question(exp_list1: list, exp_list2: list, logi_list: list):
    """体裁を整えて返却する.（例：6 <= 3 AND 1 = 1,False,,は,,より大きい、かつ,,と,,が等しい）"""
    res = eval_expression(exp_list1[0] + logi_list[0] + exp_list2[0])
    exp = convert_expression(exp_list1[0]) + convert_logi_exp(logi_list[0]) + convert_expression(exp_list2[0])
    return exp+','+res+',,'+exp_list1[1][0]+',,'+exp_list1[1][1]+logi_list[1]+',,'+exp_list2[1][0]+',,'+exp_list2[1][1]


def create_logical_conditions(number: int):
    """応用である and, or を含んだ条件式問題を生成する."""
    question_list = []
    for _ in range(number):
        exp_list1 = gen.int_condition(number)
        exp_list2 = gen.int_condition(number)
        logi_list = gen.select_logical()
        result = format_logical_question(exp_list1, exp_list2, logi_list)
        question_list.append(result)

    return question_list


def main():
    """合計50問を生成して標準出力に出力する"""
    print("No,条件式,True | False,説明")

    ls = create_basic_conditions(10) + create_logical_conditions(20)
    for no, i in enumerate(range(len(ls))):
        print(no+1, ls[i], sep=',')


# gen クラスをインスタンス化する
gen = gen()


if __name__ == '__main__':
    main()
    sys.exit(0)
